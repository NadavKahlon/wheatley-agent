import asyncio
from typing import TYPE_CHECKING

from loguru import logger

from wheatley_server.proto import write_protobuf, read_protobuf
from wheatley_server.proto.agent import commands_pb2

if TYPE_CHECKING:
    from wheatley_server.server import WheatleyServer


class AgentConnection:

    id: int
    reader: asyncio.StreamReader
    writer: asyncio.StreamWriter
    _server: "WheatleyServer"

    def __init__(
        self,
        conn_id: int,
        reader: asyncio.StreamReader,
        writer: asyncio.StreamWriter,
        server: "WheatleyServer",
    ):
        self.id = conn_id
        self.reader = reader
        self.writer = writer
        self._server = server

    @property
    def address(self) -> tuple[str, int]:
        return self.writer.get_extra_info("peername")

    def __repr__(self) -> str:
        host, port = self.address
        return f"<wheatley@{host}:{port}>"

    def is_active(self) -> bool:
        return not self.writer.is_closing()

    def close(self) -> None:
        """Thread-safe close."""

        def _close() -> None:
            self.writer.close()
            del self._server.connections[self.id]
            logger.info(f"Closed connection to {self.address} (ConnID: {self.id})")

        self._server.loop.call_soon_threadsafe(_close)

    def health_check(self) -> None:
        write_protobuf(self.writer, commands_pb2.HealthCheckRequest())
        logger.debug(f"Send health check request to {self.address} (ConnID: {self.id})")
        read_protobuf(self.reader, commands_pb2.HealthCheckResponse)
        logger.debug(f"Received health check response from {self.address} (ConnID: {self.id})")
