from pathlib import Path
import pandas as pd
import streamlit as st

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "processed"
MARTS_DIR = DATA_DIR / "marts"

# =========================================================
# BRAND DESIGN SYSTEM & PALETTE
# =========================================================
# Wild Berry #621E3E, Cypress #667436, Bamboo #C6C954,
# Chrysanthemum Red #D9282D, Ylang Ylang Gold #FFEC8E, Warm Ivory #FFFDF0
COLORS = {
    "berry": "#621E3E",
    "dark_berry": "#3A1024",
    "cypress": "#667436",
    "bamboo": "#C6C954",
    "red": "#D9282D",
    "ylang": "#FFEC8E",
    "cream": "#FFF3B0",
    "muted": "#9C7A8B",
    "card": "#FFFFFF",
    "page": "#FFFDF0",
    "border": "rgba(98, 30, 62, 0.14)",
}

PALETTE = [
    COLORS["cypress"],
    COLORS["berry"],
    COLORS["bamboo"],
    COLORS["red"],
    COLORS["ylang"],
    COLORS["muted"],
]

# Brazilian Federative Units (States & Federal District) Mapping
BRAZILIAN_STATES = {
    "AC": "Acre",
    "AL": "Alagoas",
    "AP": "Amapá",
    "AM": "Amazonas",
    "BA": "Bahia",
    "CE": "Ceará",
    "DF": "Distrito Federal",
    "ES": "Espírito Santo",
    "GO": "Goiás",
    "MA": "Maranhão",
    "MT": "Mato Grosso",
    "MS": "Mato Grosso do Sul",
    "MG": "Minas Gerais",
    "PA": "Pará",
    "PB": "Paraíba",
    "PR": "Paraná",
    "PE": "Pernambuco",
    "PI": "Piauí",
    "RJ": "Rio de Janeiro",
    "RN": "Rio Grande do Norte",
    "RS": "Rio Grande do Sul",
    "RO": "Rondônia",
    "RR": "Roraima",
    "SC": "Santa Catarina",
    "SP": "São Paulo",
    "SE": "Sergipe",
    "TO": "Tocantins",
}

def format_state_name(code):
    """Format 2-letter state code into 'Full Official Name (UF)', e.g. 'São Paulo (SP)'."""
    if not isinstance(code, str) or not code.strip():
        return "" if code is None or (isinstance(code, float) and pd.isna(code)) else str(code).strip()
    clean = code.strip().upper()
    full_name = BRAZILIAN_STATES.get(clean)
    if full_name:
        return f"{full_name} ({clean})"
    return clean



