from typing import List

from .graph_builder import KnowledgeGraph  # type: ignore


def recommend(graph: KnowledgeGraph, inferred_intent: str) -> List[str]:
    """Return products related to the inferred intent via the knowledge graph."""
    return graph.query(inferred_intent)

