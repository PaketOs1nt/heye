from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QCheckBox, QPushButton

from api.client import HEYEClient
from service.gui import PluginUI


class SettingsPlugin(PluginUI):
    def __init__(self) -> None:
        super().__init__()
        self.client = HEYEClient()

    def test_notify(self):
        self.client.send({"type": "notify", "msg": "Test Notify!", "time": 2000})

    def send_status(self, state):
        self.client.send({"type": "notify-set", "data": state})

    def set_ui(self):
        btn_test_notify = QPushButton("Test Notify")
        btn_test_notify.pressed.connect(self.test_notify)

        notify_status = QCheckBox("Notify")
        notify_status.setCheckState(Qt.CheckState.Checked)
        notify_status.stateChanged.connect(self.send_status)

        self.rlayout.addWidget(btn_test_notify)
        self.rlayout.addWidget(notify_status)
