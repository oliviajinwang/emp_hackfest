import streamlit as st
import pandas as pd
import plotly.express as px
import folium
from folium import Element
import json
from ai_predictor import train_model, predict_species_risk
from utils import load_data
import numpy as np

st.set_page_config(page_title="Park Guardian AI", layout="wide", page_icon="🌲")

# Initialize Session State for the side panel
if 'selected_park_name' not in st.session_state:
    st.session_state.selected_park_name = None

# st saves it in the local memory, so we can cache the model to avoid retraining on every interaction
@st.cache_resource
def get_ai_model(species_df, parks_df):
    return train_model(species_df, parks_df)

# this function processes the park and species data to calculate baseline metrics
# like species count and biodiversity density, and also handles outliers in density
# for better map visualization
def process_baseline_metrics(parks_df, species_df):
    # Species Per Park
    species_counts = species_df.groupby('Park Name').size().reset_index(name='Species Count')

    # Merge with Park Info
    merged_df = pd.merge(parks_df, species_counts, on='Park Name')

    # Calculate Density
    merged_df['Biodiversity Density'] = merged_df['Species Count'] / merged_df['Acres'] * 1000

    upper_limit = merged_df['Biodiversity Density'].quantile(1)
    merged_df['Visual_Biodiversity_Density'] = merged_df['Biodiversity Density'].clip(upper=upper_limit)

    return merged_df

try:
    parks, species = load_data()
    merged = process_baseline_metrics(parks, species)

    # Train AI Model
    ai_model, encoders = get_ai_model(species, parks)
    
    st.sidebar.title("Filters & Options")
    st.sidebar.info("Analyze and predict biodiversity health across US National Parks.")
    map_mode = st.sidebar.radio("Map Color Represents: ", ["Total Species", "Biodiversity Density"])

    st.title("National Park Guardian Interactive Map")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Parks Monitored", len(parks))
    col2.metric("Species Cataloged", f"{len(species):,}")
    col3.metric("At Risk Species", len(species[species['Conservation Status'].isin(['Endangered', 'Threatened'])]))

    # Map gets 80% of the width, panel gets 20%
    map_col, panel_col = st.columns([8, 2])

    # map
    with map_col:
        st.subheader("Interactive Biodiversity Map")
        st.write("Each point represents a National Park. Size represents acreage.")
        # changes the color of the node based on the mode of the map
        color_col = "Species Count" if map_mode == "Total Species" else "log_density"
        # map_label changes the label in the hover tooltip based on the mode of the map
        map_label = "Total Species" if map_mode == "Total Species" else "Logarithmic Density per 1000 Acres"

        # create the map w/ plotly
        merged["log_density"] = np.log10(merged['Visual_Biodiversity_Density'] + 1e-8)

        fig = px.scatter_map(
            merged, 
            lat="Latitude", 
            lon="Longitude", 
            hover_name="Park Name",
            # includes the state and acres when you hover over the node
            hover_data=["State", "Acres"],
            size="Acres",
            color=color_col,
            color_continuous_scale="Viridis",
            size_max=40,
            color_discrete_sequence=["#2E7D32"],
            zoom=3, 
            height=1200,
            labels={color_col: map_label}
        )

        # Use open-source map tiles (does not require an API key)
        fig.update_layout(
            # clean open-street map with borders but not too busy
            map_style="open-street-map",
            # this limits the map to the continaer
            margin={"r":0,"t":0,"l":0,"b":0}
        )

        selected_points = st.plotly_chart(fig, use_container_width=True, on_select="rerun", key="park_map")

        # Update Session State based on click
        if selected_points and "selection" in selected_points:
            points = selected_points["selection"].get("points", [])
            if len(points) > 0:
                # Hovertext contains the Park Name
                selected_park = points[0].get("hovertext")
                if selected_park:
                    st.session_state.selected_park_name = selected_park

    # side panel
    with panel_col:
        st.header("Park Details")
        if st.session_state.selected_park_name:
            # iloc gets the first row of the df
            park_info = merged[merged['Park Name'] == st.session_state.selected_park_name].iloc[0]
            # asterisks for bold, double for bold in markdown
            st.markdown(f"### {park_info['Park Name']}")
            st.write(f"**State:** {park_info['State']}")
            st.write(f"**Acres:** {park_info['Acres']:,}")
            st.write(f"**Total Species:** {park_info['Species Count']}")

            if st.button("Close Panel"):
                st.session_state.selected_park_name = None
                st.rerun()

            st.divider()
            
            # AI Predictions for Vulnerable Species
            park_name = st.session_state.selected_park_name
            st.subheader(f"{park_name} AI Forecast: top 10 most vulnerable species")
            # park_species filters the species df to only include species found in the selected park 
            park_species = species[species['Park Name'] == park_name].copy()
            
            # Predict risk scores for each species in the park
            risks = []
            # this for loop uses the ai model to predict the risk score for each species based on category
            # abundance, and acres and biodiversity density
            for _, row in park_species.iterrows():
                risk = predict_species_risk(ai_model, encoders, row['Category'], row['Abundance'], park_info['Acres'], park_info['Biodiversity Density'])
                risks.append(risk)

            # Add risk scores to the DataFrame and get top 10 most vulnerable species
            park_species['risk_score'] = risks
            top_ten = park_species.sort_values(by="risk_score", ascending=False).head(10)

            # Display top 10 species with risk scores
            for _, row in top_ten.iterrows():
                risk = row['risk_score']

                # Display species name and risk score with color coding
                col_a, col_b = st.columns([1, 1])

                # clean up common names for display
                cleaned_name = str(row['Common Names']).split(',')[0]
                col_a.write(f"**{cleaned_name}**")

                # Color code risk: red for >66%, orange for 33-66%, green for <33%
                color = "red" if risk > 66 else "orange" if risk > 33 else "green"
                col_b.markdown(f":{color}[{risk}%]")

            st.caption("AI estimates vulnerability based on category abundance trends and park-level metrics.")
        else:
            st.info("Click on a park on the map to see details and AI insights here.")

except FileNotFoundError:
    st.error("Please place 'parks.csv' and 'species.csv' in the same folder as this script.")