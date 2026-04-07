import struct
from typing import Iterator, BinaryIO

from google.protobuf.message import Message

import socket

from wheatley_server.proto import stream_pb2


def recv_exactly(sock, size):
    data = bytearray()
    while len(data) < size:
        packet = sock.recv(size - len(data))
        if not packet:
            raise ConnectionError(
                f"Connection closed before receiving {size} expected bytes (got {len(data)})"
            )
        data.extend(packet)
    return bytes(data)


def recv_protobuf(
    sock: socket.socket,
    msg: Message,
):
    header = recv_exactly(sock, 4)
    msg_len = struct.unpack(">I", header)[0]
    payload = recv_exactly(sock, msg_len)
    msg.ParseFromString(payload)


def send_protobuf(sock: socket.socket, msg: Message) -> None:
    serialized_msg = msg.SerializeToString()
    header = struct.pack(">I", len(serialized_msg))
    sock.send(header + serialized_msg)


def is_socket_closed(sock: socket.socket) -> bool:
    original_timeout = sock.gettimeout()
    try:
        sock.settimeout(0)
        data = sock.recv(1, socket.MSG_PEEK)
        if len(data) == 0:
            return True
    except BlockingIOError:
        return False  # socket is open and reading from it would block
    except ConnectionResetError:
        return True  # socket was closed for some other reason
    finally:
        sock.settimeout(original_timeout)  # Restore original state
    return False


def recv_stream(sock: socket.socket) -> Iterator[bytes]:
    while True:
        packet = stream_pb2.WheatleyStreamPacket()
        recv_protobuf(sock, packet)
        yield packet.chunk
        if packet.is_last:
            break


def send_stream(sock: socket.socket, stream: BinaryIO, chunk_size: int = 4096) -> None:
    next_chunk = stream.read(chunk_size)
    while next_chunk != "":
        curr_chunk = next_chunk
        next_chunk = stream.read(chunk_size)

        packet = stream_pb2.WheatleyStreamPacket()
        packet.chunk = curr_chunk
        packet.is_last = next_chunk == ""
        send_protobuf(sock, packet)
