from agents.summary_agent import SummaryAgent
from agents.search_agent  import SearchAgent

class OrchestratorAgent:
    def __init__(self):
        # ← You need both of these!
        self.searcher   = SearchAgent()
        self.summarizer = SummaryAgent()

    def run(self, instruction: str) -> dict[str,str]:
        records = self.searcher.find_papers(instruction)
        print(f"[*] Found {len(records)} matching papers. Summarizing…")

        results: dict[str,str] = {}
        for rec in records:
            url      = rec["url"]
            print(f"PDF link: {url}")
            abstract = rec.get("abstract","").strip()
            if abstract:
                summary = self.summarizer.summarize_text(abstract)
            else:
                summary = self.summarizer.summarize_url(url)
            results[url] = summary

        return results