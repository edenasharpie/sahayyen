import time
from core.event_bus import Event
from core.plugin import Plugin

class Heartbeat(Plugin):
    name = "heartbeat"
    version = "1.0.0"

    async def setup(self, event_bus, state_store, scheduler):
        self.event_bus = event_bus
        self.state_store = state_store
        self.scheduler = scheduler

        # schedule a repeating task every 5 seconds
        self.scheduler.call_every(5, self._tick, owner=self.name)

    async def _tick(self):
        now = time.time()

        # update state
        await self.state_store.set("heartbeat.tick", now, source=self.name)
        print(f"Heartbeat at {now}")

        # emit event
        await self.event_bus.emit(
            Event(
                type="heartbeat.tick",
                data={"timestamp": now},
                source=self.name,
            )
        )
        print("Event emitted: heartbeat.tick")

    async def stop(self):
        self.scheduler.cancel_owner(self.name)