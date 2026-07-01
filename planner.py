import requests

API_URL = "https://api-inference.huggingface.co/models/Qwen/Qwen3-8B-Instruct"

headers = {
    "Authorization": "Bearer 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"
}

session = requests.Session()
session.trust_env = False


def call_llm(prompt):
    try:
        response = session.post(
            API_URL,
            headers=headers,
            json={"inputs": prompt},
            timeout=60
        )

        data = response.json()

        if isinstance(data, list) and len(data) > 0:
            return data[0].get("generated_text", "")

        return ""

    except Exception as e:
        print("LLM ERROR:", e)
        return ""

def plan(query):

    prompt = f"""
You are a BMW strategic planner.

Break the question into:
- key insights
- risks
- opportunities
- required data

Question: {query}

Return plain text.
"""

    return call_llm(prompt)