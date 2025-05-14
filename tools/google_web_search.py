import os
from serpapi import GoogleSearch

def search_web(query: str, num_results: int = 5) -> list[str]:
    params = {
        "engine": "google",
        "q":      query,
        "api_key": os.getenv("SERPAPI_API_KEY"),
        "num":    num_results
    }
    search = GoogleSearch(params)
    data   = search.get_dict()
    return [r["link"] for r in data.get("organic_results", []) if r.get("link")]
