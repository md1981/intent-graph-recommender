"""Entry point for running the intent aware recommendation prototype.

This script builds a knowledge graph from a set of candidate products given a user query
and prints the list of products associated with a chosen concept.  It is meant to be
simple and self‟contained for demonstration purposes.

Run this file with a query and a list of products to see how the pipeline works.
"""

from src.llm.generator import generate_reason
from src.filtering.filter import is_generic, similarity_filter
from src.graph.graph_builder import KnowledgeGraph


def run_pipeline(query: str, products: list[str]) -> KnowledgeGraph:
    """Builds a knowledge graph for the given query and products.

    Args:
        query: The user query (e.g. "shoes for elderly people").
        products: A list of product names to consider.

    Returns:
        A KnowledgeGraph instance populated with triplets based on the query and products.
    """
    kg = KnowledgeGraph()
    for product in products:
        explanation = generate_reason(query, product)
        # Skip overly generic or irrelevant explanations
        if is_generic(explanation):
            continue
        # Skip explanations that are too similar to the query (lack of useful additional information)
        if not similarity_filter(query, explanation):
            continue
        # Very naive concept extractor: take the last word of the explanation
        concept = explanation.split()[-1]
        kg.add_triplet(product, "used_for", concept)
    return kg


if __name__ == "__main__":
    example_query = "shoes for elderly people"
    example_products = ["running shoes", "slip‟resistant shoes", "formal shoes"]
    kg = run_pipeline(example_query, example_products)
    results = kg.query("stability")
    print(results)
