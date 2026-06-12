# Commented lines are system related issues on python 3.13, instead use 3.11

import os
from langchain_community.document_loaders import DirectoryLoader
# from pathlib import Path
# from langchain_community.document_loaders import TextLoader
# try:
#     from langchain_text_splitters import RecursiveCharacterTextSplitter
# except ImportError:
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

    # """Load all markdown files from the knowledge base directory."""
    # documents = []
    # kb_path = Path(KNOWLEDGE_BASE_PATH)

    # if not kb_path.exists():
    #     raise FileNotFoundError(f"Knowledge base directory '{KNOWLEDGE_BASE_PATH}' not found.")

    # md_files = list(kb_path.glob("**/*.md"))

    # if not md_files:
    #     raise FileNotFoundError(f"No .md files found in '{KNOWLEDGE_BASE_PATH}'.")

    # print(f"Found {len(md_files)} markdown files in the knowledge base.")

    # for md_file in md_files:
    #     try:
    #         loader = TextLoader(str(md_file), encoding="utf-8")
    #         docs = loader.load()
    #         # Add source metadata to each document
    #         for doc in docs:
    #             doc.metadata["source"] = str(md_file)
    #         documents.extend(docs)
    #         print(f"Loaded: {md_file.name}")
    #     except Exception as e:
    #         print(f"Error loading {md_file.name}: {str(e)}")
    # return documents

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