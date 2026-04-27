from sentence_transformers import SentenceTransformer
import numpy as np

# Preload the embedding model
_model = SentenceTransformer("all-MiniLM-L6-v2")


def is_generic(text: str) -> bool:
    """
    Heuristic check for generic explanations that don't add useful reasoning.
    """
    generic_phrases = [
        "people buy",
        "because they like",
        "used for the same reason",
    ]
    return any(phrase in text.lower() for phrase in generic_phrases)


def similarity_filter(query: str, explanation: str, threshold: float = 0.8) -> bool:
    """
    Returns True if the explanation is dissimilar enough to the query (cosine similarity below threshold).
    Explanations that are too similar to the query are filtered out as uninformative.
    """
    emb_query = _model.encode(query)
    emb_expl = _model.encode(explanation)
    sim = np.dot(emb_query, emb_expl) / (np.linalg.norm(emb_query) * np.linalg.norm(emb_expl))
    return sim < threshold
