import streamlit as st
import plotly.express as px

from tabs.map import load_data

def species_analytics_tab(species_df):
    st.title("Species Distribution and Statistics")
    st.write("Explore the distribution of species across different parks and categories.")

    # Interactive selection bar
    all_categories = sorted(species_df['Category'].unique())
    selected_categories = st.multiselect("Select Species to Visualize", options=all_categories, default=all_categories[:7])
    
    # Filter data based on selection
    filtered_df = species_df[species_df['Category'].isin(selected_categories)]

    st.subheader("Category Distribution")
    cat_counts = filtered_df.groupby('Category').size().reset_index(name='Species_Count')
    cat_counts = cat_counts.sort_values(by='Species_Count', ascending=False)

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

    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric("Total Species", f"{len(species_df):,}")
    with m2:
        at_risk_statuses = ['Endangered', 'Threatened', 'Species of Concern']
        at_risk_total = filtered_df[filtered_df['Conservation Status'].isin(at_risk_statuses)].shape[0]
        st.metric("At Risk Species", f"{at_risk_total:,}")
    with m3:
        top_cat = cat_counts.iloc[0]['Category'] if not cat_counts.empty else "N/A"
        st.metric("Most Common Category", top_cat)

try:
    _, species = load_data()
    species_analytics_tab(species)

except FileNotFoundError:
    st.error("Please place 'parks.csv' and 'species.csv' in the same folder as this script.")