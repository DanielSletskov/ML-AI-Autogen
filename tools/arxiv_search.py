import requests, feedparser

ARXIV_API = "http://export.arxiv.org/api/query"

def search_arxiv(topic: str, max_results: int = 5) -> list[dict]:
    params = {"search_query": f"all:{topic}", "start": 0, "max_results": max_results}
    resp = requests.get(ARXIV_API, params=params, timeout=10)
    resp.raise_for_status()
    feed = feedparser.parse(resp.text)

    results = []
    for entry in feed.entries:
        pdf_url = next((l.href for l in entry.links if l.type == "application/pdf"),
                       entry.link)
        results.append({
            "url":          pdf_url,
            "abstract":     entry.summary.replace("\n"," "),
            "year":         int(entry.published[:4]) if hasattr(entry, "published") else None,
            "citationCount": None
        })
    return results