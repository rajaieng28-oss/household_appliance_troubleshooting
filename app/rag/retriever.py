from app.rag.vectordb import get_vectorstore
from app.rag.embeddings import get_embeddings


def get_retriever():
    embeddings = get_embeddings()
    vectorstore = get_vectorstore(embeddings)

    # MMR = diversity + relevance (avoids repetitive appliance chunks)
    return vectorstore.as_retriever(
        search_type="mmr",
        search_kwargs={
            "k": 4,
            "fetch_k": 10
        }
    )


def retrieve_documents(query: str):
    retriever = get_retriever()
    docs = retriever.invoke(query)

    cleaned_docs = []
    sources = []

    for doc in docs:
        cleaned_docs.append(doc.page_content)
        sources.append(doc.metadata.get("source", "unknown.md"))

    return {
        "documents": cleaned_docs,
        "sources": list(set(sources))
    }