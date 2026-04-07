import socket
from typing import TYPE_CHECKING, Iterator

from google.protobuf.json_format import ParseDict, MessageToDict
from loguru import logger

from wheatley_server.proto.agent import command_pb2
from wheatley_server.network import (
    send_protobuf,
    recv_protobuf,
    recv_stream,
    send_stream,
)
from wheatley_server.utils import snake_to_pascal

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

    def _raw_command_interaction(self, name: str, **contents) -> dict:
        if contents is None:
            contents = {}

        request = command_pb2.Request()
        sub_request = getattr(command_pb2, f"{snake_to_pascal(name)}Request")()
        getattr(request, name).CopyFrom(sub_request)
        ParseDict(contents, getattr(request, name))
        send_protobuf(self.sock, request)

        response = command_pb2.Response()
        recv_protobuf(self.sock, response)
        response_command_name = response.WhichOneof("response")
        assert response_command_name == name
        return MessageToDict(getattr(response, response_command_name))

    def health_check(self) -> None:
        self._raw_command_interaction("health_check")
        logger.debug(f"{self}: Successful health check complete")

    def execute(self, command: str) -> str:
        return self._raw_command_interaction("execute", command=command)["output"]

    def kill(self) -> None:
        self._raw_command_interaction("self_destroy")

    def get_file(
        self, remote_path: str, local_path: str, suggested_chunk_size: int = 4096
    ) -> None:
        self._raw_command_interaction(
            "get_file", path=remote_path, suggested_chunk_size=suggested_chunk_size
        )
        with open(local_path, "wb") as f:
            for chunk in recv_stream(self.sock):
                f.write(chunk)

    def put_file(
        self, local_path: str, remote_path: str, chunk_size: int = 4096
    ) -> None:
        self._raw_command_interaction("put_file", path=remote_path)
        with open(local_path, "rb") as f:
            send_stream(self.sock, f)
