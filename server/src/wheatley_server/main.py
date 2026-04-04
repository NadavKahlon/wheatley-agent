import argparse

from wheatley_server.constants import WHEATLY_SERVER_PORT, WHEATLY_SERVER_HOST, \
    WHEATLEY_SERVER_BANNER, WHEATLEY_SERVER_INTERACTIVE_BANNER
from wheatley_server.server import WheatleyServer
from wheatley_server.shell import LocalShell


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Wheatley Command & Control Server"
    )
    parser.add_argument(
        "-i", "--interactive",
        action="store_true",
        help="Start the server with a local interactive shell",
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
