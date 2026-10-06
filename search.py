import os
from urllib.parse import urlparse

import httpx


async def web_search(query: str, max_results: int = 6) -> list[dict]:
    """Search + content extraction in one call (Tavily returns page text)."""
    async with httpx.AsyncClient(timeout=45) as c:
        r = await c.post(
            "https://api.tavily.com/search",
            headers={"Authorization": f"Bearer {os.getenv('TAVILY_API_KEY', '')}"},
            json={
                "query": query,
                "max_results": max_results,
                "search_depth": "advanced",
                "include_raw_content": "text",
            },
        )
        r.raise_for_status()
    out = []
    for x in r.json().get("results", []):
        url = x["url"]
        out.append(
            {
                "url": url,
                "title": x.get("title") or url,
                "domain": urlparse(url).netloc.removeprefix("www."),
                "content": (x.get("raw_content") or x.get("content") or "")[:8000],
                "published": x.get("published_date"),
            }
        )
    return out
