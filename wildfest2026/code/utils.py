import streamlit as st
import pandas as pd

@st.cache_resource
def load_data():
    parks_df = pd.read_csv('data/national-parks.csv')
    species_df = pd.read_csv('data/national-park-species.csv')
    return parks_df, species_df