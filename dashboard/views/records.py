import pandas as pd
import plotly.express as px
import streamlit as st

import uuid
from datetime import datetime

from common import (
    COLORS, PALETTE, footer, get_data, money, page_header, polish, filter_bar,
    save_user_order,
)

orders, customers, segments, cluster_summary = get_data()

page_header("RECORDS", "Order records", "Browse the order rows behind every chart.")

with st.expander("Add an order", expanded=False):
    with st.form("add_order", clear_on_submit=True):
        c1, c2 = st.columns(2)
        customer_id = c1.text_input("Customer ID")
        status = c2.selectbox(
            "Status", sorted(orders["order_status"].dropna().unique())
        )
        purchase_date = c1.date_input("Purchase date", datetime.now().date())
        purchase_time = c2.time_input(
            "Purchase time", datetime.now().time().replace(microsecond=0)
        )
        item_total = c1.number_input("Item total", min_value=0.0, step=0.01)
        freight_total = c2.number_input("Freight total", min_value=0.0, step=0.01)
        payment_total = c1.number_input("Payment total", min_value=0.0, step=0.01)
        submitted = st.form_submit_button("Save order")

    if submitted:
        if not customer_id.strip():
            st.error("Customer ID is required.")
        else:
            order_id = uuid.uuid4().hex
            save_user_order({
                "order_id": order_id,
                "customer_id": customer_id.strip(),
                "order_status": status,
                "order_purchase_timestamp": datetime.combine(
                    purchase_date, purchase_time
                ),
                "item_total": item_total,
                "freight_total": freight_total,
                "payment_total": payment_total,
            })
            st.toast(f"Order {order_id} saved.")
            st.rerun()

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
