# Intent-Aware Product Recommendation System

## Overview

Traditional recommendation systems rely on keyword matching or collaborative filtering. These methods fall short when users express needs indirectly.  This project demonstrates a simple intent aware pipeline that bridges the gap between user queries and product attributes using:

* **LLM generated reasoning** – a language model generates a short explanation of why a product might satisfy a query.
* **Noise filtering** – generic or off‟topic outputs are discarded using simple heuristics and similarity checks.
* **Knowledge graph construction** – explanations are converted into triplets (product, relation, concept) that capture intent.
* **Intent‟based retrieval** – the knowledge graph enables explainable recommendations for new queries.

The goal is to illustrate an architecture inspired by common sense reasoning systems such as Amazon’s COSMO without attempting to reproduce their scale.

## Key Idea

Instead of directly matching:

```
query → product
```

we model a latent concept that explains why a user needs something:

```
query → intent (concept) → product
```

For example, the query "shoes for elderly people" is mapped to the intent **stability**, and stability implies **slip‟resistant shoes**.  This intermediate concept improves recommendations and makes them explainable.

## Architecture

1. **Reasoning generation** – The language model is prompted with the query and product to produce a one‟sentence explanation.
2. **Filtering** – Generic phrases are removed and similarity between query and explanation is used to weed out noise.
3. **Triple extraction** – The last word of the explanation is taken as the concept (a naive extractor).  You can improve this step later.
4. **Graph construction** – The triples are inserted into a directed graph using NetworkX.  Each edge stores the relation between a product and a concept.
5. **Intent‟based retrieval** – Given a new query, the inferred intent is matched against the graph to return relevant products.

The code is intentionally lightweight to emphasise the design rather than production‟scale engineering.

## Features

* LLM‟based reasoning generation (via OpenAI or other models).
* Basic noise filtering using heuristics and vector similarity.
* Knowledge graph construction with NetworkX.
* Streamlit demo for interactive queries.
* Easy to extend and improve (e.g. better concept extraction, additional filtering, evaluation metrics).

## Running the Project

This project is built as a small end‟to‟end prototype, so you can run it in two ways: from the command line or through the Streamlit demo.

### 1. Clone the repository

```bash
git clone https://github.com/your-username/intent-graph-recommender.git
cd intent-graph-recommender
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it:

```bash
# macOS / Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the main pipeline

```bash
python main.py
```

This runs a small sample flow that takes a user‟style product query, generates intent‟based reasoning, filters weak explanations, and builds a lightweight knowledge graph for recommendations.

### 5. Run the demo app

```bash
streamlit run demo/app.py
```

The demo lets you enter a query and see how the system connects the query to an inferred intent and a recommended product.

Example queries to try:

```
shoes for elderly people
jacket for winter hiking
chair for long working hours
gift for someone who runs
```

### Notes

The current version is intentionally lightweight.  It is meant to show the core idea clearly rather than simulate a production‟scale recommendation system.  The main focus is the pipeline design: reasoning generation, filtering, graph construction, and explainable retrieval.

## Example Outputs

Below are a few sample cases that show how the system moves beyond keyword matching by identifying the intent behind a user query.

### Example 1

**Query**

```
shoes for elderly people
```

**Inferred intent**

```
stability, safety, slip resistance
```

**Recommended product**

```
Slip‟resistant walking shoes
```

**Reasoning**

```
Elderly users may need shoes that reduce the risk of slipping and provide better balance while walking.
```

---

### Example 2

**Query**

```
chair for long working hours
```

**Inferred intent**

```
comfort, posture support, back support
```

**Recommended product**

```
Ergonomic office chair
```

**Reasoning**

```
A user sitting for long hours likely needs a chair that supports posture and reduces back strain.
```

---

### Example 3

**Query**

```
jacket for winter hiking
```

**Inferred intent**

```
warmth, weather protection, mobility
```

**Recommended product**

```
Insulated waterproof hiking jacket
```

**Reasoning**

```
Winter hiking requires clothing that keeps the user warm, protects against wind or snow, and still allows movement.
```

---

### Example 4

**Query**

```
gift for someone who runs
```

**Inferred intent**

```
running comfort, recovery, performance
```

**Recommended product**

```
Running socks or hydration belt
```

**Reasoning**

```
A runner may benefit from products that improve comfort during runs or help with training and recovery.
```

## What This Demonstrates

This project demonstrates a simplified version of an intent‟aware recommendation pipeline:

```
User query → inferred intent → structured graph relationship → explainable product recommendation
```

The main goal is not to build a production‟scale recommendation engine but to show how LLM‟generated reasoning and graph‟based retrieval can make recommendations more explainable than basic keyword matching.
