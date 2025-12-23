# app.py
import streamlit as st
from scraper import run

st.set_page_config(page_title="Business Intelligence Scraper", layout="wide")

st.title("Company Intelligence Scraper")
st.write("Enter a company website URL to extract structured business data.")

url = st.text_input(
    "Website URL",
    placeholder="https://example.com"
)

if st.button("Run Scraper"):
    if not url:
        st.warning("Please enter a valid website URL.")
    else:
        with st.spinner("Scraping website..."):
            result = run(url)

        st.success("Scraping completed")

        st.subheader("Structured Company Profile")
        st.json(result)
