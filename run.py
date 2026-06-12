# run.py

# Commented lines are system related issues on python 3.13, instead use 3.11

"""
Entry point for the Appliance Monitoring AI Agent.
Supports both CLI queries and batch testing.
"""

import os
# os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"  # Fix for potential OpenMP issues on some platforms
# os.environ["OMP_NUM_THREADS"] = "1"  # Limit OpenMP to 1 thread to avoid conflicts

# # Add DLL search path for Windows (if needed)
# if sys.platform == "win32":
#     import pathlib
#     venv_path = pathlib.Path(sys.executable).parent.parent
#     dll_path = venv_path / "Lib" / "site-packages" / "torch" / "lib"
#     if dll_path.exists():
#         os.add_dll_directory(str(dll_path))

import sys
import json
import argparse
import time

from app.workflows.graph import ApplianceGraph

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# --- Initialize Global Objects ---
graph = ApplianceGraph()          # LangGraph workflow

def run_cli(query: str):
    """
    Run a single query from CLI.
    """
    state = {
        "query": query,
        "category": "",
        "retrieved_docs": [],
        "sources": [],
        "diagnosis": "",
        "root_cause": "",
        "safety_status": "",
        "risk_level": "",
        "safety_flags": [],
        "tool_results": {},
        "resolution": "",
        "response": "",
        "need_retrieval": False,
        "need_safety_check": False,
        "retry_count": 0,
        "start_time": time.time(),
        "latency": 0.0,
        "error": "",
        "execution_path": []
    }

    try:
        # Invoke the workflow graph
        final_state = graph.invoke(state)

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