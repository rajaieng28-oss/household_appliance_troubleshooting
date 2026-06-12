from typing import TypedDict, List, Dict, Any

class ApplianceState(TypedDict):
    # ── INPUT ──
    query: str

    # ── RAG ──
    category: str
    retrieved_docs: List[str]
    sources: List[str]

    # ── LLM OUTPUTS ──
    diagnosis: str
    root_cause: str
    safety_status: str
    risk_level: str

    # ── TOOL / SAFETY ──
    safety_flags: List[str]
    tool_results: Dict[str, Any]

    # ── FINAL OUTPUT ──
    resolution: str
    response: str

    # ── CONTROL FLOW ──
    need_retrieval: bool
    need_safety_check: bool
    retry_count: int

    # ── OBSERVABILITY ──
    start_time: float
    latency: float
    error: str