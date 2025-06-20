import streamlit as st

# Optional page config
st.set_page_config(
    page_title="My App Hub",
    page_icon="🌐",
    layout="centered"
)

# Style
st.markdown("""
    <style>
    .css-18e3th9 {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    .css-1d391kg {
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# Main page
st.markdown("""
    <div style="text-align: center;">
        <img src="assets/foxcodelogo.png" width="200"/>
        <h1>Welcome to My App Hub</h1>
        <h3>Select a project to explore:</h3>
    </div>
""", unsafe_allow_html=True)

st.markdown("---")

# Create links or buttons to other apps
col1, col2 = st.columns(2)

with col1:
#    st.markdown("### 📊 [Data Dashboard](https://your-dashboard-url.com)")
    st.markdown("### 🧙 [D&D Character Sheet](https://your-dnd-app-url.com)")

#with col2:
#    st.markdown("### 📧 [CSV Email Processor](https://your-email-tool.com)")
#    st.markdown("### 🌍 [Web Crawler Bot](https://your-webcrawler.com)")

st.markdown("---")

