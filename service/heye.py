from typing import Sequence

from api.server import HEYEServer
from core.threads import Thread, Threads
from service.gui import MainUI, Mod, PluginUI


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

    def apply_mods(self, mods: Sequence[Mod]):
        for mod in mods:
            mod.apply(self.ui)

    def main(self):
        Threads.INSTANCE.post(Thread(target=self.server.listen, name="HEYE Server"))
        self.ui.main()
