import pandas as pd
import plotly.express as px
import streamlit as st

from common import (
    COLORS, PALETTE, footer, get_data, money, page_header, polish, filter_bar
)

orders, customers, segments, cluster_summary = get_data()

page_header(
    "ORDER PERFORMANCE & LIFECYCLE",
    "Order Volume & Fulfillment Mix",
    "Comprehensive order volume dynamics, cancellation rates, hourly ordering behavior, and status distribution over time."
)

filtered, date_data, delivered, selected_status = filter_bar(orders)

# High-Level Order Metrics
total_orders_in_scope = filtered["order_id"].nunique()
delivered_count = filtered[filtered["order_status"].eq("delivered")]["order_id"].nunique()
cancelled_count = filtered[filtered["order_status"].eq("canceled")]["order_id"].nunique()
unavailable_count = filtered[filtered["order_status"].eq("unavailable")]["order_id"].nunique()

cancel_rate = (cancelled_count / total_orders_in_scope * 100) if total_orders_in_scope else 0
unavail_rate = (unavailable_count / total_orders_in_scope * 100) if total_orders_in_scope else 0
fulfillment_rate = (delivered_count / total_orders_in_scope * 100) if total_orders_in_scope else 0

st.markdown(f"""
<div class="kpi-grid">
    <div class="kpi-card kpi-cypress">
        <div class="kpi-label">Total orders placed</div>
        <div class="kpi-value">{total_orders_in_scope:,}</div>
        <div class="kpi-caption">Unique order IDs in selected period</div>
    </div>
    <div class="kpi-card kpi-bamboo">
        <div class="kpi-label">Fulfillment rate</div>
        <div class="kpi-value">{fulfillment_rate:.1f}%</div>
        <div class="kpi-caption">{delivered_count:,} orders successfully delivered</div>
    </div>
    <div class="kpi-card kpi-red">
        <div class="kpi-label">Cancellation rate</div>
        <div class="kpi-value">{cancel_rate:.2f}%</div>
        <div class="kpi-caption">{cancelled_count:,} orders explicitly canceled</div>
    </div>
    <div class="kpi-card kpi-secondary">
        <div class="kpi-label">Unavailable rate</div>
        <div class="kpi-value">{unavail_rate:.2f}%</div>
        <div class="kpi-caption">{unavailable_count:,} orders marked unavailable</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

metric_choice = st.selectbox(
    "Select trend metric to analyze",
    ["Order count", "Item spend", "Payment total"],
    help="Toggle between distinct volume or aggregate currency amounts."
)

c_left, c_right = st.columns(2, gap="large")

with c_left:
    status_counts = (
        date_data.groupby("order_status")
        .agg(orders=("order_id", "nunique"))
        .reset_index()
        .sort_values("orders", ascending=True)
    )

    fig = px.bar(
        status_counts,
        x="orders",
        y="order_status",
        orientation="h",
        text="orders",
        color="order_status",
        color_discrete_sequence=PALETTE,
        title="Order status mix (Selected date bounds)",
        labels={"orders": "Orders", "order_status": "Status"},
    )
    fig.update_traces(
        texttemplate="%{text:,}",
        textposition="outside",
        cliponaxis=False,
    )
    if not status_counts.empty:
        fig.update_xaxes(range=[0, status_counts["orders"].max() * 1.2])
    fig.update_layout(showlegend=False)
    polish(fig, 380, legend=False)
    st.plotly_chart(fig, use_container_width=True)

with c_right:
    trend_data = date_data.dropna(subset=["order_purchase_timestamp"]).copy()
    trend_data["month"] = trend_data["order_purchase_timestamp"].dt.to_period("M").astype(str)

    if metric_choice == "Order count":
        count_data = trend_data.copy()
        if selected_status != "All statuses":
            count_data = count_data[count_data["order_status"].eq(selected_status)]

        monthly = (
            count_data.groupby("month")
            .agg(value=("order_id", "nunique"))
            .reset_index()
        )
        y_label = "Orders"
    elif metric_choice == "Item spend":
        monthly = (
            trend_data[trend_data["order_status"].eq("delivered")]
            .groupby("month")
            .agg(value=("item_total", "sum"))
            .reset_index()
        )
        y_label = "Item spend (R$)"
    else:
        monthly = (
            trend_data[trend_data["order_status"].eq("delivered")]
            .groupby("month")
            .agg(value=("payment_total", "sum"))
            .reset_index()
        )
        y_label = "Payment total (R$)"

    monthly = monthly.sort_values("month")

    if not monthly.empty:
        # Calculate Month-over-Month (MoM) change %
        monthly["mom_pct"] = monthly["value"].pct_change() * 100

        fig = px.area(
            monthly,
            x="month",
            y="value",
            title=f"Monthly trajectory · {metric_choice}",
            labels={"month": "Purchase month", "value": y_label},
        )
        fig.update_traces(
            line=dict(color=COLORS["cypress"], width=3.0),
            fillcolor="rgba(102, 116, 54, 0.20)",
            hovertemplate="<b>%{x}</b><br>Value: %{y:,.2f}<extra></extra>",
        )
        polish(fig, 380, legend=False)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No monthly data matches the selected filters.")

st.markdown("---")

# Hourly & Day of Week Purchasing Patterns
st.markdown("### Customer Ordering Timing Patterns")
t_col1, t_col2 = st.columns(2, gap="large")

with t_col1:
    time_df = filtered.dropna(subset=["order_purchase_timestamp"]).copy()
    time_df["hour"] = time_df["order_purchase_timestamp"].dt.hour
    hourly_counts = time_df.groupby("hour")["order_id"].nunique().reindex(range(24), fill_value=0).reset_index()

    fig_hour = px.bar(
        hourly_counts,
        x="hour",
        y="order_id",
        title="Orders by Hour of Day (24-Hour Cycle)",
        labels={"hour": "Hour of Day (00:00 to 23:00)", "order_id": "Orders Placed"},
        color_discrete_sequence=[COLORS["berry"]]
    )
    polish(fig_hour, 360, legend=False)
    st.plotly_chart(fig_hour, use_container_width=True)

with t_col2:
    time_df["day_name"] = time_df["order_purchase_timestamp"].dt.day_name()
    day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    day_counts = time_df.groupby("day_name")["order_id"].nunique().reindex(day_order, fill_value=0).reset_index()

    fig_day = px.bar(
        day_counts,
        x="day_name",
        y="order_id",
        title="Orders by Day of Week",
        labels={"day_name": "Day of Week", "order_id": "Orders Placed"},
        color="order_id",
        color_continuous_scale=[COLORS["cream"], COLORS["cypress"]]
    )
    fig_day.update_layout(coloraxis_showscale=False)
    polish(fig_day, 360, legend=False)
    st.plotly_chart(fig_day, use_container_width=True)

footer()
