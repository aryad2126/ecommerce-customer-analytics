from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# =========================================================
# CONFIGURATION
# =========================================================
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "processed"

st.set_page_config(
    page_title="E-Commerce Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Cohesive palette: teal, blue, violet, amber and coral
COLORS = {
    "teal": "#14B8A6",
    "blue": "#5B8DEF",
    "violet": "#9270E8",
    "amber": "#F5B544",
    "coral": "#F17C67",
    "green": "#36B37E",
    "muted": "#8492A6",
}
PALETTE = [
    COLORS["teal"],
    COLORS["blue"],
    COLORS["violet"],
    COLORS["amber"],
    COLORS["coral"],
    COLORS["green"],
]

# Use Streamlit's theme variables instead of forcing light/dark backgrounds.
st.markdown("""
<style>
    .block-container {
        padding-top: 1.7rem;
        padding-bottom: 2.5rem;
        max-width: 1600px;
    }

    .hero {
        padding: 1.35rem 1.55rem;
        border-radius: 18px;
        border: 1px solid var(--border-color);
        background: linear-gradient(
            120deg,
            var(--secondary-background-color),
            var(--background-color)
        );
        margin-bottom: 1.25rem;
    }

    .hero-kicker {
        color: #14B8A6;
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 0.14em;
        text-transform: uppercase;
        margin-bottom: 0.5rem;
    }

    .hero-title {
        color: var(--text-color);
        font-size: clamp(1.7rem, 3vw, 2.5rem);
        font-weight: 750;
        line-height: 1.15;
        margin: 0;
    }

    .hero-subtitle {
        color: var(--text-color);
        opacity: 0.72;
        margin-top: 0.65rem;
        font-size: 1rem;
    }

    [data-testid="stMetric"] {
        background: var(--secondary-background-color);
        border: 1px solid var(--border-color);
        padding: 1.05rem 1.1rem;
        border-radius: 15px;
        min-height: 125px;
    }

    [data-testid="stMetricLabel"] {
        color: var(--text-color);
        opacity: 0.78;
        font-size: 0.9rem;
    }

    [data-testid="stMetricValue"] {
        color: var(--text-color);
        font-size: clamp(1.3rem, 2vw, 1.9rem);
        font-weight: 720;
    }

    [data-testid="stMetricDelta"] {
        font-size: 0.8rem;
    }

    [data-testid="stPlotlyChart"] {
        border: 1px solid var(--border-color);
        border-radius: 14px;
        padding: 0.35rem;
    }

    div[data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 14px;
    }

    .section-note {
        color: var(--text-color);
        opacity: 0.7;
        font-size: 0.88rem;
    }

    div[data-testid="stExpander"] {
        border-radius: 12px;
    }


    /* Theme-aware visual upgrades */
    div[data-testid="stMetric"] {
        background: var(--secondary-background-color);
        border: 1px solid var(--border-color);
        border-top: 4px solid #14B8A6;
        border-radius: 14px;
        padding: 15px 16px;
        min-height: 112px;
        box-shadow: 0 3px 12px rgba(20, 184, 166, 0.08);
    }

    div[data-testid="stHorizontalBlock"] div[data-testid="stMetric"]:nth-child(4n+2) {
        border-top-color: #5B8DEF;
    }

    div[data-testid="stHorizontalBlock"] div[data-testid="stMetric"]:nth-child(4n+3) {
        border-top-color: #9270E8;
    }

    div[data-testid="stHorizontalBlock"] div[data-testid="stMetric"]:nth-child(4n+4) {
        border-top-color: #F5B544;
    }

    .segment-card {
        background: var(--secondary-background-color);
        border: 1px solid var(--border-color);
        border-left: 4px solid var(--segment-accent);
        border-radius: 14px;
        padding: 16px;
        margin: 6px 0 12px 0;
        min-height: 200px;
    }

    .segment-label {
        color: var(--text-color);
        font-size: 0.92rem;
        font-weight: 650;
        min-height: 42px;
    }

    .segment-count {
        color: var(--segment-accent);
        font-size: 1.8rem;
        line-height: 1.3;
        font-weight: 750;
        margin-top: 6px;
    }

    .segment-caption {
        color: var(--text-color);
        opacity: 0.7;
        font-size: 0.8rem;
        margin-bottom: 12px;
    }

    .segment-stat {
        display: flex;
        justify-content: space-between;
        gap: 8px;
        border-top: 1px solid var(--border-color);
        padding-top: 8px;
        margin-top: 8px;
        font-size: 0.8rem;
        color: var(--text-color);
    }


    /* KPI hierarchy and accent colors */
    div[data-testid="stVerticalBlock"]:has(.kpi-primary) .kpi-teal [data-testid="stMetric"] {
        border-top-color: #14B8A6;
        box-shadow: 0 4px 14px rgba(20, 184, 166, 0.12);
    }
    div[data-testid="stVerticalBlock"]:has(.kpi-primary) .kpi-green [data-testid="stMetric"] {
        border-top-color: #36B37E;
        box-shadow: 0 4px 14px rgba(54, 179, 126, 0.12);
    }
    div[data-testid="stVerticalBlock"]:has(.kpi-primary) .kpi-blue [data-testid="stMetric"] {
        border-top-color: #5B8DEF;
        box-shadow: 0 4px 14px rgba(91, 141, 239, 0.12);
    }
    div[data-testid="stVerticalBlock"]:has(.kpi-primary) .kpi-amber [data-testid="stMetric"] {
        border-top-color: #F5B544;
        box-shadow: 0 4px 14px rgba(245, 181, 68, 0.12);
    }
    .kpi-secondary [data-testid="stMetric"] {
        border-top-color: #94A3B8;
        box-shadow: none;
    }
    /* KPI card styling: consistent base, clear visual hierarchy */
    div[data-testid="stMetric"] {
        background: var(--secondary-background-color);
        border: 1px solid var(--border-color);
        border-top: 4px solid #94A3B8;
        border-radius: 14px;
        padding: 15px 16px;
        min-height: 112px;
        box-shadow: 0 3px 10px rgba(100, 116, 139, 0.06);
        transition: border-color 0.2s ease, transform 0.2s ease;
    }

    div[data-testid="stMetric"]:hover {
        transform: translateY(-2px);
    }

    div[data-testid="stMetricLabel"] p {
        font-weight: 600;
    }

    div[data-testid="stMetricValue"] {
        font-weight: 750;
        letter-spacing: -0.025em;
    }
    /* KPI cards: explicit colors on self-contained HTML cards */
    .kpi-grid {
        display: grid;
        grid-template-columns: repeat(4, minmax(0, 1fr));
        gap: 14px;
        margin: 8px 0 16px 0;
    }
    .kpi-card {
        background: var(--secondary-background-color);
        border: 1px solid var(--border-color);
        border-top: 4px solid #94A3B8;
        border-radius: 14px;
        padding: 17px 16px;
        min-height: 122px;
        box-sizing: border-box;
        transition: transform 0.2s ease;
    }
    .kpi-card:hover {
        transform: translateY(-2px);
    }
    .kpi-teal { border-top-color: #14B8A6; }
    .kpi-green { border-top-color: #36B37E; }
    .kpi-blue { border-top-color: #5B8DEF; }
    .kpi-amber { border-top-color: #F5B544; }
    .kpi-secondary { border-top-color: #94A3B8; }
    .kpi-label {
        color: var(--text-color);
        opacity: 0.82;
        font-size: 0.88rem;
        font-weight: 600;
        margin-bottom: 10px;
    }
    .kpi-value {
        color: var(--text-color);
        font-size: clamp(1.15rem, 1.7vw, 1.75rem);
        font-weight: 750;
        line-height: 1.3;
        overflow-wrap: anywhere;
    }
    .kpi-caption {
        color: var(--text-color);
        opacity: 0.65;
        font-size: 0.76rem;
        margin-top: 8px;
    }
    @media (max-width: 900px) {
        .kpi-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
    }
    @media (max-width: 480px) {
        .kpi-grid { grid-template-columns: 1fr; }
    }
    #MainMenu, footer {
        visibility: hidden;
    }
</style>
""", unsafe_allow_html=True)


# =========================================================
# DATA LOADING
# =========================================================
@st.cache_data(show_spinner="Loading processed analytics...")
def read_spark_csv(folder_string):
    folder = Path(folder_string)
    files = sorted(folder.glob("part-*.csv"))

    if not files:
        raise FileNotFoundError(
            f"No Spark CSV part files found in {folder}"
        )

    return pd.concat(
        [pd.read_csv(file) for file in files],
        ignore_index=True,
    )


@st.cache_data(show_spinner="Preparing dashboard...")
def load_data():
    orders = read_spark_csv(
        str(DATA_DIR / "cleaned" / "orders")
    )
    purchase = read_spark_csv(
        str(DATA_DIR / "cleaned" / "order_purchase_summary")
    )
    customers = read_spark_csv(
        str(DATA_DIR / "marts" / "customer_purchase")
    )
    segments = pd.read_csv(
        DATA_DIR / "segmentation" / "kmeans" / "customer_segments.csv"
    )
    cluster_summary = pd.read_csv(
        DATA_DIR / "segmentation" / "kmeans" / "cluster_summary.csv"
    )

    orders["order_purchase_timestamp"] = pd.to_datetime(
        orders["order_purchase_timestamp"], errors="coerce"
    )

    # Both tables are one row per order; do not join raw item and payment rows.
    data = orders.merge(
        purchase,
        on="order_id",
        how="left",
        validate="one_to_one",
    )

    for col in [
        "item_total", "freight_total", "payment_total",
        "item_count", "distinct_products",
    ]:
        if col in data.columns:
            data[col] = pd.to_numeric(data[col], errors="coerce")

    customers["delivered_item_spend"] = pd.to_numeric(
        customers["delivered_item_spend"], errors="coerce"
    )
    customers["delivered_payment_total"] = pd.to_numeric(
        customers["delivered_payment_total"], errors="coerce"
    )
    customers["delivered_order_count"] = pd.to_numeric(
        customers["delivered_order_count"], errors="coerce"
    )

    return data, customers, segments, cluster_summary


# =========================================================
# REUSABLE CHART FORMATTING
# =========================================================
def polish(fig, height=360, legend=True):
    fig.update_layout(
        template="streamlit",
        height=height,
        autosize=True,
        margin=dict(l=18, r=18, t=48, b=18),
        font=dict(family="Arial", size=12),
        title=dict(
            x=0.025,
            xanchor="left",
            font=dict(size=16),
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
        ) if legend else dict(visible=False),
        hoverlabel=dict(
            font_size=12,
        ),
    )
    fig.update_xaxes(showgrid=False, automargin=True)
    fig.update_yaxes(
        gridcolor="rgba(128, 145, 165, 0.18)",
        zeroline=False,
        automargin=True,
    )
    return fig


def money(value):
    if pd.isna(value):
        value = 0
    if abs(value) >= 1_000_000:
        return f"R$ {value / 1_000_000:.2f}M"
    if abs(value) >= 1_000:
        return f"R$ {value / 1_000:.1f}K"
    return f"R$ {value:,.2f}"


# =========================================================
# SIDEBAR
# =========================================================
st.sidebar.markdown("## 📊 E-Commerce")
st.sidebar.caption("CUSTOMER INTELLIGENCE")
st.sidebar.divider()

page = st.sidebar.radio(
    "WORKSPACE",
    ["Overview"],
    label_visibility="visible",
)

st.sidebar.divider()
st.sidebar.markdown("**Data source**")
st.sidebar.caption("Brazilian Olist public dataset")
st.sidebar.caption("Historical period: 2016–2018")
st.sidebar.markdown("---")
st.sidebar.caption(
    "Pipeline: Hadoop · PySpark · MongoDB · Cassandra"
)

try:
    orders, customers, segments, cluster_summary = load_data()
except Exception as exc:
    st.error(f"Dashboard data could not be loaded: {exc}")
    st.info(
        "Check that the preprocessing and segmentation scripts "
        "have completed and their output files are present."
    )
    st.stop()


# =========================================================
# HERO
# =========================================================
st.markdown("""
<div class="hero">
    <div class="hero-kicker">CUSTOMER & PURCHASE INTELLIGENCE</div>
    <div class="hero-title">E-Commerce Analytics</div>
    <div class="hero-subtitle">
        Understand order performance, spending patterns, and customer
        behaviour through one unified analytical view.
    </div>
</div>
""", unsafe_allow_html=True)


# =========================================================

# =========================================================
# =========================================================
# FILTERS
# =========================================================
valid_dates = orders["order_purchase_timestamp"].dropna()

if valid_dates.empty:
    st.error("No valid purchase timestamps were found.")
    st.stop()

min_date = valid_dates.min().date()
max_date = valid_dates.max().date()

with st.container(border=True):
    st.markdown("#### Refine your view")

    date_col, status_col, metric_col = st.columns([1.7, 1, 1])

    with date_col:
        date1, date2 = st.columns(2)
        with date1:
            start_date = st.date_input(
                "Start date",
                value=min_date,
                min_value=min_date,
                max_value=max_date,
                key="custom_start_date",
            )
        with date2:
            end_date = st.date_input(
                "End date",
                value=max_date,
                min_value=min_date,
                max_value=max_date,
                key="custom_end_date",
            )

    with status_col:
        statuses = ["All statuses"] + sorted(
            orders["order_status"].dropna().unique().tolist()
        )
        selected_status = st.selectbox("Order status", statuses)

    with metric_col:
        metric_choice = st.selectbox(
            "Trend metric",
            ["Order count", "Item spend", "Payment total"],
        )

if start_date > end_date:
    st.warning("Start date is after end date. The dates have been swapped.")
    start_date, end_date = end_date, start_date

start_ts = pd.Timestamp(start_date)
end_ts = pd.Timestamp(end_date) + pd.Timedelta(days=1)

date_mask = (
    orders["order_purchase_timestamp"].ge(start_ts)
    & orders["order_purchase_timestamp"].lt(end_ts)
)
date_data = orders.loc[date_mask].copy()

if selected_status == "All statuses":
    filtered = date_data.copy()
else:
    filtered = date_data[
        date_data["order_status"].eq(selected_status)
    ].copy()

delivered = filtered[
    filtered["order_status"].eq("delivered")
].copy()

st.caption(
    f"Showing purchase dates from {start_date} to {end_date}. "
    f"{len(filtered):,} orders match the current filters."
)

# KPI CARDS
# =========================================================
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

st.divider()


# =========================================================
# ORDER STATUS + MONTHLY TREND
# =========================================================
left, right = st.columns(2, gap="large")

with left:
    status_counts = (
        date_data.groupby("order_status")
        .agg(orders=("order_id", "nunique"))
        .reset_index()
        .sort_values("orders", ascending=True)
    )

    fig = px.bar(
        status_counts,
        x="orders",
        y="order_status",
        orientation="h",
        text="orders",
        color="order_status",
        color_discrete_sequence=PALETTE,
        title="Order status distribution",
        labels={"orders": "Orders", "order_status": ""},
    )
    fig.update_traces(
        texttemplate="%{text:,}",
        textposition="outside",
        cliponaxis=False,
    )
    fig.update_layout(showlegend=False)
    polish(fig, 380, legend=False)
    st.plotly_chart(fig, use_container_width=True)

with right:
    trend_data = filtered.dropna(
        subset=["order_purchase_timestamp"]
    ).copy()

    trend_data["month"] = (
        trend_data["order_purchase_timestamp"]
        .dt.to_period("M")
        .astype(str)
    )

    if metric_choice == "Order count":
        monthly = (
            trend_data.groupby("month")
            .agg(value=("order_id", "nunique"))
            .reset_index()
        )
        y_label = "Orders"
    elif metric_choice == "Item spend":
        monthly = (
            trend_data[trend_data["order_status"].eq("delivered")]
            .groupby("month")
            .agg(value=("item_total", "sum"))
            .reset_index()
        )
        y_label = "Item spend (R$)"
    else:
        monthly = (
            trend_data[trend_data["order_status"].eq("delivered")]
            .groupby("month")
            .agg(value=("payment_total", "sum"))
            .reset_index()
        )
        y_label = "Payment total (R$)"

    monthly = monthly.sort_values("month")

    if not monthly.empty:
        fig = px.area(
            monthly,
            x="month",
            y="value",
            title=f"Monthly trend · {metric_choice}",
            labels={"month": "Purchase month", "value": y_label},
        )
        fig.update_traces(
            line=dict(color=COLORS["teal"], width=2.8),
            fillcolor="rgba(20, 184, 166, 0.15)",
            hovertemplate="%{x}<br>%{y:,.0f}<extra></extra>",
        )
        polish(fig, 380, legend=False)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No monthly data matches the selected filters.")


# =========================================================
# SPENDING COMPARISON + ORDER TIMING
# =========================================================
st.divider()
st.markdown("### Spending & purchasing patterns")

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
            COLORS["teal"], COLORS["amber"], COLORS["violet"]
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
        color_continuous_scale=["#BDEFE7", COLORS["teal"]],
    )
    fig.update_layout(coloraxis_showscale=False)
    polish(fig, 360, legend=False)
    st.plotly_chart(fig, use_container_width=True)


