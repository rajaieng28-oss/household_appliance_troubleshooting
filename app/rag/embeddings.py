from langchain_huggingface import HuggingFaceEmbeddings


def get_embeddings():
    """
    Uses a free sentence-transformer model from HuggingFace.
    Good balance of speed + accuracy for appliance troubleshooting.
    """

    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )