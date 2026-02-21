import streamlit as st
from themes import set_theme

st.logo("https://pbs.twimg.com/media/GRBDcDFaYAA0yPt.jpg", size="large")

home_page = st.Page(page="tabs/homepage.py", title="Home", default=True)
map_page = st.Page(page="tabs/map.py", title="Map", default=False)
cta_page = st.Page(page="tabs/cta.py", title="Get Involved", default=False)

pg = st.navigation([home_page, map_page, cta_page])
st.set_page_config(page_title="Park Guardian", layout="wide")
set_theme()
pg.run()
