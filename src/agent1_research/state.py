from typing import TypedDict, Annotated, List
from langgraph.graph.message import add_messages


class ResearchState(TypedDict):
    """State partagé entre tous les noeuds du Research Agent."""

    # La question posée par l'utilisateur
    query: str

    # Historique des messages (LangGraph accumule automatiquement)
    messages: Annotated[list, add_messages]

    # Résultats bruts des recherches web
    search_results: List[str]

    # Synthèse finale générée par le LLM
    synthesis: str

    # Compteur d'itérations pour éviter les boucles infinies
    iterations: int
    max_iterations: int