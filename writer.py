from services.llm import complete


async def write(question: str, plan: dict, sources: list[dict],
                comparison: dict, checks: list[dict]) -> str:
    material = "\n\n".join(
        f"[{s['id']}] {s['title']} — {s['domain']} (credibility {s['credibility']['label']})\n"
        f"{s['summary']}\n- " + "\n- ".join(s["key_points"])
        for s in sources
    )
    body = await complete(
        "You write rigorous research reports. Cite every factual claim inline as [n] "
        "using ONLY the provided source numbers. Flag contested or unverified claims "
        "explicitly. Never cite a source for something it does not say.",
        f"""Question: {question}
Objective: {plan.get('objective')}
Sub-questions: {plan.get('sub_questions')}

Fact-check results: {checks}
Cross-source comparison: {comparison}

Sources:
{material}

Write the report in Markdown with: an executive summary, a section per sub-question,
a "Where sources disagree" section, and "Limitations". Nothing after that (references are added separately).""",
        4000,
    )
    refs = "\n".join(
        f"{s['id']}. [{s['title']}]({s['url']}) — {s['domain']}" for s in sources
    )
    return f"# {question}\n\n{body}\n\n## References\n\n{refs}\n"
