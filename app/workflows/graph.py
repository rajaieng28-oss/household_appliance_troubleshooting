from langgraph.graph import StateGraph, END
from app.workflows.state import ApplianceState

from app.agents.orchestrator import orchestrator_agent
from app.agents.retrieval_agent import retrieval_agent
from app.agents.diagnostic_agent import diagnostic_agent
from app.agents.safety_agent import safety_agent
from app.agents.response_agent import response_agent
from app.agents.monitoring_agent import monitoring_agent


# ─────────────────────────────
# ROUTING FUNCTIONS
# ─────────────────────────────

def route_after_diagnostic(state: ApplianceState):
    if state.get("need_safety_check", False):
        return "safety"
    return "response"


def route_after_safety(state: ApplianceState):
    return "response"


# ─────────────────────────────
# BUILD GRAPH
# ─────────────────────────────

def build_graph():
    builder = StateGraph(ApplianceState)

    # Nodes
    builder.add_node("orchestrator", orchestrator_agent)
    builder.add_node("retrieval", retrieval_agent)
    builder.add_node("diagnostic", diagnostic_agent)
    builder.add_node("safety", safety_agent)
    builder.add_node("response", response_agent)
    builder.add_node("monitoring", monitoring_agent)

    # Flow
    builder.set_entry_point("orchestrator")

    builder.add_edge("orchestrator", "retrieval")
    builder.add_edge("retrieval", "diagnostic")

    builder.add_conditional_edges(
        "diagnostic",
        route_after_diagnostic,
        {
            "safety": "safety",
            "response": "response"
        }
    )

    builder.add_edge("safety", "response")
    builder.add_edge("response", "monitoring")
    builder.add_edge("monitoring", END)

    return builder.compile()


graph = build_graph()