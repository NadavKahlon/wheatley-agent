import argparse
import asyncio
from venv import logger

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


def start():
    args = parse_args()
    server = WheatleyServer(WHEATLY_SERVER_HOST, WHEATLY_SERVER_PORT)
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    try:
        if args.interactive:
            print(WHEATLEY_SERVER_INTERACTIVE_BANNER)
            shell = LocalShell(server)
            loop.create_task(shell.launch())
        else:
            print(WHEATLEY_SERVER_BANNER)
        loop.run_until_complete(server.run())
        loop.run_forever()

    except KeyboardInterrupt:
        pass
    finally:
        tasks = asyncio.all_tasks(loop)
        for t in tasks:
            t.cancel()
        loop.run_until_complete(asyncio.gather(*tasks, return_exceptions=True))
        loop.close()
