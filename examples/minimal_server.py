#!/usr/bin/env python3
"""
Minimal MCP Server Example using FastMCP

This demonstrates the bare minimum needed to create a working MCP server
that can be used with Claude Desktop or other MCP clients.
"""

from fastmcp import FastMCP

# Create the MCP server instance with a name
mcp = FastMCP(name="Minimal MCP Server")


# Define a simple tool - tools allow the LLM to execute actions
@mcp.tool()
def greet(name: str) -> str:
    """
    Greet a user by name.
    
    Args:
        name: The name of the person to greet
        
    Returns:
        A greeting message
    """
    return f"Hello, {name}! Welcome to the minimal MCP server."


@mcp.tool()
def add_numbers(a: int, b: int) -> int:
    """
    Add two numbers together.
    
    Args:
        a: First number
        b: Second number
        
    Returns:
        The sum of a and b
    """
    return a + b


@mcp.tool()
def get_current_time() -> str:
    """
    Get the current date and time.
    
    Returns:
        Current datetime as a string
    """
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# Define a resource - resources provide data that can be loaded into context
@mcp.resource("config://settings")
def get_settings() -> str:
    """
    Get the server configuration settings.
    
    Returns:
        Configuration as a JSON string
    """
    import json
    config = {
        "server_name": "Minimal MCP Server",
        "version": "1.0.0",
        "features": ["greetings", "math", "time"],
        "author": "Example"
    }
    return json.dumps(config, indent=2)


# Main function that can be called from the command line
def main():
    """Main entry point for the MCP server."""
    # Run the server using stdio transport (default)
    mcp.run()


# Main entry point
if __name__ == "__main__":
    main()