CSS = """
<style>
    :root {
        --c-ylang: #FFEC8E;
        --c-cream: #FFF3B0;
        --c-bamboo: #C6C954;
        --c-cypress: #667436;
        --c-red: #D9282D;
        --c-berry: #621E3E;
        --c-dark-berry: #3A1024;
        --c-page: #FFFDF0;
        --c-card: #FFFFFF;
        --c-line: rgba(98, 30, 62, 0.14);
        --shadow-sm: 0 2px 8px rgba(98, 30, 62, 0.06);
        --shadow-md: 0 6px 18px rgba(98, 30, 62, 0.10);
    }

    html { scroll-behavior: smooth; }
    .stApp { background: var(--c-page); }

    /* Streamlit toolbar & headers */
    header[data-testid="stHeader"] { background: transparent; }
    [data-testid="stToolbar"], [data-testid="stDecoration"] { display: none; }
    .block-container {
        padding-top: 1.8rem;
        padding-bottom: 2.8rem;
        padding-left: 2.2rem;
        padding-right: 2.2rem;
        max-width: 1650px;
    }

    h1, h2, h3, h4, h5, p, label, span, li { 
        color: var(--c-berry);
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }

    /* ---------- SIDE NAVIGATION ---------- */
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
        width: 16.5rem !important;
        min-width: 16.5rem !important;
        background: linear-gradient(180deg, #7A2A4E 0%, var(--c-berry) 38%, #220815 100%);
        border-right: 1px solid rgba(255, 236, 142, 0.25);
        border-radius: 0 28px 28px 0;
        box-shadow: 6px 0 28px rgba(98, 30, 62, 0.24);
    }
    section[data-testid="stSidebar"] > div,
    section[data-testid="stSidebar"] [data-testid="stSidebarContent"] {
        background: transparent;
    }
    section[data-testid="stSidebar"] [data-testid="stSidebarUserContent"] {
        padding: 0 1rem 1.2rem 1.3rem;
    }

    [data-testid="stSidebarNav"] { padding: 0.4rem 0 0.4rem 0.8rem; }
    [data-testid="stSidebarNav"]::before {
        content: "E-COMMERCE\\A INTELLIGENCE";
        white-space: pre;
        display: block;
        margin: 0.4rem 0 1.2rem 0.6rem;
        color: var(--c-ylang);
        font-size: 1.12rem;
        font-weight: 850;
        line-height: 1.25;
        letter-spacing: 0.04em;
    }
    [data-testid="stSidebarNav"] ul { padding: 0; gap: 0.35rem; }

    [data-testid="stSidebarNavLink"] {
        height: 2.75rem;
        padding: 0 0.9rem;
        border-radius: 14px 0 0 14px;
        background: rgba(255, 255, 255, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.10);
        border-right: none;
        transition: all 0.18s ease;
    }
    [data-testid="stSidebarNavLink"],
    [data-testid="stSidebarNavLink"] span,
    [data-testid="stSidebarNavLink"] p {
        color: var(--c-ylang) !important;
        font-weight: 600;
        font-size: 0.90rem;
    }
    [data-testid="stSidebarNavLink"]:hover { 
        background: rgba(255, 255, 255, 0.16);
        transform: translateX(3px);
    }

    /* active tab */
    [data-testid="stSidebarNavLink"][aria-current="page"] {
        background: var(--c-page);
        border-color: var(--c-page);
        box-shadow: none;
    }
    [data-testid="stSidebarNavLink"][aria-current="page"],
    [data-testid="stSidebarNavLink"][aria-current="page"] span,
    [data-testid="stSidebarNavLink"][aria-current="page"] p {
        color: var(--c-berry) !important;
        font-weight: 850;
    }

    section[data-testid="stSidebar"] .sn-foot {
        color: var(--c-bamboo);
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        margin-top: 1rem;
        padding-top: 0.6rem;
        border-top: 1px solid rgba(255, 236, 142, 0.18);
    }

    /* Status Badges */
    .status-badge-container {
        display: flex;
        flex-direction: column;
        gap: 0.45rem;
        margin-top: 0.5rem;
    }
    .service-badge {
        display: flex;
        align-items: center;
        gap: 0.65rem;
        padding: 0.55rem 0.75rem;
        border-radius: 12px;
        background: rgba(255, 255, 255, 0.09);
        border: 1px solid rgba(255, 255, 255, 0.13);
        box-sizing: border-box;
    }
    .service-dot {
        flex: none;
        width: 0.65rem; height: 0.65rem;
        border-radius: 50%;
        background: var(--c-bamboo);
        box-shadow: 0 0 0 2px rgba(198, 201, 84, 0.25), 0 0 8px var(--c-bamboo);
    }
    .service-empty .service-dot {
        background: var(--c-ylang);
        box-shadow: 0 0 0 2px rgba(255, 236, 142, 0.25), 0 0 8px var(--c-ylang);
    }
    .service-down .service-dot {
        background: var(--c-red);
        box-shadow: 0 0 0 2px rgba(217, 40, 45, 0.3), 0 0 8px var(--c-red);
    }
    .service-label { color: var(--c-ylang); font-size: 0.80rem; font-weight: 700; }
    .service-detail {
        color: #EBD6E0;
        font-size: 0.66rem;
        margin-top: 1px;
        line-height: 1.3;
        overflow-wrap: anywhere;
    }

    /* ---------- HERO SECTION ---------- */
    .hero {
        padding: 1.4rem 1.7rem;
        border-radius: 18px;
        background: linear-gradient(120deg, var(--c-berry) 0%, #7E2650 60%, var(--c-dark-berry) 100%);
        border-bottom: 4px solid var(--c-ylang);
        margin-bottom: 1.25rem;
        box-shadow: var(--shadow-md);
        position: relative;
        overflow: hidden;
    }
    .hero-kicker {
        color: var(--c-bamboo);
        font-size: 0.74rem;
        font-weight: 800;
        letter-spacing: 0.14em;
        text-transform: uppercase;
        margin-bottom: 0.4rem;
    }
    .hero-title {
        color: var(--c-ylang);
        font-size: clamp(1.6rem, 2.5vw, 2.2rem);
        font-weight: 800;
        line-height: 1.18;
        margin: 0;
    }
    .hero-subtitle {
        color: #F8EDF3;
        margin-top: 0.5rem;
        font-size: 0.95rem;
        max-width: 950px;
        line-height: 1.4;
    }

    /* ---------- LANDING HERO & SHOWCASE (ECOMMERCE) ---------- */
    .landing-hero {
        position: relative;
        overflow: hidden;
        background: linear-gradient(135deg, #4A152E 0%, #621E3E 55%, #7E2650 100%);
        border-radius: 24px;
        padding: 2.2rem 2.8rem;
        margin-bottom: 1.6rem;
        border: 1px solid rgba(255, 236, 142, 0.28);
        box-shadow: 0 16px 40px rgba(74, 21, 46, 0.22);
    }
    .hero-eyebrow {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        font-size: 0.78rem;
        font-weight: 850;
        letter-spacing: 0.14em;
        text-transform: uppercase;
        color: #FFEC8E;
        background: rgba(255, 236, 142, 0.14);
        border: 1px solid rgba(255, 236, 142, 0.32);
        padding: 0.35rem 0.9rem;
        border-radius: 999px;
        margin-bottom: 0.8rem;
    }
    .hero-headline {
        color: #FFFDF0 !important;
        font-size: clamp(2.1rem, 3.4vw, 3.1rem) !important;
        font-weight: 900 !important;
        line-height: 1.14 !important;
        letter-spacing: -0.02em !important;
        margin: 0.2rem 0 0.8rem 0 !important;
    }
    .hero-headline span.gold-highlight {
        color: #FFEC8E !important;
    }
    .hero-copy {
        color: #F7EBF1 !important;
        font-size: 1.05rem !important;
        line-height: 1.55 !important;
        max-width: 680px;
        margin: 0 !important;
    }

    /* Showcase Category Cards */
    .showcase-card {
        background: var(--c-card);
        border: 1px solid var(--c-line);
        border-radius: 18px;
        padding: 1.4rem;
        box-shadow: var(--shadow-sm);
        transition: transform 0.22s ease, box-shadow 0.22s ease, border-color 0.22s ease;
        display: flex;
        flex-direction: column;
        height: 100%;
        box-sizing: border-box;
    }
    .showcase-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 28px rgba(98, 30, 62, 0.12);
        border-color: rgba(98, 30, 62, 0.3);
    }
    .showcase-card-img {
        width: 100%;
        height: 140px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: #FFFDF0;
        border-radius: 12px;
        overflow: hidden;
        margin-bottom: 1rem;
    }
    .showcase-card-title {
        color: var(--c-berry);
        font-size: 1.18rem;
        font-weight: 850;
        margin: 0 0 0.4rem 0;
    }
    .showcase-card-desc {
        color: #553344;
        font-size: 0.88rem;
        line-height: 1.5;
        flex-grow: 1;
        margin-bottom: 1rem;
    }
    div[data-testid="stPageLink-NavLink"] {
        border-radius: 10px;
        font-weight: 700;
        transition: all 0.18s ease;
    }

    /* ---------- CARDS & CONTAINERS ---------- */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 16px;
        border-color: var(--c-line);
        background: var(--c-card);
        box-shadow: var(--shadow-sm);
    }
    [data-testid="stPlotlyChart"] {
        background: var(--c-card);
        border: 1px solid var(--c-line);
        border-radius: 16px;
        padding: 0.45rem;
        box-shadow: var(--shadow-sm);
    }
    div[data-testid="stExpander"] {
        border-radius: 14px;
        border-color: var(--c-line);
        background: var(--c-card);
        box-shadow: var(--shadow-sm);
    }
    hr { border-color: var(--c-line) !important; }

    .section-note {
        color: var(--c-berry);
        opacity: 0.8;
        font-size: 0.86rem;
        line-height: 1.4;
    }

    /* Inputs & Select styling */
    div[data-baseweb="select"] > div,
    div[data-baseweb="input"],
    div[data-testid="stDateInput"] > div > div {
        background: #FFFBE4 !important;
        border-color: var(--c-line) !important;
        color: var(--c-berry) !important;
        border-radius: 10px !important;
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
        padding: 16px 18px;
        min-height: 120px;
        box-sizing: border-box;
        box-shadow: var(--shadow-sm);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .kpi-card:hover {
        transform: translateY(-2px);
        box-shadow: var(--shadow-md);
    }
    .kpi-cypress { border-top-color: var(--c-cypress); }
    .kpi-bamboo { border-top-color: var(--c-bamboo); }
    .kpi-gold { border-top-color: var(--c-ylang); }
    .kpi-red { border-top-color: var(--c-red); }
    .kpi-secondary { border-top-color: rgba(98, 30, 62, 0.35); }
    .kpi-label {
        color: var(--c-berry);
        opacity: 0.88;
        font-size: 0.86rem;
        font-weight: 650;
        margin-bottom: 8px;
    }
    .kpi-value {
        color: var(--c-berry);
        font-size: clamp(1.2rem, 1.8vw, 1.75rem);
        font-weight: 850;
        line-height: 1.25;
        overflow-wrap: anywhere;
    }
    .kpi-caption {
        color: var(--c-berry);
        opacity: 0.68;
        font-size: 0.76rem;
        margin-top: 8px;
    }

    /* ---------- INSIGHT CALLOUT BOX ---------- */
    .insight-box {
        background: linear-gradient(135deg, #FFFDEE 0%, #FFF8CC 100%);
        border: 1px solid var(--c-ylang);
        border-left: 5px solid var(--c-cypress);
        border-radius: 14px;
        padding: 14px 18px;
        margin: 12px 0 18px 0;
        box-shadow: var(--shadow-sm);
    }
    .insight-title {
        color: var(--c-cypress);
        font-weight: 800;
        font-size: 0.88rem;
        letter-spacing: 0.04em;
        text-transform: uppercase;
        margin-bottom: 4px;
    }
    .insight-text {
        color: var(--c-berry);
        font-size: 0.94rem;
        line-height: 1.45;
        margin: 0;
    }

    /* ---------- SEGMENT CARDS ---------- */
    .segment-card {
        background: var(--c-card);
        border: 1px solid var(--c-line);
        border-left: 5px solid var(--segment-accent);
        border-radius: 16px;
        padding: 18px;
        margin: 6px 0 12px 0;
        min-height: 210px;
        box-shadow: var(--shadow-sm);
    }
    .segment-label {
        color: var(--c-berry);
        font-size: 0.96rem;
        font-weight: 750;
        min-height: 38px;
    }
    .segment-count {
        color: var(--segment-accent);
        font-size: 1.9rem;
        line-height: 1.3;
        font-weight: 850;
        margin-top: 4px;
    }
    .segment-caption {
        color: var(--c-berry);
        opacity: 0.72;
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
        font-size: 0.82rem;
        color: var(--c-berry);
    }

    #MainMenu, footer { visibility: hidden; }

    @media (max-width: 900px) {
        .kpi-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
    }
    @media (max-width: 480px) {
        .kpi-grid { grid-template-columns: 1fr; }
    }
</style>
"""

