import networkx as nx

class KnowledgeGraph:
    """A simple directed graph to store product-concept relationships."""

    def __init__(self) -> None:
        # Directed graph where edges are labelled with a relation
        self.graph = nx.DiGraph()

    def add_triplet(self, product: str, relation: str, concept: str) -> None:
        """Add a (product, relation, concept) triple to the graph."""
        self.graph.add_edge(product, concept, relation=relation)

    def query(self, concept: str):
        """Return all products that point to the given concept."""
        return [u for u, v in self.graph.edges() if v == concept]

