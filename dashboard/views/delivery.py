import pandas as pd
import plotly.express as px
import streamlit as st

from common import (
    COLORS, PALETTE, footer, get_data, money, page_header, polish,
    load_delivery_mart
)

page_header(
    "FULFILLMENT & SUPPLY CHAIN",
    "Delivery & Logistics Analytics",
    "End-to-end delivery transit duration, carrier turnaround, estimated vs. actual delivery delay, on-time success rates, and regional fulfillment bottlenecks."
)

delivery_orders, state_delivery = load_delivery_mart()

if delivery_orders.empty:
    st.error("Delivery data mart is missing. Run `scripts/preprocess_extended_analytics.py` to generate it.")
    st.stop()

delivery_orders = delivery_orders.copy()

# Overall Delivery Calculations
total_delivered_evaluated = len(delivery_orders)
avg_duration = delivery_orders["delivery_duration_days"].mean()
median_duration = delivery_orders["delivery_duration_days"].median()

late_count = int(delivery_orders["is_late"].sum())
on_time_count = total_delivered_evaluated - late_count
on_time_rate = (on_time_count / total_delivered_evaluated * 100) if total_delivered_evaluated else 0
late_rate = 100.0 - on_time_rate

# Delay relative to estimate: positive = late, negative = early
avg_delay = delivery_orders["delivery_delay_days"].mean()

