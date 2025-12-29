import asyncio
from typing import Callable, Awaitable, Any

class Scheduler:
    """
    Allows coroutines to be called later or periodically
    """
    def __init__(self):
        """
        Initialize the Scheduler with an empty task list (key = plugin name, value = list of tasks).
        """
        self._tasks: dict[str, list[asyncio.Task]] = {}
    
    def call_later(self, delay: float, coroutine: Callable[[], Awaitable[Any]], *, owner: str) -> asyncio.Task:
        """
        Schedule a coroutine to be called once after a delay.

        :param delay: Delay in seconds before calling the coroutine
        :type delay: float
        :param coroutine: The coroutine function to be called
        :type coroutine: Callable[[], Awaitable[Any]]
        :param owner: The owner of the task, typically the plugin name
        :type owner: str
        :return: The created asyncio Task
        :rtype: asyncio.Task
        """
        async def _delayed():
            await asyncio.sleep(delay)
            await coroutine()

        task = asyncio.create_task(_delayed())
        self._tasks.setdefault(owner, []).append(task)
        return task
    
    def call_every(self, interval: float, coroutine: Callable[[], Awaitable[Any]], *, owner: str) -> asyncio.Task:
        """
        Schedule a coroutine to be called repeatedly at an interval.

        :param interval: Interval in seconds between calls
        :type interval: float
        :param coroutine: The coroutine function to be called
        :type coroutine: Callable[[], Awaitable[Any]]
        :param owner: The owner of the task, typically the plugin name
        :type owner: str
        :return: The created asyncio Task
        :rtype: asyncio.Task
        """
        async def _periodic():
            while True:
                await asyncio.sleep(interval)
                await coroutine()

        task = asyncio.create_task(_periodic())
        self._tasks.setdefault(owner, []).append(task)
        return task

    def cancel_owner(self, owner: str) -> None:
        """
        Cancel all scheduled tasks for a specific owner.
        
        :param owner: The owner of the task, typically the plugin name
        :type owner: str
        """
        for task in self._tasks.get(owner, []):
            task.cancel()
        self._tasks.pop(owner, None)

    def cancel_all(self) -> None:
        """
        Cancel all scheduled tasks.
        """
        for tasks in self._tasks.values():
            for task in tasks:
                task.cancel()
        self._tasks.clear()