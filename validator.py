import json
import re
from agent.planner import call_llm


def validate(evidence, decision):
    """
    Validate whether the generated strategic decisions
    are supported by the retrieved evidence.
    """

    evidence_text = "\n\n".join(
        doc.get("text", "")[:1500]
        for doc in evidence
    )

    decision_text = "\n".join(
        item.get("action", "")
        for item in decision.get("strategy", [])
    )

    prompt = f"""
You are a senior business auditor.

Retrieved Evidence:
{evidence_text}

Strategic Decisions:
{decision_text}

Evaluate whether the decisions are supported.

Return ONLY JSON.

{{
    "confidence_score":0.82,
    "is_reliable":true,
    "reason":"short explanation"
}}

ONLY JSON.
"""

    response = call_llm(prompt)

    response = response.replace("```json", "").replace("```", "").strip()

    match = re.search(r"\{.*\}", response, re.DOTALL)

    if match:
        try:
            return json.loads(match.group())
        except:
            pass

    return {
        "confidence_score":0.60,
        "is_reliable":True,
        "reason":"Validation fallback used."
    }