from app.rag.retriever import retrieve_documents


def run_retrieval(state):
    result = retrieve_documents(state["query"])

    state["retrieved_docs"] = result["documents"]
    state["sources"] = result["sources"]

    state["execution_path"].append("retrieval")

    return state