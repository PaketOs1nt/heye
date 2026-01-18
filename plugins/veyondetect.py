import logging
import socket
import time
from dataclasses import dataclass
from functools import cache
from typing import Set

import psutil
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import QCheckBox, QListWidget

from api.client import HEYEClient
from config import VEYON_DETECTOR_LOGGING_LEVEL, VEYON_DETECTOR_SCAN_DELAY
from core.threads import Thread, Threads
from service.gui import PluginUI

VEYON_PORTS = [11100, 11200, 11300]

logger = logging.getLogger(__name__)
logger.setLevel(VEYON_DETECTOR_LOGGING_LEVEL)


@cache
def gethost(ip: str):
    return socket.gethostbyaddr(ip)


@dataclass
class VeyonClient:
    ip: str

    def __hash__(self) -> int:
        return hash(self.ip) + 1

    def __str__(self) -> str:
        try:
            return gethost(self.ip)[0]
        except (OSError, IndexError):
            return self.ip


class VeyonDetector(PluginUI):
    def __init__(self) -> None:
        super().__init__("Veyon detector")
        self.old_clients: Set[VeyonClient] = set()
        self.clients: Set[VeyonClient] = set()
        self.notify = True

        self.client = HEYEClient()

    def update_clients(self):
        self.old_clients = self.clients.copy()
        self.clients.clear()
        for conn in psutil.net_connections("tcp"):
            try:
                if (
                    conn.laddr
                    and conn.laddr.port in VEYON_PORTS
                    and conn.status == psutil.CONN_ESTABLISHED
                    and conn.raddr
                ):
                    self.clients.add(VeyonClient(conn.raddr.ip))

            except Exception as e:
                logger.exception("exception %s", e)

    def update_render_clients(self):
        self.clients_w.clear()
        self.clients_w.addItems(str(c) for c in self.clients)
        logger.debug("updated widgets")

    def update_cycle(self):
        while True:
            self.update_clients()
            logger.debug("clients: %s", self.clients)
            if self.clients != self.old_clients:
                added = self.clients - self.old_clients
                removed = self.old_clients - self.clients

                added_formatted = ", ".join(str(c) for c in added)
                removed_formatted = ", ".join(str(c) for c in removed)

                if added:
                    logger.info("added clients: %s", added_formatted)
                    if self.notify:
                        self.client.send(
                            {
                                "type": "notify",
                                "msg": f"VEYON DETECTOR\nadded {added_formatted}",
                                "time": 5000,
                            }
                        )

                if removed:
                    logger.info("removed clients: %s", removed_formatted)
                    if self.notify:
                        self.client.send(
                            {
                                "type": "notify",
                                "msg": f"VEYON DETECTOR\nremoved {removed_formatted}",
                                "time": 5000,
                            }
                        )

                QTimer.singleShot(0, self.update_render_clients)

            time.sleep(VEYON_DETECTOR_SCAN_DELAY)

    def callback_notify_box(self, val):
        self.notify = val

    def set_ui(self):
        notify_status = QCheckBox("Send notify")
        notify_status.setCheckState(Qt.CheckState.Checked)
        notify_status.stateChanged.connect(self.callback_notify_box)

        self.clients_w = QListWidget()
        self.clients_w.setFixedHeight(100)
        self.clients_w.setFixedWidth(150)

        self.rlayout.addWidget(notify_status)
        self.rlayout.addWidget(self.clients_w)

        Threads.INSTANCE.post(
            Thread(target=self.update_cycle, name="Veyon Detector Cycle")
        )
