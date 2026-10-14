import pandas as pd
import plotly.express as px
import streamlit as st

from common import COLORS, PALETTE, footer, get_data, money, page_header, polish

orders, customers, segments, cluster_summary = get_data()

page_header("GEOGRAPHY", "Customer geography", "Where customers are located and how much they spend.")


if "customer_state" in customers.columns:
    state_data = (
        customers.dropna(subset=["customer_state"])
        .groupby("customer_state")
        .agg(
            customers=("customer_unique_id", "nunique"),
            delivered_spend=("delivered_item_spend", "sum"),
        )
        .reset_index()
        .sort_values("customers", ascending=False)
        .head(12)
        .sort_values("customers", ascending=True)
    )

    fig = px.bar(
        state_data,
        x="customers",
        y="customer_state",
        orientation="h",
        text="customers",
        color="delivered_spend",
        color_continuous_scale=[COLORS["ylang"], COLORS["bamboo"], COLORS["cypress"]],
        title="Top customer states",
        labels={
            "customers": "Unique customers",
            "customer_state": "State",
            "delivered_spend": "Delivered item spend (R$)",
        },
    )
    fig.update_traces(texttemplate="%{text:,}", textposition="outside")
    polish(fig, 430, legend=False)
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Customer state data is unavailable.")

footer()
