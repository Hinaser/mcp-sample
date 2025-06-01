#!/usr/bin/env python3
"""
Simple Echo MCP Server

This MCP server has just one tool that returns the input as-is.
"""

from fastmcp import FastMCP

# Create the MCP server
mcp = FastMCP(name="Echo Server")


@mcp.tool()
def echo(message: str) -> str:
    """
    Echo the input message back as-is.
    
    Args:
        message: The message to echo back
        
    Returns:
        The same message unchanged
    """
    return message


def main():
    """Main entry point for the server."""
    mcp.run()


if __name__ == "__main__":
    main()