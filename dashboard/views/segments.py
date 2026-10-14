import pandas as pd
import plotly.express as px
import streamlit as st

from common import COLORS, PALETTE, footer, get_data, money, page_header, polish

orders, customers, segments, cluster_summary = get_data()

page_header("CUSTOMERS", "Customer segmentation", "RFM-based K-means groups across delivered purchases.")

st.markdown(
    '<div class="section-note">RFM-based K-means groups across delivered '
    'purchases. Segment totals use the complete segmentation dataset.</div>',
    unsafe_allow_html=True,
)

segment_names = {
    0: "Mostly one-time purchasers",
    1: "Repeat purchasers",
}

segment_view = cluster_summary.copy()
segment_view["segment_name"] = segment_view["cluster"].map(
    segment_names
).fillna(segment_view["cluster"].astype(str))

left, right = st.columns([0.9, 1.3], gap="large")

with left:
    fig = px.pie(
        segment_view,
        names="segment_name",
        values="customer_count",
        hole=0.62,
        title="Customer share by segment",
        color_discrete_sequence=[COLORS["cypress"], COLORS["berry"]],
    )
    fig.update_traces(textposition="inside", textinfo="percent")
    polish(fig, 350, legend=True)
    fig.update_layout(
        legend=dict(orientation="h", yanchor="top", y=-0.04, xanchor="center", x=0.5)
    )
    st.plotly_chart(fig, use_container_width=True)

with right:
    st.markdown("#### Segment snapshot")
    card_columns = st.columns(max(1, len(segment_view)))

    for index, (_, row) in enumerate(segment_view.iterrows()):
        with card_columns[index]:
            label = str(row["segment_name"])
            count = int(row["customer_count"])
            frequency = float(row["avg_frequency"])
            avg_monetary = float(row["avg_monetary"])
            accent = COLORS["berry"] if index % 2 == 0 else COLORS["cypress"]

            st.markdown(
                f"""
                <div class="segment-card" style="--segment-accent:{accent}">
                    <div class="segment-label">{label}</div>
                    <div class="segment-count">{count:,}</div>
                    <div class="segment-caption">Customers</div>
                    <div class="segment-stat">
                        <span>Avg. orders</span><strong>{frequency:.2f}</strong>
                    </div>
                    <div class="segment-stat">
                        <span>Avg. item spend</span>
                        <strong>{money(avg_monetary)}</strong>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

st.caption(
    "RFM reference date: 30 August 2018. Segment labels describe the "
    "K-means output; they are not predefined customer classes."
)

footer()
