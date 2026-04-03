from typing import TYPE_CHECKING

import IPython
from traitlets.config import Config

from c2.constants import WHEATLEY_SERVER_BANNER

if TYPE_CHECKING:
    from c2.network.server import WheatleyServer


class WheatleyServerShell:
    _server: "WheatleyServer"

    def __init__(self, server: "WheatleyServer"):
        self._server = server

    def _prepare_user_ns(self):
        return {
            "get_conn": lambda conn_id: self._server.connections[conn_id],
            "list_conns": lambda: list(self._server.connections),
            "connections": self._server.connections,
        }

    def launch(self) -> None:
        c = Config()
        c.InteractiveShellEmbed.banner1 = ""
        c.InteractiveShellEmbed.banner2 = WHEATLEY_SERVER_BANNER
        c.InteractiveShellEmbed.quiet = True
        IPython.embed(
            colors="neutral",
            config=c,
            header="",
            user_ns=self._prepare_user_ns(),
        )
