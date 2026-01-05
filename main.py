import logging
import time

from api.client import HEYEClient
from api.server import HEYEServer
from config import LOGGING_LEVEL, SERVER_ADDR
from core.events import MsgEvent
from core.threads import Thread, Threads

logging.basicConfig(
    level=LOGGING_LEVEL,
    format="%(asctime)s [%(name)s : %(funcName)s] %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)
logger.setLevel(LOGGING_LEVEL)

server = HEYEServer()
server.bind(SERVER_ADDR)


def run():
    server.listen()


@MsgEvent.on
def on_msg(msg: MsgEvent):
    print(msg.data)
    return {1: 2}


Threads.INSTANCE.post(Thread(target=run))

client = HEYEClient()

while True:
    time.sleep(5)
    print(client.send({"a": 123}))
