from typing import List, Optional, Dict

from pydantic import BaseModel


class Answer(BaseModel):
    answer: str
    good: bool = False
    value: Optional[int] = None

    @property
    def points(self) -> int:
        if self.value is not None:
            return self.value
        return 1 if self.good else 0


class Question(BaseModel):
    question: str
    answers: List[Answer]
    score_factor: int = 1

    def get_points_for_answer(self, answer: int) -> int:
        return self.score_factor * self.answers[answer].points


class Quizz(BaseModel):
    name: str
    questions: List[Question]

    @property
    def length(self) -> int:
        return len(self.questions)

    def get_points_for_answers(self, answers: Dict[int, int]) -> int:
        return sum(self.questions[q].get_points_for_answer(a) for q, a in answers.items())
