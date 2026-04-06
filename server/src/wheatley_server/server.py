import socket
import threading
from itertools import count

from loguru import logger

from wheatley_server.agent.connection import AgentConnection
from wheatley_server.network import is_socket_closed


class WheatleyServer:

    address: tuple[str, int]
    connections: dict[int, AgentConnection]  # TODO Implement locking
    _agent_conn_id_gen: count
    _sock: socket.socket | None = None
    shutdown_event: threading.Event | None = None

    def __init__(self, address: tuple[str, int]):
        self.address = address
        self.connections = {}
        self._agent_conn_id_gen = count(1)

    @property
    def host(self) -> str:
        return self.address[0]

    @property
    def port(self) -> int:
        return self.address[1]

    def run(self) -> None:
        try:
            self.shutdown_event = threading.Event()
            self._sock = socket.socket()
            self._sock.bind(self.address)
            self._sock.listen()
            self._sock.settimeout(0.5)

            logger.info(f"Listening for agent connections at {self.host}:{self.port}")
            while True:
                try:
                    conn, addr = self._sock.accept()
                    conn_id = next(self._agent_conn_id_gen)
                    self.connections[conn_id] = AgentConnection(
                        conn_id, conn, addr, self
                    )
                except socket.timeout:
                    pass

                if self.shutdown_event.is_set():
                    break
                for conn_id, conn in list(self.connections.items()):
                    if is_socket_closed(conn.sock):
                        conn.close()
                        del self.connections[conn_id]

        finally:
            self._sock.close()
            self._sock = None
            self.shutdown_event = None
            logger.info(f"Stopped server at {self.host}:{self.port}")
