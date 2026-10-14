import pandas as pd
import plotly.express as px
import streamlit as st

from common import COLORS, PALETTE, footer, get_data, money, page_header, polish, filter_bar

orders, customers, segments, cluster_summary = get_data()

page_header("CUSTOMER & PURCHASE INTELLIGENCE", "E-Commerce Analytics", "Understand order performance, spending patterns, and customer behaviour through one unified analytical view.")

filtered, date_data, delivered, selected_status = filter_bar(orders)

total_orders = filtered["order_id"].nunique()
delivered_orders = delivered["order_id"].nunique()

# Customers in the customer mart are distinct across the complete dataset.
# For a date/status-filtered view, count distinct customer IDs from orders.
customer_ids = orders[
    ["order_id", "customer_id"]
].drop_duplicates()
filtered_ids = filtered[["order_id", "customer_id"]].drop_duplicates()
filtered_customers = filtered_ids["customer_id"].nunique()

item_spend = delivered["item_total"].sum()
payment_total = delivered["payment_total"].sum()
avg_order_spend = item_spend / delivered_orders if delivered_orders else 0

st.markdown("### Performance at a glance")

delivery_share = (
    f"{delivered_orders / total_orders * 100:.1f}%"
    if total_orders else "0.0%"
)
orders_with_totals = f"{filtered['item_total'].notna().sum():,}"

st.markdown(f"""
<div class="kpi-grid">
    <div class="kpi-card kpi-teal">
        <div class="kpi-label">Orders in view</div>
        <div class="kpi-value">{total_orders:,}</div>
        <div class="kpi-caption">Orders matching current filters</div>
    </div>
    <div class="kpi-card kpi-green">
        <div class="kpi-label">Delivered orders</div>
        <div class="kpi-value">{delivered_orders:,}</div>
        <div class="kpi-caption">Successfully delivered</div>
    </div>
    <div class="kpi-card kpi-blue">
        <div class="kpi-label">Customers in view</div>
        <div class="kpi-value">{filtered_customers:,}</div>
        <div class="kpi-caption">Distinct customers</div>
    </div>
    <div class="kpi-card kpi-amber">
        <div class="kpi-label">Delivered payment total</div>
        <div class="kpi-value">{money(payment_total)}</div>
        <div class="kpi-caption">Payments for delivered orders</div>
    </div>
    <div class="kpi-card kpi-secondary">
        <div class="kpi-label">Delivered item spend</div>
        <div class="kpi-value">{money(item_spend)}</div>
        <div class="kpi-caption">Excludes freight</div>
    </div>
    <div class="kpi-card kpi-secondary">
        <div class="kpi-label">Avg. item spend / order</div>
        <div class="kpi-value">{money(avg_order_spend)}</div>
        <div class="kpi-caption">Per delivered order</div>
    </div>
    <div class="kpi-card kpi-secondary">
        <div class="kpi-label">Delivery share</div>
        <div class="kpi-value">{delivery_share}</div>
        <div class="kpi-caption">Delivered / all orders in view</div>
    </div>
    <div class="kpi-card kpi-secondary">
        <div class="kpi-label">Orders with item totals</div>
        <div class="kpi-value">{orders_with_totals}</div>
        <div class="kpi-caption">Orders with recorded item totals</div>
    </div>
</div>
""", unsafe_allow_html=True)
st.markdown(
    '<div class="section-note">Item spend excludes freight. '
    'Payment totals are shown separately and may include freight or '
    'other order charges. These are transaction values, not profit.</div>',
    unsafe_allow_html=True,
)

footer()
