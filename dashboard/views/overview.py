import base64
from pathlib import Path
import pandas as pd
import plotly.express as px
import streamlit as st

from common import (
    COLORS, PALETTE, footer, get_data, money, polish, filter_bar,
    load_category_mart, load_delivery_mart
)

# 1. Base Paths & Asset Helpers
ASSETS_DIR = Path(__file__).resolve().parent.parent / "assets" / "images"

def get_svg_data_uri(filename):
    svg_path = ASSETS_DIR / filename
    if svg_path.exists():
        encoded = base64.b64encode(svg_path.read_bytes()).decode("utf-8")
        return f"data:image/svg+xml;base64,{encoded}"
    return ""

hero_img_uri = get_svg_data_uri("hero_ecommerce.svg")
card_sales_uri = get_svg_data_uri("card_sales_revenue.svg")
card_cust_uri = get_svg_data_uri("card_customer_intelligence.svg")
card_prod_uri = get_svg_data_uri("card_products_fulfillment.svg")

# 2. Load Core Data
orders, customers, segments, cluster_summary = get_data()
cat_df = load_category_mart()
delivery_orders_df, state_delivery_df = load_delivery_mart()

def safe_page_link(page_path, label, icon=None):
    try:
        st.page_link(page_path, label=label, icon=icon)
    except Exception:
        page_slug = Path(page_path).stem.replace("_", " ").title().replace(" ", "_")
        st.markdown(
            f'<a href="{page_slug}" style="color:var(--c-berry)!important; font-weight:700; text-decoration:none;" target="_self">{label}</a>',
            unsafe_allow_html=True
        )

# 3. Premium E-Commerce Hero Section
hero_html = f"""
<div class="landing-hero">
    <div style="display: flex; flex-direction: row; gap: 2.5rem; align-items: center; justify-content: space-between; flex-wrap: wrap;">
        <div style="flex: 1.35; min-width: 320px;">
            <div class="hero-eyebrow">E-COMMERCE INTELLIGENCE</div>
            <h1 class="hero-headline">Turn Every Order <span class="gold-highlight">Into Insight</span></h1>
            <p class="hero-copy">Understand customer behavior, discover top-performing products, track revenue, and improve the shopping experience through data-driven insights.</p>
        </div>
        <div style="flex: 1; min-width: 280px; max-width: 420px; text-align: center;">
            <img src="{hero_img_uri}" style="width: 100%; height: auto; max-height: 280px; object-fit: contain; filter: drop-shadow(0 14px 26px rgba(0,0,0,0.28));" alt="E-Commerce Intelligence Hero" />
        </div>
    </div>
</div>
"""
st.markdown(hero_html, unsafe_allow_html=True)

# 4. Explore Your Business (Category Showcase)
col_sc1, col_sc2, col_sc3 = st.columns(3, gap="medium")

with col_sc1:
    with st.container(border=True):
        if card_sales_uri:
            st.markdown(f'<div class="showcase-card-img"><img src="{card_sales_uri}" style="max-height: 125px; width: auto;" alt="Sales & Revenue" /></div>', unsafe_allow_html=True)
        st.markdown("#### Sales & Revenue")
        st.markdown('<p class="showcase-card-desc">Track sales velocity, payment installments, and monthly revenue trajectories across Brazilian regions.</p>', unsafe_allow_html=True)
        safe_page_link("views/spending.py", label="Explore Spending & Revenue →", icon=":material/trending_up:")

with col_sc2:
    with st.container(border=True):
        if card_cust_uri:
            st.markdown(f'<div class="showcase-card-img"><img src="{card_cust_uri}" style="max-height: 125px; width: auto;" alt="Customer Intelligence" /></div>', unsafe_allow_html=True)
        st.markdown("#### Customer Intelligence")
        st.markdown('<p class="showcase-card-desc">Analyze customer lifecycles, RFM segmentation clusters, behavioral loyalty, and buyer geography.</p>', unsafe_allow_html=True)
        safe_page_link("views/segments.py", label="Explore Customer Segments →", icon=":material/donut_small:")

with col_sc3:
    with st.container(border=True):
        if card_prod_uri:
            st.markdown(f'<div class="showcase-card-img"><img src="{card_prod_uri}" style="max-height: 125px; width: auto;" alt="Products & Fulfillment" /></div>', unsafe_allow_html=True)
        st.markdown("#### Products & Fulfillment")
        st.markdown('<p class="showcase-card-desc">Monitor catalog sales velocity, freight cost ratios, carrier lead times, and fulfillment SLAs.</p>', unsafe_allow_html=True)
        safe_page_link("views/products.py", label="Explore Products & Categories →", icon=":material/category:")

