from typing import TYPE_CHECKING

import IPython

if TYPE_CHECKING:
    from wheatley_server.server import WheatleyServer


class LocalShell:
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
        IPython.embed(
            user_ns=self._prepare_user_ns(),
            colors="neutral",
            header="",
            display_banner=False,
        )
