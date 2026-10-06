import asyncio

from services.credibility import score_source
from services.search import web_search


async def collect(queries: list[str], per_query: int, limit: int) -> list[dict]:
    batches = await asyncio.gather(
        *[web_search(q, per_query) for q in queries], return_exceptions=True
    )
    seen, sources = set(), []
    for b in batches:
        if isinstance(b, Exception):
            continue
        for s in b:
            if s["url"] in seen or len(s["content"]) < 300:
                continue
            seen.add(s["url"])
            s["credibility"] = score_source(s["domain"], s["content"])
            sources.append(s)
    sources.sort(key=lambda s: s["credibility"]["score"], reverse=True)
    sources = sources[:limit]
    for i, s in enumerate(sources, 1):
        s["id"] = i
    return sources
