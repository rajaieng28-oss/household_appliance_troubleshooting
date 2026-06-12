from app.llm import invoke


SYSTEM_PROMPT = """
You are an appliance support orchestrator.

Classify the user query into one of:
- Refrigerator
- Washing Machine
- Microwave
- Air Conditioner
- Dishwasher
- Vacuum Cleaner
- General

Also decide if knowledge base retrieval is required.

Respond strictly in format:
CATEGORY: <category>
NEEDS_RETRIEVAL: YES or NO
"""


def orchestrator_agent(state):
    response = invoke(
        prompt=state["query"],
        system_prompt=SYSTEM_PROMPT,
        max_tokens=80
    )

    state["execution_path"].append("orchestrator")

    lines = response.split("\n")
    for line in lines:
        if "CATEGORY" in line:
            state["category"] = line.split(":")[1].strip()
        if "NEEDS_RETRIEVAL" in line:
            state["need_retrieval"] = "YES" in line.upper()

    return state