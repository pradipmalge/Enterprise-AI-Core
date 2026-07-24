import asyncio
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from enterprise_ai_core.plugins.loader import PluginLoader

class CustomAuditPlugin:
    def audit(self, action: str):
        print(f"[AUDIT PLUGIN] Logged action: {action}")

async def main():
    print("=== Example 12: External Plugin Loader ===")
    loader = PluginLoader()
    loader.register_plugin("audit", CustomAuditPlugin())

    plugin = loader.get_plugin("audit")
    plugin.audit("User initialized enterprise agent")

if __name__ == "__main__":
    asyncio.run(main())
