import logging
import signal

from api.server import HEYEServer
from config import LOGGING_LEVEL, SERVER_ADDR
from plugins.test import TestPlugin
from service.gui import MainUI
from service.heye import Service

signal.signal(signal.SIGINT, signal.SIG_DFL)  # что бы qt киллялось от ctrl+c


# настройка логгера
logging.basicConfig(
    level=LOGGING_LEVEL,
    format="%(asctime)s [%(name)s : %(funcName)s] %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)
logger.setLevel(LOGGING_LEVEL)

# создание сервера и UI
server = HEYEServer()
server.bind(SERVER_ADDR)

ui = MainUI()

service = Service(server=server, ui=ui)

plugins = [TestPlugin()]

# запуск
if __name__ == "__main__":
    service.config()
    service.add_plugins(plugins)
    service.main()
