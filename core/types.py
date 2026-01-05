from typing import TYPE_CHECKING, Any, Callable, Type

if TYPE_CHECKING:
    from core.events import BaseEvent

type Event = Type[BaseEvent]
type Listener = Callable[[Any], Any]
