import streamlit as st
import plotly.express as px

from utils import load_data

# Logic and data cleaning for the Species Analytics tab
def species_analytics_tab(species_df):
    # Page title and description
    st.title("Species Distribution and Statistics")
    st.write("Explore the distribution of species across different parks and categories.")

    # Interactive selection bar
    all_categories = sorted(species_df['Category'].unique())
    # Multiselect for categories to visualize, with a default selection of the top 7 categories
    selected_categories = st.multiselect("Select Species to Visualize", options=all_categories, default=all_categories[:7])
    
    # Filter data based on selection
    filtered_df = species_df[species_df['Category'].isin(selected_categories)]

    st.subheader("Category Distribution")
    # Calculate species count by category for the filtered data
    cat_counts = filtered_df.groupby('Category').size().reset_index(name='Species_Count')
    # Sort categories by species count for better visualization
    cat_counts = cat_counts.sort_values(by='Species_Count', ascending=False)

    # Bar chart of species count by category
    fig = px.bar(
        cat_counts, 
        x='Category', 
        y='Species_Count', 
        color='Category', 
        text_auto=True,
        title="Species Count by Category",
        color_continuous_scale="Viridis"
        )
    
    st.plotly_chart(fig, use_container_width=True)

    st.divider()
    st.subheader("Conservation Status by Category")

    # Group by Category and Conservation Status
    status_stats = filtered_df.groupby(['Category', 'Conservation Status']).size().reset_index(name='Count')

    # Stacked bar chart of conservation status distribution by category
    fig_status = px.bar(
        status_stats,
        x="Category",
        y="Count",
        color="Conservation Status",
        barmode="stack",
        title="Conservation Status Distribution by Category",
        labels={'Count': 'Number of Species'},
    )

    st.plotly_chart(fig_status, use_container_width=True)

    # Display key statistics at the bottom of the page
    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric("Total Species", f"{len(species_df):,}")
    with m2:
        at_risk_statuses = ['Endangered', 'Threatened', 'Species of Concern']
        # Count the number of species in the filtered data that are considered at risk. Shape sets the dimension of the resulting DataFrame, and [0] gets the count of rows.
        at_risk_total = filtered_df[filtered_df['Conservation Status'].isin(at_risk_statuses)].shape[0]
        # Display the total number of at-risk species as a metric
        st.metric("At Risk Species", f"{at_risk_total:,}")
    with m3:
        # Determine the most common category in the filtered data and display it as a metric. If there are no categories (e.g., if the user deselects all), show "N/A".
        top_cat = cat_counts.iloc[0]['Category'] if not cat_counts.empty else "N/A"
        st.metric("Most Common Category", top_cat)

# Attempt to load data and display the species analytics tab, with error handling for missing files
try:
    # _ because load_data returns both parks and species, but we only need species for this tab
    _, species = load_data()
    # Call the function to display the species analytics tab, passing the loaded species DataFrame
    species_analytics_tab(species)

except FileNotFoundError:
    st.error("Please place 'parks.csv' and 'species.csv' in the same folder as this script.")