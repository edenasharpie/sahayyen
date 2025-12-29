import asyncio
from pathlib import Path
from core import Core

PLUGINS_DIR = Path("plugins")

async def main():
    core = Core()

    # load all plugins from plugins/
    for plugin_file in PLUGINS_DIR.glob("*.py"):
        try:
            name = await core.plugins.load(str(plugin_file))
            print(f"Loaded plugin: {name}")
        except Exception as e:
            print(f"Failed to load {plugin_file.name}: {e}")

    print("Home assistant running. Press Ctrl+C to exit.")

    try:
        await asyncio.Event().wait()
    except KeyboardInterrupt:
        print("Shutting down...")
        core.cleanup()

        # unload plugins
        for plugin in core.plugins.list():
            await core.plugins.unload(plugin["name"])

if __name__ == "__main__":
    asyncio.run(main())