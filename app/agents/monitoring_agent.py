import time
import json
import os


LOG_PATH = "logs/execution.json"


def monitoring_agent(state):

    start_time = state.get("start_time", time.time())
    latency = round(time.time() - start_time, 2)

    log_entry = {
        "query": state["query"],
        "category": state.get("category"),
        "latency_seconds": latency,
        "execution_path": state.get("execution_path", []),
        "sources": state.get("sources", []),
        "need_retrieval": state.get("need_retrieval", False),
        "status": "success" if not state.get("error") else "failed"
    }

    os.makedirs("logs", exist_ok=True)

    if os.path.exists(LOG_PATH):
        with open(LOG_PATH, "r") as f:
            data = json.load(f)
    else:
        data = []

    data.append(log_entry)

    with open(LOG_PATH, "w") as f:
        json.dump(data, f, indent=2)

    state["latency"] = latency
    state["monitoring"] = log_entry
    state["execution_path"].append("monitoring")

    return state