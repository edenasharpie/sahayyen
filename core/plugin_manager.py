import importlib.util
import sys
from pathlib import Path
from core.event_bus import EventBus
from core.state_store import StateStore
from core.scheduler import Scheduler
from core.plugin import Plugin

class PluginManager:
    """
    Can load, unload, and list plugins
    """
    def __init__(self, event_bus: EventBus, state_store: StateStore, scheduler: Scheduler):
        """
        Initialize the PluginManager with core services.
        
        :param event_bus: The EventBus instance
        :param state_store: The StateStore instance
        :param scheduler: The Scheduler instance
        """
        self._plugins: dict[str, Plugin] = {}
        self._event_bus = event_bus
        self._state_store = state_store
        self._scheduler = scheduler

    async def load(self, plugin_path: str) -> str:
        """
        Load a plugin from a Python file.

        :param plugin_path: Path to the plugin Python file
        :return: The name of the loaded plugin
        :rtype: str
        """
        path = Path(plugin_path)
        if not path.exists():
            raise FileNotFoundError(f"Plugin file not found: {plugin_path}")
        
        # load the module dynamically
        spec = importlib.util.spec_from_file_location(path.stem, path)
        if spec is None or spec.loader is None:
            raise ImportError(f"Could not load plugin from: {plugin_path}")
        
        module = importlib.util.module_from_spec(spec)
        sys.modules[path.stem] = module
        spec.loader.exec_module(module)
        
        # find the plugin class (look for a class that implements Plugin interface)
        plugin_instance = None
        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            if isinstance(attr, type) and hasattr(attr, 'setup') and hasattr(attr, 'stop'):
                plugin_instance = attr()
                break
        
        if plugin_instance is None:
            raise ValueError(f"No valid plugin class found in: {plugin_path}")
        
        # set up the plugin
        await plugin_instance.setup(self._event_bus, self._state_store, self._scheduler)
        self._plugins[plugin_instance.name] = plugin_instance
        
        return plugin_instance.name

    async def unload(self, name: str) -> None:
        """
        Unload a plugin by name.
        
        :param name: Name of the plugin to unload
        :type name: str
        """
        if name not in self._plugins:
            raise KeyError(f"Plugin not found: {name}")
        
        plugin = self._plugins[name]
        await plugin.stop()
        del self._plugins[name]

    def list(self) -> list[dict[str, str]]:
        """
        List all loaded plugins with their names and versions.
        
        :return: List of dictionaries with plugin names and versions
        :rtype: list[dict[str, str]]
        """
        return [
            {"name": plugin.name, "version": plugin.version}
            for plugin in self._plugins.values()
        ]