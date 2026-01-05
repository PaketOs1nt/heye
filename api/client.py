import json
import socket

from config import SERVER_ADDR


class HEYEClient:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.connect(SERVER_ADDR)

    def send(self, data: dict) -> dict:
        raw = json.dumps(data).encode()
        self.sock.send(len(raw).to_bytes(4, byteorder="big"))
        self.sock.send(raw)

        recved, _ = self.sock.recvfrom(4)
        size = int.from_bytes(recved, byteorder="big")
        raw, _ = self.sock.recvfrom(size)
        return json.loads(raw)
