from core.events import MsgEvent
from service.gui import MainUI, Mod


class NotifyMod(Mod):
    def __init__(self) -> None:
        self.can = True

    def on_msg(self, e: MsgEvent):
        if e.data.get("type", "") == "notify":
            msg = e.data.get("msg", "")
            if msg:
                pass

            e.canceled = True

        elif e.data.get("type", "") == "notify-set":
            e.canceled = True

        elif e.data.get("type", "") == "notify-get":
            e.canceled = True
            return {"data": self.can}

        return {}

    def apply(self, main: MainUI):
        MsgEvent.on(self.on_msg)
