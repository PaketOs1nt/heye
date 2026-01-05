import json
import logging
import socket
from typing import Tuple

from config import SERVER_LOGGING_LEVEL, SERVER_TIMEOUT, SERVER_WAIT_MSG_TIMEOUT
from core.eventbus import EventBus
from core.events import MsgEvent
from utils.sock import Timeout

logger = logging.getLogger(__name__)
logger.setLevel(SERVER_LOGGING_LEVEL)


class HEYEServer:
    def __init__(self) -> None:
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.timeout = Timeout(self.sock)

        self.sock.settimeout(SERVER_TIMEOUT)
        self.timeout.timeout(SERVER_WAIT_MSG_TIMEOUT)

    def bind(self, addr: Tuple[str, int]):
        self.sock.bind(addr)

    def listen(self):
        while True:
            try:
                data, pre_addr = self.sock.recvfrom(4)
                size = int.from_bytes(data, byteorder="big")
                with self.timeout:
                    raw, addr = self.sock.recvfrom(size)
                    data = json.loads(raw)
                    if addr == pre_addr:
                        EventBus.INSTANCE.post(
                            MsgEvent(sock=self.sock, data=data, addr=addr)
                        )

            except ConnectionAbortedError:
                pass

            except TimeoutError:
                pass

            except Exception as e:
                logger.exception("server exception: %s", e)
