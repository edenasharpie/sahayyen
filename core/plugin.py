from typing import Protocol
from core.event_bus import EventBus
from core.state_store import StateStore
from core.scheduler import Scheduler

class Plugin(Protocol):
    """
    Base interface that all plugins must implement
    """
    name: str
    version: str
    
    async def setup(self, event_bus: EventBus, state_store: StateStore, scheduler: Scheduler):
        """Called when the plugin is loaded"""
        ...
    
    async def stop(self):
        """Called when the plugin is unloaded"""
        ...