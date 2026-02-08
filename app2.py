import streamlit as st
import time
from datetime import datetime, timedelta
import random

# 1. CONFIGURATION (Must be the first Streamlit command)
st.set_page_config(
    page_title="GreenFlow Hydroponics",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. CUSTOM STYLE INJECTION (The "Fancy" Part)
st.markdown("""
    <style>
    /* Import Premium Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@700&family=Open+Sans:wght@400;600&display=swap');

    /* Background: Green-White-Black Gradient */
    .stApp {
        background: linear-gradient(135deg, #e8f5e9 0%, #ffffff 50%, #121212 100%);
        background-attachment: fixed;
    }

    /* Headings: Bold, Professional Green */
    h1, h2, h3 {
        font-family: 'Montserrat', sans-serif !important;
        color: #2e7d32 !important;
        letter-spacing: -0.5px;
    }

    /* Description Text: Bold and Clean */
    .stMarkdown p, .plant-desc {
        font-family: 'Open Sans', sans-serif !important;
        font-weight: 600 !important;
        color: #333333;
    }

    /* Card Styling */
    div[data-testid="stVerticalBlock"] > div[style*="border: 1px solid"] {
        background-color: rgba(255, 255, 255, 0.9) !important;
        border-radius: 15px !important;
        border: 1px solid #e0e0e0 !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1) !important;
        padding: 20px !important;
    }

    /* Sidebar Customization */
    [data-testid="stSidebar"] {
        background-color: #000000 !important;
    }
    [data-testid="stSidebar"] * {
        color: #ffffff !important;
    }

    /* Metrics Styling */
    [data-testid="stMetricValue"] {
        font-family: 'Montserrat', sans-serif !important;
        color: #1b5e20 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# ... [Rest of your code: PLANTS_DB, PACKAGES, Session State, etc.] ...
