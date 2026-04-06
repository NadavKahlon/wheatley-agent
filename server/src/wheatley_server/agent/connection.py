import socket
from typing import TYPE_CHECKING

from loguru import logger

from wheatley_server.proto.agent import command_pb2
from wheatley_server.network import send_protobuf, recv_protobuf

if TYPE_CHECKING:
    from wheatley_server.server import WheatleyServer


class AgentConnection:

    id: int
    sock: socket.socket
    address: tuple[str, int]
    _server: "WheatleyServer"

    def __init__(
        self,
        conn_id: int,
        sock: socket.socket,
        address: tuple[str, int],
        server: "WheatleyServer",
    ):
        host, port = address
        logger.info(
            f"Received connection from agent at {host}:{port} (ConnID: {conn_id})"
        )
        self.id = conn_id
        self.sock = sock
        self.address = address
        self._server = server

    def __repr__(self) -> str:
        host, port = self.address
        return f"<conn#{self.id}@{host}:{port}>"

    def close(self) -> None:
        logger.debug(f"{self}\tConnection closed")
        self.sock.close()

    def health_check(self) -> None:
        request = command_pb2.Request()
        request.health_check.CopyFrom(command_pb2.HealthCheckRequest())
        send_protobuf(self.sock, request)
        logger.debug(f"{self}\tSent health check request")

        response = command_pb2.Response()
        response = recv_protobuf(self.sock, response)
        active_field = response.WhichOneof("response")
        if active_field == "health_check":
            logger.debug(f"{self}\tReceived health check response")
