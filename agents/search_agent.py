import re
from tools.web_search        import search_scholar
from tools.arxiv_search      import search_arxiv
from tools.google_web_search import search_web

class SearchAgent:
    def __init__(self):
        pass

    def find_papers(self, instruction: str) -> list[dict]:
        """
        instruction: "Find a research paper on [topic]
                      that was published [in|before|after] [year]
                      and has [N] citations."
        Returns a list of records (dicts) with keys:
          - url
          - abstract
          - (optional) year, citationCount
        """
        # 1) Parse filters
        pattern = (
            r"Find a research paper on\s+(.+?)\s+that was published\s+"
            r"(in|before|after)\s+(\d{4})\s+and has\s+(\d+)\s+citations"
        )
        m = re.match(pattern, instruction, re.IGNORECASE)
        if not m:
            topic, when, year, citations = instruction, None, None, None
        else:
            topic     = m.group(1).strip()
            when      = m.group(2).lower()
            year      = int(m.group(3))
            citations = int(m.group(4))

        # 2) Try Semantic Scholar
        records = search_scholar(topic, num_results=20)

        # 3) Fallback to arXiv
        if not records:
            records = search_arxiv(topic, max_results=20)

        # 4) Fallback to generic web search
        if not records:
            urls = search_web(topic, num_results=20)
            records = [{"url": u, "abstract": ""} for u in urls]

        # 5) Apply year & citation filters
        def year_ok(rec_year):
            if when == "in":    return rec_year == year
            if when == "before":return rec_year <  year
            if when == "after": return rec_year >  year
            return True
        def cit_ok(rec_cit):
            return citations is None or rec_cit >= citations

        filtered = []
        for rec in records:
            rec_year = rec.get("year", 0)
            rec_cit  = rec.get("citationCount", 0)
            if year is not None and not year_ok(rec_year):
                continue
            if citations is not None and not cit_ok(rec_cit):
                continue
            filtered.append(rec)

        # 6) Return top 5 matches
        return filtered[:5]