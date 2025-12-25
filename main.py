import asyncio
from core import Core

async def main():
    core = Core()

    ...

    try:
        await asyncio.Event().wait()
    except KeyboardInterrupt:
        print("Shutting down...")
        core.cleanup()

if __name__ == "__main__":
    asyncio.run(main())