import pandas as pd
import plotly.express as px
import streamlit as st

from common import COLORS, PALETTE, footer, get_data, money, page_header, polish, filter_bar

orders, customers, segments, cluster_summary = get_data()

page_header("ORDERS", "Order performance", "Order status mix and monthly trends for the selected period.")

filtered, date_data, delivered, selected_status = filter_bar(orders)

metric_choice = st.selectbox(
    "Trend metric",
    ["Order count", "Item spend", "Payment total"],
)

left, right = st.columns(2, gap="large")

with left:
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
        title="Order status distribution",
        labels={"orders": "Orders", "order_status": ""},
    )
    fig.update_traces(
        texttemplate="%{text:,}",
        textposition="outside",
        cliponaxis=False,
    )
    fig.update_xaxes(range=[0, status_counts["orders"].max() * 1.18])
    fig.update_layout(showlegend=False)
    polish(fig, 380, legend=False)
    st.plotly_chart(fig, use_container_width=True)

with right:
    trend_data = date_data.dropna(
        subset=["order_purchase_timestamp"]
    ).copy()

    trend_data["month"] = (
        trend_data["order_purchase_timestamp"]
        .dt.to_period("M")
        .astype(str)
    )

    if metric_choice == "Order count":
        count_data = trend_data.copy()

        if selected_status != "All statuses":
            count_data = count_data[
                count_data["order_status"].eq(selected_status)
            ]

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
        fig = px.area(
            monthly,
            x="month",
            y="value",
            title=f"Monthly trend · {metric_choice}",
            labels={"month": "Purchase month", "value": y_label},
        )
        fig.update_traces(
            line=dict(color=COLORS["cypress"], width=2.8),
            fillcolor="rgba(102, 116, 54, 0.18)",
            hovertemplate="%{x}<br>%{y:,.0f}<extra></extra>",
        )
        polish(fig, 380, legend=False)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No monthly data matches the selected filters.")


footer()