# 5. Performance at a Glance (Filters + Business Performance Anchor)
st.markdown('<div id="business-performance" style="scroll-margin-top: 24px;"></div>', unsafe_allow_html=True)
st.markdown("### Business Performance")
st.caption("Real-time operational KPIs and sales velocity computed across Brazilian e-commerce orders.")

# Date and Status Filters
filtered, date_data, delivered, selected_status = filter_bar(orders)

# Calculate Core Metrics from Real Data
total_orders = filtered["order_id"].nunique()
delivered_orders = delivered["order_id"].nunique()

filtered_ids = filtered[["order_id", "customer_id"]].drop_duplicates()
filtered_customers = filtered_ids["customer_id"].nunique()

item_spend = delivered["item_total"].sum()
payment_total = delivered["payment_total"].sum()
freight_total = delivered["freight_total"].sum()
avg_order_spend = item_spend / delivered_orders if delivered_orders else 0
delivery_share_val = (delivered_orders / total_orders * 100) if total_orders else 0
orders_with_totals = filtered["item_total"].notna().sum()

# Concise Data-Driven Business Insights
insights = []
if not date_data.empty and "order_purchase_timestamp" in date_data.columns:
    month_counts = date_data.dropna(subset=["order_purchase_timestamp"]).copy()
    month_counts["month"] = month_counts["order_purchase_timestamp"].dt.to_period("M").astype(str)
    month_grp = month_counts.groupby("month")["order_id"].nunique()
    if not month_grp.empty:
        peak_m = month_grp.idxmax()
        peak_v = month_grp.max()
        insights.append(f"**Peak Order Month:** **{peak_m}** with **{peak_v:,}** orders placed.")

if not cat_df.empty:
    top_c = cat_df.iloc[0]
    insights.append(f"**Leading Category:** **{top_c['category_english']}** leads with **{money(top_c['revenue'])}** revenue across **{int(top_c['units_sold']):,}** units sold.")

if "customer_state" in customers.columns:
    top_st = customers["customer_state"].value_counts().idxmax()
    st_custs = customers["customer_state"].value_counts().max()
    insights.append(f"**Primary Market:** State **{top_st}** has the highest buyer density (**{st_custs:,}** unique customers).")

if not delivery_orders_df.empty:
    on_time_pct = (delivery_orders_df["is_late"].eq(False).mean() * 100)
    avg_transit = delivery_orders_df["delivery_duration_days"].mean()
    insights.append(f"**Logistics Timeliness:** **{on_time_pct:.1f}%** on-time delivery rate with an average transit time of **{avg_transit:.1f} days**.")

