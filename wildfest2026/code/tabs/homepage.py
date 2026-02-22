import streamlit as st

# make sure to revise before submission

st.title("Welcome to National Park Guardian AI", text_alignment="center")
st.write("### Predicting the Future of Biodiversity in US National Parks, using AI to monitor National Park health and the safety of at-risk species.")

st.set_page_config(page_title="Park Guardian AI", layout="wide", page_icon="🌲")

text_col1, text_col2 = st.columns(2)

with text_col1:
    st.header("About Our Project")
    st.write("""
        Park Guardian was made from the need to prevent harmful human-wildlife interactions in national parks.
        Using our national Park Service data, we can provide an accessible lens into the health of our natural
        heritage. 
    """)
    if st.button("Explore the Map"):
        st.switch_page("tabs/map.py")

with text_col2:
    st.header("Our Mission")
    st.write("""
        We hope to conserve the biodiversity of our national parks while keeping a safe place for people to enjoy
        the wonders of nature. 
        By using AI to predict which species are most at risk, we can help park rangers and conservationists
        prioritize their efforts and protect our wild spaces for generations to come.
    """)
    if st.button("Get Involved"):
        st.switch_page("tabs/cta.py")

_, image_col1, _, image_col2, _ = st.columns([0.2, 1, 0.4, 1, 0.2])

with image_col1:
    st.image("assets/homepage_photo.jpg", width="content", 
             caption="Protecting our Wild Spaces")

with image_col2:
    st.image("assets/yellowstone2.jpg", width="content", 
             caption="Protecting our Wild Spaces")

st.divider()
cols = st.columns(4)
cols[0].metric("Parks Covered", "56")
cols[1].metric("Species Tracked", "100,000+")
cols[2].metric("AI Accuracy", "89%")
cols[3].metric("Risk Species", "558 Active")
st.divider()

