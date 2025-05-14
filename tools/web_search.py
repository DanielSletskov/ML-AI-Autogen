import requests, time, random

SEMANTIC_SCHOLAR_SEARCH = "https://api.semanticscholar.org/graph/v1/paper/search"

def search_scholar(topic: str, num_results: int = 5) -> list[dict]:
    params = {
        "query": topic,
        "limit": num_results,
        "fields": "title,abstract,url,openAccessPdf,year,citationCount"
    }
    for attempt in range(1, 6):
        resp = requests.get(SEMANTIC_SCHOLAR_SEARCH, params=params, timeout=10)
        if resp.status_code == 429:
            wait = 2**attempt + random.random()
            print(f"[!] Rate limited, retrying in {wait:.1f}s…")
            time.sleep(wait)
            continue
        resp.raise_for_status()
        data = resp.json().get("data", [])
        break
    else:
        raise RuntimeError("Semantic Scholar API rate limited")
    results = []
    for p in data:
        oa = p.get("openAccessPdf", {}).get("url")
        rec = {
            "url":        oa or p.get("url"),
            "abstract":   p.get("abstract", ""),
            "year":       p.get("year"),
            "citationCount": p.get("citationCount")
        }
        results.append(rec)
    return results
