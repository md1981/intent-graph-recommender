import streamlit as st
import yaml

from src.llm.generator import generate_reason
from src.filtering.filter import is_generic, similarity_filter
from src.graph.graph_builder import KnowledgeGraph
from src.retrieval.recommender import recommend


st.title("Intent-Based Product Recommender")

query = st.text_input("Enter a product-related query")

if query:
    # Load the list of candidate products from the config file
    try:
        with open("configs/config.yaml") as f:
            config = yaml.safe_load(f)
        products = config.get("products", [])
    except FileNotFoundError:
        products = []

    kg = KnowledgeGraph()
    reasoning_map = {}
    extracted_concepts = []

    for product in products:
        explanation = generate_reason(query, product)
        reasoning_map[product] = explanation
        # Discard generic or high-similarity explanations
        if is_generic(explanation):
            continue
        if not similarity_filter(query, explanation):
            continue
        # Naive concept extraction: take the last word of the explanation
        concept = explanation.split()[-1]
        extracted_concepts.append(concept)
        kg.add_triplet(product, "used_for", concept)

    # Display generated explanations
    if reasoning_map:
        st.subheader("Generated explanations (raw)")
        for prod, expl in reasoning_map.items():
            st.write(f"**{prod}**: {expl}")

    if extracted_concepts:
        st.subheader("Inferred concepts")
        unique_concepts = sorted(set(extracted_concepts))
        selected_concept = st.selectbox(
            "Select an inferred concept to see recommendations",
            options=["-- Select --"] + unique_concepts,
        )
        if selected_concept and selected_concept != "-- Select --":
            recommendations = recommend(kg, selected_concept)
            st.subheader("Recommended products")
            if recommendations:
                for item in recommendations:
                    st.write(f"- {item}")
            else:
                st.write("No products found for that concept.")
    else:
        st.write("No concepts extracted from explanations; try a different query.")
