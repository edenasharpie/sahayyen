from typing import Callable, Awaitable
import asyncio
from core.event import Event

class EventBus:
    """
    Allows publishing and subscribing to events within the system.
    """

    def __init__(self):
        """
        Initializes the EventBus with an empty handler registry.
        """
        self._handlers: dict[str, list[Callable[[Event], Awaitable[None]]]] = {}
    
    def subscribe(self, event_type: str, handler: Callable[[Event], Awaitable[None]]) -> None:
        """
        Subscribe a handler to a specific event type.
        
        :param event_type: The type of event to subscribe to (string)
        :type event_type: str
        :param handler: An async function that takes an Event as argument and returns None
        :type handler: Callable[[Event], Awaitable[None]]
        """
        if event_type not in self._handlers:
            # event type is not found, so initialize the list for it
            self._handlers[event_type] = []
        # add the handler to the list for this event type
        self._handlers[event_type].append(handler)

    async def emit(self, event: Event) -> None:
        """
        Emit an event to all subscribed handlers.

        :param event: The Event instance to emit
        :type event: Event
        """
        if event.type in self._handlers:
            # call all handlers concurrently
            await asyncio.gather(
                *[handler(event) for handler in self._handlers[event.type]],
                return_exceptions=True
            )