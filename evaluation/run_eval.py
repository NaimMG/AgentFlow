"""
Script principal d'évaluation automatique des agents AgentFlow.
Lance les agents sur le dataset et score les réponses avec LLM-as-a-Judge.
"""
import json
from datetime import datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from dotenv import load_dotenv

from agent1_research.graph import build_graph as build_research_graph
from agent2_analyst.graph import build_analyst_graph
from evaluation.dataset import RESEARCH_DATASET, ANALYST_DATASET
from evaluation.judge import evaluate_response
from shared.observability import langfuse

load_dotenv()
console = Console()


def run_research_eval() -> list:
    """Evalue l'Agent 1 Research sur le dataset."""
    console.print("\n[bold blue]🔍 Evaluation Agent 1 — Research[/bold blue]")
    graph = build_research_graph()
    results = []

    for item in RESEARCH_DATASET:
        console.print(f"  → Question : {item['query'][:60]}...")

        result = graph.invoke({
            "query": item["query"],
            "messages": [],
            "search_results": [],
            "synthesis": "",
            "iterations": 0,
            "max_iterations": 2
        })

        response = result.get("synthesis", "")
        scores = evaluate_response(
            query=item["query"],
            response=response,
            expected_keywords=item["expected_keywords"],
            min_length=item["min_length"]
        )

        # Envoi scores dans Langfuse
        try:
            trace = langfuse.trace(
                name="eval_research_agent",
                input={"query": item["query"]},
                output={"response": response[:300], "scores": scores},
                tags=["evaluation", "research_agent"]
            )
            langfuse.flush()
        except Exception:
            pass

        results.append({
            "query": item["query"],
            "scores": scores
        })

        console.print(f"    Score global : [bold green]{scores['score_global']}[/bold green] — {scores['commentaire'][:60]}")

    return results


def run_analyst_eval() -> list:
    """Evalue l'Agent 2 Analyst sur le dataset."""
    console.print("\n[bold blue]📊 Evaluation Agent 2 — Analyst[/bold blue]")
    graph = build_analyst_graph()
    results = []

    for item in ANALYST_DATASET:
        console.print(f"  → Question : {item['query'][:60]}...")

        result = graph.invoke({
            "query": item["query"],
            "messages": [],
            "csv_path": item["csv_path"],
            "data_preview": "",
            "generated_code": "",
            "execution_result": "",
            "chart_path": None,
            "final_answer": "",
            "attempts": 0,
            "max_attempts": 2
        })

        response = result.get("final_answer", "")
        scores = evaluate_response(
            query=item["query"],
            response=response,
            expected_keywords=item["expected_keywords"],
            min_length=item["min_length"]
        )

        # Envoi scores dans Langfuse
        try:
            langfuse.trace(
                name="eval_analyst_agent",
                input={"query": item["query"]},
                output={"response": response[:300], "scores": scores},
                tags=["evaluation", "analyst_agent"]
            )
            langfuse.flush()
        except Exception:
            pass

        results.append({
            "query": item["query"],
            "scores": scores
        })

        console.print(f"    Score global : [bold green]{scores['score_global']}[/bold green] — {scores['commentaire'][:60]}")

    return results


def print_summary(research_results: list, analyst_results: list):
    """Affiche un tableau récapitulatif des scores."""

    table = Table(title="📊 Résultats Evaluation AgentFlow", show_lines=True)
    table.add_column("Agent", style="cyan")
    table.add_column("Question", style="white", max_width=40)
    table.add_column("Pertinence", justify="center")
    table.add_column("Qualité", justify="center")
    table.add_column("Factualité", justify="center")
    table.add_column("Global", justify="center", style="bold green")

    for r in research_results:
        s = r["scores"]
        table.add_row(
            "Research",
            r["query"][:40],
            str(s["pertinence"]),
            str(s["qualite"]),
            str(s["factualite"]),
            str(s["score_global"])
        )

    for r in analyst_results:
        s = r["scores"]
        table.add_row(
            "Analyst",
            r["query"][:40],
            str(s["pertinence"]),
            str(s["qualite"]),
            str(s["factualite"]),
            str(s["score_global"])
        )

    console.print(table)

    # Score moyen global
    all_scores = [r["scores"]["score_global"]
                  for r in research_results + analyst_results]
    avg = round(sum(all_scores) / len(all_scores), 2)

    console.print(Panel(
        f"[bold green]Score moyen global : {avg}/1.0[/bold green]\n"
        f"Timestamp : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"Dashboard Langfuse : http://localhost:3000",
        title="🏆 Résumé"
    ))

    # Sauvegarde JSON
    report = {
        "timestamp": datetime.now().isoformat(),
        "avg_score": avg,
        "research": research_results,
        "analyst": analyst_results
    }
    with open("evaluation/last_report.json", "w") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    console.print("[dim]📄 Rapport sauvegardé : evaluation/last_report.json[/dim]")


if __name__ == "__main__":
    console.print(Panel(
        "[bold]🤖 AgentFlow — Evaluation Automatique[/bold]\n"
        "LLM-as-a-Judge avec Groq llama-3.3-70b",
        border_style="blue"
    ))

    research_results = run_research_eval()
    analyst_results = run_analyst_eval()
    print_summary(research_results, analyst_results)