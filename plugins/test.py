from PyQt6.QtWidgets import QHBoxLayout, QLabel, QPushButton, QWidget

from service.gui import PluginUI


class TestPlugin(PluginUI):
    def __init__(self) -> None:
        super().__init__()

    def set_ui(self):
        self.label = QLabel("0")

        btnadd = QPushButton("+")
        btnsub = QPushButton("-")

        btnadd.pressed.connect(
            lambda: self.label.setText(str(int(self.label.text()) + 1))
        )

        btnsub.pressed.connect(
            lambda: self.label.setText(str(int(self.label.text()) - 1))
        )

        buttons = QHBoxLayout()
        buttons.addWidget(btnadd)
        buttons.addWidget(btnsub)

        self.rlayout.addWidget(self.label)
        self.rlayout.addLayout(buttons)
