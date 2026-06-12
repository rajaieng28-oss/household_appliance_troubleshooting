# Commented lines are system related issues on python 3.13, instead use 3.11

import sys
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
import time
import streamlit as st

# ─────────────────────────────────────────────
# Ensure project root is in path
# ─────────────────────────────────────────────
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from app.workflows.graph import graph
from app.tools.appliance_tools import (
    power_supply_check,
    error_code_lookup,
    maintenance_scheduler,
    safety_risk_analyzer
)

# ─────────────────────────────────────────────
# Page Config
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Household Appliance Monitoring Agent",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─────────────────────────────────────────────
# UI Styling
# ─────────────────────────────────────────────
st.markdown("""
<style>
body {
    background-color: #0b0f19;
    color: #e2e8f0;
    font-family: 'Outfit', sans-serif;
}

.title {
    font-size: 2.2rem;
    font-weight: 700;
    background: linear-gradient(to right, #38bdf8, #a855f7);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.card {
    background: rgba(17, 24, 39, 0.7);
    padding: 16px;
    border-radius: 12px;
    border: 1px solid rgba(255,255,255,0.08);
    margin-bottom: 12px;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# Header
# ─────────────────────────────────────────────
st.markdown("<div class='title'>🏠 Household Appliance Monitoring Agent</div>", unsafe_allow_html=True)
st.caption("Multi-Agent RAG System for Appliance Troubleshooting + Safety Analysis")

# ─────────────────────────────────────────────
# Query Input
# ─────────────────────────────────────────────
query = st.text_area(
    "Describe your appliance issue",
    placeholder="e.g. Washing machine is leaking water and vibrating heavily",
    height=100
)

# ─────────────────────────────────────────────
# Submit Button
# ─────────────────────────────────────────────
if st.button("🚀 Diagnose Issue"):

    if not query.strip():
        st.warning("Please enter an appliance issue.")
        st.stop()

    # ─────────────────────────────────────────
    # INITIAL STATE
    # ─────────────────────────────────────────
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

    # ─────────────────────────────────────────
    # RUN PIPELINE
    # ─────────────────────────────────────────
    with st.spinner("🧠 Running appliance diagnostics..."):
        result = graph.invoke(state)

    # ─────────────────────────────────────────
    # OUTPUT
    # ─────────────────────────────────────────
    st.markdown("## 📊 Diagnosis Result")

    st.markdown(f"""
    <div class="card">
        <b>Category:</b> {result.get('category', 'N/A')} <br>
        <b>Root Cause:</b> {result.get('root_cause', 'N/A')} <br>
        <b>Risk Level:</b> {result.get('risk_level', 'N/A')} <br>
        <b>Latency:</b> {result.get('latency', 0)} sec
    </div>
    """, unsafe_allow_html=True)

    # ─────────────────────────────────────────
    # RESPONSE
    # ─────────────────────────────────────────
    st.markdown("## 🛠️ Recommended Fix")
    st.write(result.get("response", "No response generated"))

    # ─────────────────────────────────────────
    # SAFETY SECTION
    # ─────────────────────────────────────────
    st.markdown("## ⚠️ Safety Status")

    if result.get("risk_level") in ["HIGH", "CRITICAL"]:
        st.error("🚨 HIGH RISK DETECTED — Stop using the appliance immediately")
    elif result.get("risk_level") == "MEDIUM":
        st.warning("⚠️ Moderate risk detected — proceed carefully")
    else:
        st.success("✅ No safety risks detected")

    # ─────────────────────────────────────────
    # RETRIEVED KNOWLEDGE
    # ─────────────────────────────────────────
    st.markdown("## 📚 Knowledge Base References")

    docs = result.get("retrieved_docs", [])
    sources = result.get("sources", [])

    if docs:
        for i, doc in enumerate(docs):
            src = sources[i] if i < len(sources) else "unknown"
            with st.expander(f"📄 Source {i+1}: {src}"):
                st.write(doc)
    else:
        st.info("No knowledge base documents retrieved.")

    # ─────────────────────────────────────────
    # TOOL OUTPUTS
    # ─────────────────────────────────────────
    st.markdown("## 🛠️ Tool Outputs")

    tools = result.get("tool_results", {})

    if tools:
        for k, v in tools.items():
            st.json({k: v})
    else:
        st.info("No tools were executed for this query.")

    # ─────────────────────────────────────────
    # MONITORING
    # ─────────────────────────────────────────
    st.markdown("## 📈 Monitoring Info")

    st.json({
        "latency": result.get("latency"),
        "category": result.get("category"),
        "risk_level": result.get("risk_level"),
        "error": result.get("error"),
        "docs_retrieved": len(result.get("retrieved_docs", []))
    })