import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage
from agent3_orchestrator.state import OrchestratorState
from agent1_research.graph import build_graph as build_research_graph
from agent2_analyst.graph import build_analyst_graph

load_dotenv()


def get_llm():
    """Groq par défaut, Ollama en fallback."""
    groq_key = os.getenv("GROQ_API_KEY")
    if groq_key:
        return ChatGroq(model="llama-3.3-70b-versatile", temperature=0)
    return ChatOllama(model="llama3.2:latest", temperature=0)


llm = get_llm()


def supervisor_node(state: OrchestratorState) -> dict:
    """Analyse la question et route vers le bon agent."""
    csv_available = bool(state.get("csv_path"))

    response = llm.invoke([
        HumanMessage(content=f"""
Tu es un supervisor qui dirige des agents spécialisés.

Agents disponibles :
- "research" : recherche web, actualités, questions générales
- "analyst" : analyse de données CSV, statistiques, visualisations

Question : "{state['query']}"
Fichier CSV disponible : {"Oui" if csv_available else "Non"}

Réponds UNIQUEMENT en JSON avec ce format exact :
{{"agent": "research" ou "analyst", "reason": "justification courte"}}
        """)
    ])

    import json
    try:
        content = response.content.strip()
        content = content.replace("```json", "").replace("```", "").strip()
        decision = json.loads(content)
        selected = decision.get("agent", "research")
        reason = decision.get("reason", "")
    except Exception:
        selected = "research"
        reason = "Fallback vers research (parsing error)"

    # Force analyst uniquement si CSV disponible
    if selected == "analyst" and not csv_available:
        selected = "research"
        reason = "CSV non disponible, redirection vers research"

    return {
        "selected_agent": selected,
        "routing_reason": reason,
        "messages": [response]
    }


def research_agent_node(state: OrchestratorState) -> dict:
    """Délègue au Research Agent."""
    graph = build_research_graph()
    result = graph.invoke({
        "query": state["query"],
        "messages": [],
        "search_results": [],
        "synthesis": "",
        "iterations": 0,
        "max_iterations": 3
    })
    return {"agent_result": result.get("synthesis", "")}


def analyst_agent_node(state: OrchestratorState) -> dict:
    """Délègue au Data Analyst Agent."""
    graph = build_analyst_graph()
    result = graph.invoke({
        "query": state["query"],
        "messages": [],
        "csv_path": state.get("csv_path", ""),
        "data_preview": "",
        "generated_code": "",
        "execution_result": "",
        "chart_path": None,
        "final_answer": "",
        "attempts": 0,
        "max_attempts": 3
    })
    return {"agent_result": result.get("final_answer", "")}


def synthesizer_node(state: OrchestratorState) -> dict:
    """Formule la réponse finale avec contexte du routing."""
    response = llm.invoke([
        HumanMessage(content=f"""
Question : {state['query']}
Agent utilisé : {state['selected_agent']}
Raison du choix : {state['routing_reason']}

Résultat de l'agent :
{state['agent_result']}

Présente une réponse finale claire et professionnelle.
Mentionne quel agent a traité la demande et pourquoi.
        """)
    ])
    return {
        "final_response": response.content,
        "messages": [response]
    }


def route_to_agent(state: OrchestratorState) -> str:
    """Route vers le bon agent selon la décision du supervisor."""
    return state.get("selected_agent", "research")