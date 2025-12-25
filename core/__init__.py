from core.event_bus import EventBus, Event
from core.state_store import StateStore
from core.scheduler import Scheduler
from core.plugin_manager import PluginManager
from core.plugin import Plugin

class Core:
    """
    Main entry point for the home assistant system.
    Initializes and provides access to all core services.
    """
    def __init__(self):
        """
        Initialize core services.
        """
        self.events = EventBus()
        self.state = StateStore(self.events)
        self.scheduler = Scheduler()
        self.plugins = PluginManager(self.events, self.state, self.scheduler)
    
    def cleanup(self) -> None:
        """
        Clean up all scheduled tasks.
        """
        self.scheduler.cancel_all()

# define what is available when importing * from this module
__all__ = ["Core", "EventBus", "Event", "StateStore", "Scheduler", "PluginManager", "Plugin"]