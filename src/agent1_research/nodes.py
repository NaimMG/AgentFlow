import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_ollama import ChatOllama
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.messages import HumanMessage
from agent1_research.state import ResearchState

load_dotenv()


def get_llm():
    """Groq par défaut, Ollama en fallback si pas de clé API."""
    groq_key = os.getenv("GROQ_API_KEY")
    if groq_key:
        print("🚀 LLM : Groq (llama-3.3-70b)")
        return ChatGroq(model="llama-3.3-70b-versatile", temperature=0)
    print("🏠 LLM : Ollama (llama3.2 local)")
    return ChatOllama(model="llama3.2:latest", temperature=0)


# Initialisation
llm = get_llm()
search_tool = DuckDuckGoSearchRun()


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


def search_node(state: ResearchState) -> dict:
    """Exécute une recherche web avec DuckDuckGo."""
    results = search_tool.run(state["query"])
    current_results = state.get("search_results", [])
    return {
        "search_results": current_results + [results],
        "iterations": state.get("iterations", 0) + 1
    }


def synthesizer_node(state: ResearchState) -> dict:
    """Synthétise les résultats de recherche en une réponse claire."""
    context = "\n\n---\n\n".join(state["search_results"][-3:])
    response = llm.invoke([
        HumanMessage(content=f"""
        Question originale : {state['query']}

        Résultats de recherche :
        {context}

        Donne une réponse complète, structurée et sourcée.
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