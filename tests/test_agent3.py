import pytest
from unittest.mock import patch, MagicMock
from agent3_orchestrator.state import OrchestratorState
from agent3_orchestrator.nodes import route_to_agent
from agent3_orchestrator.graph import build_orchestrator_graph


# ── Tests sur OrchestratorState ───────────────────────────────────────

def test_orchestrator_state_keys():
    """Vérifie que OrchestratorState contient tous les champs requis."""
    required_keys = {"query", "messages", "selected_agent", "csv_path",
                     "agent_result", "final_response", "routing_reason"}
    assert required_keys == set(OrchestratorState.__annotations__.keys())


# ── Tests sur route_to_agent ──────────────────────────────────────────

def test_route_to_agent_returns_research():
    """Retourne 'research' quand selected_agent est research."""
    state = {"selected_agent": "research"}
    assert route_to_agent(state) == "research"


def test_route_to_agent_returns_analyst():
    """Retourne 'analyst' quand selected_agent est analyst."""
    state = {"selected_agent": "analyst"}
    assert route_to_agent(state) == "analyst"


def test_route_to_agent_defaults_to_research():
    """Retourne 'research' par défaut si selected_agent est vide."""
    state = {"selected_agent": ""}
    assert route_to_agent(state) == "research"


# ── Tests sur le graphe ───────────────────────────────────────────────

def test_build_orchestrator_graph_compiles():
    """Vérifie que le graphe compile sans erreur."""
    graph = build_orchestrator_graph()
    assert graph is not None


def test_build_orchestrator_graph_has_correct_nodes():
    """Vérifie que le graphe contient les bons noeuds."""
    graph = build_orchestrator_graph()
    nodes = graph.get_graph().nodes
    assert "supervisor" in nodes
    assert "research" in nodes
    assert "analyst" in nodes
    assert "synthesizer" in nodes


# ── Tests sur supervisor_node avec mock ──────────────────────────────

@patch("agent3_orchestrator.nodes.llm")
def test_supervisor_routes_to_research_without_csv(mock_llm):
    """Supervisor route vers research si pas de CSV."""
    from agent3_orchestrator.nodes import supervisor_node

    mock_response = MagicMock()
    mock_response.content = '{"agent": "research", "reason": "question générale"}'
    mock_llm.invoke.return_value = mock_response

    state = {
        "query": "Quelles sont les dernières avancées en IA ?",
        "csv_path": None,
        "messages": []
    }

    result = supervisor_node(state)
    assert result["selected_agent"] == "research"


@patch("agent3_orchestrator.nodes.llm")
def test_supervisor_routes_to_analyst_with_csv(mock_llm):
    """Supervisor route vers analyst si CSV disponible."""
    from agent3_orchestrator.nodes import supervisor_node

    mock_response = MagicMock()
    mock_response.content = '{"agent": "analyst", "reason": "CSV disponible"}'
    mock_llm.invoke.return_value = mock_response

    state = {
        "query": "Quel produit génère le plus de CA ?",
        "csv_path": "docs/sample_data.csv",
        "messages": []
    }

    result = supervisor_node(state)
    assert result["selected_agent"] == "analyst"


@patch("agent3_orchestrator.nodes.llm")
def test_supervisor_forces_research_when_analyst_without_csv(mock_llm):
    """Supervisor force research si analyst demandé mais pas de CSV."""
    from agent3_orchestrator.nodes import supervisor_node

    mock_response = MagicMock()
    mock_response.content = '{"agent": "analyst", "reason": "analyse data"}'
    mock_llm.invoke.return_value = mock_response

    state = {
        "query": "Analyse ces données",
        "csv_path": None,
        "messages": []
    }

    result = supervisor_node(state)
    assert result["selected_agent"] == "research"


@patch("agent3_orchestrator.nodes.llm")
def test_supervisor_handles_malformed_json(mock_llm):
    """Supervisor gère proprement un JSON malformé."""
    from agent3_orchestrator.nodes import supervisor_node

    mock_response = MagicMock()
    mock_response.content = "réponse invalide non JSON"
    mock_llm.invoke.return_value = mock_response

    state = {
        "query": "Question test",
        "csv_path": None,
        "messages": []
    }

    result = supervisor_node(state)
    assert result["selected_agent"] == "research"