"""Shared HTTP client helper for Maitabi MCP Server."""

import httpx

_client: httpx.AsyncClient | None = None

def get_http_client() -> httpx.AsyncClient:
    """Get or initialize the shared httpx.AsyncClient instance."""
    global _client
    if _client is None or _client.is_closed:
        _client = httpx.AsyncClient(
            timeout=httpx.Timeout(15.0),
            follow_redirects=True
        )
    return _client

async def close_http_client() -> None:
    """Close the shared httpx.AsyncClient instance."""
    global _client
    if _client is not None and not _client.is_closed:
        await _client.aclose()
        _client = None
