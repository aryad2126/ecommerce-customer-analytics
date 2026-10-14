from pathlib import Path

import pandas as pd
import streamlit as st

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "processed"

# Palette: Ylang Ylang #FFEC8E, Bamboo #C6C954, Cypress #667436,
# Chrysanthemum #D9282D, Wild Berry #621E3E
COLORS = {
    "berry": "#621E3E",
    "cypress": "#667436",
    "bamboo": "#C6C954",
    "red": "#D9282D",
    "ylang": "#FFEC8E",
    "muted": "#9C7A8B",
}
PALETTE = [
    COLORS["cypress"],
    COLORS["berry"],
    COLORS["bamboo"],
    COLORS["red"],
    COLORS["ylang"],
    COLORS["muted"],
]

CSS = """
<style>
    :root {
        --c-ylang: #FFEC8E;
        --c-bamboo: #C6C954;
        --c-cypress: #667436;
        --c-red: #D9282D;
        --c-berry: #621E3E;
        --c-page: #FFFDF0;
        --c-card: #FFFFFF;
        --c-line: rgba(98, 30, 62, 0.16);
        --rail-w: 4.6rem;
        --rail-w-open: 15rem;
    }

    html { scroll-behavior: smooth; }
    .stApp { background: var(--c-page); }

    /* keep the header so the sidebar expand/collapse toggle stays reachable */
    header[data-testid="stHeader"] { background: transparent; }
    [data-testid="stToolbar"], [data-testid="stDecoration"] { display: none; }
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2.5rem;
        padding-left: 2.5rem;
        padding-right: 2.5rem;
        max-width: 1600px;
    }

    h1, h2, h3, h4, h5, p, label, span, li { color: var(--c-berry); }

    /* ---------- SIDE NAV (st.navigation in the sidebar) ---------- */
    /* always visible: no collapse control, and override any saved collapsed state */
    [data-testid="stSidebarCollapseButton"],
    [data-testid="stExpandSidebarButton"],
    [data-testid="stSidebarCollapsedControl"] { display: none !important; }
    section[data-testid="stSidebar"],
    section[data-testid="stSidebar"][aria-expanded="false"] {
        transform: none !important;
        margin-left: 0 !important;
        visibility: visible !important;
    }
    section[data-testid="stSidebar"] {
        width: 15.5rem !important;
        min-width: 15.5rem !important;
        background: linear-gradient(180deg, #7A2A4E 0%, var(--c-berry) 38%, #1C0A13 100%);
        border-right: 1px solid rgba(255, 236, 142, 0.25);
        border-radius: 0 32px 32px 0;
        box-shadow: 8px 0 30px rgba(98, 30, 62, 0.25);
    }
    section[data-testid="stSidebar"] > div,
    section[data-testid="stSidebar"] [data-testid="stSidebarContent"] {
        background: transparent;
    }
    section[data-testid="stSidebar"] [data-testid="stSidebarUserContent"] {
        padding: 0 1rem 1rem 1.4rem;
    }

    [data-testid="stSidebarNav"] { padding: 0.5rem 0 0.5rem 0.9rem; }
    [data-testid="stSidebarNav"]::before {
        content: "E-Commerce\\A Intelligence";
        white-space: pre;
        display: block;
        margin: 0.4rem 0 1.4rem 0.5rem;
        color: var(--c-ylang);
        font-size: 1.15rem;
        font-weight: 800;
        line-height: 1.25;
        letter-spacing: 0.01em;
    }
    [data-testid="stSidebarNav"] ul { padding: 0; gap: 0.45rem; }

    [data-testid="stSidebarNavLink"] {
        height: 2.9rem;
        padding: 0 0.9rem;
        border-radius: 16px 0 0 16px;
        background: rgba(255, 255, 255, 0.10);
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-right: none;
        transition: background 0.15s ease;
    }
    [data-testid="stSidebarNavLink"],
    [data-testid="stSidebarNavLink"] span,
    [data-testid="stSidebarNavLink"] p {
        color: var(--c-ylang) !important;
        font-weight: 650;
        font-size: 0.95rem;
    }
    [data-testid="stSidebarNavLink"]:hover { background: rgba(255, 255, 255, 0.18); }

    /* active tab: merges into the page */
    [data-testid="stSidebarNavLink"][aria-current="page"] {
        background: var(--c-page);
        border-color: var(--c-page);
        box-shadow: none;
    }
    [data-testid="stSidebarNavLink"][aria-current="page"],
    [data-testid="stSidebarNavLink"][aria-current="page"] span,
    [data-testid="stSidebarNavLink"][aria-current="page"] p {
        color: var(--c-berry) !important;
        font-weight: 800;
    }

    section[data-testid="stSidebar"] .sn-foot {
        color: var(--c-bamboo);
        font-size: 0.7rem;
        font-weight: 700;
        letter-spacing: 0.1em;
        margin-top: 1rem;
    }
    section[data-testid="stSidebar"] button { color: var(--c-ylang); }

    .mongo-badge {
        display: flex;
        align-items: center;
        gap: 0.7rem;
        margin-top: 0.6rem;
        padding: 0.65rem 0.8rem;
        border-radius: 14px;
        background: rgba(255, 255, 255, 0.10);
        border: 1px solid rgba(255, 255, 255, 0.14);
    }
    .mongo-dot {
        flex: none;
        width: 0.7rem; height: 0.7rem;
        border-radius: 50%;
        background: var(--c-bamboo);
        box-shadow: 0 0 0 3px rgba(198, 201, 84, 0.25), 0 0 10px var(--c-bamboo);
    }
    .mongo-empty .mongo-dot {
        background: var(--c-ylang);
        box-shadow: 0 0 0 3px rgba(255, 236, 142, 0.25), 0 0 10px var(--c-ylang);
    }
    .mongo-down .mongo-dot {
        background: var(--c-red);
        box-shadow: 0 0 0 3px rgba(217, 40, 45, 0.3), 0 0 10px var(--c-red);
    }
    .mongo-badge { box-sizing: border-box; max-width: 100%; overflow: hidden; }
    .mongo-badge > div:last-child { min-width: 0; flex: 1 1 auto; }
    .mongo-label { color: var(--c-ylang); font-size: 0.82rem; font-weight: 700; overflow-wrap: anywhere; }
    .mongo-detail {
        color: #E9D3DD;
        font-size: 0.68rem;
        margin-top: 2px;
        line-height: 1.35;
        overflow-wrap: anywhere;
        word-break: break-word;
    }

    /* ---------- HERO ---------- */
    .hero {
        padding: 1.5rem 1.7rem;
        border-radius: 22px;
        background: linear-gradient(120deg, var(--c-berry), #8A2C58);
        border-bottom: 5px solid var(--c-ylang);
        margin-bottom: 1.25rem;
        box-shadow: 0 8px 24px rgba(98, 30, 62, 0.22);
    }
    .hero-kicker {
        color: var(--c-bamboo);
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 0.14em;
        text-transform: uppercase;
        margin-bottom: 0.5rem;
    }
    .hero-title {
        color: var(--c-ylang);
        font-size: clamp(1.7rem, 3vw, 2.5rem);
        font-weight: 750;
        line-height: 1.15;
        margin: 0;
    }
    .hero-subtitle {
        color: #F6E7EE;
        margin-top: 0.65rem;
        font-size: 1rem;
    }

    /* ---------- CARDS / CONTAINERS ---------- */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 16px;
        border-color: var(--c-line);
        background: var(--c-card);
    }
    [data-testid="stPlotlyChart"] {
        background: var(--c-card);
        border: 1px solid var(--c-line);
        border-radius: 16px;
        padding: 0.35rem;
    }
    div[data-testid="stExpander"] {
        border-radius: 14px;
        border-color: var(--c-line);
        background: var(--c-card);
    }
    hr { border-color: var(--c-line) !important; }

    .section-note {
        color: var(--c-berry);
        opacity: 0.75;
        font-size: 0.88rem;
    }

    div[data-baseweb="select"] > div,
    div[data-baseweb="input"],
    div[data-testid="stDateInput"] > div > div {
        background: rgba(255, 236, 142, 0.35) !important;
        border-color: var(--c-line) !important;
        color: var(--c-berry) !important;
    }

    /* ---------- KPI CARDS ---------- */
    .kpi-grid {
        display: grid;
        grid-template-columns: repeat(4, minmax(0, 1fr));
        gap: 14px;
        margin: 8px 0 16px 0;
    }
    .kpi-card {
        background: var(--c-card);
        border: 1px solid var(--c-line);
        border-top: 5px solid var(--c-berry);
        border-radius: 16px;
        padding: 17px 16px;
        min-height: 122px;
        box-sizing: border-box;
        box-shadow: 0 3px 12px rgba(98, 30, 62, 0.08);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .kpi-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 18px rgba(98, 30, 62, 0.16);
    }
    .kpi-teal { border-top-color: var(--c-cypress); }
    .kpi-green { border-top-color: var(--c-bamboo); }
    .kpi-blue { border-top-color: var(--c-ylang); }
    .kpi-amber { border-top-color: var(--c-red); }
    .kpi-secondary { border-top-color: rgba(98, 30, 62, 0.35); }
    .kpi-label {
        color: var(--c-berry);
        opacity: 0.85;
        font-size: 0.88rem;
        font-weight: 600;
        margin-bottom: 10px;
    }
    .kpi-value {
        color: var(--c-berry);
        font-size: clamp(1.15rem, 1.7vw, 1.75rem);
        font-weight: 800;
        line-height: 1.3;
        overflow-wrap: anywhere;
    }
    .kpi-caption {
        color: var(--c-berry);
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

    /* ---------- SEGMENT CARDS ---------- */
    .segment-card {
        background: var(--c-card);
        border: 1px solid var(--c-line);
        border-left: 5px solid var(--segment-accent);
        border-radius: 16px;
        padding: 16px;
        margin: 6px 0 12px 0;
        min-height: 200px;
    }
    .segment-label {
        color: var(--c-berry);
        font-size: 0.92rem;
        font-weight: 650;
        min-height: 42px;
    }
    .segment-count {
        color: var(--segment-accent);
        font-size: 1.8rem;
        line-height: 1.3;
        font-weight: 800;
        margin-top: 6px;
    }
    .segment-caption {
        color: var(--c-berry);
        opacity: 0.7;
        font-size: 0.8rem;
        margin-bottom: 12px;
    }
    .segment-stat {
        display: flex;
        justify-content: space-between;
        gap: 8px;
        border-top: 1px solid var(--c-line);
        padding-top: 8px;
        margin-top: 8px;
        font-size: 0.8rem;
        color: var(--c-berry);
    }

    #MainMenu, footer { visibility: hidden; }
</style>
"""


