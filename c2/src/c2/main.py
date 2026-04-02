import threading

import IPython
from traitlets.config import Config

from c2.constants import WHEATLY_C2_PORT, WHEATLY_C2_HOST, WHEATLEY_C2_BANNER
from c2.network.server import WheatleyServer


def start():
    server = WheatleyServer(WHEATLY_C2_HOST, WHEATLY_C2_PORT)
    server.start_daemon()

    c = Config()
    c.InteractiveShellEmbed.banner1 = ""
    c.InteractiveShellEmbed.banner2 = WHEATLEY_C2_BANNER
    c.InteractiveShellEmbed.quiet = True
    IPython.embed(
        colors="neutral",
        config=c,
        header="",
    )
