import asyncio
from typing import Callable, Awaitable, Any

class Scheduler:
    """
    Allows scheduling coroutines to be called later or periodically
    """
    def __init__(self):
        """
        Initialize the Scheduler with an empty task list
        """
        self._tasks: list[asyncio.Task] = []
    
    def call_later(self, delay: float, coroutine: Callable[[], Awaitable[Any]]) -> asyncio.Task:
        """
        Schedule a coroutine to be called once after a delay.

        :param delay: Delay in seconds before calling the coroutine
        :type delay: float
        :param coroutine: The coroutine function to be called
        :type coroutine: Callable[[], Awaitable[Any]]
        :return: The created asyncio Task
        :rtype: asyncio.Task
        """
        async def _delayed():
            await asyncio.sleep(delay)
            await coroutine()
        
        task = asyncio.create_task(_delayed())
        self._tasks.append(task)
        return task
    
    def call_every(self, interval: float, coroutine: Callable[[], Awaitable[Any]]) -> asyncio.Task:
        """
        Schedule a coroutine to be called repeatedly at an interval.

        :param interval: Interval in seconds between calls
        :type interval: float
        :param coroutine: The coroutine function to be called
        :type coroutine: Callable[[], Awaitable[Any]]
        :return: The created asyncio Task
        :rtype: asyncio.Task
        """
        async def _periodic():
            while True:
                await asyncio.sleep(interval)
                await coroutine()
        
        task = asyncio.create_task(_periodic())
        self._tasks.append(task)
        return task
    
    def cancel_all(self) -> None:
        """
        Cancel all scheduled tasks.
        """
        for task in self._tasks:
            task.cancel()
        self._tasks.clear()