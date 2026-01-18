import logging

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QColor, QPalette
from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget

from config import NOTIFY_LOGGING_LEVEL
from core.events import MsgEvent
from service.gui import GuiExecutor, MainUI, Mod

logger = logging.getLogger(__name__)
logger.setLevel(NOTIFY_LOGGING_LEVEL)


class NotifyWindow(QWidget):
    def __init__(self, text: str, timeout: int, p) -> None:
        super().__init__(p)

        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.Tool
        )

        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 10, 15, 10)

        label = QLabel(text)
        label.setStyleSheet("color: white; font-weight: bold;")

        layout.addWidget(label)

        self.setLayout(layout)

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor())

        self.setPalette(palette)
        self.setAutoFillBackground(True)

        self.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating)

        QTimer.singleShot(timeout, self.destroy)

        self.adjustSize()

        screen = self.screen()
        if screen:
            geo = screen.availableGeometry()
            self.move(
                geo.right() - self.width() - 20, geo.bottom() - self.height() - 20
            )

        QTimer.singleShot(0, self.show)

        logger.debug("notify window inited")


class Notify:
    def __init__(self, text: str, timeout: int, app: QWidget):
        self.text = text
        self.timeout = timeout
        self.app = app

    def run(self):
        GuiExecutor.ARGS = [self.text, self.timeout, self.app]
        GuiExecutor.EXECUTOR = NotifyWindow
        GuiExecutor.INSTANCE.trigger()


class NotifyMod(Mod):
    def __init__(self) -> None:
        self.can = True

    def on_msg(self, e: MsgEvent):
        if e.data.get("type", "") == "notify":
            msg: str = e.data.get("msg", "")
            time: int = e.data.get("time", 3000)
            if msg:
                logger.info("recved notify '%s' : %s", msg, time)

                if self.can:
                    Notify(text=msg, timeout=time, app=self.main).run()

            e.canceled = True

        elif e.data.get("type", "") == "notify-set":
            data = e.data.get("data", 123)
            if data != 123:
                logger.info("notify was %s", "ON" if data else "OFF")
                self.can = data
                e.canceled = True

        elif e.data.get("type", "") == "notify-get":
            e.canceled = True
            return {"data": self.can}

        return {}

    def apply(self, main: MainUI):
        self.main = main
        MsgEvent.on(self.on_msg)
