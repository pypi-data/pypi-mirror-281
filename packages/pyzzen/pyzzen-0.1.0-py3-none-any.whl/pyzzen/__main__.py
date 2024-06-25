import argparse
from typing import Optional

from pyzzen import server
from quart_babel import Babel


def main(port: int, admin_pass: Optional[str] = None) -> None:
    app = server.create_app(admin_pass)
    Babel(app)
    app.run(port=port)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="Pyzzen",
        description="A simple Python Quizz Engine",
        epilog="",
    )
    parser.add_argument(
        "--admin-pass",
        dest="admin_pass",
        default=None,
        help="Password used in the admin panel",
    )
    parser.add_argument(
        "--port", "-p",
        dest="port",
        default=5000,
        help="Port to listen to",
    )
    args = parser.parse_args()
    main(admin_pass=args.admin_pass, port=args.port)
