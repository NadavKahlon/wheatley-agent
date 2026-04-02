from importlib.metadata import version

import IPython

WHEATLEY_C2_VERSION = version("c2")
WHEATLEY_C2_BANNER = (
    f"┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓\n"
    f"┃ Wheatley Command & Control Server ┃\n"
    f"┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛\n"
    f"Software version: {WHEATLEY_C2_VERSION}\n"
    f"Powered by IPython {IPython.__version__}\n"
)

WHEATLY_C2_HOST = "172.24.128.1"
WHEATLY_C2_PORT = 45454
