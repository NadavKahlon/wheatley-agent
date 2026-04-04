import argparse

from wheatley.constants import WHEATLY_SERVER_PORT, WHEATLY_SERVER_HOST, \
    WHEATLEY_SERVER_BANNER, WHEATLEY_SERVER_INTERACTIVE_BANNER
from wheatley.server import WheatleyServer
from wheatley.shell import LocalShell


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Wheatley Command & Control Server"
    )
    parser.add_argument(
        "-i", "--interactive",
        action="store_true",
        help="Start a local interactive shell",
    )
    return parser.parse_args()


def start():
    args = parse_args()
    server = WheatleyServer(WHEATLY_SERVER_HOST, WHEATLY_SERVER_PORT)
    if args.interactive:
        print(WHEATLEY_SERVER_INTERACTIVE_BANNER)
        server.start_daemon()
        LocalShell(server).launch()
    else:
        print(WHEATLEY_SERVER_BANNER)
        server.run()