st.markdown(f"""
<div class="kpi-grid">
    <div class="kpi-card kpi-cypress">
        <div class="kpi-label">On-time delivery rate</div>
        <div class="kpi-value">{on_time_rate:.1f}%</div>
        <div class="kpi-caption">{on_time_count:,} orders delivered on or before estimate</div>
    </div>
    <div class="kpi-card kpi-bamboo">
        <div class="kpi-label">Average delivery duration</div>
        <div class="kpi-value">{avg_duration:.1f} days</div>
        <div class="kpi-caption">Median duration: {median_duration:.1f} days from purchase</div>
    </div>
    <div class="kpi-card kpi-red">
        <div class="kpi-label">Late delivery count</div>
        <div class="kpi-value">{late_count:,}</div>
        <div class="kpi-caption">{late_rate:.1f}% of deliveries arrived past estimate</div>
    </div>
    <div class="kpi-card kpi-gold">
        <div class="kpi-label">Average days early / late</div>
        <div class="kpi-value">{avg_delay:+.1f} days</div>
        <div class="kpi-caption">Negative indicates delivered ahead of estimated date</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# Monthly Delivery Performance Trend
st.markdown("### Monthly Fulfillment Performance Trend")
delivery_orders["month"] = delivery_orders["order_purchase_timestamp"].dt.to_period("M").astype(str)

monthly_delivery = delivery_orders.groupby("month").agg(
    total_orders=("order_id", "count"),
    avg_duration=("delivery_duration_days", "mean"),
    late_orders=("is_late", "sum"),
).reset_index().sort_values("month")

monthly_delivery["on_time_rate"] = (1 - monthly_delivery["late_orders"] / monthly_delivery["total_orders"]) * 100
monthly_delivery = monthly_delivery[monthly_delivery["total_orders"] > 30]

col_trend1, col_trend2 = st.columns(2, gap="large")

with col_trend1:
    fig_ontime = px.line(
        monthly_delivery,
        x="month",
        y="on_time_rate",
        markers=True,
        title="Monthly On-Time Delivery Success Rate (%)",
        labels={"month": "Month", "on_time_rate": "On-Time Delivery Rate (%)"},
        color_discrete_sequence=[COLORS["cypress"]]
    )
    polish(fig_ontime, 360, legend=False)
    st.plotly_chart(fig_ontime, use_container_width=True)

with col_trend2:
    fig_dur = px.area(
        monthly_delivery,
        x="month",
        y="avg_duration",
        title="Average Delivery Duration over Time (Days)",
        labels={"month": "Month", "avg_duration": "Average Transit Days"},
        color_discrete_sequence=[COLORS["berry"]]
    )
    polish(fig_dur, 360, legend=False)
    st.plotly_chart(fig_dur, use_container_width=True)

st.markdown("---")

# Delivery Duration Distribution
st.markdown("### Delivery Duration Distribution")
col_hist, col_delay_bins = st.columns([1.2, 1], gap="large")

with col_hist:
    clean_durations = delivery_orders[delivery_orders["delivery_duration_days"].between(0, 50)]

    fig_hist = px.histogram(
        clean_durations,
        x="delivery_duration_days",
        nbins=40,
        title="Distribution of Order Delivery Duration (Days)",
        labels={"delivery_duration_days": "Delivery Duration (Days)"},
        color_discrete_sequence=[COLORS["cypress"]]
    )
    polish(fig_hist, 360, legend=False)
    st.plotly_chart(fig_hist, use_container_width=True)

with col_delay_bins:
    delivery_orders["delay_cat"] = pd.cut(
        delivery_orders["delivery_delay_days"],
        bins=[-999, -7, 0, 7, 999],
        labels=["7+ Days Early", "0-7 Days Early (On Time)", "1-7 Days Late", "7+ Days Late"]
    )
    cat_counts = delivery_orders["delay_cat"].value_counts().reset_index()
    cat_counts.columns = ["Fulfillment Status", "Orders"]

    fig_donut = px.pie(
        cat_counts,
        names="Fulfillment Status",
        values="Orders",
        hole=0.55,
        title="Orders Grouped by Estimate Adherence",
        color_discrete_sequence=[COLORS["cypress"], COLORS["bamboo"], COLORS["ylang"], COLORS["red"]]
    )
    fig_donut.update_traces(textposition="inside", textinfo="percent+label")
    polish(fig_donut, 360, legend=False)
    st.plotly_chart(fig_donut, use_container_width=True)

st.markdown("---")

# Regional Logistics Comparison
st.markdown("### Regional Logistics Comparison by Brazilian State")

if not state_delivery.empty:
    top_states_log = state_delivery.sort_values("orders_count", ascending=False).head(15).copy()

    col_state1, col_state2 = st.columns(2, gap="large")

    with col_state1:
        fig_st_speed = px.bar(
            top_states_log.sort_values("avg_delivery_days", ascending=True),
            x="avg_delivery_days",
            y="customer_state",
            orientation="h",
            text="avg_delivery_days",
            title="Fastest to Slowest Delivery States (Average Days)",
            labels={"avg_delivery_days": "Avg Transit Days", "customer_state": "State"},
            color="avg_delivery_days",
            color_continuous_scale=[COLORS["cypress"], COLORS["ylang"], COLORS["red"]]
        )
        fig_st_speed.update_traces(texttemplate="%{x:.1f} d", textposition="outside")
        fig_st_speed.update_layout(coloraxis_showscale=False)
        polish(fig_st_speed, 420, legend=False)
        st.plotly_chart(fig_st_speed, use_container_width=True)

    with col_state2:
        fig_st_late = px.bar(
            top_states_log.sort_values("late_rate", ascending=False),
            x="late_rate",
            y="customer_state",
            orientation="h",
            text="late_rate",
            title="Late Delivery Rate by State (%)",
            labels={"late_rate": "Late Rate (%)", "customer_state": "State"},
            color="late_rate",
            color_continuous_scale=[COLORS["cream"], COLORS["red"]]
        )
        fig_st_late.update_traces(texttemplate="%{x:.1f}%", textposition="outside")
        fig_st_late.update_layout(coloraxis_showscale=False)
        polish(fig_st_late, 420, legend=False)
        st.plotly_chart(fig_st_late, use_container_width=True)

    st.markdown("---")

    # Ranked State Logistics Table
    st.markdown("### Ranked State-Level Logistics Performance Table")
    state_table = state_delivery.sort_values("orders_count", ascending=False).copy()
    state_table["avg_delivery_days"] = state_table["avg_delivery_days"].map(lambda x: f"{x:.1f} days")
    state_table["median_delivery_days"] = state_table["median_delivery_days"].map(lambda x: f"{x:.1f} days")
    state_table["on_time_rate"] = state_table["on_time_rate"].map(lambda x: f"{x:.1f}%")
    state_table["late_rate"] = state_table["late_rate"].map(lambda x: f"{x:.1f}%")
    state_table["late_orders_count"] = state_table["late_orders_count"].map(lambda x: f"{int(x):,}")

    state_table.columns = [
        "State", "Total Shipments", "Average Transit Days", "Median Transit Days",
        "Late Orders Count", "Average Delay (Days)", "On-Time Rate (%)", "Late Delivery Rate (%)"
    ]

    st.dataframe(state_table, hide_index=True, use_container_width=True)

    csv_log = state_delivery.to_csv(index=False).encode("utf-8")
    st.download_button(
        "📥 Download State Logistics Performance CSV",
        data=csv_log,
        file_name="brazil_state_logistics_performance.csv",
        mime="text/csv"
    )

footer()
