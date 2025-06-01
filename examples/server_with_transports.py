#!/usr/bin/env python3
"""
MCP Server with Different Transport Options

This example shows how to create an MCP server that can use different
transport mechanisms (stdio, SSE, HTTP).
"""

import asyncio
import logging
from typing import Optional
from fastmcp import FastMCP
from pydantic import Field
from typing import Annotated

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create the MCP server
mcp = FastMCP(
    name="Transport Example Server",
    description="Demonstrates different MCP transport options"
)


# Example tool with more complex parameters
@mcp.tool()
async def fetch_data(
    source: Annotated[str, Field(description="Data source name")],
    limit: Annotated[int, Field(description="Maximum items to fetch", ge=1, le=100)] = 10,
    filter_by: Annotated[Optional[str], Field(description="Optional filter criteria")] = None
) -> dict:
    """
    Fetch data from a source with optional filtering.
    
    This is an async tool that simulates fetching data.
    """
    # Simulate async operation
    await asyncio.sleep(0.1)
    
    result = {
        "source": source,
        "count": limit,
        "filter": filter_by,
        "data": [f"Item {i}" for i in range(min(limit, 5))],
        "timestamp": asyncio.get_event_loop().time()
    }
    
    logger.info(f"Fetched data from {source} with limit {limit}")
    return result


@mcp.tool()
def calculate(expression: str) -> float:
    """
    Safely evaluate a mathematical expression.
    
    Args:
        expression: A mathematical expression like "2 + 2" or "10 * 5"
        
    Returns:
        The result of the calculation
    """
    # Only allow safe operations
    allowed_chars = "0123456789+-*/(). "
    if not all(c in allowed_chars for c in expression):
        raise ValueError("Invalid characters in expression")
    
    try:
        result = eval(expression)
        return float(result)
    except Exception as e:
        raise ValueError(f"Invalid expression: {e}")


# Resource that provides dynamic content
@mcp.resource("stats://server")
async def get_server_stats() -> str:
    """Get current server statistics."""
    import json
    import os
    import platform
    
    stats = {
        "platform": platform.system(),
        "python_version": platform.python_version(),
        "process_id": os.getpid(),
        "transport": "varies",  # Will be set by transport method
        "timestamp": asyncio.get_event_loop().time()
    }
    
    return json.dumps(stats, indent=2)


def main():
    """
    Main entry point with transport selection.
    
    This can be run in different modes:
    - Default (stdio): python server_with_transports.py
    - SSE: python server_with_transports.py --transport sse --port 8000
    - HTTP: python server_with_transports.py --transport streamable-http --port 8000
    """
    import sys
    
    # Simple argument parsing for demonstration
    transport = "stdio"
    port = 8000
    
    if "--transport" in sys.argv:
        idx = sys.argv.index("--transport")
        if idx + 1 < len(sys.argv):
            transport = sys.argv[idx + 1]
    
    if "--port" in sys.argv:
        idx = sys.argv.index("--port")
        if idx + 1 < len(sys.argv):
            port = int(sys.argv[idx + 1])
    
    logger.info(f"Starting MCP server with {transport} transport")
    
    if transport == "stdio":
        # Standard I/O transport (default) - used by Claude Desktop
        mcp.run()
    elif transport == "sse":
        # Server-Sent Events transport
        asyncio.run(mcp.run_async(
            transport="sse",
            host="0.0.0.0",
            port=port
        ))
    elif transport == "streamable-http":
        # HTTP transport with streaming
        asyncio.run(mcp.run_async(
            transport="streamable-http",
            host="0.0.0.0",
            port=port,
            path="/mcp"
        ))
    else:
        logger.error(f"Unknown transport: {transport}")
        sys.exit(1)


if __name__ == "__main__":
    main()