def inject_css():
    st.markdown(CSS, unsafe_allow_html=True)


# =========================================================
# DATABASE INTEGRATIONS & STATUS
# =========================================================
MONGO_URI = "mongodb://localhost:27017/"
MONGO_DB = "ecommerce_analytics"
MONGO_COLLECTION = "customers"

@st.cache_data(ttl=10, show_spinner=False)
def mongo_status():
    """Return (state, detail); state is 'up', 'empty' or 'down'."""
    try:
        from pymongo import MongoClient
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=1200)
        try:
            client.admin.command("ping")
            count = client[MONGO_DB][MONGO_COLLECTION].estimated_document_count()
        finally:
            client.close()
    except Exception:
        return "down", "Not reachable at localhost:27017"

    if count:
        return "up", f"{count:,} customer documents"
    return "empty", "Connected (no docs loaded)"

HDFS_HOST = "localhost"
HDFS_RPC_PORT = 9000
HDFS_WEB_PORT = 9870

def _port_open(host, port, timeout=0.6):
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
        return "up", f"NameNode active on port {HDFS_RPC_PORT}"
    if _port_open(HDFS_HOST, HDFS_WEB_PORT):
        return "up", f"NameNode UI on port {HDFS_WEB_PORT}"
    return "down", "NameNode not running"

