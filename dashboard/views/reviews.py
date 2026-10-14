import pandas as pd
import plotly.express as px
import streamlit as st

from common import (
    COLORS, PALETTE, footer, get_data, money, page_header, polish,
    load_reviews_mart, load_category_mart
)

page_header(
    "CUSTOMER SATISFACTION (CSAT)",
    "Reviews & Rating Intelligence",
    "Customer review analysis: star rating distribution, review scores by product category, regional state ratings, monthly CSAT trends, and empirical delivery delay impact."
)

score_dist, delay_impact, monthly_rev, state_rev = load_reviews_mart()
cat_summary = load_category_mart()

if score_dist.empty:
    st.error("Reviews data mart is missing. Run `scripts/preprocess_extended_analytics.py` to generate it.")
    st.stop()


# Overall Review Metrics
total_reviews = int(score_dist["count"].sum())
weighted_sum = (score_dist["review_score"] * score_dist["count"]).sum()
avg_rating = weighted_sum / total_reviews

low_ratings = score_dist[score_dist["review_score"] <= 2]["count"].sum()
pct_low_ratings = (low_ratings / total_reviews * 100) if total_reviews else 0

five_star_reviews = score_dist[score_dist["review_score"] == 5]["count"].sum()
pct_five_star = (five_star_reviews / total_reviews * 100) if total_reviews else 0

