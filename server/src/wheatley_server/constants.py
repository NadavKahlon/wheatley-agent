from importlib.metadata import version

import IPython

WHEATLEY_SERVER_VERSION = version("wheatley_server")
WHEATLEY_SERVER_BANNER = (
    f"\n"
    f"┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓\n"
    f"┃ Wheatley Command & Control Server ┃\n"
    f"┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛\n"
    f"Software version: {WHEATLEY_SERVER_VERSION}\n"
)
WHEATLEY_SERVER_INTERACTIVE_BANNER = (
    f"\n"
    f"┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓\n"
    f"┃ Wheatley Command & Control Server ┃\n"
    f"┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛\n"
    f"Software version: {WHEATLEY_SERVER_VERSION}\n"
    f"Powered by IPython {IPython.__version__}\n"
)

WHEATLY_SERVER_HOST = "172.24.128.1"
WHEATLY_SERVER_PORT = 45454
