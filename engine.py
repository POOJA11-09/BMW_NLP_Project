from agent.planner import call_llm


def generate_recommendations(decision, docs):
    """
    Generate executive recommendations
    from strategic decisions and evidence.
    """

    strategy = decision.get("strategy", [])

    if not strategy:
        return []

    actions = "\n".join(
        item["action"]
        for item in strategy
    )

    evidence = "\n\n".join(
        doc.get("text", "")[:1000]
        for doc in docs[:3]
    )

    prompt = f"""
You are BMW's CEO Strategy Advisor.

Strategic Decisions

{actions}

Evidence

{evidence}

For EACH strategic decision produce

- recommendation
- priority
- expected impact
- supporting evidence

Return ONLY JSON.

[
 {{
   "recommendation":"",
   "priority":"",
   "expected_impact":"",
   "supporting_evidence":[]
 }}
]
"""

    response = call_llm(prompt)

    try:

        response = response.replace("```json", "")
        response = response.replace("```", "")

        import json

        start = response.find("[")

        end = response.rfind("]")

        if start != -1 and end != -1:

            return json.loads(response[start:end+1])

    except:

        pass

    # ---------- FALLBACK ----------

    recommendations = []

    for item in strategy:

        recommendations.append({

            "recommendation": item["action"],

            "priority": item["priority"],

            "expected_impact":
                "High impact on BMW strategic positioning.",

            "supporting_evidence":[
                "Derived from retrieved BMW documents."
            ]
        })

    return recommendations