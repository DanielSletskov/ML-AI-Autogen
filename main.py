from agents.orchestrator_agent import OrchestratorAgent


def main():
    instruction = input(
        "Enter a search instruction\n"
        "(e.g. \"Find a research paper on SQL that was published after 2010 "
        "and has 100 citations\"):\n> "
    ).strip()

    orchestrator = OrchestratorAgent()
    summaries   = orchestrator.run(instruction)

    print("\n== Research Summaries ==\n")
    for url, summary in summaries.items():
        print(f"URL: {url}\nSummary: {summary}\n")


if __name__ == "__main__":
    main()