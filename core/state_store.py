from typing import Callable, Awaitable, Any
import asyncio
from core.event_bus import EventBus, Event

class StateStore:
    """
    Allows getting, setting, and subscribing to state changes
    """
    def __init__(self, event_bus: EventBus):
        """
        Initializes the StateStore with an empty state and event bus.
        
        :param event_bus: The EventBus instance to use for emitting state change events
        :type event_bus: EventBus
        """
        self._state: dict[str, Any] = {}
        self._event_bus = event_bus
        self._handlers: dict[str, list[Callable[[Any, Any], Awaitable[None]]]] = {}
    
    def get(self, key: str, default: Any | None = None) -> Any | None:
        """
        Get the current value for a key.

        :param key: The key to retrieve
        :type key: str
        :param default: The default value to return if the key is not found
        :type default: Any | None
        :return: The value associated with the key, or default if not found
        :rtype: Any | None
        """
        return self._state.get(key, default)

    async def set(self, key: str, value: Any, *, source: Any | None=None) -> None:
        """
        Set a value and notify subscribers of the change.

        :param key: The key to set
        :type key: str
        :param value: The value to set it as
        :type value: Any
        :param source: Optional source identifier for the change
        :type source: Any | None
        """
        old_value = self._state.get(key)
        self._state[key] = value
        
        # notify key-specific subscribers
        if key in self._handlers:
            await asyncio.gather(
                *[handler(old_value, value) for handler in self._handlers[key]],
                return_exceptions=True
            )
        
        # emit state change event to the event bus
        await self._event_bus.emit(Event(
            type="state.changed",
            data={"key": key, "old_value": old_value, "new_value": value},
            source=source
        ))

    def subscribe(self, key: str, handler: Callable[[Any, Any], Awaitable[None]]) -> None:
        """
        Subscribe to changes for a specific key.
        
        :param key: The key to subscribe to
        :type key: str
        :param handler: An async function that takes old and new values as arguments and returns None
        :type handler: Callable[[Any, Any], Awaitable[None]]
        """
        if key not in self._handlers:
            self._handlers[key] = []
        self._handlers[key].append(handler)