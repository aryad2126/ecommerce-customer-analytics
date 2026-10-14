import pandas as pd
import plotly.express as px
import streamlit as st

from common import (
    COLORS, PALETTE, footer, get_data, money, page_header, polish, filter_bar,
    load_category_mart, DATA_DIR, BASE_DIR
)

orders, customers, segments, cluster_summary = get_data()

page_header(
    "FINANCIAL DYNAMICS",
    "Spending & Revenue Analytics",
    "Detailed evaluation of merchandise item revenues, freight charges, average order values, payment methods, and installments."
)

filtered, date_data, delivered, selected_status = filter_bar(orders)

# Core Financial Computations on Delivered Orders
delivered_orders_count = delivered["order_id"].nunique()
item_revenue = delivered["item_total"].sum()
freight_revenue = delivered["freight_total"].sum()
payment_sum = delivered["payment_total"].sum()

aov = (item_revenue / delivered_orders_count) if delivered_orders_count else 0
avg_freight = (freight_revenue / delivered_orders_count) if delivered_orders_count else 0
freight_ratio = (freight_revenue / item_revenue * 100) if item_revenue else 0

st.markdown(f"""
<div class="kpi-grid">
    <div class="kpi-card kpi-cypress">
        <div class="kpi-label">Delivered item revenue</div>
        <div class="kpi-value">{money(item_revenue)}</div>
        <div class="kpi-caption">Sum of item prices (excl. freight)</div>
    </div>
    <div class="kpi-card kpi-bamboo">
        <div class="kpi-label">Freight charges total</div>
        <div class="kpi-value">{money(freight_revenue)}</div>
        <div class="kpi-caption">Total shipping fees collected</div>
    </div>
    <div class="kpi-card kpi-gold">
        <div class="kpi-label">Average Order Value (AOV)</div>
        <div class="kpi-value">{money(aov)}</div>
        <div class="kpi-caption">Delivered item spend per order</div>
    </div>
    <div class="kpi-card kpi-secondary">
        <div class="kpi-label">Average freight per order</div>
        <div class="kpi-value">{money(avg_freight)}</div>
        <div class="kpi-caption">{freight_ratio:.1f}% freight-to-item ratio</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# Monthly Item Revenue & Freight Trends
st.markdown("### Monthly Revenue & Freight Trajectory")

timed_delivered = delivered.dropna(subset=["order_purchase_timestamp"]).copy()
timed_delivered["month"] = timed_delivered["order_purchase_timestamp"].dt.to_period("M").astype(str)

monthly_fin = timed_delivered.groupby("month").agg(
    item_revenue=("item_total", "sum"),
    freight_total=("freight_total", "sum"),
    payment_total=("payment_total", "sum"),
    order_count=("order_id", "nunique")
).reset_index().sort_values("month")

if not monthly_fin.empty:
    fig_fin = px.line(
        monthly_fin,
        x="month",
        y=["item_revenue", "freight_total"],
        markers=True,
        title="Monthly Item Merchandise Revenue vs. Freight Fees (R$)",
        labels={"value": "Amount (R$)", "month": "Month", "variable": "Stream"},
        color_discrete_map={
            "item_revenue": COLORS["berry"],
            "freight_total": COLORS["cypress"]
        }
    )
    fig_fin.for_each_trace(lambda t: t.update(name="Item Revenue" if t.name == "item_revenue" else "Freight Charges"))
    polish(fig_fin, 380, legend=True)
    st.plotly_chart(fig_fin, use_container_width=True)
else:
    st.info("No monthly financial data found for current filters.")

st.markdown("---")

# Payment Methods & Installments Breakdown
st.markdown("### Payment Methods & Installment Distribution")

@st.cache_data(show_spinner=False)
def load_payments_sample():
    raw_path = BASE_DIR / "data" / "raw" / "olist" / "olist_order_payments_dataset.csv"
    if raw_path.exists():
        return pd.read_csv(raw_path)
    return pd.DataFrame()

payments_df = load_payments_sample()

p_col1, p_col2 = st.columns(2, gap="large")

with p_col1:
    if not payments_df.empty:
        # Filter payments matching current delivered order IDs
        valid_orders = set(filtered["order_id"].unique())
        filtered_payments = payments_df[payments_df["order_id"].isin(valid_orders)]
        if filtered_payments.empty:
            filtered_payments = payments_df

        type_summary = filtered_payments.groupby("payment_type").agg(
            volume=("payment_value", "sum"),
            transactions=("payment_sequential", "count")
        ).reset_index().sort_values("volume", ascending=False)

        type_summary["payment_label"] = type_summary["payment_type"].str.replace("_", " ").str.title()

        fig_pm = px.pie(
            type_summary,
            names="payment_label",
            values="volume",
            hole=0.55,
            title="Payment Method Breakdown by Value",
            color_discrete_sequence=[COLORS["berry"], COLORS["cypress"], COLORS["bamboo"], COLORS["ylang"]]
        )
        fig_pm.update_traces(textposition="inside", textinfo="percent+label")
        polish(fig_pm, 360, legend=False)
        st.plotly_chart(fig_pm, use_container_width=True)
    else:
        st.info("Payment type data unavailable.")

with p_col2:
    if not payments_df.empty:
        # Installment count histogram / bar
        inst_counts = filtered_payments[filtered_payments["payment_installments"] > 0]["payment_installments"].value_counts().head(10).reset_index()
        inst_counts.columns = ["installments", "count"]
        inst_counts = inst_counts.sort_values("installments")

        fig_inst = px.bar(
            inst_counts,
            x="installments",
            y="count",
            text="count",
            title="Top Installment Options Selected by Buyers",
            labels={"installments": "Number of Installments", "count": "Transactions"},
            color_discrete_sequence=[COLORS["bamboo"]]
        )
        fig_inst.update_traces(textposition="outside")
        polish(fig_inst, 360, legend=False)
        st.plotly_chart(fig_inst, use_container_width=True)

st.markdown("---")

# Item Spending by Category
st.markdown("### Item Spending by Category")
cat_df = load_category_mart()

if not cat_df.empty:
    top_cat_spend = cat_df.head(10).sort_values("revenue", ascending=True)

    fig_cat = px.bar(
        top_cat_spend,
        x="revenue",
        y="category_english",
        orientation="h",
        text="revenue",
        title="Top 10 Merchandise Categories by Gross Item Revenue",
        labels={"revenue": "Item Revenue (R$)", "category_english": "Category"},
        color="revenue",
        color_continuous_scale=[COLORS["ylang"], COLORS["cypress"]]
    )
    fig_cat.update_traces(texttemplate="R$ %{x:,.0f}", textposition="outside")
    fig_cat.update_layout(coloraxis_showscale=False)
    polish(fig_cat, 400, legend=False)
    st.plotly_chart(fig_cat, use_container_width=True)

footer()
