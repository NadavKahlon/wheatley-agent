from typing import TYPE_CHECKING

from IPython.terminal.embed import InteractiveShellEmbed

if TYPE_CHECKING:
    from wheatley_server.server.server import WheatleyServer


class LocalServerShell:
    _server: "WheatleyServer"

    def __init__(self, server: "WheatleyServer"):
        self._server = server

    def _prepare_user_ns(self):
        return {
            "server": lambda: self._server,
            "get_agent_conn": lambda conn_id: self._server.agent_conns[conn_id],
            "list_agent_conns": lambda: list(self._server.agent_conns),
            "agent_conns": self._server.agent_conns,
            "a": lambda: (list(self._server.agent_conns.values()) or [None])[0],
        }

    def run(self) -> None:
        shell = InteractiveShellEmbed(
            user_ns=self._prepare_user_ns(),
            colors="neutral",
            header="",
            display_banner=False,
        )
        shell()
