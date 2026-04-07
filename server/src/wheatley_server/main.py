import argparse
import threading

from wheatley_server.constants import (
    WHEATLY_SERVER_PORT,
    WHEATLY_SERVER_HOST,
    WHEATLEY_SERVER_BANNER,
    WHEATLEY_SERVER_INTERACTIVE_BANNER,
)
from wheatley_server.server import WheatleyServer
from wheatley_server.shell import LocalShell


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Wheatley Command & Control Server")
    parser.add_argument(
        "-i",
        "--interactive",
        action="store_true",
        help="Start the server with a local interactive shell",
    )
    return parser.parse_args()


def start_interactive(args: argparse.Namespace):
    print(WHEATLEY_SERVER_INTERACTIVE_BANNER)
    server = WheatleyServer((WHEATLY_SERVER_HOST, WHEATLY_SERVER_PORT))
    server_thread = threading.Thread(target=server.run, daemon=True)
    server_thread.start()
    LocalShell(server).run()
    server.terminate_run()


def start_non_interactive(args: argparse.Namespace):
    print(WHEATLEY_SERVER_BANNER)
    server = WheatleyServer((WHEATLY_SERVER_HOST, WHEATLY_SERVER_PORT))
    try:
        server.run()
    except KeyboardInterrupt:
        return


def start():
    args = parse_args()
    if args.interactive:
        start_interactive(args)
    else:
        start_non_interactive(args)
