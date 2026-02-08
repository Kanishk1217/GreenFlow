# ==========================================
# 1.5 CUSTOM STYLING (CSS)
# ==========================================
st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Inter:wght@400;600&display=swap');

    /* Main Background: Green to Black/White Gradient */
    .stApp {
        background: linear-gradient(135deg, #f0fdf4 0%, #ffffff 50%, #1a1c1a 100%);
        background-attachment: fixed;
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #0d1117;
        border-right: 1px solid #2e7d32;
    }

    /* Heading Fonts */
    h1, h2, h3 {
        font-family: 'Playfair Display', serif !important;
        color: #1b5e20 !important;
        font-weight: 700 !important;
    }

    /* Body and Description Fonts */
    p, span, label, .stMarkdown {
        font-family: 'Inter', sans-serif !important;
        color: #2c3e50;
    }

    /* Bold Descriptions */
    .description-text {
        font-weight: 600;
        color: #1a1a1a;
    }

    /* Custom Card Styling for "My Garden" and "Store" */
    div[data-testid="stVerticalBlock"] > div[style*="border: 1px solid"] {
        background-color: rgba(255, 255, 255, 0.8) !important;
        border: 2px solid #e0e0e0 !important;
        border-radius: 15px !important;
        padding: 20px !important;
        transition: transform 0.3s ease;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    }
    
    div[data-testid="stVerticalBlock"] > div[style*="border: 1px solid"]:hover {
        transform: translateY(-5px);
        border-color: #4caf50 !important;
        box-shadow: 0 10px 20px rgba(76, 175, 80, 0.2);
    }

    /* Buttons Styling */
    .stButton>button {
        background-color: #2e7d32 !important;
        color: white !important;
        border-radius: 8px !important;
        border: none !important;
        font-weight: 600 !important;
        padding: 0.5rem 2rem !important;
    }
    
    .stButton>button:hover {
        background-color: #1b5e20 !important;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    </style>
    """, unsafe_allow_html=True)
