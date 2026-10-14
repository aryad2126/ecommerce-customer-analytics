import pandas as pd
import plotly.express as px
import streamlit as st

from common import (
    COLORS, PALETTE, footer, get_data, money, page_header, polish,
    load_category_mart, load_top_products_mart
)

page_header(
    "MERCHANDISE & CATALOG INTELLIGENCE",
    "Products & Categories Analytics",
    "Multi-dimensional analysis of product catalog performance: category revenues, units sold, distinct product count, pricing distribution, and shipping intensity."
)

cat_summary = load_category_mart()
top_products_df = load_top_products_mart()

if cat_summary.empty:
    st.error("Category data mart is missing. Run `scripts/preprocess_extended_analytics.py` to generate it.")
    st.stop()

# Core Catalog KPIs
total_categories = len(cat_summary)
total_catalog_revenue = cat_summary["revenue"].sum()
total_units_sold = int(cat_summary["units_sold"].sum())
total_distinct_products = int(cat_summary["distinct_products"].sum())
avg_catalog_price = cat_summary["revenue"].sum() / cat_summary["units_sold"].sum()

st.markdown(f"""
<div class="kpi-grid">
    <div class="kpi-card kpi-cypress">
        <div class="kpi-label">Active product categories</div>
        <div class="kpi-value">{total_categories}</div>
        <div class="kpi-caption">Distinct catalog merchandise categories</div>
    </div>
    <div class="kpi-card kpi-bamboo">
        <div class="kpi-label">Total merchandise revenue</div>
        <div class="kpi-value">{money(total_catalog_revenue)}</div>
        <div class="kpi-caption">Delivered item gross merchandise volume</div>
    </div>
    <div class="kpi-card kpi-gold">
        <div class="kpi-label">Total units sold</div>
        <div class="kpi-value">{total_units_sold:,}</div>
        <div class="kpi-caption">{total_distinct_products:,} distinct catalog products</div>
    </div>
    <div class="kpi-card kpi-secondary">
        <div class="kpi-label">Average item price</div>
        <div class="kpi-value">{money(avg_catalog_price)}</div>
        <div class="kpi-caption">Catalog-wide average price per unit</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# Category Visual Tiles Showcase
st.markdown("### Top Merchandise Categories Showcase")
st.markdown("Leading merchandise categories ranked by delivered customer spending.")

CATEGORY_ICONS = {
    "Health Beauty": "💄",
    "Watches Gifts": "⌚",
    "Bed Bath Table": "🛏️",
    "Sports Leisure": "⚽",
    "Computers Accessories": "💻",
    "Furniture Decor": "🛋️",
    "Housewares": "🍳",
    "Auto": "🚗",
    "Toys": "🧸",
    "Garden Tools": "🌿",
    "Telephony": "📱",
    "Baby": "👶",
}

top_8_cats = cat_summary.head(8)
cols_row1 = st.columns(4)
cols_row2 = st.columns(4)

for i in range(4):
    row1 = top_8_cats.iloc[i]
    c_name1 = str(row1["category_english"])
    icon1 = CATEGORY_ICONS.get(c_name1, "🛍️")
    with cols_row1[i]:
        with st.container(border=True):
            st.markdown(f"### {icon1}")
            st.markdown(f"**{c_name1}**")
            st.markdown(f"<h3 style='color:{COLORS['berry']}; margin:4px 0 0 0;'>{money(row1['revenue'])}</h3>", unsafe_allow_html=True)
            st.caption(f"{int(row1['units_sold']):,} units · {money(row1['avg_item_price'])} avg")

for j in range(4, 8):
    row2 = top_8_cats.iloc[j]
    c_name2 = str(row2["category_english"])
    icon2 = CATEGORY_ICONS.get(c_name2, "🛍️")
    with cols_row2[j - 4]:
        with st.container(border=True):
            st.markdown(f"### {icon2}")
            st.markdown(f"**{c_name2}**")
            st.markdown(f"<h3 style='color:{COLORS['berry']}; margin:4px 0 0 0;'>{money(row2['revenue'])}</h3>", unsafe_allow_html=True)
            st.caption(f"{int(row2['units_sold']):,} units · {money(row2['avg_item_price'])} avg")

st.markdown("---")

# Analytics Section: Top Categories by Revenue vs Quantity
col_rev, col_units = st.columns(2, gap="large")

with col_rev:
    top_10_rev = cat_summary.head(10).sort_values("revenue", ascending=True)

    fig_rev = px.bar(
        top_10_rev,
        x="revenue",
        y="category_english",
        orientation="h",
        text="revenue",
        title="Top 10 Categories by Delivered Item Revenue",
        labels={"revenue": "Delivered Revenue (R$)", "category_english": "Category"},
        color="revenue",
        color_continuous_scale=[COLORS["ylang"], COLORS["cypress"]]
    )
    fig_rev.update_traces(texttemplate="R$ %{x:,.0f}", textposition="outside")
    fig_rev.update_layout(coloraxis_showscale=False)
    polish(fig_rev, 420, legend=False)
    st.plotly_chart(fig_rev, use_container_width=True)

with col_units:
    top_10_units = cat_summary.sort_values("units_sold", ascending=False).head(10).sort_values("units_sold", ascending=True)

    fig_units = px.bar(
        top_10_units,
        x="units_sold",
        y="category_english",
        orientation="h",
        text="units_sold",
        title="Top 10 Categories by Quantity Sold (Units)",
        labels={"units_sold": "Units Sold", "category_english": "Category"},
        color="units_sold",
        color_continuous_scale=[COLORS["cream"], COLORS["berry"]]
    )
    fig_units.update_traces(texttemplate="%{x:,}", textposition="outside")
    fig_units.update_layout(coloraxis_showscale=False)
    polish(fig_units, 420, legend=False)
    st.plotly_chart(fig_units, use_container_width=True)

st.markdown("---")

# Category Price vs Freight Relationship
st.markdown("### Category Pricing vs. Freight Charges")
st.markdown("Examining item prices relative to average freight fees across leading categories.")

scatter_df = cat_summary.head(25).copy()

fig_scatter = px.scatter(
    scatter_df,
    x="avg_item_price",
    y="avg_freight",
    size="units_sold",
    color="category_english",
    hover_name="category_english",
    title="Average Item Price vs. Average Freight Fee (Top 25 Categories)",
    labels={
        "avg_item_price": "Average Item Price (R$)",
        "avg_freight": "Average Freight Fee (R$)",
        "units_sold": "Units Sold"
    },
    color_discrete_sequence=px.colors.qualitative.Prism
)
polish(fig_scatter, 400, legend=False)
st.plotly_chart(fig_scatter, use_container_width=True)

st.markdown("---")

# Ranked Category Directory with Filter & Export
st.markdown("### Complete Product Category Directory")

col_search, col_filter = st.columns([2, 1])
with col_search:
    cat_search = st.text_input("🔍 Search category name:", placeholder="Type to search...")
with col_filter:
    sort_option = st.selectbox(
        "Sort Categories By",
        ["Revenue (High to Low)", "Units Sold (High to Low)", "Average Price (High to Low)", "Rating (High to Low)"]
    )

table_df = cat_summary.copy()

if cat_search.strip():
    table_df = table_df[table_df["category_english"].str.lower().str.contains(cat_search.strip().lower())]

if sort_option == "Revenue (High to Low)":
    table_df = table_df.sort_values("revenue", ascending=False)
elif sort_option == "Units Sold (High to Low)":
    table_df = table_df.sort_values("units_sold", ascending=False)
elif sort_option == "Average Price (High to Low)":
    table_df = table_df.sort_values("avg_item_price", ascending=False)
elif sort_option == "Rating (High to Low)":
    table_df = table_df.sort_values("avg_review_score", ascending=False)

table_formatted = table_df.copy()
table_formatted["revenue"] = table_formatted["revenue"].map(lambda x: f"R$ {x:,.2f}")
table_formatted["total_freight"] = table_formatted["total_freight"].map(lambda x: f"R$ {x:,.2f}")
table_formatted["avg_item_price"] = table_formatted["avg_item_price"].map(lambda x: f"R$ {x:,.2f}")
table_formatted["avg_freight"] = table_formatted["avg_freight"].map(lambda x: f"R$ {x:,.2f}")
table_formatted["avg_review_score"] = table_formatted["avg_review_score"].map(lambda x: f"★ {x:.2f}" if pd.notna(x) else "N/A")

table_formatted = table_formatted[[
    "category_english", "revenue", "units_sold", "orders_count",
    "distinct_products", "avg_item_price", "avg_freight", "avg_review_score"
]]
table_formatted.columns = [
    "Category Name", "Gross Revenue (R$)", "Units Sold", "Orders Fulfilled",
    "Distinct Products", "Avg Item Price", "Avg Shipping Fee", "Avg Review Rating"
]

st.dataframe(table_formatted, hide_index=True, use_container_width=True)

csv_cat = cat_summary.to_csv(index=False).encode("utf-8")
st.download_button(
    "📥 Download Complete Category Directory (CSV)",
    data=csv_cat,
    file_name="ecommerce_product_categories.csv",
    mime="text/csv"
)

footer()
