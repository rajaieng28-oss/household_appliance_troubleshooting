import os
from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

from app.rag.vectordb import get_vectorstore
from app.rag.embeddings import get_embeddings


KNOWLEDGE_BASE_PATH = "knowledge_base"


def load_documents():
    loader = DirectoryLoader(
        KNOWLEDGE_BASE_PATH,
        glob="**/*.md",
        show_progress=True
    )
    return loader.load()


def split_documents(docs):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150
    )
    return splitter.split_documents(docs)


def ingest():
    print("📥 Loading documents...")
    docs = load_documents()

    print(f"📄 Loaded {len(docs)} documents")

    chunks = split_documents(docs)
    print(f"✂️ Split into {len(chunks)} chunks")

    embeddings = get_embeddings()
    vectorstore = get_vectorstore(embeddings)

    print("💾 Adding to vector DB...")
    vectorstore.add_documents(chunks)

    print("✅ Ingestion complete!")


if __name__ == "__main__":
    ingest()