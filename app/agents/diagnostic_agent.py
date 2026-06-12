from app.llm import invoke


SYSTEM_PROMPT = """
You are an expert appliance repair technician.

Given the context, identify:
- Root cause
- Severity (Low / Medium / High)
- Short explanation

Respond in format:
ROOT_CAUSE: ...
SEVERITY: ...
EXPLANATION: ...
"""


def run_diagnostic(state):

    context = "\n".join(state.get("retrieved_docs", []))

    response = invoke(
        prompt=f"Query: {state['query']}\n\nContext:\n{context}",
        system_prompt=SYSTEM_PROMPT,
        max_tokens=200
    )

    state["diagnosis"] = response
    state["execution_path"].append("diagnostic")

    return state