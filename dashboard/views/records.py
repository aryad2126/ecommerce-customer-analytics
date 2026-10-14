import uuid
from datetime import datetime
import pandas as pd
import streamlit as st

from common import (
    COLORS, PALETTE, footer, get_data, money, page_header, polish, filter_bar,
    save_user_order
)

orders, customers, segments, cluster_summary = get_data()

page_header(
    "TRANSACTION AUDIT TRAIL",
    "Order Records & Data Management",
    "Search, inspect, and filter historical transaction records, or enter new orders into the database."
)

# Expandable Form for Adding a New Order
with st.expander("➕ Add an Order", expanded=False):
    with st.form("add_order_form", clear_on_submit=True):
        c1, c2 = st.columns(2)
        customer_id = c1.text_input("Customer ID*", placeholder="e.g. 06b8999e2fba1a1fbc88172c00ba8bc7")
        order_status = c2.selectbox(
            "Order Status*",
            ["delivered", "shipped", "processing", "invoiced", "canceled", "unavailable"]
        )
        purchase_date = c1.date_input("Purchase Date*", datetime.now().date())
        purchase_time = c2.time_input("Purchase Time*", datetime.now().time().replace(microsecond=0))
        item_total = c1.number_input("Item Merchandise Total (R$)*", min_value=0.0, step=0.01, format="%.2f")
        freight_total = c2.number_input("Freight Shipping Fee (R$)*", min_value=0.0, step=0.01, format="%.2f")
        payment_total = c1.number_input("Total Payment Settled (R$)*", min_value=0.0, step=0.01, format="%.2f")

        submitted = st.form_submit_button("💾 Save Order")

    if submitted:
        customer_id_clean = customer_id.strip()
        if not customer_id_clean:
            st.error("Validation Error: Customer ID is required.")
        elif len(customer_id_clean) < 4:
            st.error("Validation Error: Customer ID must be at least 4 characters.")
        elif payment_total < 0 or item_total < 0 or freight_total < 0:
            st.error("Validation Error: Amounts cannot be negative.")
        else:
            new_order_id = uuid.uuid4().hex
            combined_timestamp = datetime.combine(purchase_date, purchase_time)

            row_data = {
                "order_id": new_order_id,
                "customer_id": customer_id_clean,
                "order_status": order_status,
                "order_purchase_timestamp": combined_timestamp,
                "item_total": float(item_total),
                "freight_total": float(freight_total),
                "payment_total": float(payment_total),
                "source": "User Entry"
            }

            mongo_synced = save_user_order(row_data)

            st.success(f"✅ Order **{new_order_id}** saved successfully.")
            st.toast(f"Order {new_order_id[:8]}... added successfully!")
            st.rerun()

st.markdown("---")

filtered, date_data, delivered, selected_status = filter_bar(orders)

# Search & Controls Toolbar
st.markdown("### Search & Filter Order Records")
search_col, sort_col, limit_col = st.columns([2, 1.2, 1])

with search_col:
    search_query = st.text_input("🔍 Search by Order ID or Customer ID", placeholder="Paste Order ID or Customer ID...")

with sort_col:
    sort_by = st.selectbox(
        "Sort By",
        ["Purchase Date (Newest)", "Purchase Date (Oldest)", "Item Total (High to Low)", "Payment Total (High to Low)"]
    )

with limit_col:
    display_limit = st.selectbox("Max rows to display", [100, 250, 500, 1000], index=1)

# Apply Search
records_view = filtered.copy()

if search_query.strip():
    q = search_query.strip().lower()
    records_view = records_view[
        records_view["order_id"].astype(str).str.lower().str.contains(q, na=False) |
        records_view["customer_id"].astype(str).str.lower().str.contains(q, na=False)
    ]

# Apply Sorting
if sort_by == "Purchase Date (Newest)":
    records_view = records_view.sort_values("order_purchase_timestamp", ascending=False)
elif sort_by == "Purchase Date (Oldest)":
    records_view = records_view.sort_values("order_purchase_timestamp", ascending=True)
