import streamlit as st

from common import inject_css, status_badges

st.set_page_config(
    page_title="E-Commerce Intelligence",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_css()

pages = [
    st.Page("views/overview.py", title="Overview", icon=":material/home:", default=True),
    st.Page("views/orders.py", title="Orders", icon=":material/inventory_2:"),
    st.Page("views/spending.py", title="Spending & Revenue", icon=":material/trending_up:"),
    st.Page("views/segments.py", title="Customer Segments", icon=":material/donut_small:"),
    st.Page("views/geography.py", title="Geography", icon=":material/public:"),
    st.Page("views/records.py", title="Order Records", icon=":material/table_rows:"),
    st.Page("views/products.py", title="Products & Categories Analytics", icon=":material/category:"),
    st.Page("views/delivery.py", title="Delivery & Logistics Analytics", icon=":material/local_shipping:"),
    st.Page("views/reviews.py", title="Reviews & Rating Intelligence", icon=":material/star:"),
]

st.sidebar.markdown(
    '<div class="sn-foot">BRAZILIAN E-COMMERCE · 2016–2018</div>', unsafe_allow_html=True
)

status_badges()

st.navigation(pages).run()
