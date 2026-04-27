import os
import openai


def generate_reason(query: str, product: str) -> str:
    """
    Generate a one-sentence explanation for why a user with the given query might be interested in the product.
    Falls back to a simple heuristic if no API key is available.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        # naive fallback explanation
        return f"{product} may satisfy needs implied by '{query}'"

    openai.api_key = api_key
    prompt = (
        "Given a user query and a product, explain in one sentence why the user might buy this product.\n\n"
        f"Query: {query}\n"
        f"Product: {product}\n"
    )
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=60,
        )
        return response.choices[0].message["content"].strip()
    except Exception:
        return f"{product} may satisfy needs implied by '{query}'"
