import json
import socket

from config import SERVER_ADDR
from utils.sock import Timeout


class HEYEClient:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.connect(SERVER_ADDR)
        self.timeout = Timeout(self.sock)

        self.timeout.timeout(1)

    def send(self, data: dict) -> dict:
        raw = json.dumps(data).encode()
        self.sock.send(len(raw).to_bytes(4, byteorder="big"))
        self.sock.send(raw)

        with self.timeout:
            recved = self.sock.recv(4)
            size = int.from_bytes(recved, byteorder="big")
            raw = self.sock.recv(size)
            return json.loads(raw)
