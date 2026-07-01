import streamlit as st
from agent.agent import run_agent

# ---------------------------
# PAGE CONFIG
# ---------------------------
st.set_page_config(page_title="BMW Strategic Intelligence Engine", layout="wide")

st.title("🚗 BMW AI CEO Strategic Intelligence Dashboard")

# ---------------------------
# COMPANY OVERVIEW
# ---------------------------
st.subheader("🏢 Company Overview")

col1, col2, col3 = st.columns(3)
col1.metric("Company", "BMW")
col2.metric("Industry", "Automotive")
col3.metric("Documents", 104)

st.metric("Data Sources", 3)
st.divider()

# ---------------------------
# INPUT
# ---------------------------
query = st.text_input("Ask a Strategic Question")

# ---------------------------
# RUN BUTTON
# ---------------------------
if st.button("Run Analysis"):

    result = run_agent(query)

    # =========================
    # SAFE EXTRACTION
    # =========================
    analysis = result.get("analysis") or {}
    decision = result.get("decision") or {}
    recommendations = result.get("recommendations") or []
    sentiment = result.get("sentiment") or {}

    # FORCE STRUCTURE
    opportunities = analysis.get("opportunities") or []
    risks = analysis.get("risks") or []
    trends = analysis.get("trends") or []

    # CLEAN SENTIMENT
    sentiment = {
        "Positive": int(sentiment.get("Positive", 0) or 0),
        "Negative": int(sentiment.get("Negative", 0) or 0),
        "Neutral": int(sentiment.get("Neutral", 0) or 0)
    }

    st.success("Analysis Complete")

    # ---------------------------
    # MARKET INTELLIGENCE
    # ---------------------------
    st.subheader("📊 Market Intelligence")

    st.markdown("### Opportunities")
    for item in opportunities:
        st.write("•", item)

    st.markdown("### Risks")
    for item in risks:
        st.write("•", item)

    st.markdown("### Trends")
    for item in trends:
        st.write("•", item)

    st.divider()

    # ---------------------------
    # CEO DECISION ENGINE
    # ---------------------------
    st.subheader("📌 CEO Decision Engine")

    strategy = decision.get("strategy", [])

    if strategy:
        for item in strategy:
            st.info(f"""
🎯 Action: {item.get('action', 'N/A')}
🔥 Priority: {item.get('priority', 'Medium')}
💡 Reason: {item.get('reason', 'Not provided')}
""")
    else:
        st.warning("No strategic decisions generated")

    st.divider()

    # ---------------------------
    # STRATEGIC RECOMMENDATIONS
    # ---------------------------
    st.subheader("📈 Strategic Recommendations")

    if recommendations:
        for r in recommendations:
            if isinstance(r, dict):
                title = r.get("recommendation", "No recommendation")
                priority = r.get("priority", "Medium")
                impact = r.get("expected_impact", "N/A")
                evidence = r.get("supporting_evidence", [])
            else:
                title, priority, impact, evidence = str(r), "Medium", "N/A", []

            st.markdown(f"### 🎯 {title}")
            col1, col2 = st.columns(2)

            with col1:
                st.success(f"Priority: {priority}")
                st.write("Impact:", impact)

            with col2:
                st.warning("Risk Level: Medium")

            if evidence:
                st.write("📚 Evidence:")
                for e in evidence:
                    st.write("•", e)

            st.divider()
    else:
        st.warning("No recommendations generated")

    # ---------------------------
    # 🔥 INSIGHT DISTRIBUTION (FIXED + ROBUST GRAPH)
    # ---------------------------
    st.subheader("📊 Insight Distribution")

    chart_data = {
        "Opportunities": len([x for x in opportunities if x]),
        "Risks": len([x for x in risks if x]),
        "Trends": len([x for x in trends if x]),
    }

    st.bar_chart(chart_data)

    st.divider()

    # ---------------------------
    # SENTIMENT ANALYSIS
    # ---------------------------
    st.subheader("💬 Sentiment Analysis")

    st.bar_chart(sentiment)

    col1, col2, col3 = st.columns(3)
    col1.metric("Positive", sentiment["Positive"])
    col2.metric("Negative", sentiment["Negative"])
    col3.metric("Neutral", sentiment["Neutral"])

    st.divider()

    # ---------------------------
    # CEO BRIEFING
    # ---------------------------
    st.subheader("🧠 CEO Briefing")

    top_action = strategy[0]["action"] if strategy else "No action identified"
    top_priority = strategy[0]["priority"] if strategy else "N/A"

    briefing = f"""
WHAT HAPPENED:
- Found {len(opportunities)} opportunities, {len(risks)} risks, {len(trends)} trends.

WHY IT MATTERS:
- BMW is undergoing EV + AI transformation.

WHAT MANAGEMENT SHOULD DO NEXT:
- Action: {top_action}
- Priority: {top_priority}
"""

    st.info(briefing)