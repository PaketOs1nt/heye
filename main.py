import logging
import signal

from api.server import HEYEServer
from config import LOGGING_LEVEL, SERVER_ADDR
from mods.notify import NotifyMod
from plugins.settings import SettingsPlugin
from plugins.test import TestPlugin
from plugins.veyondetect import VeyonDetector
from service.gui import MainUI
from service.heye import Service

signal.signal(signal.SIGINT, signal.SIG_DFL)  # что бы qt киллялось от ctrl+c


# настройка логгера
logging.basicConfig(
    level=LOGGING_LEVEL,
    format="%(asctime)s [%(name)s:%(funcName)s] %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)
logger.setLevel(LOGGING_LEVEL)

# создание сервера и UI
ui = MainUI()
server = HEYEServer()
server.bind(SERVER_ADDR)

service = Service(server=server, ui=ui)

# плагины и моды
plugins = [TestPlugin(), SettingsPlugin(), VeyonDetector()]
mods = [NotifyMod()]

# запуск
if __name__ == "__main__":
    service.config()
    service.apply_mods(mods)
    service.add_plugins(plugins)
    service.main()
