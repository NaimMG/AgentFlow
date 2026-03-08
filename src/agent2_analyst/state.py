from typing import TypedDict, Annotated, List, Optional
from langgraph.graph.message import add_messages


class AnalystState(TypedDict):
    """State partagé entre tous les noeuds du Data Analyst Agent."""

    # Question de l'utilisateur sur les données
    query: str

    # Historique des messages
    messages: Annotated[list, add_messages]

    # Chemin vers le fichier CSV
    csv_path: str

    # Aperçu des données (head + info)
    data_preview: str

    # Code Python généré par le LLM
    generated_code: str

    # Résultat de l'exécution du code
    execution_result: str

    # Chemin vers le graphique généré (si applicable)
    chart_path: Optional[str]

    # Réponse finale
    final_answer: str

    # Nombre de tentatives (en cas d'erreur de code)
    attempts: int
    max_attempts: int