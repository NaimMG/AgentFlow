import pytest
from unittest.mock import patch, MagicMock
from agent1_research.state import ResearchState
from agent1_research.nodes import should_continue
from agent1_research.graph import build_graph


# ── Tests sur ResearchState ──────────────────────────────────────────

def test_research_state_keys():
    """Vérifie que ResearchState contient tous les champs requis."""
    required_keys = {"query", "messages", "search_results",
                     "synthesis", "iterations", "max_iterations"}
    assert required_keys == set(ResearchState.__annotations__.keys())


# ── Tests sur should_continue ─────────────────────────────────────────

def test_should_continue_returns_end_when_synthesis_ok():
    """Retourne 'end' quand la synthèse est complète."""
    state = {
        "synthesis": "Voici une réponse complète.",
        "iterations": 1,
        "max_iterations": 3
    }
    assert should_continue(state) == "end"


def test_should_continue_returns_continue_when_need_more_info():
    """Retourne 'continue' quand le LLM demande plus d'info."""
    state = {
        "synthesis": "NEED_MORE_INFO sur ce sujet.",
        "iterations": 1,
        "max_iterations": 3
    }
    assert should_continue(state) == "continue"


def test_should_continue_returns_end_when_max_iterations_reached():
    """Retourne 'end' même si NEED_MORE_INFO quand max atteint."""
    state = {
        "synthesis": "NEED_MORE_INFO mais on a atteint la limite.",
        "iterations": 3,
        "max_iterations": 3
    }
    assert should_continue(state) == "end"


def test_should_continue_returns_end_when_empty_synthesis():
    """Retourne 'end' si synthesis est vide."""
    state = {
        "synthesis": "",
        "iterations": 0,
        "max_iterations": 3
    }
    assert should_continue(state) == "end"


# ── Tests sur le graphe ───────────────────────────────────────────────

def test_build_graph_compiles():
    """Vérifie que le graphe compile sans erreur."""
    graph = build_graph()
    assert graph is not None


def test_build_graph_has_correct_nodes():
    """Vérifie que le graphe contient les bons noeuds."""
    graph = build_graph()
    nodes = graph.get_graph().nodes
    assert "planner" in nodes
    assert "web_search" in nodes
    assert "synthesizer" in nodes


# ── Tests sur planner_node avec mock ─────────────────────────────────

@patch("agent1_research.nodes.llm")
def test_planner_node_returns_correct_keys(mock_llm):
    """Vérifie que planner_node retourne les bons champs."""
    from agent1_research.nodes import planner_node

    mock_response = MagicMock()
    mock_response.content = "LangGraph latest advances 2025"
    mock_llm.invoke.return_value = mock_response

    state = {
        "query": "Quelles sont les avancées de LangGraph ?",
        "messages": [],
        "search_results": [],
        "synthesis": "",
        "iterations": 0,
        "max_iterations": 3
    }

    result = planner_node(state)
    assert "messages" in result
    assert "iterations" in result
    assert result["iterations"] == 0


# ── Tests sur search_node ─────────────────────────────────────────────

@patch("agent1_research.nodes.search_tool")
def test_search_node_accumulates_results(mock_search):
    """Vérifie que search_node accumule les résultats."""
    from agent1_research.nodes import search_node

    mock_search.run.return_value = "Résultats de recherche simulés."

    state = {
        "query": "LangGraph 2025",
        "search_results": ["premier résultat"],
        "iterations": 0
    }

    result = search_node(state)
    assert len(result["search_results"]) == 2
    assert result["iterations"] == 1