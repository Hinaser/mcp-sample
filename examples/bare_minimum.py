#!/usr/bin/env python3
"""The absolute bare minimum MCP server - just 6 lines of code!"""

from fastmcp import FastMCP

mcp = FastMCP(name="Bare Minimum")

@mcp.tool()
def hello() -> str:
    """Say hello"""
    return "Hello from MCP!"

if __name__ == "__main__":
    mcp.run()