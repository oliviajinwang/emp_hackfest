import streamlit as st
from themes import set_theme

st.logo("assets/pglogo4.webp", size="large")

# the 4 pages we have
home_page = st.Page(page="tabs/homepage.py", title="Home", default=True)
map_page = st.Page(page="tabs/map.py", title="Map", default=False)
categores_page = st.Page(page="tabs/categories.py", title="Species Analytics", default=False)
cta_page = st.Page(page="tabs/cta.py", title="Get Involved", default=False)

# navigation sets up the sidebar
pg = st.navigation([home_page, map_page, categores_page, cta_page])
st.set_page_config(page_title="Park Guardian", layout="wide")
set_theme()
pg.run()
