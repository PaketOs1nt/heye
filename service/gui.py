import sys

import keyboard
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QColor, QPalette
from PyQt6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from config import GUI_TITLE_NAME, GUI_TOGGLE_HOTKEY


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

    def toggle_menu(self):
        self.setHidden(not self.isHidden())

    def config(self):
        keyboard.add_hotkey(GUI_TOGGLE_HOTKEY, callback=self.toggle_menu)
        self.create_widgets()

    def create_widgets(self):
        self.rlayout = QHBoxLayout()

        context = QWidget()
        context.setContentsMargins(0, 0, 0, 0)
        context.setLayout(self.rlayout)

        self.setCentralWidget(context)

    def add_plugin(self, p: PluginUI):
        p.set_ui()
        self.rlayout.addWidget(p, stretch=0, alignment=Qt.AlignmentFlag.AlignTop)

    def main(self):
        self.show()
        self.app.exec()
