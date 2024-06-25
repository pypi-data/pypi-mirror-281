from typing import Optional, Dict, Sequence, Tuple, Set
try:
    import tomllib
except ImportError:
    import toml as tomllib
import os
import random
import asyncio
from collections import defaultdict
import datetime
from quart import Quart, session, request, render_template, redirect, flash, websocket, send_from_directory
from quart_babel import gettext, format_datetime

from pyzzen.quizz import Quizz
from pyzzen.admin_pass import ADMIN_PASSWORD

known_players: Dict[int, str] = {}


class QuizzState(object):
    quizz: Quizz
    player_answers: Dict[int, Dict[int, int]]
    state: Optional[int]
    _ranking_cache: Optional[Sequence[Tuple[int, int]]] = None
    _ranking_cache_per_question: Dict[int, Sequence[Tuple[int, int]]]
    locked_questions: Set[int]
    creation_date: datetime.datetime

    def __init__(self, quizz: Quizz):
        self.quizz = quizz
        self.player_answers = defaultdict(dict)
        self.state = None
        self._ranking_cache_per_question = {}
        self.locked_questions = set()
        self.creation_date = datetime.datetime.now()

    def get_formated_creation_date(self) -> str:
        return format_datetime(self.creation_date, "short")

    def lock(self, question: int) -> None:
        self.locked_questions.add(question)

    def unlock(self, question: int) -> None:
        try:
            self.locked_questions.remove(question)
        except KeyError:
            pass

    def get_player_answer(self, player_id: int) -> Optional[int]:
        if self.state is None or self.state == -1:
            return None
        return self.player_answers[player_id].get(self.state, None)

    def set_player_answer(self, player_id: int, answer: int) -> None:
        if self.state is None or self.state == -1:
            return None

        # Invalidate cache
        self._ranking_cache = None
        try:
            del self._ranking_cache_per_question[self.state]
        except KeyError:
            pass

        self.player_answers[player_id][self.state] = answer

    def update_global_ranking(self) -> Sequence[Tuple[int, int]]:
        self._ranking_cache = sorted(
            ((player_id, self.quizz.get_points_for_answers(answers))
                for player_id, answers in self.player_answers.items()),
            key=lambda i: i[1],
            reverse=True,
        )
        return self._ranking_cache

    def get_global_ranking(self) -> Sequence[Tuple[int, int]]:
        if self._ranking_cache is not None:
            return self._ranking_cache
        return self.update_global_ranking()

    def get_global_ranking_with_names(self) -> Sequence[Tuple[str, int]]:
        return [(known_players.get(player_id, "???"), score)
                for player_id, score in self.get_global_ranking()]

    def get_answers_for_current_question(self) -> Sequence[Tuple[str, int]]:
        return [(known_players.get(player_id, "???"), self.get_player_answer(player_id))
                for player_id in self.player_answers]


quizzes: Dict[str, QuizzState] = {}

reload_events: Dict[str, asyncio.Event] = defaultdict(asyncio.Event)


def refresh_quizz(quizz_id: str) -> None:
    reload_events[quizz_id].set()
    del reload_events[quizz_id]


