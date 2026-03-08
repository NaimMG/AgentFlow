from langgraph.graph import StateGraph, END
from agent1_research.state import ResearchState
from agent1_research.nodes import planner_node, search_node, synthesizer_node, should_continue


def build_graph():
    """Construit et compile le graphe LangGraph du Research Agent."""

    graph = StateGraph(ResearchState)

    # Noeuds
    graph.add_node("planner", planner_node)
    graph.add_node("web_search", search_node)
    graph.add_node("synthesizer", synthesizer_node)

    # Point d'entrée
    graph.set_entry_point("planner")

    # Edges fixes
    graph.add_edge("planner", "web_search")
    graph.add_edge("web_search", "synthesizer")

    # Edge conditionnel : boucle ou fin
    graph.add_conditional_edges(
        "synthesizer",
        should_continue,
        {
            "continue": "web_search",
            "end": END
        }
    )

    return graph.compile()