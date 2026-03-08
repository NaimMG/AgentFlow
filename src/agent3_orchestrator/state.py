from typing import TypedDict, Annotated, Optional
from langgraph.graph.message import add_messages


class OrchestratorState(TypedDict):
    """State partagé du Multi-Agent Orchestrator."""

    # Question de l'utilisateur
    query: str

    # Historique des messages
    messages: Annotated[list, add_messages]

    # Agent sélectionné par le supervisor : "research" ou "analyst"
    selected_agent: str

    # Chemin CSV optionnel (pour l'Analyst Agent)
    csv_path: Optional[str]

    # Résultat brut de l'agent sélectionné
    agent_result: str

    # Réponse finale synthétisée
    final_response: str

    # Justification du choix d'agent par le supervisor
    routing_reason: str