import pandas as pd
import plotly.express as px
import streamlit as st

from common import COLORS, PALETTE, footer, get_data, money, page_header, polish, filter_bar

orders, customers, segments, cluster_summary = get_data()

page_header("RECORDS", "Order records", "Browse the order rows behind every chart.")

filtered, date_data, delivered, selected_status = filter_bar(orders)

show_columns = [
    "order_id",
    "order_status",
    "order_purchase_timestamp",
    "item_total",
    "freight_total",
    "payment_total",
]
available_columns = [
    col for col in show_columns if col in filtered.columns
]

st.dataframe(
    filtered[available_columns].head(500),
    hide_index=True,
    use_container_width=True,
)
st.caption(
    f"Showing up to 500 of {len(filtered):,} filtered orders."
)

footer()
