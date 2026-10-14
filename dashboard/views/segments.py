import pandas as pd
import plotly.express as px
import streamlit as st

from common import COLORS, PALETTE, footer, get_data, money, page_header, polish

orders, customers, segments, cluster_summary = get_data()

page_header(
    "CUSTOMER BEHAVIORAL SEGMENTATION",
    "Customer Segments",
    "Customer segmentation derived through K-means clustering over Recency, Frequency, and Monetary (RFM) behavioral metrics."
)

segment_names = {
    0: "Mostly One-Time Purchasers",
    1: "High-Engagement Repeat Purchasers",
}

segment_view = cluster_summary.copy()
segment_view["segment_name"] = segment_view["cluster"].map(segment_names).fillna(segment_view["cluster"].astype(str))

# KPI Overview
total_segmented = int(segment_view["customer_count"].sum())
repeat_seg = segment_view[segment_view["cluster"] == 1]
repeat_count = int(repeat_seg["customer_count"].values[0]) if not repeat_seg.empty else 0
repeat_share = (repeat_count / total_segmented * 100) if total_segmented else 0

st.markdown(f"""
<div class="kpi-grid">
    <div class="kpi-card kpi-cypress">
        <div class="kpi-label">Analyzed customer base</div>
        <div class="kpi-value">{total_segmented:,}</div>
        <div class="kpi-caption">Customers with valid delivered orders</div>
    </div>
    <div class="kpi-card kpi-bamboo">
        <div class="kpi-label">Repeat customer cohort</div>
        <div class="kpi-value">{repeat_count:,}</div>
        <div class="kpi-caption">{repeat_share:.2f}% of total customer universe</div>
    </div>
    <div class="kpi-card kpi-gold">
        <div class="kpi-label">Repeat buyer avg spend</div>
        <div class="kpi-value">{money(repeat_seg['avg_monetary'].values[0] if not repeat_seg.empty else 0)}</div>
        <div class="kpi-caption">1.88x higher than one-time purchasers</div>
    </div>
    <div class="kpi-card kpi-secondary">
        <div class="kpi-label">Active clusters (k)</div>
        <div class="kpi-value">2</div>
        <div class="kpi-caption">Optimal k determined via Silhouette Analysis</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

left, right = st.columns([0.9, 1.3], gap="large")

with left:
    fig = px.pie(
        segment_view,
        names="segment_name",
        values="customer_count",
        hole=0.62,
        title="Customer Population Share by Segment",
        color_discrete_sequence=[COLORS["cypress"], COLORS["berry"]],
    )
    fig.update_traces(textposition="inside", textinfo="percent+label")
    polish(fig, 360, legend=False)
    st.plotly_chart(fig, use_container_width=True)

with right:
    st.markdown("#### Segment Behavioral Profiles")
    card_columns = st.columns(max(1, len(segment_view)))

    for index, (_, row) in enumerate(segment_view.iterrows()):
        with card_columns[index]:
            label = str(row["segment_name"])
            count = int(row["customer_count"])
            frequency = float(row["avg_frequency"])
            avg_monetary = float(row["avg_monetary"])
            median_monetary = float(row["median_monetary"]) if "median_monetary" in row else avg_monetary
            accent = COLORS["berry"] if index % 2 == 0 else COLORS["cypress"]

            st.markdown(
                f"""
                <div class="segment-card" style="--segment-accent:{accent}">
                    <div class="segment-label">{label}</div>
                    <div class="segment-count">{count:,}</div>
                    <div class="segment-caption">Distinct customers ({count/total_segmented*100:.1f}%)</div>
                    <div class="segment-stat">
                        <span>Avg. order count</span><strong>{frequency:.2f} orders</strong>
                    </div>
                    <div class="segment-stat">
                        <span>Avg. item spend</span><strong>{money(avg_monetary)}</strong>
                    </div>
                    <div class="segment-stat">
                        <span>Median item spend</span><strong>{money(median_monetary)}</strong>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

st.markdown("---")

# Feature Comparison Chart
st.markdown("### Cluster Feature Comparison")
comp_df = pd.DataFrame({
    "Segment": ["Mostly One-Time", "Repeat Purchasers"],
    "Avg Frequency (Orders)": [float(segment_view.iloc[0]["avg_frequency"]), float(segment_view.iloc[1]["avg_frequency"])],
    "Avg Spend (R$)": [float(segment_view.iloc[0]["avg_monetary"]), float(segment_view.iloc[1]["avg_monetary"])],
    "Avg Recency (Days)": [245.0, 218.0] # empirical RFM averages from dataset
})

comp_col1, comp_col2 = st.columns(2, gap="large")

with comp_col1:
    fig_spend = px.bar(
        comp_df,
        x="Segment",
        y="Avg Spend (R$)",
        text="Avg Spend (R$)",
        title="Average Monetary Spend by Cluster",
        color="Segment",
        color_discrete_sequence=[COLORS["cypress"], COLORS["berry"]]
    )
    fig_spend.update_traces(texttemplate="R$ %{y:,.0f}", textposition="outside")
    polish(fig_spend, 340, legend=False)
    st.plotly_chart(fig_spend, use_container_width=True)

with comp_col2:
    fig_freq = px.bar(
        comp_df,
        x="Segment",
        y="Avg Frequency (Orders)",
        text="Avg Frequency (Orders)",
        title="Average Purchase Frequency by Cluster",
        color="Segment",
        color_discrete_sequence=[COLORS["cypress"], COLORS["berry"]]
    )
    fig_freq.update_traces(texttemplate="%{y:.2f}", textposition="outside")
    polish(fig_freq, 340, legend=False)
    st.plotly_chart(fig_freq, use_container_width=True)

st.markdown("---")

# Business Recommendations
st.markdown("### Tactical Business & Marketing Recommendations")
r_col1, r_col2 = st.columns(2, gap="large")

with r_col1:
    st.markdown(f"""
    <div style="background:#FFFFFF; border:1px solid rgba(98,30,62,0.12); border-left:5px solid {COLORS['cypress']}; border-radius:14px; padding:16px;">
        <h4 style="margin:0 0 8px 0; color:{COLORS['cypress']};">🎯 Segment 0: One-Time Purchasers (~97.0%)</h4>
        <p style="font-size:0.88rem; line-height:1.45; margin:0; color:{COLORS['berry']};">
            <strong>Observation:</strong> Vast majority of customers complete only a single order.<br>
            <strong>Actionable Recommendations:</strong><br>
            • Automated Post-Purchase Follow-up: Trigger personalized category recommendations within 14–30 days.<br>
            • Welcome Back Incentives: Deploy time-limited free shipping or bundle discounts to reduce churn.<br>
            • Review-Driven Re-engagement: Capitalize on satisfied 5-star buyers by offering exclusive next-order promotions.
        </p>
    </div>
    """, unsafe_allow_html=True)

with r_col2:
    st.markdown(f"""
    <div style="background:#FFFFFF; border:1px solid rgba(98,30,62,0.12); border-left:5px solid {COLORS['berry']}; border-radius:14px; padding:16px;">
        <h4 style="margin:0 0 8px 0; color:{COLORS['berry']};">⭐ Segment 1: High-Engagement Repeat Buyers (~3.0%)</h4>
        <p style="font-size:0.88rem; line-height:1.45; margin:0; color:{COLORS['berry']};">
            <strong>Observation:</strong> Drives disproportionate revenue with 1.88x higher average order values.<br>
            <strong>Actionable Recommendations:</strong><br>
            • VIP Loyalty Program: Introduce tiered loyalty perks, early access to seasonal promotions, and dedicated customer support.<br>
            • Cross-Sell Expansion: Promote complementary categories based on historical affinities.<br>
            • Referral Program: Turn high-frequency buyers into brand advocates with referral bonuses.
        </p>
    </div>
    """, unsafe_allow_html=True)

footer()
