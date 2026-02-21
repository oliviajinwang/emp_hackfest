import streamlit as st

# make sure to revise before submission

st.title("Home Page")
st.write("### Welcome to Park Guardian AI")

col1, col2 = st.columns(2)

with col1:
    st.header("About Our Project")
    st.write("""
        Park Guardian was made from the need to prevent harmful human-wildlife interactions in national parks.
        Using our national Park Service data, we can provide an accessible lens into the health of our natural
        heritage. 
    """)

with col2:
    st.header("Our Mission")
    st.write("""
        We hope to conserve the biodiversity of our national parks while keeping a safe place for people to enjoy
        the wonders of nature. 
    """)