def _badge(label, state, detail):
    st.sidebar.markdown(
        f"""
<div class="service-badge service-{state}">
    <span class="service-dot"></span>
    <div>
        <div class="service-label">{label}</div>
        <div class="service-detail">{detail}</div>
    </div>
</div>
""",
        unsafe_allow_html=True,
    )

def status_badges():
    st.sidebar.markdown('<div class="status-badge-container">', unsafe_allow_html=True)
    m_state, m_detail = mongo_status()
    _badge("MongoDB online" if m_state == "up" else "MongoDB offline", m_state, m_detail)

    h_state, h_detail = hadoop_status()
    _badge("Hadoop online" if h_state == "up" else "Hadoop offline", h_state, h_detail)
    st.sidebar.markdown('</div>', unsafe_allow_html=True)


# =========================================================
# DATA LOADING & PERSISTENCE
# =========================================================
@st.cache_data(show_spinner="Loading Spark processed CSV...")
def read_spark_csv(folder_string):
    folder = Path(folder_string)
    files = sorted(folder.glob("part-*.csv"))
    if not files:
        raise FileNotFoundError(f"No Spark CSV part files found in {folder}")
    return pd.concat([pd.read_csv(file) for file in files], ignore_index=True)

USER_ORDER_COLUMNS = [
    "order_id", "customer_id", "order_status", "order_purchase_timestamp",
    "item_total", "freight_total", "payment_total", "source"
]

