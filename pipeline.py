import asyncio
import traceback

from agents import analyzer, fact_checker, planner, researcher, writer
from models.schemas import DEPTH
from services import store

EVENTS: dict[str, list[dict]] = {}  # job_id -> ordered events (SSE replays these)


def emit(job_id: str, stage: str, status: str, detail: str = "", data=None):
    EVENTS.setdefault(job_id, []).append(
        {"stage": stage, "status": status, "detail": detail, "data": data}
    )


async def run(job_id: str, question: str, depth: str):
    cfg = DEPTH.get(depth, DEPTH["standard"])

    def e(*a, **k):
        emit(job_id, *a, **k)

    try:
        e("understanding", "active")
        await asyncio.sleep(0.4)
        e("understanding", "done")

        e("planning", "active")
        plan = await planner.plan(question, cfg["queries"])
        e("planning", "done", plan.get("objective", ""), plan)

        e("searching", "active")
        sources = await researcher.collect(plan["search_queries"], cfg["results"], cfg["read"])
        if not sources:
            raise RuntimeError("No usable sources found. Check TAVILY_API_KEY.")
        e("searching", "done", f"{len(sources)} sources found")

        e("reading", "active")
        sources = list(await analyzer.extract(question, sources))
        e("reading", "done", f"{len(sources)} sources read")

        e("comparing", "active")
        comparison = await analyzer.compare(question, sources)
        e("comparing", "done")

        e("fact_checking", "active")
        checks = await fact_checker.check(question, sources, comparison)
        e("fact_checking", "done", f"{len(checks)} claims checked")

        e("writing", "active")
        report = await writer.write(question, plan, sources, comparison, checks)
        e("writing", "done")

        slim = [{k: v for k, v in s.items() if k != "content"} for s in sources]
        store.finish(job_id, "done", {"plan": plan, "sources": slim, "comparison": comparison,
                                      "checks": checks, "report": report})
        e("complete", "done")
    except Exception as ex:
        traceback.print_exc()
        store.finish(job_id, "error", {"error": str(ex)})
        e("error", "error", str(ex))
