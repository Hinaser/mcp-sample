# Minimal MCP Server Requirements

## Absolute Minimum Files

To create a working MCP server, you need just **ONE file**:

### 1. Python Server File (e.g., `server.py`)

```python
from fastmcp import FastMCP

mcp = FastMCP(name="My Server")

@mcp.tool()
def my_tool() -> str:
    return "Hello!"

if __name__ == "__main__":
    mcp.run()
```

That's it! Just 6 lines of code for a working MCP server.

## Recommended Minimal Setup

For a more practical setup, you should have:

### 1. **server.py** - Your main server implementation
### 2. **pyproject.toml** - For packaging and dependencies

```toml
[project]
name = "my-mcp-server"
version = "0.1.0"
requires-python = ">=3.10"
dependencies = ["fastmcp>=2.0.0"]

[project.scripts]
my-mcp-server = "server:main"
```

### 3. **README.md** - Documentation (optional but recommended)

## File Structure Comparison

### Bare Minimum (1 file):
```
my-mcp-server/
└── server.py
```

### Recommended Minimum (3 files):
```
my-mcp-server/
├── server.py
├── pyproject.toml
└── README.md
```

### Production Setup (from mcp-atlassian example):
```
my-mcp-server/
├── src/
│   └── my_mcp_server/
│       ├── __init__.py      # Package init with main entry
│       ├── server.py        # Server implementation
│       └── tools.py         # Tool definitions
├── tests/                   # Unit tests
├── pyproject.toml          # Package configuration
├── README.md               # Documentation
└── LICENSE                 # License file
```

## Key Components Explained

### 1. FastMCP Instance
```python
mcp = FastMCP(name="Server Name")
```
This creates the MCP server instance.

### 2. Tools
```python
@mcp.tool()
def tool_name(param: str) -> str:
    """Tool description."""
    return "result"
```
Tools are functions the LLM can call.

### 3. Resources (optional)
```python
@mcp.resource("protocol://path")
def resource_name() -> str:
    """Resource description."""
    return "data"
```
Resources provide data/context to the LLM.

### 4. Entry Point
```python
if __name__ == "__main__":
    mcp.run()
```
Runs the server (default: stdio transport).

## Running Your Server

### Direct execution:
```bash
python server.py
```

### With package installation:
```bash
pip install -e .
my-mcp-server
```

### Testing with inspector:
```bash
fastmcp inspect server.py
```

## Transport Options

1. **stdio** (default) - Used by Claude Desktop
2. **sse** - Server-Sent Events for web clients
3. **streamable-http** - HTTP with streaming support

## Adding to Claude Desktop

Add to your Claude Desktop config:
```json
{
  "mcpServers": {
    "my-server": {
      "command": "python",
      "args": ["/path/to/server.py"]
    }
  }
}
```

## Summary

The minimal MCP server is incredibly simple:
- **1 file minimum** (just the Python script)
- **6 lines of code** for basic functionality
- **No complex setup** required
- **FastMCP handles** all the protocol details

Start with the bare minimum and add features as needed!