def create_app(admin_pass: Optional[str] = None) -> Quart:
    app = Quart(__name__, instance_relative_config=True)
    app.config.update(
        SECRET_KEY=str(random.getrandbits(64)),
        ADMIN_PASS=ADMIN_PASSWORD if admin_pass is None else admin_pass,
    )

    @app.route("/")
    async def root():
        return await render_template("base.html")

    @app.route('/favicon.ico')
    async def favicon():
        return await send_from_directory(os.path.join(app.root_path, 'static'),
                                         'favicon.ico', mimetype='image/vnd.microsoft.icon')

    @app.route("/admin", methods=("GET", "POST"))
    async def admin():
        if "is_admin" not in session:
            if request.method == "POST":
                pwd = (await request.form)["password"]
                if pwd == app.config["ADMIN_PASS"]:
                    session["is_admin"] = True
                    return redirect("/admin")
                else:
                    await flash(gettext(u"Wrong password"))

            return await render_template("admin.html")

        if request.method == "POST":
            files = await request.files
            if "file" in files:
                file = files["file"]
                if file.filename != '':
                    quizz_raw = file.stream.read().decode()
                    try:
                        quizz_obj = tomllib.loads(quizz_raw)
                        quizz = Quizz.parse_obj(quizz_obj)
                        quizz_id = str(random.getrandbits(19))
                        quizz_state = QuizzState(quizz=quizz)
                        quizzes[quizz_id] = quizz_state
                    except Exception as e:
                        print(e)
                        await flash(gettext(u"An error occurred while loading the quiz: %(e)s", e=e))

        return await render_template("panel.html", quizzes=quizzes)

    @app.route("/username", methods=("GET", "POST"))
    async def choose_username():
        if request.method == "POST":
            username = (await request.form)["username"]
            id_ = random.getrandbits(64)
            known_players[id_] = username
            session["username"] = username
            session["id"] = id_
            if "redirect" in session:
                target = session["redirect"]
                del session["redirect"]
                return redirect(target)

        return await render_template("username.html")

    async def keepalive_ws():
        while True:
            await websocket.send(".")
            await asyncio.sleep(5)

    @app.websocket("/ws_reload/<string:quizz_id>")
    async def ws_reload(quizz_id: str):
        keepalive_task = asyncio.create_task(keepalive_ws())
        await reload_events[quizz_id].wait()
        keepalive_task.cancel()
        await websocket.send("reload")

    async def get_quizz_user(quizz_id: str):
        if "id" not in session:
            session["redirect"] = f"/quizz/{quizz_id}"
            return redirect("/username")
        try:
            quizz_state = quizzes[quizz_id]
        except KeyError:
            return await render_template("quizz_not_found.html")
        quizz = quizz_state.quizz
        answer = quizz_state.get_player_answer(session["id"])
        if quizz_state.state is None:
            return await render_template(
                "quizz_user_start.html",
                quizz=quizz,
                quizz_state=quizz_state,
                quizz_id=quizz_id,
            )
        if quizz_state.state == -1:
            return await render_template(
                "quizz_user_end.html",
                quizz=quizz,
                quizz_state=quizz_state,
                quizz_id=quizz_id,
            )

        seed = int(session["id"]) + quizz_state.state
        random.seed(seed)
        answer_order = list(range(len(quizz.questions[quizz_state.state].answers)))
        random.shuffle(answer_order)

        return await render_template(
            "quizz_user.html",
            quizz=quizz,
            quizz_id=quizz_id,
            question_idx=quizz_state.state,
            answer_order=answer_order,
            answer=answer,
        )

    async def get_quizz_admin(quizz_id: str):
        try:
            quizz_state = quizzes[quizz_id]
        except KeyError:
            return await render_template("quizz_not_found.html")
        quizz = quizz_state.quizz
        if quizz_state.state is None:
            return await render_template(
                "quizz_admin_start.html",
                quizz=quizz,
                quizz_state=quizz_state,
                quizz_id=quizz_id,
            )
        if quizz_state.state == -1:
            return await render_template(
                "quizz_admin_end.html",
                quizz=quizz,
                quizz_state=quizz_state,
                quizz_id=quizz_id,
            )
        return await render_template(
            "quizz_admin.html",
            quizz=quizz,
            quizz_state=quizz_state,
            quizz_id=quizz_id,
            question_idx=quizz_state.state,
            answer_order=range(len(quizz.questions[quizz_state.state].answers)),
            question_locked=(quizz_state.state in quizz_state.locked_questions),
        )

    @app.route("/quizz/<string:quizz_id>")
    async def get_quizz(quizz_id: str):
        if "is_admin" in session:
            return await get_quizz_admin(quizz_id)
        else:
            return await get_quizz_user(quizz_id)

    async def post_quizz_user(quizz_id: str):
        if "id" not in session:
            session["redirect"] = f"/quizz/{quizz_id}"
            return redirect("/username")
        try:
            quizz_state = quizzes[quizz_id]
        except KeyError:
            return await render_template("quizz_not_found.html")
        if quizz_state.state not in (None, -1):
            answer = (await request.form)["answer"]
            if quizz_state.state not in quizz_state.locked_questions:
                quizz_state.set_player_answer(session["id"], int(answer))
        return redirect(f"/quizz/{quizz_id}")

    async def post_quizz_admin(quizz_id: str):
        try:
            quizz_state = quizzes[quizz_id]
        except KeyError:
            return await render_template("quizz_not_found.html")
        form = await request.form
        if "start" in form:
            quizz_state.state = 0
            refresh_quizz(quizz_id)

        elif "prev" in form:
            if quizz_state.state not in (0, None, -1):
                quizz_state.state -= 1
                refresh_quizz(quizz_id)

        elif "next" in form:
            if quizz_state.state not in (None, -1):
                if quizz_state.state == quizz_state.quizz.length - 1:
                    quizz_state.state = -1
                else:
                    quizz_state.state += 1
                refresh_quizz(quizz_id)

        elif "lock" in form:
            quizz_state.lock(quizz_state.state)

        elif "unlock" in form:
            quizz_state.unlock(quizz_state.state)

        return redirect(f"/quizz/{quizz_id}")

    @app.route("/quizz/<string:quizz_id>", methods=["POST"])
    async def post_quizz(quizz_id: str):
        if "is_admin" in session:
            return await post_quizz_admin(quizz_id)
        else:
            return await post_quizz_user(quizz_id)

    return app