elif sort_by == "Item Total (High to Low)":
    records_view = records_view.sort_values("item_total", ascending=False)
elif sort_by == "Payment Total (High to Low)":
    records_view = records_view.sort_values("payment_total", ascending=False)

# Ensure source column exists
if "source" not in records_view.columns:
    records_view["source"] = "Historical Dataset"
records_view["source"] = records_view["source"].fillna("Historical Dataset")

show_columns = [
    "order_id",
    "customer_id",
    "order_status",
    "order_purchase_timestamp",
    "item_total",
    "freight_total",
    "payment_total",
    "source",
]
available_columns = [col for col in show_columns if col in records_view.columns]

# Display Summary
user_count = (records_view["source"] == "User Entry").sum()
hist_count = len(records_view) - user_count

st.markdown(f"""
<div style="display:flex; gap:16px; align-items:center; margin-bottom:8px; font-size:0.86rem;">
    <span>Showing <strong>{min(display_limit, len(records_view)):,}</strong> of <strong>{len(records_view):,}</strong> matching records</span>
    <span style="background:rgba(102,116,54,0.15); color:{COLORS['cypress']}; padding:3px 8px; border-radius:12px; font-weight:700;">Historical: {hist_count:,}</span>
    <span style="background:rgba(255,236,142,0.45); color:{COLORS['berry']}; padding:3px 8px; border-radius:12px; font-weight:700;">User Submitted: {user_count:,}</span>
</div>
""", unsafe_allow_html=True)

# Format for display table
display_df = records_view[available_columns].head(display_limit).copy()

st.dataframe(
    display_df,
    hide_index=True,
    use_container_width=True,
    column_config={
        "order_id": st.column_config.TextColumn("Order ID"),
        "customer_id": st.column_config.TextColumn("Customer ID"),
        "order_status": st.column_config.TextColumn("Status"),
        "order_purchase_timestamp": st.column_config.DatetimeColumn("Purchase Timestamp", format="YYYY-MM-DD HH:mm"),
        "item_total": st.column_config.NumberColumn("Item Total", format="R$ %.2f"),
        "freight_total": st.column_config.NumberColumn("Freight", format="R$ %.2f"),
        "payment_total": st.column_config.NumberColumn("Payment Total", format="R$ %.2f"),
        "source": st.column_config.TextColumn("Data Source")
    }
)

# Detailed Order Inspector
st.markdown("### Inspect Specific Order Details")
inspect_id = st.text_input("Enter Order ID to inspect full transaction record:", placeholder="Paste Order ID here...")

if inspect_id.strip():
    match = orders[orders["order_id"].astype(str).eq(inspect_id.strip())]
    if not match.empty:
        rec = match.iloc[0]
        st.success(f"Found record for Order `{rec['order_id']}`")
        detail_col1, detail_col2 = st.columns(2)
        with detail_col1:
            st.markdown(f"""
            - **Status:** `{rec.get('order_status', 'N/A')}`
            - **Customer ID:** `{rec.get('customer_id', 'N/A')}`
            - **Purchase Timestamp:** `{rec.get('order_purchase_timestamp', 'N/A')}`
            - **Approved Date:** `{rec.get('order_approved_at', 'N/A')}`
            """)
        with detail_col2:
            st.markdown(f"""
            - **Item Total:** `{money(rec.get('item_total', 0))}`
            - **Freight Total:** `{money(rec.get('freight_total', 0))}`
            - **Payment Total:** `{money(rec.get('payment_total', 0))}`
            - **Customer Delivered Date:** `{rec.get('order_delivered_customer_date', 'N/A')}`
            - **Estimated Delivery Date:** `{rec.get('order_estimated_delivery_date', 'N/A')}`
            """)
    else:
        st.warning(f"No order found matching ID `{inspect_id.strip()}`.")

# CSV Download
csv_filtered = records_view[available_columns].to_csv(index=False).encode("utf-8")
st.download_button(
    "📥 Download Filtered Order Records (CSV)",
    data=csv_filtered,
    file_name="filtered_ecommerce_orders.csv",
    mime="text/csv"
)

footer()
