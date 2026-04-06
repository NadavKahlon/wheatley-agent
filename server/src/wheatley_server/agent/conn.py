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
        agent_conn_id: int,
        sock: socket.socket,
        address: tuple[str, int],
        server: "WheatleyServer",
    ):
        host, port = address
        self.id = agent_conn_id
        self.sock = sock
        self.address = address
        self._server = server
        logger.info(f"{self}: New agent connection")

    def __repr__(self) -> str:
        host, port = self.address
        return f"<conn#{self.id}@{host}:{port}>"

    def close(self) -> None:
        logger.debug(f"{self}: Connection closed")
        self.sock.close()

    def health_check(self) -> None:
        request = command_pb2.Request()
        request.health_check.CopyFrom(command_pb2.HealthCheckRequest())
        send_protobuf(self.sock, request)
        logger.debug(f"{self}: Sent health check request")

        response = command_pb2.Response()
        recv_protobuf(self.sock, response)
        if response.WhichOneof("response") == "health_check":
            logger.debug(f"{self}: Received health check response")

    def execute(self, command: str) -> str:
        request = command_pb2.Request()
        request.execute.CopyFrom(command_pb2.ExecuteRequest())
        request.execute.command = command
        send_protobuf(self.sock, request)

        response = command_pb2.Response()
        recv_protobuf(self.sock, response)
        return response.execute.output
