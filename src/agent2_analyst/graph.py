from langgraph.graph import StateGraph, END
from agent2_analyst.state import AnalystState
from agent2_analyst.nodes import (
    loader_node,
    code_generator_node,
    code_executor_node,
    answer_node,
    should_retry
)


def build_analyst_graph():
    """Construit et compile le graphe du Data Analyst Agent."""

    graph = StateGraph(AnalystState)

    # Noeuds
    graph.add_node("loader", loader_node)
    graph.add_node("code_generator", code_generator_node)
    graph.add_node("code_executor", code_executor_node)
    graph.add_node("answer", answer_node)

    # Point d'entrée
    graph.set_entry_point("loader")

    # Edges fixes
    graph.add_edge("loader", "code_generator")
    graph.add_edge("code_generator", "code_executor")

    # Edge conditionnel : retry si erreur ou answer si succès
    graph.add_conditional_edges(
        "code_executor",
        should_retry,
        {
            "retry": "code_generator",
            "answer": "answer"
        }
    )

    graph.add_edge("answer", END)

    return graph.compile()