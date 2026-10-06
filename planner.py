from services.llm import complete_json

SYSTEM = "You are a research planner. Break questions into focused, searchable parts."


async def plan(question: str, n_queries: int) -> dict:
    return await complete_json(
        SYSTEM,
        f"""Research question: {question}

Return JSON:
{{"objective": "one sentence",
 "sub_questions": ["3-5 sub-questions that together answer it"],
 "search_queries": ["{n_queries} diverse web search queries, incl. one for counter-evidence or criticism"]}}""",
    )
