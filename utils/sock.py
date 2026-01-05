import socket


class Timeout:
    def __init__(self, sock: socket.socket) -> None:
        self.sock = sock
        self.old = sock.gettimeout()
        self.time = self.old

    def timeout(self, timeout: float):
        self.time = timeout

    def __enter__(self):
        self.old = self.sock.gettimeout()
        self.sock.settimeout(self.time)

    def __exit__(self, *info):
        self.sock.settimeout(self.old)
