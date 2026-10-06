from services.llm import complete_json


async def check(question: str, sources: list[dict], comparison: dict) -> list[dict]:
    evidence = "\n".join(
        f"[{s['id']}] cred={s['credibility']['score']} " + " | ".join(s["key_points"])
        for s in sources
    )
    res = await complete_json(
        "You are a strict fact checker. A claim is 'supported' only if 2+ independent "
        "sources agree or one high-credibility source states it clearly.",
        f"""Question: {question}
Candidate consensus: {comparison.get('consensus', [])}
Conflicts: {comparison.get('conflicts', [])}
Evidence:
{evidence}

Return JSON: {{"checks": [{{"claim": "...", "status": "supported|contested|unverified",
"source_ids": [1], "note": "one line why"}}]}}""",
        2500,
    )
    return res.get("checks", [])