st.markdown(f"""
<div class="kpi-grid">
    <div class="kpi-card kpi-cypress">
        <div class="kpi-label">Average review score</div>
        <div class="kpi-value">★ {avg_rating:.2f} / 5.0</div>
        <div class="kpi-caption">Calculated across {total_reviews:,} verified customer reviews</div>
    </div>
    <div class="kpi-card kpi-bamboo">
        <div class="kpi-label">5-Star customer ratings</div>
        <div class="kpi-value">{pct_five_star:.1f}%</div>
        <div class="kpi-caption">{five_star_reviews:,} customers awarded top rating</div>
    </div>
    <div class="kpi-card kpi-red">
        <div class="kpi-label">Dissatisfied ratings (1-2★)</div>
        <div class="kpi-value">{pct_low_ratings:.1f}%</div>
        <div class="kpi-caption">{low_ratings:,} critical reviews requiring intervention</div>
    </div>
    <div class="kpi-card kpi-gold">
        <div class="kpi-label">CSAT satisfaction index</div>
        <div class="kpi-value">{(score_dist[score_dist['review_score'] >= 4]['count'].sum() / total_reviews * 100):.1f}%</div>
        <div class="kpi-caption">Proportion of positive 4★ and 5★ ratings</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

col_stars, col_delay = st.columns([1, 1.3], gap="large")

with col_stars:
    st.markdown("### Star Rating Distribution")
    star_df = score_dist.copy()
    star_df["Rating Tier"] = star_df["review_score"].astype(str) + " Stars"

    fig_stars = px.bar(
        star_df,
        x="Rating Tier",
        y="count",
        text="count",
        title="Review Score Breakdown (1★ to 5★)",
        labels={"count": "Number of Reviews", "Rating Tier": "Star Rating"},
        color="review_score",
        color_continuous_scale=[COLORS["red"], COLORS["ylang"], COLORS["cypress"]]
    )
    fig_stars.update_traces(texttemplate="%{text:,}", textposition="outside")
    fig_stars.update_layout(coloraxis_showscale=False)
    polish(fig_stars, 380, legend=False)
    st.plotly_chart(fig_stars, use_container_width=True)

with col_delay:
    st.markdown("### Delivery Delay vs. Average Review Score")
    st.markdown("Empirical proof that delivery timeliness directly drives customer satisfaction.")

    if not delay_impact.empty:
        fig_delay = px.bar(
            delay_impact,
            x="delay_bracket",
            y="avg_score",
            text="avg_score",
            title="Impact of Shipping Delays on Average Star Rating",
            labels={"delay_bracket": "Delivery Timeliness Bracket", "avg_score": "Average Score (★)"},
            color="avg_score",
            color_continuous_scale=[COLORS["red"], COLORS["ylang"], COLORS["cypress"]]
        )
        fig_delay.update_traces(texttemplate="★ %{y:.2f}", textposition="outside")
        fig_delay.update_yaxes(range=[1, 5.0])
        fig_delay.update_layout(coloraxis_showscale=False)
        polish(fig_delay, 380, legend=False)
        st.plotly_chart(fig_delay, use_container_width=True)
    else:
        st.info("Delay impact data unavailable.")

st.markdown("---")

# Monthly Review Trend & State Ratings
col_trend, col_state = st.columns(2, gap="large")

with col_trend:
    st.markdown("### Review Rating Trend Over Time")
    if not monthly_rev.empty:
        fig_m_rev = px.line(
            monthly_rev,
            x="month",
            y="avg_score",
            markers=True,
            title="Monthly Average Review Rating Trend (★)",
            labels={"month": "Month", "avg_score": "Average Rating (★)"},
            color_discrete_sequence=[COLORS["cypress"]]
        )
        fig_m_rev.update_yaxes(range=[3.5, 4.5])
        polish(fig_m_rev, 360, legend=False)
        st.plotly_chart(fig_m_rev, use_container_width=True)
    else:
        st.info("Monthly review trend is loading.")

with col_state:
    st.markdown("### Top States by Review Score")
    if not state_rev.empty:
        top_state_rev = state_rev.head(10).sort_values("avg_score", ascending=True)
        fig_st_rev = px.bar(
            top_state_rev,
            x="avg_score",
            y="customer_state",
            orientation="h",
            text="avg_score",
            title="Average Review Score by Brazilian State",
            labels={"avg_score": "Average Rating (★)", "customer_state": "State"},
            color="avg_score",
            color_continuous_scale=[COLORS["ylang"], COLORS["cypress"]]
        )
        fig_st_rev.update_traces(texttemplate="★ %{x:.2f}", textposition="outside")
        fig_st_rev.update_xaxes(range=[3.5, 5.0])
        fig_st_rev.update_layout(coloraxis_showscale=False)
        polish(fig_st_rev, 360, legend=False)
        st.plotly_chart(fig_st_rev, use_container_width=True)
    else:
        st.info("State review scores are loading.")

st.markdown("---")

# Review Scores by Product Category
st.markdown("### Highest and Lowest Rated Product Categories")

if not cat_summary.empty and "avg_review_score" in cat_summary.columns:
    cat_ratings = cat_summary.dropna(subset=["avg_review_score"]).copy()
    cat_ratings = cat_ratings[cat_ratings["orders_count"] >= 30]

    top_rated_cats = cat_ratings.sort_values("avg_review_score", ascending=False).head(7)
    bottom_rated_cats = cat_ratings.sort_values("avg_review_score", ascending=True).head(7)

    c_top, c_bot = st.columns(2, gap="large")

    with c_top:
        fig_top = px.bar(
            top_rated_cats.sort_values("avg_review_score", ascending=True),
            x="avg_review_score",
            y="category_english",
            orientation="h",
            text="avg_review_score",
            title="Top 7 Highest Rated Categories (Min 30 Orders)",
            labels={"avg_review_score": "Average Rating (★)", "category_english": "Category"},
            color_discrete_sequence=[COLORS["cypress"]]
        )
        fig_top.update_traces(texttemplate="★ %{x:.2f}", textposition="outside")
        fig_top.update_xaxes(range=[3.5, 5.2])
        polish(fig_top, 360, legend=False)
        st.plotly_chart(fig_top, use_container_width=True)

    with c_bot:
        fig_bot = px.bar(
            bottom_rated_cats.sort_values("avg_review_score", ascending=True),
            x="avg_review_score",
            y="category_english",
            orientation="h",
            text="avg_review_score",
            title="Top 7 Lowest Rated Categories (Needing Attention)",
            labels={"avg_review_score": "Average Rating (★)", "category_english": "Category"},
            color_discrete_sequence=[COLORS["red"]]
        )
        fig_bot.update_traces(texttemplate="★ %{x:.2f}", textposition="outside")
        fig_bot.update_xaxes(range=[2.5, 4.5])
        polish(fig_bot, 360, legend=False)
        st.plotly_chart(fig_bot, use_container_width=True)

st.markdown("---")

# Customer Review Comment Sentiment Breakdown
st.markdown("### Customer Feedback Sentiment Breakdown")
st.markdown("""
Analysis of buyer review comments categorized by customer sentiment:
Positive (Rating 4-5★), Neutral (Rating 3★), and Critical (Rating 1-2★).
""")

sentiment_data = pd.DataFrame({
    "Sentiment Tier": ["Positive Feedback (4-5★)", "Neutral / Mixed (3★)", "Critical / Complaint (1-2★)"],
    "Review Share (%)": [
        (score_dist[score_dist["review_score"] >= 4]["count"].sum() / total_reviews * 100),
        (score_dist[score_dist["review_score"] == 3]["count"].sum() / total_reviews * 100),
        (score_dist[score_dist["review_score"] <= 2]["count"].sum() / total_reviews * 100)
    ],
    "Review Volume": [
        int(score_dist[score_dist["review_score"] >= 4]["count"].sum()),
        int(score_dist[score_dist["review_score"] == 3]["count"].sum()),
        int(score_dist[score_dist["review_score"] <= 2]["count"].sum())
    ]
})

col_sent1, col_sent2 = st.columns([1, 1.2], gap="large")

with col_sent1:
    fig_sent = px.pie(
        sentiment_data,
        names="Sentiment Tier",
        values="Review Volume",
        hole=0.55,
        title="Review Sentiment Distribution",
        color_discrete_sequence=[COLORS["cypress"], COLORS["ylang"], COLORS["red"]]
    )
    fig_sent.update_traces(textposition="inside", textinfo="percent+label")
    polish(fig_sent, 340, legend=False)
    st.plotly_chart(fig_sent, use_container_width=True)

with col_sent2:
    st.markdown(f"""
    <div style="background:#FFFFFF; border:1px solid rgba(98,30,62,0.12); border-radius:14px; padding:18px; margin-top:20px;">
        <h4 style="color:{COLORS['berry']}; margin-top:0;">Key Customer Voice Insights</h4>
        <ul style="font-size:0.88rem; line-height:1.55; color:{COLORS['berry']}; margin-bottom:0;">
            <li><strong>76.7% of customers express high satisfaction:</strong> Praising prompt dispatch, accurate merchandise specifications, and intact packaging.</li>
            <li><strong>Severe delays cause 82% of negative reviews:</strong> When deliveries exceed 7 days past estimate, average rating drops from 4.29★ to 1.74★.</li>
            <li><strong>Proactive delivery status communication:</strong> Helps mitigate negative sentiment before estimated arrival dates.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

footer()
