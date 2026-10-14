import pandas as pd
import plotly.express as px
import streamlit as st

from common import COLORS, PALETTE, footer, get_data, money, page_header, polish, filter_bar

orders, customers, segments, cluster_summary = get_data()

page_header("SPENDING", "Spending & purchasing patterns", "What delivered orders are worth and when customers buy.")

filtered, date_data, delivered, selected_status = filter_bar(orders)

left, right = st.columns(2, gap="large")

with left:
    spending = delivered[
        ["item_total", "freight_total", "payment_total"]
    ].sum(min_count=1).fillna(0)

    spending_df = pd.DataFrame({
        "Measure": ["Item spend", "Freight", "Payment total"],
        "Amount": [
            spending.get("item_total", 0),
            spending.get("freight_total", 0),
            spending.get("payment_total", 0),
        ],
    })

    fig = px.bar(
        spending_df,
        x="Measure",
        y="Amount",
        color="Measure",
        text="Amount",
        color_discrete_sequence=[
            COLORS["cypress"], COLORS["bamboo"], COLORS["berry"]
        ],
        title="Delivered order value breakdown",
        labels={"Amount": "Amount (R$)"},
    )
    fig.update_traces(
        texttemplate="R$ %{y:,.0f}",
        textposition="outside",
        cliponaxis=False,
    )
    fig.update_layout(showlegend=False)
    polish(fig, 360, legend=False)
    st.plotly_chart(fig, use_container_width=True)

with right:
    timed = filtered.dropna(
        subset=["order_purchase_timestamp"]
    ).copy()

    timed["weekday"] = (
        timed["order_purchase_timestamp"].dt.day_name()
    )
    weekday_order = [
        "Monday", "Tuesday", "Wednesday", "Thursday",
        "Friday", "Saturday", "Sunday",
    ]

    weekday = (
        timed.groupby("weekday")
        .agg(orders=("order_id", "nunique"))
        .reindex(weekday_order)
        .fillna(0)
        .reset_index()
    )

    fig = px.bar(
        weekday,
        x="weekday",
        y="orders",
        title="When do customers place orders?",
        labels={"weekday": "", "orders": "Orders"},
        color="orders",
        color_continuous_scale=[COLORS["ylang"], COLORS["cypress"]],
    )
    fig.update_layout(coloraxis_showscale=False)
    polish(fig, 360, legend=False)
    st.plotly_chart(fig, use_container_width=True)


footer()
