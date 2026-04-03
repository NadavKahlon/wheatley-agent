import asyncio
from typing import TYPE_CHECKING

from loguru import logger

if TYPE_CHECKING:
    from wheatley.network.server import WheatleyServer


class WheatleyConnection:

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
