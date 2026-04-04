import asyncio
import threading
from itertools import count

from loguru import logger

from wheatley_server.agent.connection import AgentConnection


class WheatleyServer:

    host: str
    port: int
    connections: dict[int, AgentConnection] = {}
    _agent_conn_id_gen: count = count(1)
    loop: asyncio.AbstractEventLoop | None = None

    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port

    async def _accept_connection(
        self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter
    ) -> None:
        if self.loop:
            agent_conn_id = next(self._agent_conn_id_gen)
            new_conn = AgentConnection(agent_conn_id, reader, writer, self)
            self.connections[agent_conn_id] = new_conn
            host, port = new_conn.address
            logger.info(
                f"[+] Received connection from agent at {host}:{port} "
                f"(ConnID: {agent_conn_id})"
            )

    def run(self) -> None:
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(
            asyncio.start_server(self._accept_connection, self.host, self.port)
        )
        logger.info(f"Listening for agent connections at {self.host}:{self.port}")
        self.loop.run_forever()

    def start_daemon(self) -> None:
        thread = threading.Thread(target=self.run, daemon=True)
        thread.start()
