import streamlit as st

from common import inject_css, status_badges

st.set_page_config(
    page_title="E-Commerce Intelligence",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_css()

pages = [
    st.Page("views/overview.py", title="Overview", icon=":material/home:", default=True),
    st.Page("views/orders.py", title="Orders", icon=":material/inventory_2:"),
    st.Page("views/spending.py", title="Spending", icon=":material/trending_up:"),
    st.Page("views/segments.py", title="Segments", icon=":material/donut_small:"),
    st.Page("views/geography.py", title="Geography", icon=":material/location_on:"),
    st.Page("views/records.py", title="Records", icon=":material/table_rows:"),
]

st.sidebar.markdown(
    '<div class="sn-foot">OLIST · 2016–2018</div>', unsafe_allow_html=True
)

status_badges()

st.navigation(pages).run()