# 8 KPI Cards
st.markdown(f"""
<div class="kpi-grid">
    <div class="kpi-card kpi-cypress">
        <div class="kpi-label">Orders in view</div>
        <div class="kpi-value">{total_orders:,}</div>
        <div class="kpi-caption">Orders matching current filters</div>
    </div>
    <div class="kpi-card kpi-bamboo">
        <div class="kpi-label">Delivered orders</div>
        <div class="kpi-value">{delivered_orders:,}</div>
        <div class="kpi-caption">Successfully delivered ({delivery_share_val:.1f}%)</div>
    </div>
    <div class="kpi-card kpi-gold">
        <div class="kpi-label">Customers in view</div>
        <div class="kpi-value">{filtered_customers:,}</div>
        <div class="kpi-caption">Unique buyers in active period</div>
    </div>
    <div class="kpi-card kpi-red">
        <div class="kpi-label">Delivered payment total</div>
        <div class="kpi-value">{money(payment_total)}</div>
        <div class="kpi-caption">Settled customer payments</div>
    </div>
    <div class="kpi-card kpi-secondary">
        <div class="kpi-label">Delivered item spend</div>
        <div class="kpi-value">{money(item_spend)}</div>
        <div class="kpi-caption">Net merchandise revenue (excl. freight)</div>
    </div>
    <div class="kpi-card kpi-secondary">
        <div class="kpi-label">Avg. item spend / order</div>
        <div class="kpi-value">{money(avg_order_spend)}</div>
        <div class="kpi-caption">Average basket value per order</div>
    </div>
    <div class="kpi-card kpi-secondary">
        <div class="kpi-label">Delivery share</div>
        <div class="kpi-value">{delivery_share_val:.1f}%</div>
        <div class="kpi-caption">Delivered out of all orders</div>
    </div>
    <div class="kpi-card kpi-secondary">
        <div class="kpi-label">Orders with item records</div>
        <div class="kpi-value">{orders_with_totals:,}</div>
        <div class="kpi-caption">Orders with itemized records</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown(
    '<div class="section-note">Item spend excludes freight charges. '
    'Payment totals reflect collected transactions and may include shipping charges.</div>',
    unsafe_allow_html=True,
)

st.markdown("---")

# 6. Monthly Order Trends & Order Status Distribution
col_trend, col_status = st.columns(2, gap="large")

with col_trend:
    trend_data = date_data.dropna(subset=["order_purchase_timestamp"]).copy()
    trend_data["month"] = trend_data["order_purchase_timestamp"].dt.to_period("M").astype(str)

    monthly_orders = trend_data.groupby("month").agg(
        orders=("order_id", "nunique")
    ).reset_index().sort_values("month")

    if not monthly_orders.empty:
        fig_trend = px.area(
            monthly_orders,
            x="month",
            y="orders",
            title="Monthly Order Volume Trajectory",
            labels={"month": "Purchase Month", "orders": "Orders Placed"},
        )
        fig_trend.update_traces(
            line=dict(color=COLORS["cypress"], width=3.0),
            fillcolor="rgba(102, 116, 54, 0.18)",
            hovertemplate="<b>%{x}</b><br>Orders: %{y:,}<extra></extra>",
        )
        polish(fig_trend, 360, legend=False)
        st.plotly_chart(fig_trend, use_container_width=True)
    else:
        st.info("No order trend data available for current date range.")

with col_status:
    status_counts = (
        date_data.groupby("order_status")
        .agg(orders=("order_id", "nunique"))
        .reset_index()
        .sort_values("orders", ascending=True)
    )

    fig_status = px.bar(
        status_counts,
        x="orders",
        y="order_status",
        orientation="h",
        text="orders",
        color="order_status",
        color_discrete_sequence=PALETTE,
        title="Order Status Distribution",
        labels={"orders": "Orders", "order_status": "Status"},
    )
    fig_status.update_traces(
        texttemplate="%{text:,}",
        textposition="outside",
        cliponaxis=False,
    )
    if not status_counts.empty:
        fig_status.update_xaxes(range=[0, status_counts["orders"].max() * 1.2])
    fig_status.update_layout(showlegend=False)
    polish(fig_status, 360, legend=False)
    st.plotly_chart(fig_status, use_container_width=True)

st.markdown("---")

# 7. Spending / Revenue Summary & Top-Category Preview
col_spending, col_cats = st.columns([1, 1.3], gap="large")

with col_spending:
    st.markdown("#### Delivered Order Value Breakdown")
    spend_df = pd.DataFrame({
        "Measure": ["Item Spend", "Freight Shipping", "Payment Total"],
        "Amount (R$)": [item_spend, freight_total, payment_total]
    })

    fig_spend = px.bar(
        spend_df,
        x="Measure",
        y="Amount (R$)",
        text="Amount (R$)",
        color="Measure",
        color_discrete_sequence=[COLORS["cypress"], COLORS["bamboo"], COLORS["berry"]],
        title="Revenue Breakdown (Delivered Orders)",
        labels={"Amount (R$)": "Amount (R$)"}
    )
    fig_spend.update_traces(texttemplate="R$ %{y:,.0f}", textposition="outside")
    fig_spend.update_layout(showlegend=False)
    polish(fig_spend, 340, legend=False)
    st.plotly_chart(fig_spend, use_container_width=True)

with col_cats:
    st.markdown("#### Top Merchandise Categories Preview")
    if not cat_df.empty:
        top_cats = cat_df.head(6)[["category_english", "revenue", "units_sold", "avg_item_price"]].copy()
        top_cats.columns = ["Category", "Delivered Revenue", "Units Sold", "Avg Unit Price"]
        top_cats["Delivered Revenue"] = top_cats["Delivered Revenue"].map(lambda x: f"R$ {x:,.2f}")
        top_cats["Units Sold"] = top_cats["Units Sold"].map(lambda x: f"{int(x):,}")
        top_cats["Avg Unit Price"] = top_cats["Avg Unit Price"].map(lambda x: f"R$ {x:,.2f}")

        st.dataframe(top_cats, hide_index=True, use_container_width=True)
        st.caption("Explore comprehensive catalog metrics in the **Products & Categories Analytics** page.")
    else:
        st.info("Product category summary is loading.")

# 8. Automated Business Insights (Positioned at bottom before footer)
if insights:
    st.markdown("---")
    with st.container(border=True):
        st.markdown("##### 💡 Automated Business Insights")
        for ins in insights:
            st.markdown(f"• {ins}")

footer()