def inject_css():
    st.markdown(CSS, unsafe_allow_html=True)


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
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=height,
        autosize=True,
        margin=dict(l=18, r=18, t=48, b=18),
        font=dict(family="Arial", size=12, color=COLORS["berry"]),
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
        gridcolor="rgba(98, 30, 62, 0.12)",
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




MONGO_URI = "mongodb://localhost:27017/"
MONGO_DB = "ecommerce_analytics"
MONGO_COLLECTION = "customers"


@st.cache_data(ttl=10, show_spinner=False)
def mongo_status():
    """Return (state, detail); state is 'up', 'empty' or 'down'."""
    try:
        from pymongo import MongoClient

        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=1500)
        try:
            client.admin.command("ping")
            count = client[MONGO_DB][MONGO_COLLECTION].estimated_document_count()
        finally:
            client.close()
    except Exception:
        return "down", "Not reachable at localhost:27017"

    if count:
        return "up", f"{count:,} customer documents"
    return "empty", "No data loaded yet"


HDFS_HOST = "localhost"
HDFS_RPC_PORT = 9000   # fs.defaultFS = hdfs://localhost:9000
HDFS_WEB_PORT = 9870   # NameNode web UI


def _port_open(host, port, timeout=0.8):
    import socket

    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except OSError:
        return False


