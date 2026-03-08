from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from agent1_research.graph import build_graph

load_dotenv()
console = Console()


def run_agent(query: str, max_iterations: int = 3):
    """Lance le Research Agent sur une question."""

    console.print(Panel(f"[bold blue]🔍 Question :[/bold blue] {query}"))

    graph = build_graph()

    result = graph.invoke({
        "query": query,
        "messages": [],
        "search_results": [],
        "synthesis": "",
        "iterations": 0,
        "max_iterations": max_iterations
    })

    console.print(Panel(
        f"[bold green]✅ Réponse après {result['iterations']} itération(s) :[/bold green]\n\n{result['synthesis']}",
        title="Résultat",
        border_style="green"
    ))

    return result


if __name__ == "__main__":
    run_agent("Quelles sont les dernières avancées de LangGraph en 2025 ?")