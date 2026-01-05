from typing import Sequence

from api.server import HEYEServer
from service.gui import MainUI, PluginUI


class Service:
    def __init__(self, server: HEYEServer, ui: MainUI):
        self.server = server
        self.ui = ui

    def config(self):
        self.ui.config()

    def add_plugin(self, plugin: PluginUI):
        self.ui.add_plugin(plugin)

    def add_plugins(self, plugins: Sequence[PluginUI]):
        for plugin in plugins:
            self.ui.add_plugin(plugin)

    def main(self):
        self.ui.main()
