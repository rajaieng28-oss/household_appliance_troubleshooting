# run.py
"""
Entry point for the Appliance Monitoring AI Agent.
Supports both CLI queries and batch testing.
"""

import os
import sys
import json
import argparse
import time

from app.workflows.graph import ApplianceGraph
from app.agents.monitoring_agent import MonitoringAgent

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# --- Initialize Global Objects ---
graph = ApplianceGraph()          # LangGraph workflow
monitoring_agent = MonitoringAgent()  # Observability agent

def run_cli(query: str):
    """
    Run a single query from CLI.
    """
    state = {
        "query": query,
        "retrieved_docs": [],
        "diagnosis": "",
        "tool_results": {},
        "resolution": "",
        "response": "",
        "execution_path": [],
        "monitoring": {},
        "need_tool": False,
        "route": "",
        "error": "",
        "rewritten_query": query,
        "sources": [],
        "category": "",
        "retry_count": 0,
        "start_time": time.time()
    }

    try:
        # Invoke the workflow graph
        final_state = graph.invoke(state)
        
        # Logging & observability
        monitoring_agent.log(final_state)

        # Print final formatted response
        print("\n=== Appliance Monitoring Response ===\n")
        print(final_state.get("response", "No response generated"))
        print("\n=== Sources Used ===")
        print(", ".join(final_state.get("sources", [])))
        print("\n=== Monitoring ===")
        print(json.dumps(final_state.get("monitoring", {}), indent=2))

    except Exception as e:
        print(f"[ERROR] Failed to process query: {str(e)}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Appliance Monitoring AI Agent")
    parser.add_argument(
        "-q", "--query", type=str, help="Query about an appliance", required=False
    )
    args = parser.parse_args()

    if args.query:
        run_cli(args.query)
    else:
        print("No query provided. You can run via Streamlit UI too:")
        print("streamlit run app/ui/streamlit_app.py --server.headless true")

if __name__ == "__main__":
    main()