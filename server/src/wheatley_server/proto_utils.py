import asyncio
import struct

from google.protobuf.message import Message


def write_protobuf(writer: asyncio.StreamWriter, msg: Message) -> None:
    serialized_msg = msg.SerializeToString()
    header = struct.pack(">I", len(serialized_msg))
    writer.write(header + serialized_msg)


async def read_protobuf(
    reader: asyncio.StreamReader,
    msg: Message,
) -> Message:
    header = await reader.readexactly(4)
    msg_len = struct.unpack(">I", header)[0]
    payload = await reader.readexactly(msg_len)
    msg.ParseFromString(payload)
    return msg
