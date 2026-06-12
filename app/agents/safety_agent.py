from app.llm import invoke


SYSTEM_PROMPT = """
You are a SAFETY inspection agent for home appliances.

Detect if the situation is dangerous.

Classify:
- SAFE
- WARNING
- DANGEROUS

Respond strictly:
SAFETY_STATUS: ...
RISK_REASON: ...
ACTION: ...
"""


def run_safety(state):

    context = "\n".join(state.get("retrieved_docs", []))

    response = invoke(
        prompt=f"{state['query']}\n\n{context}",
        system_prompt=SYSTEM_PROMPT,
        max_tokens=150
    )

    state["safety_risk"] = response
    state["execution_path"].append("safety")

    return state