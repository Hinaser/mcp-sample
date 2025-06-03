#!/usr/bin/env python3
"""
Windows Authentication MCP Server using FastMCP

Fetches URLs using automatic Windows authentication (NTLM/Kerberos).
"""

import os
import logging
from typing import Optional
from fastmcp import FastMCP
import requests

# Try to import authentication libraries
auth_available = []

try:
    from requests_ntlm import HttpNtlmAuth
    auth_available.append("ntlm")
    HAVE_NTLM = True
except ImportError:
    HAVE_NTLM = False

try:
    from requests_kerberos import HTTPKerberosAuth, OPTIONAL
    auth_available.append("kerberos")
    HAVE_KERBEROS = True
except ImportError:
    HAVE_KERBEROS = False

try:
    from pyspnego.client import HttpNegotiateAuth
    auth_available.append("negotiate")
    HAVE_NEGOTIATE = True
except ImportError:
    HAVE_NEGOTIATE = False

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create the MCP server
mcp = FastMCP(
    name="Windows Auth Fetch",
    description="Fetch URLs using Windows authentication"
)

logger.info(f"Windows Auth MCP Server - Available auth methods: {auth_available}")


@mcp.tool()
def fetch_with_windows_auth(
    url: str,
    auth_method: Optional[str] = "auto"
) -> str:
    """
    Fetch content from a URL using automatic Windows authentication.
    
    Args:
        url: The URL to fetch
        auth_method: Authentication method to use (auto, ntlm, kerberos, negotiate)
        
    Returns:
        The fetched content or error message
    """
    logger.info(f"Fetching {url} with auth method: {auth_method}")
    
    # Try without auth first
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return f"Success (no auth needed)\nStatus: {response.status_code}\n\nContent:\n{response.text[:5000]}"
    except requests.exceptions.HTTPError as e:
        if e.response.status_code != 401:
            return f"Error: {str(e)}"
        logger.info("Got 401, trying with authentication...")
    except Exception as e:
        logger.warning(f"Error without auth: {e}")
    
    # Prepare auth methods
    auth_methods = []
    
    if HAVE_NEGOTIATE and (auth_method == "auto" or auth_method == "negotiate"):
        auth_methods.append(("negotiate", HttpNegotiateAuth()))
    
    if HAVE_KERBEROS and (auth_method == "auto" or auth_method == "kerberos"):
        auth_methods.append(("kerberos", HTTPKerberosAuth(mutual_authentication=OPTIONAL)))
    
    if HAVE_NTLM and (auth_method == "auto" or auth_method == "ntlm"):
        username = os.environ.get('USERNAME', '')
        domain = os.environ.get('USERDOMAIN', '')
        if username and domain:
            auth_methods.append(("ntlm", HttpNtlmAuth(f'{domain}\\{username}', '')))
    
    if not auth_methods:
        return f"Error: No authentication methods available. Available: {auth_available}"
    
    # Try each auth method
    errors = []
    for auth_name, auth in auth_methods:
        try:
            logger.info(f"Trying {auth_name} authentication...")
            response = requests.get(url, auth=auth, timeout=30)
            response.raise_for_status()
            
            content = response.text
            if len(content) > 5000:
                content = content[:5000] + "\n\n[Content truncated to 5000 characters]"
            
            return f"Success with {auth_name}\nStatus: {response.status_code}\n\nContent:\n{content}"
            
        except requests.exceptions.HTTPError as e:
            error_msg = f"{auth_name}: {e.response.status_code} {e.response.reason}"
            logger.error(error_msg)
            errors.append(error_msg)
        except Exception as e:
            error_msg = f"{auth_name}: {str(e)}"
            logger.error(error_msg)
            errors.append(error_msg)
    
    # All methods failed
    return f"Authentication failed for {url}\n\nErrors:\n" + "\n".join(errors)


def main():
    """Main entry point."""
    mcp.run()


if __name__ == "__main__":
    main()