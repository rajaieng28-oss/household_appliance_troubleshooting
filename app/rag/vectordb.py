import os
from langchain_community.vectorstores import Chroma

VECTOR_DB_PATH = "vector_db"


def get_vectorstore(embeddings):
    """
    Initializes Chroma vector DB for persistent storage.
    """

    return Chroma(
        persist_directory=VECTOR_DB_PATH,
        embedding_function=embeddings
    )