# =========================================================

# =========================================================
# CUSTOMER SEGMENTS
# =========================================================
st.divider()
st.markdown("### Customer segmentation")
st.markdown(
    '<div class="section-note">RFM-based K-means groups across delivered '
    'purchases. Segment totals use the complete segmentation dataset.</div>',
    unsafe_allow_html=True,
)

segment_names = {
    0: "Mostly one-time purchasers",
    1: "Repeat purchasers",
}

segment_view = cluster_summary.copy()
segment_view["segment_name"] = segment_view["cluster"].map(
    segment_names
).fillna(segment_view["cluster"].astype(str))

left, right = st.columns([0.9, 1.3], gap="large")

with left:
    fig = px.pie(
        segment_view,
        names="segment_name",
        values="customer_count",
        hole=0.62,
        title="Customer share by segment",
        color_discrete_sequence=[COLORS["blue"], COLORS["teal"]],
    )
    fig.update_traces(textposition="inside", textinfo="percent")
    polish(fig, 350, legend=True)
    st.plotly_chart(fig, use_container_width=True)

with right:
    st.markdown("#### Segment snapshot")
    card_columns = st.columns(max(1, len(segment_view)))

    for index, (_, row) in enumerate(segment_view.iterrows()):
        with card_columns[index]:
            label = str(row["segment_name"])
            count = int(row["customer_count"])
            frequency = float(row["avg_frequency"])
            avg_monetary = float(row["avg_monetary"])
            accent = COLORS["blue"] if index % 2 == 0 else COLORS["teal"]

            st.markdown(
                f"""
                <div class="segment-card" style="--segment-accent:{accent}">
                    <div class="segment-label">{label}</div>
                    <div class="segment-count">{count:,}</div>
                    <div class="segment-caption">Customers</div>
                    <div class="segment-stat">
                        <span>Avg. orders</span><strong>{frequency:.2f}</strong>
                    </div>
                    <div class="segment-stat">
                        <span>Avg. item spend</span>
                        <strong>{money(avg_monetary)}</strong>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

st.caption(
    "RFM reference date: 30 August 2018. Segment labels describe the "
    "K-means output; they are not predefined customer classes."
)

# GEOGRAPHIC SNAPSHOT
# =========================================================
st.divider()
st.markdown("### Customer geography")

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
        color_continuous_scale=["#BDEFE7", COLORS["teal"], COLORS["blue"]],
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

# =========================================================
# DETAIL TABLE
# =========================================================
with st.expander("Explore filtered order records"):
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

st.divider()
st.markdown(
    '<div class="section-note">E-Commerce Customer Behavior & Purchase '
    'Analytics · Python · PySpark · Plotly · Streamlit</div>',
    unsafe_allow_html=True,
)
