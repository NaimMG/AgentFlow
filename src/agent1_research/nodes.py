import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_ollama import ChatOllama
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.messages import HumanMessage
from agent1_research.state import ResearchState
from shared.error_handler import retry_with_backoff, safe_node, logger

load_dotenv()


def get_llm():
    """Groq par défaut, Ollama en fallback."""
    groq_key = os.getenv("GROQ_API_KEY")
    if groq_key:
        logger.info("LLM : Groq (llama-3.3-70b)")
        return ChatGroq(model="llama-3.3-70b-versatile", temperature=0)
    logger.info("LLM : Ollama (llama3.2 local)")
    return ChatOllama(model="llama3.2:latest", temperature=0)


llm = get_llm()
search_tool = DuckDuckGoSearchRun()


@safe_node(fallback_message="Erreur lors de la planification.")
def planner_node(state: ResearchState) -> dict:
    """Planifie la stratégie de recherche à partir de la question."""
    response = llm.invoke([
        HumanMessage(content=f"""
        Tu es un expert en recherche d'information.
        Question : "{state['query']}"
        Reformule cette question en une requête de recherche web précise et concise.
        Réponds uniquement avec la requête, sans explication.
        """)
    ])
    return {
        "messages": [response],
        "iterations": 0,
        "search_results": []
    }


@retry_with_backoff(max_retries=3, base_delay=2.0, exceptions=(Exception,))
def _search_with_retry(query: str) -> str:
    """Recherche web avec retry automatique."""
    return search_tool.run(query)


@safe_node(fallback_message="Erreur lors de la recherche web.")
def search_node(state: ResearchState) -> dict:
    """Exécute une recherche web avec DuckDuckGo."""
    logger.info(f"Recherche web : {state['query']}")
    results = _search_with_retry(state["query"])
    current_results = state.get("search_results", [])
    return {
        "search_results": current_results + [results],
        "iterations": state.get("iterations", 0) + 1
    }


@safe_node(fallback_message="Erreur lors de la synthèse.")
def synthesizer_node(state: ResearchState) -> dict:
    """Synthétise les résultats de recherche en une réponse claire."""
    context = "\n\n---\n\n".join(state["search_results"][-3:])
    response = llm.invoke([
        HumanMessage(content=f"""
        Question originale : {state['query']}

        Résultats de recherche :
        {context}

        Donne une réponse complète et structurée.
        Si les informations sont insuffisantes, commence par "NEED_MORE_INFO".
        """)
    ])
    return {
        "synthesis": response.content,
        "messages": [response]
    }


def should_continue(state: ResearchState) -> str:
    """Décide si l'agent doit continuer à chercher ou terminer."""
    if (
        "NEED_MORE_INFO" in state.get("synthesis", "")
        and state.get("iterations", 0) < state.get("max_iterations", 3)
    ):
        return "continue"
    return "end"