from langchain_core.tools import tool
import random


# ─────────────────────────────
# 1. Power / Electrical Check Tool
# ─────────────────────────────
@tool
def power_supply_check(appliance: str) -> dict:
    """Simulates electrical/power supply diagnostics."""
    return {
        "appliance": appliance,
        "power_status": random.choice(["OK", "LOW_VOLTAGE", "NO_POWER"]),
        "risk": "HIGH" if random.random() > 0.7 else "LOW"
    }


# ─────────────────────────────
# 2. Error Code Lookup Tool
# ─────────────────────────────
@tool
def error_code_lookup(code: str) -> dict:
    """Maps appliance error codes to explanations."""
    mapping = {
        "E1": "Water supply issue",
        "E2": "Motor malfunction",
        "E3": "Temperature sensor failure",
        "F0": "Cooling system failure"
    }

    return {
        "code": code,
        "meaning": mapping.get(code, "Unknown error code")
    }


# ─────────────────────────────
# 3. Maintenance Scheduler Tool
# ─────────────────────────────
@tool
def maintenance_scheduler(appliance: str) -> dict:
    """Suggests maintenance schedule."""
    return {
        "appliance": appliance,
        "next_service_days": random.randint(30, 180),
        "priority": random.choice(["LOW", "MEDIUM", "HIGH"])
    }


# ─────────────────────────────
# 4. Safety Risk Analyzer Tool
# ─────────────────────────────
@tool
def safety_risk_analyzer(issue: str) -> dict:
    """Detects potential appliance safety risks."""
    risky_keywords = ["smoke", "burning", "leak", "shock", "fire"]

    risk = any(word in issue.lower() for word in risky_keywords)

    return {
        "issue": issue,
        "risk_detected": risk,
        "action": "TURN_OFF_IMMEDIATELY" if risk else "SAFE_TO_PROCEED"
    }