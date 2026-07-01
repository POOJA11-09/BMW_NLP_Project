def decide(analysis):
    """
    Generate CEO strategic actions from analysis.
    """

    opportunities = analysis.get("opportunities", [])
    risks = analysis.get("risks", [])
    trends = analysis.get("trends", [])

    strategy = []

    # -------------------------
    # Opportunity-based actions
    # -------------------------
    for opp in opportunities:

        strategy.append({
            "action": f"Invest in {opp}",
            "priority": "High",
            "reason": "Strategic opportunity identified"
        })

    # -------------------------
    # Risk mitigation
    # -------------------------
    for risk in risks:

        strategy.append({
            "action": f"Reduce exposure to {risk}",
            "priority": "High",
            "reason": "Business risk detected"
        })

    # -------------------------
    # Trend alignment
    # -------------------------
    for trend in trends:

        strategy.append({
            "action": f"Align future strategy with {trend}",
            "priority": "Medium",
            "reason": "Industry trend"
        })

    # Remove duplicate actions
    unique = []
    seen = set()

    for item in strategy:

        if item["action"] not in seen:
            unique.append(item)
            seen.add(item["action"])

    if not unique:

        unique = [{
            "action": "Continue monitoring market developments",
            "priority": "Medium",
            "reason": "Insufficient strategic evidence"
        }]

    return {
        "strategy": unique
    }