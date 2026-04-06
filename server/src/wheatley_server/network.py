import struct

from google.protobuf.message import Message

import socket


def recv_exactly(sock, size):
    data = bytearray()
    while len(data) < size:
        packet = sock.recv(size - len(data))
        if not packet:
            raise ConnectionError(
                f"Connection closed before receiving {size} expected bytes (got {len(data)})."
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
    try:
        # Peek into buffer
        data = sock.recv(1, socket.MSG_PEEK)
        if len(data) == 0:
            return True
    except BlockingIOError:
        return False  # socket is open and reading from it would block
    except ConnectionResetError:
        return True  # socket was closed for some other reason
    return False
