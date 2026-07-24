# Tools & MCP Module (`enterprise_ai_core.tools` & `enterprise_ai_core.mcp`)

The **Tools & MCP Module** manages tool declaration, schema generation, parameter validation, execution, and Model Context Protocol (MCP) server integration.

## Tools (`enterprise_ai_core.tools`)

### `@tool` Decorator
Converts Python functions into agent tools with automatic OpenAPI-compliant JSON schema generation.

```python
from enterprise_ai_core import tool

@tool(name="customer_search", description="Search customer CRM profile by ID")
def customer_search(customer_id: str) -> str:
    return f"Profile for {customer_id}: Tier=Enterprise"
```

### `ToolRegistry`
Registers, manages, validates, and executes tools safely with authorization and RBAC checks.

---

## Model Context Protocol (`enterprise_ai_core.mcp`)

### `MCPClient` & `MCPDiscovery`
Connects to local or remote MCP servers via standard I/O or SSE transport, discovers available tools dynamically, and manages execution sessions.

```python
mcp_client = MCPClient(server_url="http://localhost:8080/mcp")
await mcp_client.connect()
discovered_tools = await mcp_client.discover_tools()
```
