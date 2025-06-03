# Windows Authentication MCP Server

This MCP server allows Claude Desktop to fetch URLs using Windows authentication (NTLM/Kerberos).

## Setup

1. Install dependencies:
```bash
pip install -e ".[windows-auth]"
```

2. Configure Claude Desktop:

### Option 1: Using Python in PATH
If your virtual environment Python is in PATH:
```json
{
  "mcpServers": {
    "windows-auth-fetch": {
      "command": "python",
      "args": ["win_auth_http.py"],
      "cwd": "C:\\path\\to\\mcp-sample\\examples"
    }
  }
}
```

### Option 2: Using full paths
```json
{
  "mcpServers": {
    "windows-auth-fetch": {
      "command": "C:\\path\\to\\your\\.venv\\Scripts\\python.exe",
      "args": ["C:\\path\\to\\mcp-sample\\examples\\win_auth_http.py"]
    }
  }
}
```

### Option 3: Using module execution
```json
{
  "mcpServers": {
    "windows-auth-fetch": {
      "command": "python",
      "args": ["-m", "examples.win_auth_http"],
      "cwd": "C:\\path\\to\\mcp-sample"
    }
  }
}
```

## Usage

In Claude Desktop, you can use the tool like this:
- "Fetch http://internal.site.com using Windows authentication"
- "Get the content from http://dbweb/"

The server will automatically try different authentication methods (NTLM, Kerberos, Negotiate).

## Note

Do not commit configuration files with hardcoded paths. Use the template and adjust paths locally.