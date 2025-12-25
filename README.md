# **sahayyen**

### sahayyen is a custom made personal home assistant made to run on a raspberry pi.

The project's name is from the globasa word for assistant or helper: sahay-yen ( \[help/helping\] - \[animate-agent\] )

# Documentation Overview

Project structure:

### -/main.py

```py
(async) main()
```

## -/core/

### \_\_init\_\_.py:
#### class `Core` 

```py
cleanup()
```
Cleans up all scheduled tasks.

---
### event_bus.py:

#### class `EventBus`
Allows publishing and subscribing to events within the system.

```py 
subscribe(event_type: str, handler: Callable[[Event], Awaitable[None]])
```
Subscribes a handler to a specific event type.

- `event_type` [`str`]:
The type of event to subscribe to.

- `handler` [`Callable[[Event], Awaitable[None]]`]:
An async function that takes an Event as argument and returns None.


```py 
(async) emit(event: Event)
```
Emits an event to all subscribed handlers.

- `event` [`Event`]:
The Event instance to emit.

---
### event.py:

#### @dataclass `Event`
Represents a single event in the system.

**Member variables**:
- `type`      [`str`]:        The type of the event
- `data`      [`dict`]:       The data associated with the event
- `source`    [`str | None`]: Optional source identifier of the event
- `timestamp` [`float`]:      The time the event was created

---
### plugin_manager.py:

#### class `PluginManager`
Can load, unload, and list plugins

**Initialization parameters**:
- `event_bus` [`EventBus`]: The EventBus instance
- `state_store` [`StateStore`]: The StateStore instance
- `scheduler` [`Scheduler`]: The Scheduler instance

```py
(async) load(plugin_path: str) -> str
```
Loads a plugin from a Python file.

- `plugin_path` [`str`]: Path to the plugin Python file
- returns [`str`]: The name of the loaded plugin

```py
(async) unload(name: str)
```
Unloads a plugin by name.

- `name` [`str`]: Name of the plugin to unload

```py
list() -> list[dict[str, str]]
```
Lists all loaded plugins with their names and versions.

- returns [`list[dict[str, str]]`]:
List of dictionaries with plugin names and versions

---
### plugin.py:

#### class `Plugin(Protocol)`
Base interface that all plugins must implement

**Member variables**:
- `name` [str]: name of the plugin
- `version` [str]: version of the plugin


```py
(async) setup(event_bus: EventBus, state_store: StateStore, scheduler: Scheduler)
```
Called when the plugin is loaded

- `event_bus` [`EventBus`]: The EventBus instance
- `state_store` [`StateStore`]: The StateStore instance
- `scheduler` [`Scheduler`]: The Scheduler instance

```py
(async) stop()
```
Called when the plugin is unloaded

---
### scheduler.py:

#### class `Scheduler`
Allows scheduling coroutines to be called later or periodically

```py
call_later(delay: float, coroutine: Callable[[], Awaitable[Any]]) -> asyncio.Task
```
Schedules a coroutine to be called once after a delay.

- `delay` [`float`]: Delay in seconds before calling the coroutine
- `coroutine` [`Callable[[], Awaitable[Any]]`]: The coroutine function to be called
- returns: [`asyncio.Task`]: The created asyncio Task

```py
call_every(interval: float, coroutine: Callable[[], Awaitable[Any]]) -> asyncio.Task
```
Schedules a coroutine to be called repeatedly at an interval.

- `interval` [`float`]: Interval in seconds between calls
- `coroutine` [`Callable[[], Awaitable[Any]]`]: The coroutine function to be called
- returns [`asyncio.Task`]: The created asyncio Task

```py
cancel_all()
```
Cancels all scheduled tasks.

---
### state_store.py:

#### class `StateStore`
Allows getting, setting, and subscribing to state changes

**Initialization parameters**:
- `event_bus` [`EventBus`]: The EventBus instance to use for emitting state change events

```py
get(key: str, <default: Any | None> ) -> Any | None
```
Gets the current value for a key.

- `key` [`str`]: The key to retrieve
- `default` [`Any | None`] (optional): The default value to return if the key is not found
- returns [`Any | None`]: The value associated with the key, or default if not found

```py
(async) set(key: str, value: Any, * <source: Any | None> )
```
Sets a value and notify subscribers of the change.

- `key` [`str`]: The key to seta
- `value` [`Any`]: The value to set it as
- `source` [`Any | None`] (optional, keyword-only): Optional source identifier for the change

```py
subscribe(key: str, handler: Callable[[Any, Any], Awaitable[None]])
```
Subscribes to changes for a specific key.

- `key` [`str`]: The key to subscribe to
- `name` [`Callable[[Any, Any], Awaitable[None]]`]: An async function that takes old and new values as arguments and returns None