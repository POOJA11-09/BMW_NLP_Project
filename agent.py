from agent.planner import plan
from agent.retriever import retrieve
from agent.analyzer import analyze
from agent.decision import decide
from recommendation_engine.engine import generate_recommendations
from agent.validator import validate
from agent.sentiment import analyze_sentiment


def run_agent(question):

    # --------------------------
    # 1. PLAN
    # --------------------------
    plan_result = plan(question)

    # --------------------------
    # 2. RETRIEVE DOCS
    # --------------------------
    docs = retrieve(question)

    if not docs:
        docs = [{
            "text": "BMW is investing in EV, AI and autonomous driving technologies.",
            "source": "fallback"
        }]

    # --------------------------
    # 3. ANALYSIS
    # --------------------------
    analysis = analyze(question, docs)

    if not analysis:
        analysis = {
            "opportunities": ["EV market expansion"],
            "risks": ["High competition"],
            "trends": ["AI + Electric mobility"]
        }

    # --------------------------
    # 4. DECISION
    # --------------------------
    decision = decide(analysis)

    if not decision:
        decision = {
            "strategy": [{
                "action": "Monitor market trends",
                "priority": "Medium",
                "reason": "Fallback decision"
            }]
        }

    # --------------------------
    # 5. RECOMMENDATIONS
    # --------------------------
    recommendations = generate_recommendations(decision, docs)

    if not recommendations:
        recommendations = [{
            "recommendation": "Continue monitoring BMW EV strategy",
            "priority": "Medium",
            "expected_impact": "Moderate",
            "supporting_evidence": ["Fallback insight"]
        }]

    # --------------------------
    # 6. VALIDATION
    # --------------------------
    validation = validate(docs, decision)

    # --------------------------
    # 7. SENTIMENT
    # --------------------------
    sentiment = analyze_sentiment(docs)

    if not sentiment:
        sentiment = {"Positive": 0, "Negative": 0, "Neutral": 0}

    # --------------------------
    # FINAL OUTPUT (CLEAN)
    # --------------------------
    return {
        "plan": plan_result,
        "analysis": analysis,
        "decision": decision,
        "recommendations": recommendations,
        "validation": validation,
        "sentiment": sentiment,
        "docs": docs
    }