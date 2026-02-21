import streamlit as st
import json

st.title("Why Should You Care?")

st.write("""
        ### The Biodiversity Crisis in Our National Parks
        We are currently facing the 6th mass extinction, and national parks, which are supposed to be 
        sanctuaries for wildlife, are not immune. Climate change, invasive species, and human interference 
        are pushing many species to the brink of extinction. 
    """)

st.info("### Join the Guardian Network")
st.write("""
            Whether you're a park ranger, a local resident, or just a nature enthusiast, your contribution matters.
        """)

email = st.text_input("Enter your email to get conservation alerts")
if st.button("Become a Guardian"):
    st.success(f"Thank you for joining the Guardian Network! Alerts will be sent to {email}.")
    with open("data/emails.jsonl", "a") as f:
        f.write(json.dumps({"email": email}) + "\n")
