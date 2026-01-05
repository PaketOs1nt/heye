import logging
from typing import List

from config import EVENTBUS_LOGGING_LEVEL
from core.events import BaseEvent
from core.types import Event, Listener

logger = logging.getLogger(__name__)
logger.setLevel(EVENTBUS_LOGGING_LEVEL)


class EventBus:
    INSTANCE: "EventBus"

    def __init__(self):
        self.listeners: dict[Event, List[Listener]] = {}

    def subscribe(self, event: Event, func: Listener):
        self.listeners.setdefault(event, []).append(func)
        logger.debug("%s connected to %s", func.__qualname__, event.__qualname__)

    def post(self, event: BaseEvent):
        for f in self.listeners.get(type(event), []):
            try:
                event.end(f(event))
                if event.canceled:
                    break

            except Exception as e:
                logger.exception(
                    "%s called by %s, event: %s",
                    e,
                    f.__qualname__,
                    event.__class__.__qualname__,
                )
                event.on_error(e)


EventBus.INSTANCE = EventBus()
