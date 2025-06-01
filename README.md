# MCP Echo Server

A simple Model Context Protocol (MCP) server that echoes input back as-is.

## Installation

Using pip:
```bash
pip install -e .
```

Using uv:
```bash
uv pip install -e .
```

## Usage

### Running directly

```bash
python src/echo_server.py
```

### Using with Claude Desktop

Add to your Claude Desktop configuration:

```json
{
  "mcpServers": {
    "echo-server": {
      "command": "python",
      "args": ["/path/to/mcp-sample/src/echo_server.py"]
    }
  }
}
```

## Available Tools

- `echo(message: str) -> str`: Returns the input message unchanged

## Project Structure

```text
mcp-sample/
├── src/
│   └── echo_server.py    # Main server implementation
├── examples/              # Example servers (optional)
├── pyproject.toml        # Package configuration
└── README.md             # This file
```