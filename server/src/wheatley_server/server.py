import asyncio
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

    async def accept_connection(
        self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter
    ) -> None:
        agent_conn_id = next(self._agent_conn_id_gen)
        new_conn = AgentConnection(agent_conn_id, reader, writer, self)
        self.connections[agent_conn_id] = new_conn
        host, port = new_conn.address
        logger.info(
            f"[+] Received connection from agent at {host}:{port} "
            f"(ConnID: {agent_conn_id})"
        )

    async def run(self):
        await asyncio.start_server(self.accept_connection, self.host, self.port)
        logger.info(f"Listening for agent connections at {self.host}:{self.port}")
