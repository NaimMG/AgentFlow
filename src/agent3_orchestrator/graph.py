from langgraph.graph import StateGraph, END
from agent3_orchestrator.state import OrchestratorState
from agent3_orchestrator.nodes import (
    supervisor_node,
    research_agent_node,
    analyst_agent_node,
    synthesizer_node,
    route_to_agent
)


def build_orchestrator_graph():
    """Construit le graphe du Multi-Agent Orchestrator."""

    graph = StateGraph(OrchestratorState)

    # Noeuds
    graph.add_node("supervisor", supervisor_node)
    graph.add_node("research", research_agent_node)
    graph.add_node("analyst", analyst_agent_node)
    graph.add_node("synthesizer", synthesizer_node)

    # Point d'entrée
    graph.set_entry_point("supervisor")

    # Edge conditionnel : supervisor route vers research ou analyst
    graph.add_conditional_edges(
        "supervisor",
        route_to_agent,
        {
            "research": "research",
            "analyst": "analyst"
        }
    )

    # Les deux agents convergent vers le synthesizer
    graph.add_edge("research", "synthesizer")
    graph.add_edge("analyst", "synthesizer")
    graph.add_edge("synthesizer", END)

    return graph.compile()