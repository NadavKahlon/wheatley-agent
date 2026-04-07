import socket
from typing import TYPE_CHECKING

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
    from wheatley_server.server.server import WheatleyServer


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
        return f"<agent#{self.id}@{host}:{port}>"

    def close(self) -> None:
        logger.debug(f"{self}: Connection closed")
        self.sock.close()

    def _send_command_request(self, command_name: str, **contents) -> None:
        if contents is None:
            contents = {}

        request = command_pb2.Request()
        sub_request = getattr(command_pb2, f"{snake_to_pascal(command_name)}Request")()
        getattr(request, command_name).CopyFrom(sub_request)
        ParseDict(contents, getattr(request, command_name))
        send_protobuf(self.sock, request)

    def _recv_command_response(self, command_name: str) -> dict:
        response = command_pb2.Response()
        recv_protobuf(self.sock, response)
        response_command_name = response.WhichOneof("response")
        assert response_command_name == command_name
        return MessageToDict(getattr(response, response_command_name))

    def _raw_command_interaction(self, command_name: str, **contents) -> dict:
        self._send_command_request(command_name, **contents)
        return self._recv_command_response(command_name)

    def health_check(self) -> None:
        self._raw_command_interaction("health_check")
        logger.debug(f"{self}: Successful health check complete")

    def exec(self, command: str) -> str:
        return self._raw_command_interaction("execute", command=command).get("output")

    def kill(self) -> None:
        self._raw_command_interaction("self_destroy")

    def get_file(
        self, remote_path: str, local_path: str, suggested_chunk_size: int = 4096
    ) -> None:
        self._send_command_request(
            "get_file", path=remote_path, suggested_chunk_size=suggested_chunk_size
        )
        with open(local_path, "wb") as f:
            for chunk in recv_stream(self.sock):
                f.write(chunk)
        self._recv_command_response("get_file")

    def put_file(
        self, local_path: str, remote_path: str, chunk_size: int = 4096
    ) -> None:
        self._send_command_request("put_file", path=remote_path)
        with open(local_path, "rb") as f:
            send_stream(self.sock, f)
        self._recv_command_response("get_file")
