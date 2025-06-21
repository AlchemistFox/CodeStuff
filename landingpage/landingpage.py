import streamlit as st
import os

# Set up the page
st.set_page_config(page_title="My App Hub", page_icon="🌐", layout="centered")

# Get the full path to the logo
BASE_DIR = os.path.dirname(__file__)
logo_path = os.path.join(BASE_DIR, "foxcodelogo.png")

# Read and encode the image to embed it properly
import base64

def get_image_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

image_base64 = get_image_base64(logo_path)

# Display everything centered using raw HTML
st.markdown(f"""
    <div style="text-align: center;">
        <img src="data:image/png;base64,{image_base64}" width="200"/>
        <h1 style="margin-top: 0;">Welcome to My App Hub</h1>
        <h3>Select a project to explore:</h3>
    </div>
""", unsafe_allow_html=True)

st.markdown("---")

# App links in two columns
#col1, col2 = st.columns(2)
col1, = st.columns(1)

with col1:
    st.markdown("### 🧙 [D&D Character Sheet](https://your-dnd-app-url.com)")
#    st.markdown("### 🛒 [Price Comparison App](https://your-pricing-app-url.com)")

#with col2:
#    st.markdown("### 🛒 [Price Comparison App](https://your-pricing-app-url.com)")

    st.markdown("---")
