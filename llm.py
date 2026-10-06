import asyncio
import json
import os
import re

import httpx

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"


def _provider() -> str:
    p = os.getenv("LLM_PROVIDER", "").lower()
    if p:
        return p
    return "groq" if os.getenv("GROQ_API_KEY") else "anthropic"


async def _groq(system: str, prompt: str, max_tokens: int, json_mode: bool) -> str:
    body = {
        "model": os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile"),
        "messages": [{"role": "system", "content": system}, {"role": "user", "content": prompt}],
        "max_tokens": max_tokens,
        "temperature": 0.2,
    }
    if json_mode:
        body["response_format"] = {"type": "json_object"}
    headers = {"Authorization": f"Bearer {os.getenv('GROQ_API_KEY', '')}"}
    async with httpx.AsyncClient(timeout=120) as c:
        for attempt in range(6):
            r = await c.post(GROQ_URL, headers=headers, json=body)
            if r.status_code in (429, 503):
                wait = float(r.headers.get("retry-after", 0)) or min(2 ** attempt * 3, 30)
                await asyncio.sleep(wait + 0.5)
                continue
            if r.status_code >= 400:
                raise RuntimeError(f"Groq error {r.status_code}: {r.text[:300]}")
            return r.json()["choices"][0]["message"]["content"]
    raise RuntimeError("Groq rate limit: still throttled after several retries. Try Quick depth.")


_anthropic = None


async def _anthropic_call(system: str, prompt: str, max_tokens: int) -> str:
    global _anthropic
    if _anthropic is None:
        from anthropic import AsyncAnthropic
        _anthropic = AsyncAnthropic()
    r = await _anthropic.messages.create(
        model=os.getenv("LLM_MODEL", "claude-sonnet-5-5"),
        max_tokens=max_tokens, system=system,
        messages=[{"role": "user", "content": prompt}],
    )
    return "".join(b.text for b in r.content if b.type == "text")


async def complete(system: str, prompt: str, max_tokens: int = 2000, json_mode: bool = False) -> str:
    if _provider() == "groq":
        return await _groq(system, prompt, max_tokens, json_mode)
    return await _anthropic_call(system, prompt, max_tokens)


async def complete_json(system: str, prompt: str, max_tokens: int = 2000):
    text = await complete(
        system + "\nRespond with valid JSON only. No prose, no code fences.",
        prompt, max_tokens, json_mode=True,
    )
    text = re.sub(r"^```(?:json)?\s*|\s*```$", "", text.strip())
    return json.loads(text)