def user_orders_path():
    return DATA_DIR / "user_orders.csv"

def load_user_orders():
    """Orders entered through the Records page form."""
    path = user_orders_path()
    if not path.exists():
        return pd.DataFrame(columns=USER_ORDER_COLUMNS)
    df = pd.read_csv(path)
    df["order_purchase_timestamp"] = pd.to_datetime(
        df["order_purchase_timestamp"], errors="coerce"
    )
    if "source" not in df.columns:
        df["source"] = "User Entry"
    return df

def save_user_order(row):
    """Save order to user_orders.csv and persist to MongoDB if online."""
    path = user_orders_path()
    row["source"] = "User Entry"
    df = pd.DataFrame([row])
    for col in USER_ORDER_COLUMNS:
        if col not in df.columns:
            df[col] = None
    df = df[USER_ORDER_COLUMNS]

    df.to_csv(path, mode="a", header=not path.exists(), index=False)

    mongo_saved = False
    try:
        from pymongo import MongoClient
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=1000)
        db = client[MONGO_DB]
        doc = dict(row)
        if isinstance(doc.get("order_purchase_timestamp"), pd.Timestamp):
            doc["order_purchase_timestamp"] = doc["order_purchase_timestamp"].to_pydatetime()
        db["user_orders"].insert_one(doc)
        client.close()
        mongo_saved = True
    except Exception:
        mongo_saved = False

    st.cache_data.clear()
    return mongo_saved

