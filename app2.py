aimport streamlit as st
import time
from datetime import datetime, timedelta
import random

# ==========================================
# 1. CONFIGURATION (MUST BE FIRST)
# ==========================================
st.set_page_config(
    page_title="GreenFlow",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Data: Plant Knowledge Base ---
PLANTS_DB = {
    "cherry_tomatoes": {"name": "Cherry Tomatoes", "days_to_harvest": 60, "icon": "🍅", "ph": "5.8-6.5", "tips": "Needs support stakes."},
    "spinach": {"name": "Spinach", "days_to_harvest": 40, "icon": "🥬", "ph": "6.0-7.0", "tips": "Harvest outer leaves first."},
    "lettuce": {"name": "Lettuce", "days_to_harvest": 30, "icon": "🥗", "ph": "5.5-6.5", "tips": "Keep water temp below 24°C."},
    "strawberry": {"name": "Strawberry", "days_to_harvest": 90, "icon": "🍓", "ph": "5.5-6.5", "tips": "Hand pollination required."},
    "basil": {"name": "Basil", "days_to_harvest": 25, "icon": "🌿", "ph": "5.5-6.5", "tips": "Harvest to prevent flowering."}
}

PACKAGES = {
    'starter': {'name': 'Starter Kit', 'price': 9999, 'plants_count': 4, 'area': '2x2 ft', 'desc': 'Perfect for beginners.'},
    'professional': {'name': 'Professional Setup', 'price': 24999, 'plants_count': 12, 'area': '4x4 ft', 'desc': 'High-yield system.'},
    'commercial': {'name': 'Commercial System', 'price': 59999, 'plants_count': 30, 'area': '8x8 ft', 'desc': 'IoT monitoring.'}
}

# ==========================================
# 2. CUSTOM STYLE INJECTION
# ==========================================
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;700&display=swap');

    /* --- MAIN APP AREA --- */
    .stApp { background: #FFFFFF !important; }
    
    /* Force dark text for all UI elements (Fixes Settings invisibility) */
    html, body, [data-testid="stMarkdownContainer"] p, .stCheckbox label, .stMarkdown, label {
        font-family: 'Outfit', sans-serif !important;
        color: #2D3436 !important;
    }

    /* Cards with Subtle Border */
    div[data-testid="stVerticalBlock"] > div[style*="border: 1px solid"] {
        background-color: #ffffff !important;
        border: 1px solid #d1d8e0 !important;
        border-radius: 12px !important;
        padding: 20px !important;
        transition: all 0.3s ease;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05) !important;
    }

    div[data-testid="stVerticalBlock"] > div[style*="border: 1px solid"]:hover {
        border: 1px solid #4CAF50 !important;
        box-shadow: 0 8px 16px rgba(0,0,0,0.08) !important;
    }

    h1, h2, h3 {
        font-family: 'Outfit', sans-serif !important;
        color: #1B5E20 !important;
    }

    /* --- SIDEBAR (Pure Black) --- */
    [data-testid="stSidebar"] { background-color: #000000 !important; }
    [data-testid="stSidebar"] *:not(span):not(i) {
        color: #FFFFFF !important;
        font-family: 'Outfit', sans-serif !important;
    }
    [data-testid="stIconMaterial"] { font-family: 'Material Symbols Outlined' !important; }

    /* Metric Visuals */
    [data-testid="stMetricValue"] { color: #1B5E20 !important; font-weight: 700 !important; }
    [data-testid="stMetricLabel"] { color: #636e72 !important; }

    .block-container { padding-top: 2rem !important; }
    [data-testid="stHeader"] { background: transparent; }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 3. SESSION STATE
# ==========================================
if 'user_garden' not in st.session_state:
    st.session_state.user_garden = [
        {"type": "cherry_tomatoes", "planted_at": datetime.now() - timedelta(days=45)},
        {"type": "lettuce", "planted_at": datetime.now() - timedelta(days=10)},
        {"type": "basil", "planted_at": datetime.now() - timedelta(days=20)},
    ]

# ==========================================
# 4. SIDEBAR NAVIGATION
# ==========================================
with st.sidebar:
    st.markdown("""
        <div style="margin-bottom: 20px;">
            <h2 style='color:#4CAF50 !important; margin-bottom: 0;'>🌿 GreenFlow</h2>
            <p style='color: #FFFFFF !important; font-weight: 400; font-size: 0.85rem; opacity: 0.8; margin-top: -5px;'>
                PREMIUM HYDROPONICS OS
            </p>
        </div>
    """, unsafe_allow_html=True)
    st.divider()
    menu = st.radio("MAIN MENU", ["Dashboard", "My Garden", "Store", "AI Expert", "Settings"])
    st.markdown("---")
    st.markdown("<small style='opacity:0.5;'>v2.0.4 Stable</small>", unsafe_allow_html=True)

# ==========================================
# 5. PAGE ROUTING
# ==========================================

if menu == "Dashboard":
    # Updated Header
    st.markdown('<p style="color:#4CAF50; font-weight:700; letter-spacing:2px; margin-bottom:0;">SYSTEM ACTIVE</p>', unsafe_allow_html=True)
    st.markdown('# SYSTEM OVERVIEW', unsafe_allow_html=True)

    # Intelligence Components Grid
    with st.container():
        col1, col2, col3, col4 = st.columns(4)
        with col1: st.metric("Temperature", "24°C", "1.2°C")
        with col2: st.metric("Humidity", "65%", "-2%")
        with col3: st.metric("Water pH", "6.2", "OK")
        with col4: st.metric("TDS / EC", "850 ppm", "Normal")

    st.markdown("### 🔔 Live Intelligence Alerts")
    st.warning("Tank water level is at 40%. Consider refilling in 2 days.")
    
    st.markdown("### 📈 Real-time Growth Metrics")
    st.line_chart({"Week": [1, 2, 3, 4], "Height (cm)": [5, 12, 18, 25]}, x="Week", y="Height (cm)")

elif menu == "My Garden":
    st.markdown("<h1>🌱 My Garden Status</h1>", unsafe_allow_html=True)
    
    # Grid Layout for Plants
    grid_cols = st.columns(3)
    for i, plant in enumerate(st.session_state.user_garden):
        plant_info = PLANTS_DB.get(plant['type'], {})
        days_passed = (datetime.now() - plant['planted_at']).days
        total_days = plant_info.get('days_to_harvest', 60)
        progress = min(1.0, days_passed / total_days)
        
        with grid_cols[i % 3]:
            with st.container(border=True):
                st.markdown(f"### {plant_info.get('icon')} {plant_info.get('name')}")
                st.progress(progress)
                st.write(f"Day **{days_passed}** of {total_days}")
                if progress >= 1.0: st.success("Ready to Harvest!")
                with st.expander("Care Intelligence"):
                    st.write(f"**Target pH:** {plant_info.get('ph')}")
                    st.write(plant_info.get('tips'))

elif menu == "Store":
    st.markdown("<h1>🛒 Subscription Kits</h1>", unsafe_allow_html=True)
    cols = st.columns(3)
    for idx, (key, pkg) in enumerate(PACKAGES.items()):
        with cols[idx]:
            with st.container(border=True):
                st.header(pkg['name'])
                st.subheader(f"₹{pkg['price']:,}")
                st.write(f"**Setup Details:** {pkg['desc']}")
                st.button(f"Purchase {pkg['name']}", key=f"btn_{key}")

elif menu == "AI Expert":
    st.markdown("<h1>🤖 AI Expert Assistant</h1>", unsafe_allow_html=True)
    st.info("Direct access to GreenFlow's growth intelligence database.")
    # Chat logic here...

elif menu == "Settings":
    st.markdown("<h1>⚙️ Account Settings</h1>", unsafe_allow_html=True)
    
    # Bordered container ensures dark text contrast on white background
    with st.container(border=True):
        st.write("### User Profile & Preferences")
        st.write("**Account Holder:** Demo User")
        st.write("**Registered Email:** demo@greenflow.com")
        
        st.markdown("---")
        st.checkbox("Receive weekly plant care tips via email", value=True)
        st.checkbox("Enable SMS alerts for water levels", value=False)
        
    if st.button("Reset Application Data"):
        st.session_state.clear()
        st.rerun()
