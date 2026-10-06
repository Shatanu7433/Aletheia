"""Heuristic source credibility (0-100). Swap in an LLM/domain-DB scorer later."""

HIGH = (".gov", ".edu", ".int", "nature.com", "science.org", "who.int", "nih.gov",
        "thelancet.com", "nejm.org", "arxiv.org", "ieee.org", "acm.org", "oecd.org",
        "reuters.com", "apnews.com", "worldbank.org", "mckinsey.com", "bmj.com")
MID = ("bbc.", "nytimes.com", "ft.com", "wsj.com", "economist.com", "wired.com",
       "technologyreview.com", "hbr.org", "forbes.com", "bloomberg.com",
       "statnews.com", "healthaffairs.org", "techcrunch.com", "theverge.com")
LOW = ("reddit.com", "quora.com", "medium.com", "blogspot.", "wordpress.com",
       "substack.com", "pinterest.", "facebook.com", "x.com", "twitter.com")


def score_source(domain: str, content: str) -> dict:
    d = domain.lower()
    s = 55
    if any(k in d for k in HIGH):
        s = 90
    elif any(k in d for k in MID):
        s = 75
    elif any(k in d for k in LOW):
        s = 35
    if len(content) < 800:
        s -= 10
    s = max(5, min(100, s))
    label = "high" if s >= 75 else "medium" if s >= 50 else "low"
    return {"score": s, "label": label}