@st.cache_data(show_spinner="Preparing core dataset...")
def load_data():
    orders = read_spark_csv(str(DATA_DIR / "cleaned" / "orders"))
    purchase = read_spark_csv(str(DATA_DIR / "cleaned" / "order_purchase_summary"))
    customers = read_spark_csv(str(DATA_DIR / "marts" / "customer_purchase"))
    segments = pd.read_csv(DATA_DIR / "segmentation" / "kmeans" / "customer_segments.csv")
    cluster_summary = pd.read_csv(DATA_DIR / "segmentation" / "kmeans" / "cluster_summary.csv")

    orders["order_purchase_timestamp"] = pd.to_datetime(
        orders["order_purchase_timestamp"], errors="coerce"
    )

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

    data["source"] = "Historical Dataset"

    user_orders = load_user_orders()
    if not user_orders.empty:
        data = pd.concat([data, user_orders], ignore_index=True)

    customers["delivered_item_spend"] = pd.to_numeric(customers["delivered_item_spend"], errors="coerce")
    customers["delivered_payment_total"] = pd.to_numeric(customers["delivered_payment_total"], errors="coerce")
    customers["delivered_order_count"] = pd.to_numeric(customers["delivered_order_count"], errors="coerce")

    return data, customers, segments, cluster_summary

def get_data():
    try:
        return load_data()
    except Exception as exc:
        st.error(f"Core dashboard data could not be loaded: {exc}")
        st.stop()

# Data loaders for the 3 retained new pages
@st.cache_data(show_spinner=False)
def load_category_mart():
    path = MARTS_DIR / "category_summary.csv"
    if path.exists():
        return pd.read_csv(path)
    return pd.DataFrame()

@st.cache_data(show_spinner=False)
def load_top_products_mart():
    path = MARTS_DIR / "top_products.csv"
    if path.exists():
        return pd.read_csv(path)
    return pd.DataFrame()

@st.cache_data(show_spinner=False)
def load_delivery_mart():
    orders_path = MARTS_DIR / "delivery_orders.csv"
    state_path = MARTS_DIR / "state_delivery_summary.csv"
    orders_df = pd.read_csv(orders_path) if orders_path.exists() else pd.DataFrame()
    state_df = pd.read_csv(state_path) if state_path.exists() else pd.DataFrame()
    if not orders_df.empty:
        for c in ["order_purchase_timestamp", "order_delivered_customer_date", "order_estimated_delivery_date"]:
            if c in orders_df.columns:
                orders_df[c] = pd.to_datetime(orders_df[c], errors="coerce")
    return orders_df, state_df

@st.cache_data(show_spinner=False)
def load_reviews_mart():
    dist_path = MARTS_DIR / "review_score_distribution.csv"
    delay_path = MARTS_DIR / "review_delay_impact.csv"
    trend_path = MARTS_DIR / "review_monthly_trend.csv"
    state_path = MARTS_DIR / "review_state_scores.csv"
    dist_df = pd.read_csv(dist_path) if dist_path.exists() else pd.DataFrame()
    delay_df = pd.read_csv(delay_path) if delay_path.exists() else pd.DataFrame()
    trend_df = pd.read_csv(trend_path) if trend_path.exists() else pd.DataFrame()
    state_df = pd.read_csv(state_path) if state_path.exists() else pd.DataFrame()
    return dist_df, delay_df, trend_df, state_df


