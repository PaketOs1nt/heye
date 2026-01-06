import sys
from typing import Any, List

import keyboard
from PyQt6.QtCore import QMetaObject, QObject, QSize, Qt, QTimer, pyqtSlot
from PyQt6.QtGui import QColor, QPalette
from PyQt6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QMainWindow,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from config import GUI_TITLE_NAME, GUI_TOGGLE_HOTKEY


class GuiExecutor(QObject):
    INSTANCE: "GuiExecutor"
    EXECUTOR: Any = None
    ARGS = []

    @pyqtSlot()
    def _trigger(self):
        if GuiExecutor.EXECUTOR:
            GuiExecutor.EXECUTOR(*GuiExecutor.ARGS)

    def trigger(self):
        QMetaObject.invokeMethod(
            GuiExecutor.INSTANCE, "_trigger", Qt.ConnectionType.QueuedConnection
        )


class Mod:
    def __init__(self) -> None:
        pass

    def apply(self, main: "MainUI"):
        pass


class PluginUI(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.rlayout = QVBoxLayout()

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor())

        self.setPalette(palette)
        self.setAutoFillBackground(True)

        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.setLayout(self.rlayout)

    def set_ui(self):
        pass


class MainUI(QMainWindow):
    def __init__(self) -> None:
        self.app = QApplication(sys.argv)
        self.app.setStyle("Fusion")

        GuiExecutor.INSTANCE = GuiExecutor()

        self.screen_size = QSize(0, 0)

        super().__init__()

        self.setWindowTitle(GUI_TITLE_NAME)
        self.move(0, 0)

        screen = self.app.primaryScreen()
        if screen:
            self.screen_size = screen.size()
            # self.resize(self.screen_size)

        self.showFullScreen()

        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.plugins: List[PluginUI] = []

    def toggle_menu(self):
        for p in self.plugins:
            p.setHidden(not p.isHidden())

    def config(self):
        keyboard.add_hotkey(
            GUI_TOGGLE_HOTKEY, callback=lambda: QTimer.singleShot(0, self.toggle_menu)
        )
        self.create_widgets()

    def create_widgets(self):
        self.rlayout = QHBoxLayout()

        self.rlayout.setContentsMargins(10, 10, 10, 10)

        context = QWidget()
        context.setContentsMargins(0, 0, 0, 0)
        context.setLayout(self.rlayout)

        self.setCentralWidget(context)

    def add_plugin(self, p: PluginUI):
        p.set_ui()
        self.plugins.append(p)
        self.rlayout.addWidget(p, stretch=0, alignment=Qt.AlignmentFlag.AlignTop)

    def main(self):
        self.show()
        self.app.exec()
