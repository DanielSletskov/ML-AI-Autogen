import io, json, requests
from config import LLM_CONFIG
from autogen import AssistantAgent as Agent
from fix_busted_json import repair_json as fix_json
from PyPDF2 import PdfReader

def extract_pdf_text(url: str, timeout: int = 10) -> str:
    resp = requests.get(url, timeout=timeout)
    resp.raise_for_status()
    reader = PdfReader(io.BytesIO(resp.content))
    parts = [page.extract_text() or "" for page in reader.pages]
    return "\n".join(parts)

class SummaryAgent:
    def __init__(self):
        self.agent = Agent(
            name="SummaryAgent",
            llm_config=LLM_CONFIG,
            system_message=(
                "You are an academic summarizer. Given text, "
                "respond with a JSON object {'summary': <three-sentence summary>}."
            )
        )
    def summarize_text(self, text: str) -> str:
        snippet = text.strip()[:2000]
        prompt  = (
            "Respond with a JSON object {'summary': <three-sentence summary>} "
            "for the following text:\n\n" + snippet
        )
        result = self.agent.run(prompt)
        msgs   = getattr(result, "messages", [])
        if not msgs:
            return "Sorry, I couldn’t generate a summary."
        raw   = msgs[-1].content
        fixed = fix_json(raw)
        try:
            return json.loads(fixed).get("summary", fixed)
        except json.JSONDecodeError:
            return fixed

    def summarize_url(self, url: str) -> str:
        if url.lower().endswith(".pdf"):
            try:
                text = extract_pdf_text(url)
            except Exception as e:
                print(f"[!] PDF extraction failed for {url}: {e}")
                return "Could not download or parse the PDF."
            if not text.strip():
                return "No text found in the PDF."
            return self.summarize_text(text)
        else:
            # Non‐PDF URLs get passed directly as “text”
            return self.summarize_text(url)