# =========================================================
# REUSABLE CHART & UI FORMATTING
# =========================================================
def polish(fig, height=360, legend=True):
    fig.update_layout(
        template="streamlit",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=height,
        autosize=True,
        margin=dict(l=18, r=18, t=48, b=18),
        font=dict(family="-apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Arial", size=12, color=COLORS["berry"]),
        title=dict(
            x=0.025,
            xanchor="left",
            font=dict(size=15, color=COLORS["berry"]),
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(size=11),
        ) if legend else dict(visible=False),
        hoverlabel=dict(
            font_size=12,
            bgcolor="#FFFDEE",
            bordercolor=COLORS["berry"],
            font_family="-apple-system, sans-serif"
        ),
    )
    fig.update_xaxes(showgrid=False, automargin=True, tickfont=dict(color=COLORS["berry"]))
    fig.update_yaxes(
        gridcolor="rgba(98, 30, 62, 0.10)",
        zeroline=False,
        automargin=True,
        tickfont=dict(color=COLORS["berry"])
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


# =========================================================
# SHARED FILTER BAR
# =========================================================
def filter_bar(orders, show_status=True):
    valid_dates = orders["order_purchase_timestamp"].dropna()
    if valid_dates.empty:
        st.error("No valid purchase timestamps were found.")
        st.stop()

    min_date = valid_dates.min().date()
    max_date = valid_dates.max().date()
    statuses = ["All statuses"] + sorted(orders["order_status"].dropna().unique().tolist())

    st.session_state.setdefault("f_start", min_date)
    st.session_state.setdefault("f_end", max_date)
    st.session_state.setdefault("f_status", "All statuses")

    def remember(state_key, widget_key):
        st.session_state[state_key] = st.session_state[widget_key]

    with st.container(border=True):
        f_top1, f_top2 = st.columns([4, 1])
        with f_top1:
            st.markdown("#### Filter Analytics Scope")
        with f_top2:
            if st.button("Reset Filters", use_container_width=True):
                st.session_state["f_start"] = min_date
                st.session_state["f_end"] = max_date
                st.session_state["f_status"] = "All statuses"
                st.rerun()

        if show_status:
            date_col, status_col = st.columns([1.7, 1])
        else:
            date_col = st.columns(1)[0]

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

        if show_status:
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
        st.warning("Start date was after end date. Automatically swapped.")
        start_date, end_date = end_date, start_date

    start_ts = pd.Timestamp(start_date)
    end_ts = pd.Timestamp(end_date) + pd.Timedelta(days=1)

    date_mask = (
        orders["order_purchase_timestamp"].ge(start_ts)
        & orders["order_purchase_timestamp"].lt(end_ts)
    )
    date_data = orders.loc[date_mask].copy()

    if not show_status or selected_status == "All statuses":
        filtered = date_data.copy()
    else:
        filtered = date_data[date_data["order_status"].eq(selected_status)].copy()

    delivered = filtered[filtered["order_status"].eq("delivered")].copy()

    st.caption(
        f"Active scope: **{start_date}** to **{end_date}** · **{len(filtered):,}** orders matching current filters."
    )
    return filtered, date_data, delivered, selected_status


def footer():
    st.divider()
    st.markdown(
        """
<div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px;" class="section-note">
    <div><strong>E-Commerce Intelligence Portal</strong> · Big Data Analytics Mini Project</div>
    <div>Technologies: Python · Streamlit · PySpark · Plotly · MongoDB · Apache Hadoop</div>
    <div>Data Source: Brazilian E-Commerce Public Dataset by Olist (2016–2018)</div>
</div>
""",
        unsafe_allow_html=True,
    )
