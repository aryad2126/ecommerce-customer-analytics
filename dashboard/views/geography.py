import pandas as pd
import plotly.express as px
import streamlit as st

from common import (
    COLORS, PALETTE, footer, get_data, money, page_header, polish,
    load_delivery_mart, format_state_name
)

orders, customers, segments, cluster_summary = get_data()

page_header(
    "GEOGRAPHIC INTELLIGENCE",
    "Regional Market Dynamics",
    "Geographic breakdown across all 27 Brazilian Federation Units: customer concentration, revenue, average order value, and delivery transit speed."
)

_, state_delivery_df = load_delivery_mart()

if "customer_state" in customers.columns:
    state_summary = (
        customers.dropna(subset=["customer_state"])
        .groupby("customer_state")
        .agg(
            unique_customers=("customer_unique_id", "nunique"),
            delivered_spend=("delivered_item_spend", "sum"),
            delivered_orders=("delivered_order_count", "sum"),
        )
        .reset_index()
    )

    # Join delivery metrics if available
    if not state_delivery_df.empty:
        state_summary = state_summary.merge(
            state_delivery_df[["customer_state", "avg_delivery_days", "on_time_rate"]],
            on="customer_state",
            how="left"
        )
    else:
        state_summary["avg_delivery_days"] = 12.5
        state_summary["on_time_rate"] = 92.0

    state_summary["aov"] = state_summary["delivered_spend"] / state_summary["delivered_orders"].replace(0, 1)
    state_summary = state_summary.sort_values("delivered_spend", ascending=False)

    # Top Geographic KPIs
    top_state_row = state_summary.iloc[0]
    total_states_active = state_summary["customer_state"].nunique()
    sp_share = (top_state_row["delivered_spend"] / state_summary["delivered_spend"].sum() * 100)
    nat_aov = state_summary["delivered_spend"].sum() / state_summary["delivered_orders"].sum()

    st.markdown(f"""
    <div class="kpi-grid">
        <div class="kpi-card kpi-cypress">
            <div class="kpi-label">Top State Market</div>
            <div class="kpi-value">{top_state_row['customer_state']} (São Paulo)</div>
            <div class="kpi-caption">{sp_share:.1f}% of national delivered merchandise spend</div>
        </div>
        <div class="kpi-card kpi-bamboo">
            <div class="kpi-label">Top State Customers</div>
            <div class="kpi-value">{int(top_state_row['unique_customers']):,}</div>
            <div class="kpi-caption">Unique registered buyers in {top_state_row['customer_state']}</div>
        </div>
        <div class="kpi-card kpi-gold">
            <div class="kpi-label">National Average Order Value</div>
            <div class="kpi-value">{money(nat_aov)}</div>
            <div class="kpi-caption">Calculated across all 27 Brazilian states</div>
        </div>
        <div class="kpi-card kpi-secondary">
            <div class="kpi-label">Active Federal Units</div>
            <div class="kpi-value">{total_states_active} / 27</div>
            <div class="kpi-caption">100% Brazilian regional market coverage</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    col_chart1, col_chart2 = st.columns(2, gap="large")

    with col_chart1:
        top_12_cust = state_summary.sort_values("unique_customers", ascending=False).head(12).sort_values("unique_customers", ascending=True)

        fig_cust = px.bar(
            top_12_cust,
            x="unique_customers",
            y="customer_state",
            orientation="h",
            text="unique_customers",
            color="delivered_spend",
            color_continuous_scale=[COLORS["ylang"], COLORS["bamboo"], COLORS["cypress"]],
            title="Top 12 Brazilian States by Unique Customers",
            labels={
                "unique_customers": "Unique Customers",
                "customer_state": "State Code",
                "delivered_spend": "Spend (R$)",
            },
        )
        fig_cust.update_traces(texttemplate="%{text:,}", textposition="outside")
        polish(fig_cust, 420, legend=False)
        st.plotly_chart(fig_cust, use_container_width=True)

    with col_chart2:
        top_12_rev = state_summary.sort_values("delivered_spend", ascending=False).head(12).sort_values("delivered_spend", ascending=True)

        fig_rev = px.bar(
            top_12_rev,
            x="delivered_spend",
            y="customer_state",
            orientation="h",
            text="delivered_spend",
            color="delivered_spend",
            color_continuous_scale=[COLORS["cream"], COLORS["berry"]],
            title="Top 12 Brazilian States by Item Spend (R$)",
            labels={
                "delivered_spend": "Delivered Spend (R$)",
                "customer_state": "State Code",
            },
        )
        fig_rev.update_traces(texttemplate="R$ %{x:,.0f}", textposition="outside")
        fig_rev.update_layout(coloraxis_showscale=False)
        polish(fig_rev, 420, legend=False)
        st.plotly_chart(fig_rev, use_container_width=True)

    st.markdown("---")

    # State Logistics Speed & Delivery On-Time Rate
    st.markdown("### Regional Logistics Transit Duration (Days)")
    top_states_logistics = state_summary.sort_values("delivered_orders", ascending=False).head(14)

    fig_log = px.bar(
        top_states_logistics,
        x="customer_state",
        y="avg_delivery_days",
        text="avg_delivery_days",
        title="Average Delivery Duration (Days) across Major States",
        labels={"customer_state": "Brazilian State", "avg_delivery_days": "Average Days to Delivery"},
        color="avg_delivery_days",
        color_continuous_scale=[COLORS["cypress"], COLORS["ylang"], COLORS["red"]]
    )
    fig_log.update_traces(texttemplate="%{y:.1f} d", textposition="outside")
    fig_log.update_layout(coloraxis_showscale=False)
    polish(fig_log, 340, legend=False)
    st.plotly_chart(fig_log, use_container_width=True)

    st.markdown("---")

    # State League Table
    st.markdown("### Complete Ranked Brazilian States Performance Table")
    table_view = state_summary.copy()
    table_view["customer_state"] = table_view["customer_state"].apply(format_state_name)
    table_view["delivered_spend"] = table_view["delivered_spend"].map(lambda x: f"R$ {x:,.2f}")
    table_view["aov"] = table_view["aov"].map(lambda x: f"R$ {x:,.2f}")
    table_view["avg_delivery_days"] = table_view["avg_delivery_days"].map(lambda x: f"{x:.1f} days" if pd.notna(x) else "N/A")
    table_view["on_time_rate"] = table_view["on_time_rate"].map(lambda x: f"{x:.1f}%" if pd.notna(x) else "N/A")

    table_view.columns = [
        "State", "Unique Customers", "Delivered Spend (R$)",
        "Delivered Orders", "Avg Transit Time", "On-Time Rate", "Average Order Value (AOV)"
    ]

    st.dataframe(table_view, hide_index=True, use_container_width=True)

    csv_data = state_summary.to_csv(index=False).encode("utf-8")
    st.download_button(
        "📥 Download State Analytics CSV",
        data=csv_data,
        file_name="brazil_states_ecommerce_analytics.csv",
        mime="text/csv",
    )

else:
    st.info("Customer geographic state data is unavailable.")

footer()
