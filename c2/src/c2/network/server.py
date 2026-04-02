import asyncio
import threading
import time
from itertools import count

from loguru import logger

from c2.network.connection import WheatleyConnection


class WheatleyServer:

    host: str
    port: int
    connections: dict[int, WheatleyConnection] = {}
    _id_gen: count = count(1)
    loop: asyncio.AbstractEventLoop | None = None

    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port

    async def _accept_connection(
        self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter
    ) -> None:
        if self.loop:
            conn_id = next(self._id_gen)
            new_conn = WheatleyConnection(conn_id, reader, writer, self)
            self.connections[conn_id] = new_conn
            host, port = new_conn.address
            logger.info(
                f"[+] Received connection from a Wheatley at {host}:{port} "
                f"(ConnID: {conn_id})"
            )

    def _daemon(self) -> None:
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(
            asyncio.start_server(self._accept_connection, self.host, self.port)
        )
        logger.info(f"Collecting Wheatley connections at {self.host}:{self.port}")
        self.loop.run_forever()

    def start_daemon(self) -> None:
        thread = threading.Thread(target=self._daemon, daemon=True)
        thread.start()
