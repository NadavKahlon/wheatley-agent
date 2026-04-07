import socket
import threading
from itertools import count

from loguru import logger

from wheatley_server.agent.conn import AgentConnection
from wheatley_server.network import is_socket_closed


class WheatleyServer:

    address: tuple[str, int]
    agent_conns: dict[
        int, AgentConnection
    ]  # TODO Make thread safe (it's absolutely not)
    _agent_conn_id_gen: count
    _sock: socket.socket | None = None
    _terminate_run: threading.Event
    _run_terminated: threading.Event

    def __init__(self, address: tuple[str, int]):
        self.address = address
        self.agent_conns = {}
        self._agent_conn_id_gen = count(1)
        self._terminate_run = threading.Event()
        self._run_terminated = threading.Event()

    @property
    def host(self) -> str:
        return self.address[0]

    @property
    def port(self) -> int:
        return self.address[1]

    def run(self) -> None:
        try:
            self._run_init()
            logger.info(f"Listening for agent connections at {self.host}:{self.port}")

            while not self._terminate_run.is_set():
                try:
                    conn, addr = self._sock.accept()
                    conn_id = next(self._agent_conn_id_gen)
                    self.agent_conns[conn_id] = AgentConnection(
                        conn_id, conn, addr, self
                    )
                except socket.timeout:
                    pass
                self._remove_closed_conns()

        finally:
            self._run_cleanup()

    def _run_init(self) -> None:
        self._sock = socket.socket()
        self._sock.bind(self.address)
        self._sock.listen()
        self._sock.settimeout(0.5)

    def _run_cleanup(self) -> None:
        self._sock.close()
        self._sock = None
        logger.info(f"Stopped server at {self.host}:{self.port}")
        for conn_id, conn in list(self.agent_conns.items()):
            conn.close()
            del self.agent_conns[conn_id]
        self._run_terminated.set()

    def _remove_closed_conns(self) -> None:
        for conn_id, conn in list(self.agent_conns.items()):
            if is_socket_closed(conn.sock):
                conn.close()
                del self.agent_conns[conn_id]

    def terminate_run(self) -> None:
        self._terminate_run.set()
        self._run_terminated.wait()
