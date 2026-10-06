from pydantic import BaseModel


class ResearchRequest(BaseModel):
    question: str
    depth: str = "standard"  # "quick" | "standard" | "deep"


DEPTH = {
    "quick": {"queries": 3, "results": 5, "read": 6},
    "standard": {"queries": 5, "results": 6, "read": 12},
    "deep": {"queries": 8, "results": 8, "read": 20},
}
