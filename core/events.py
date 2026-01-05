import json
import socket
from dataclasses import dataclass, field
from typing import Any

from core.types import Listener


@dataclass
class BaseEvent:
    canceled: bool = False

    def on_error(self, e: Exception):
        pass

    @classmethod
    def on(cls, f: Listener):
        from core.eventbus import EventBus

        EventBus.INSTANCE.subscribe(cls, f)

    def end(self, result: Any):
        pass


@dataclass
class MsgEvent(BaseEvent):
    sock: socket.socket | Any = None
    data: dict = field(default_factory=dict)
    addr: Any = None

    def end(self, result: Any):
        raw = json.dumps(result).encode()
        self.sock.sendto(len(raw).to_bytes(4, byteorder="big"), self.addr)
        self.sock.sendto(raw, self.addr)
        self.sock.sendto(raw, self.addr)