@st.cache_data(ttl=10, show_spinner=False)
def hadoop_status():
    """Return (state, detail); state is 'up' or 'down'."""
    if _port_open(HDFS_HOST, HDFS_RPC_PORT):
        return "up", f"NameNode on port {HDFS_RPC_PORT}"
    if _port_open(HDFS_HOST, HDFS_WEB_PORT):
        return "up", f"NameNode UI on port {HDFS_WEB_PORT}"
    return "down", "NameNode not running"


def _badge(label, state, detail):
    st.sidebar.markdown(
        f"""
<div class="mongo-badge mongo-{state}">
    <span class="mongo-dot"></span>
    <div>
        <div class="mongo-label">{label}</div>
        <div class="mongo-detail">{detail}</div>
    </div>
</div>
""",
        unsafe_allow_html=True,
    )


def status_badges():
    state, detail = mongo_status()
    _badge(
        "MongoDB offline" if state == "down" else "MongoDB connected",
        state,
        detail,
    )

    state, detail = hadoop_status()
    _badge(
        "Hadoop offline" if state == "down" else "Hadoop connected",
        state,
        detail,
    )


def page_header(kicker, title, subtitle):
    st.markdown(
        f"""
<div class="hero">
    <div class="hero-kicker">{kicker}</div>
    <div class="hero-title">{title}</div>
    <div class="hero-subtitle">{subtitle}</div>
</div>
""",
        unsafe_allow_html=True,
    )


