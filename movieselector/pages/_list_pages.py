import streamlit as st
import os

st.title("Detected pages in 'pages/' folder:")

pages_dir = os.path.dirname(__file__)
page_files = [f for f in os.listdir(pages_dir) if f.endswith(".py") and not f.startswith("_")]

for page in page_files:
    st.write(page)
