# MCP Echo Server

A simple Model Context Protocol (MCP) server that echoes input back as-is.

## Installation

```bash
pip install -e .
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

```
mcp-sample/
├── src/
│   └── echo_server.py    # Main server implementation
├── examples/              # Example servers (optional)
├── pyproject.toml        # Package configuration
└── README.md             # This file
```