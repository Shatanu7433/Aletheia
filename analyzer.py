import asyncio

from services.llm import complete_json

SYSTEM = "You extract precise, verifiable key points from a source. Never invent facts."


async def _one(question: str, s: dict, sem: asyncio.Semaphore) -> dict:
    async with sem:
        try:
            r = await complete_json(
                SYSTEM,
                f"""Question: {question}
Source: {s['title']} ({s['domain']})
Text:
{s['content'][:6000]}

Return JSON: {{"summary": "2 sentences", "key_points": ["3-6 specific claims from this source relevant to the question, with numbers/dates when present"]}}""",
                1200,
            )
        except Exception:
            r = {"summary": "", "key_points": []}
    s["summary"], s["key_points"] = r.get("summary", ""), r.get("key_points", [])
    return s


async def extract(question: str, sources: list[dict]) -> list[dict]:
    sem = asyncio.Semaphore(5)
    return await asyncio.gather(*[_one(question, s, sem) for s in sources])


async def compare(question: str, sources: list[dict]) -> dict:
    digest = "\n".join(
        f"[{s['id']}] ({s['domain']}) " + " | ".join(s["key_points"]) for s in sources
    )
    return await complete_json(
        "You compare findings across sources and surface agreement and conflict.",
        f"""Question: {question}
Sources:
{digest}

Return JSON:
{{"consensus": [{{"point": "...", "source_ids": [1,2]}}],
 "conflicts": [{{"topic": "...", "positions": [{{"claim": "...", "source_ids": [1]}}]}}],
 "gaps": ["what the sources do not cover"]}}""",
        2500,
    )
