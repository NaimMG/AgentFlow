import pytest
from unittest.mock import patch, MagicMock
from agent2_analyst.state import AnalystState
from agent2_analyst.nodes import should_retry
from agent2_analyst.graph import build_analyst_graph


# ── Tests sur AnalystState ────────────────────────────────────────────

def test_analyst_state_keys():
    """Vérifie que AnalystState contient tous les champs requis."""
    required_keys = {"query", "messages", "csv_path", "data_preview",
                     "generated_code", "execution_result",
                     "chart_path", "final_answer", "attempts", "max_attempts"}
    assert required_keys == set(AnalystState.__annotations__.keys())


# ── Tests sur should_retry ────────────────────────────────────────────

def test_should_retry_returns_answer_when_no_error():
    """Retourne 'answer' quand l'exécution est un succès."""
    state = {
        "execution_result": "Smartphone X : 475994.05",
        "attempts": 1,
        "max_attempts": 3
    }
    assert should_retry(state) == "answer"


def test_should_retry_returns_retry_on_error():
    """Retourne 'retry' quand il y a une erreur et des tentatives restantes."""
    state = {
        "execution_result": "ERREUR : NameError: name 'df' is not defined",
        "attempts": 1,
        "max_attempts": 3
    }
    assert should_retry(state) == "retry"


def test_should_retry_returns_answer_when_max_attempts_reached():
    """Retourne 'answer' même si erreur quand max atteint."""
    state = {
        "execution_result": "ERREUR : SyntaxError",
        "attempts": 3,
        "max_attempts": 3
    }
    assert should_retry(state) == "answer"


def test_should_retry_returns_answer_when_empty_result():
    """Retourne 'answer' si résultat vide."""
    state = {
        "execution_result": "",
        "attempts": 0,
        "max_attempts": 3
    }
    assert should_retry(state) == "answer"


# ── Tests sur le graphe ───────────────────────────────────────────────

def test_build_analyst_graph_compiles():
    """Vérifie que le graphe compile sans erreur."""
    graph = build_analyst_graph()
    assert graph is not None


def test_build_analyst_graph_has_correct_nodes():
    """Vérifie que le graphe contient les bons noeuds."""
    graph = build_analyst_graph()
    nodes = graph.get_graph().nodes
    assert "loader" in nodes
    assert "code_generator" in nodes
    assert "code_executor" in nodes
    assert "answer" in nodes


# ── Tests sur loader_node ─────────────────────────────────────────────

def test_loader_node_with_valid_csv():
    """Vérifie que loader_node charge correctement un CSV."""
    from agent2_analyst.nodes import loader_node

    state = {
        "csv_path": "docs/sample_data.csv",
        "query": "test"
    }

    result = loader_node(state)
    assert "data_preview" in result
    assert "Shape" in result["data_preview"]
    assert result["attempts"] == 0


def test_loader_node_with_invalid_csv():
    """Vérifie que loader_node gère proprement un CSV inexistant."""
    from agent2_analyst.nodes import loader_node

    state = {
        "csv_path": "inexistant.csv",
        "query": "test"
    }

    result = loader_node(state)
    assert "Erreur" in result["data_preview"]


# ── Tests sur code_executor_node avec mock ────────────────────────────

def test_code_executor_runs_valid_code():
    """Vérifie que code_executor exécute du code valide."""
    from agent2_analyst.nodes import code_executor_node

    state = {
        "csv_path": "docs/sample_data.csv",
        "generated_code": "print('test réussi')",
        "attempts": 0
    }

    result = code_executor_node(state)
    assert "test réussi" in result["execution_result"]
    assert result["attempts"] == 1


def test_code_executor_handles_invalid_code():
    """Vérifie que code_executor gère proprement une erreur de code."""
    from agent2_analyst.nodes import code_executor_node

    state = {
        "csv_path": "docs/sample_data.csv",
        "generated_code": "raise ValueError('erreur simulée')",
        "attempts": 0
    }

    result = code_executor_node(state)
    assert "ERREUR" in result["execution_result"]
    assert result["attempts"] == 1