def get_data():
    try:
        return load_data()
    except Exception as exc:
        st.error(f"Dashboard data could not be loaded: {exc}")
        st.info(
            "Check that the preprocessing and segmentation scripts "
            "have completed and their output files are present."
        )
        st.stop()


def filter_bar(orders):
    """Date and status filters shared by every page that uses them.

    Values live in session_state under f_* keys so they survive
    navigation between pages (widget keys are dropped when a page
    stops rendering them).
    """
    valid_dates = orders["order_purchase_timestamp"].dropna()

    if valid_dates.empty:
        st.error("No valid purchase timestamps were found.")
        st.stop()

    min_date = valid_dates.min().date()
    max_date = valid_dates.max().date()
    statuses = ["All statuses"] + sorted(
        orders["order_status"].dropna().unique().tolist()
    )

    st.session_state.setdefault("f_start", min_date)
    st.session_state.setdefault("f_end", max_date)
    st.session_state.setdefault("f_status", "All statuses")

    def remember(state_key, widget_key):
        st.session_state[state_key] = st.session_state[widget_key]

    with st.container(border=True):
        st.markdown("#### Refine your view")
        date_col, status_col = st.columns([1.7, 1])

        with date_col:
            date1, date2 = st.columns(2)
            with date1:
                st.date_input(
                    "Start date",
                    value=st.session_state["f_start"],
                    min_value=min_date,
                    max_value=max_date,
                    key="w_start",
                    on_change=remember,
                    args=("f_start", "w_start"),
                )
            with date2:
                st.date_input(
                    "End date",
                    value=st.session_state["f_end"],
                    min_value=min_date,
                    max_value=max_date,
                    key="w_end",
                    on_change=remember,
                    args=("f_end", "w_end"),
                )

        with status_col:
            st.selectbox(
                "Order status",
                statuses,
                index=statuses.index(st.session_state["f_status"]),
                key="w_status",
                on_change=remember,
                args=("f_status", "w_status"),
            )

    start_date = st.session_state["f_start"]
    end_date = st.session_state["f_end"]
    selected_status = st.session_state["f_status"]

    if start_date > end_date:
        st.warning(
            "Start date is after end date. The dates have been swapped."
        )
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

    delivered = filtered[filtered["order_status"].eq("delivered")].copy()

    st.caption(
        f"Showing purchase dates from {start_date} to {end_date}. "
        f"{len(filtered):,} orders match the current filters."
    )
    return filtered, date_data, delivered, selected_status


def footer():
    st.divider()
    st.markdown(
        '<div class="section-note">E-Commerce Customer Behavior & Purchase '
        'Analytics · Python · PySpark · Plotly · Streamlit</div>',
        unsafe_allow_html=True,
    )
