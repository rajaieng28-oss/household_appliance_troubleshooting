from app.llm import invoke


SYSTEM_PROMPT = """
You are a professional appliance repair assistant.

Create a final response with:
1. Problem Summary
2. Root Cause
3. Fix Steps (numbered)
4. Safety Warning (if any)
5. Sources used

Keep response structured and clear.
"""


def response_agent(state):

    response = invoke(
        prompt=f"""
Query: {state['query']}

Diagnosis:
{state.get('diagnosis','')}

Safety:
{state.get('safety_risk','')}

Sources:
{state.get('sources','')}
""",
        system_prompt=SYSTEM_PROMPT,
        max_tokens=400
    )

    state["response"] = response
    state["execution_path"].append("response")

    return state