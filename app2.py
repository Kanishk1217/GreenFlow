import streamlit as st
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

# ==========================================
# 2. DATA & ASSETS
# ==========================================
PLANTS_DB = {
    "cherry_tomatoes": {"name": "Cherry Tomatoes", "days_to_harvest": 60, "icon": "🍅", "ph": "5.8-6.5", "tips": "Needs support stakes."},
    "spinach": {"name": "Spinach", "days_to_harvest": 40, "icon": "🥬", "ph": "6.0-7.0", "tips": "Harvest outer leaves first."},
    "lettuce": {"name": "Lettuce", "days_to_harvest": 30, "icon": "🥗", "ph": "5.5-6.5", "tips": "Keep water temp below 24°C."},
    "strawberry": {"name": "Strawberry", "days_to_harvest": 90, "icon": "🍓", "ph": "5.5-6.5", "tips": "Hand pollination required."},
    "basil": {"name": "Basil", "days_to_harvest": 25, "icon": "🌿", "ph": "5.5-6.5", "tips": "Harvest to prevent flowering."}
}

PACKAGES = {
    'starter': {'name': 'Starter Kit', 'price': 9999, 'plants_count': 4, 'area': '2x2 ft', 'desc': 'Perfect for beginners. Includes pump, reservoir, and nutrients.'},
    'professional': {'name': 'Professional Setup', 'price': 24999, 'plants_count': 12, 'area': '4x4 ft', 'desc': 'High-yield system with automated lighting control.'},
    'commercial': {'name': 'Commercial System', 'price': 59999, 'plants_count': 30, 'area': '8x8 ft', 'desc': 'Full-scale farm setup with IoT monitoring capabilities.'}
}

BOT_RESPONSES = {
    'hello': 'Hello! I am the GreenFlow AI. How is your garden growing?',
    'ph': 'Ideal pH is usually 5.8-6.5. If too high, use pH Down.',
    'water': 'Maintain pH between 5.5-6.5. Change water every 3-4 weeks.',
    'cost': 'Starter kits begin at ₹9,999. Check the Store tab.',
    'default': 'I can help with pH, lighting, or pests. What do you need?'
}

def get_bot_response(user_input):
    user_input = user_input.lower()
    for key, response in BOT_RESPONSES.items():
        if key in user_input: return response
    return BOT_RESPONSES['default']

# ==========================================
# 3. CSS STYLING (FIXED VISIBILITY & BORDERS)
# ==========================================
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;700&display=swap');

    /* --- MAIN APP BACKGROUND --- */
    .stApp { background: #FFFFFF !important; }
    
    /* --- TEXT VISIBILITY FIX (Global Dark Text for appropriate elements) --- */
    /* This forces paragraphs, headers, and labels to be dark grey, excluding buttons */
    html, body, p, label, .stMarkdown, .stCheckbox, span, .stWrite {
        font-family: 'Outfit', sans-serif !important;
        color: #2D3436 !important;
    }
    
    /* --- BUTTON STYLING FIX (White text on dark background) --- */
    /* Purchase Now buttons and Reset button styling */
    button[kind="secondary"] {
        color: #FFFFFF !important;
        background-color: #1B5E20 !important;
        border: 1px solid #1B5E20 !important;
    }
    
    button[kind="secondary"]:hover {
        background-color: #145A1F !important;
        border: 1px solid #145A1F !important;
    }
    
    /* Streamlit button container fix */
    .stButton > button {
        color: #FFFFFF !important;
        background-color: #1B5E20 !important;
        border: 1px solid #1B5E20 !important;
        font-weight: 600 !important;
        padding: 12px 24px !important;
    }
    
    .stButton > button:hover {
        background-color: #145A1F !important;
        border: 1px solid #145A1F !important;
    }
    
    .stButton > button:active {
        background-color: #0D3A14 !important;
    }

    /* Exceptions: Sidebar text and Metrics need specific colors */
    [data-testid="stSidebar"] * { color: #FFFFFF !important; }
    [data-testid="stMetricValue"] { color: #1B5E20 !important; }
    [data-testid="stMetricLabel"] { color: #636e72 !important; }

    /* --- CARD BORDER STYLING --- */
    /* Targets any container with border=True */
    div[data-testid="stVerticalBlock"] > div[style*="border"] {
        background-color: #ffffff !important;
        border: 1px solid #d1d8e0 !important;
        border-radius: 12px !important;
        padding: 20px !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05) !important;
        transition: transform 0.2s ease;
    }

    div[data-testid="stVerticalBlock"] > div[style*="border"]:hover {
        border: 1px solid #4CAF50 !important;
        transform: translateY(-3px);
        box-shadow: 0 10px 15px rgba(0,0,0,0.1) !important;
    }

    /* --- HEADINGS --- */
    h1, h2, h3 { color: #1B5E20 !important; }

    /* --- SIDEBAR --- */
    [data-testid="stSidebar"] { background-color: #000000 !important; }
    [data-testid="stIconMaterial"] { font-family: 'Material Symbols Outlined' !important; } /* Fix Icon */

    /* --- CHAT MESSAGE STYLING (MINIMAL - LET STREAMLIT HANDLE SPACING) --- */
    /* Keep CSS minimal - use Streamlit components for spacing */
    .stChatMessage {
        font-family: 'Outfit', sans-serif !important;
    }
    
    .stChatMessage > div > p, .stChatMessage > div > span {
        color: #2D3436 !important;
        line-height: 1.6 !important;
        word-wrap: break-word !important;
    }

    /* Padding Fix */
    .block-container { padding-top: 2rem !important; }
    [data-testid="stHeader"] { background: transparent; }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 4. SESSION STATE
# ==========================================
if 'user_garden' not in st.session_state:
    st.session_state.user_garden = [
        {"type": "cherry_tomatoes", "planted_at": datetime.now() - timedelta(days=45)},
        {"type": "lettuce", "planted_at": datetime.now() - timedelta(days=10)},
    ]
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = [{"role": "assistant", "content": "Hello! Ask me about your setup."}]

# ==========================================
# 5. SIDEBAR NAVIGATION
# ==========================================
with st.sidebar:
    st.markdown("""
        <div style="margin-bottom: 20px;">
            <h2 style='color:#4CAF50 !important; margin-bottom: 0;'>🌿 GreenFlow</h2>
            <p style='color: #FFFFFF !important; font-weight: 400; font-size: 0.85rem; opacity: 0.8; margin-top: -5px;'>
                PREMIUM OS
            </p>
        </div>
    """, unsafe_allow_html=True)
    st.divider()
    menu = st.radio("MAIN MENU", ["System Overview", "My Garden", "Store", "AI Expert", "Settings"])
    st.markdown("---")
    st.markdown("<small style='opacity:0.5;'>v2.0.4 Stable</small>", unsafe_allow_html=True)

# ==========================================
# 6. PAGE ROUTING
# ==========================================

# --- SYSTEM OVERVIEW (DASHBOARD) ---
if menu == "System Overview":
    st.markdown('<p style="color:#4CAF50; font-weight:700; letter-spacing:2px; margin-bottom:0;">SYSTEM ACTIVE</p>', unsafe_allow_html=True)
    st.markdown('# SYSTEM OVERVIEW', unsafe_allow_html=True)

    # The Intelligence Components Section
    st.markdown("### 🧠 GreenFlow Intelligence Hub")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        with st.container(border=True): st.metric("Temperature", "24°C", "1.2°C")
    with col2:
        with st.container(border=True): st.metric("Humidity", "65%", "-2%")
    with col3:
        with st.container(border=True): st.metric("Water pH", "6.2", "OK")
    with col4:
        with st.container(border=True): st.metric("TDS / EC", "850 ppm", "Normal")

    st.markdown("### 🔔 Live Intelligence Alerts")
    st.warning("⚠️ Tank water level is at 40%. Intelligence suggests refilling within 48 hours.")
    
    st.markdown("### 📈 Growth Analytics")
    st.line_chart({"Week": [1, 2, 3, 4], "Height (cm)": [5, 12, 18, 25]}, x="Week", y="Height (cm)")

# --- MY GARDEN ---
elif menu == "My Garden":
    st.markdown("<h1>🌱 My Garden Status</h1>", unsafe_allow_html=True)
    
    # Existing Plants
    grid_cols = st.columns(3)
    for i, plant in enumerate(st.session_state.user_garden):
        plant_info = PLANTS_DB.get(plant['type'], {})
        days_passed = (datetime.now() - plant['planted_at']).days
        
        with grid_cols[i % 3]:
            # Added border=True to ensure the CSS border appears
            with st.container(border=True):
                st.markdown(f"### {plant_info.get('icon')} {plant_info.get('name')}")
                st.write(f"**Age:** {days_passed} Days")
                st.progress(min(1.0, days_passed / 60))
                st.caption(plant_info.get('tips'))

    # Add New Plant Section (Restored)
    st.markdown("---")
    st.markdown("### ➕ Add New Plant")
    with st.container(border=True):
        with st.form("add_plant_form"):
            col_a, col_b = st.columns([3, 1])
            with col_a:
                new_plant_type = st.selectbox("Select Plant Type", list(PLANTS_DB.keys()), format_func=lambda x: PLANTS_DB[x]['name'])
            with col_b:
                st.write("") # Spacer
                st.write("") # Spacer
                submitted = st.form_submit_button("Plant Seed 🌱")
            
            if submitted:
                st.session_state.user_garden.append({
                    "type": new_plant_type,
                    "planted_at": datetime.now()
                })
                st.success(f"Successfully planted {PLANTS_DB[new_plant_type]['name']}!")
                time.sleep(1)
                st.rerun()

# --- STORE ---
elif menu == "Store":
    st.markdown("<h1>🛒 Subscription Kits</h1>", unsafe_allow_html=True)
    cols = st.columns(3)
    for idx, (key, pkg) in enumerate(PACKAGES.items()):
        with cols[idx]:
            # Added border=True to ensure the CSS border appears
            with st.container(border=True):
                st.header(pkg['name'])
                st.subheader(f"₹{pkg['price']:,}")
                # Simple text box as requested (no switching/expanders)
                st.write(pkg['desc'])
                st.write(f"**Contains:** {pkg['plants_count']} plants")
                st.button(f"Purchase Now", key=f"btn_{key}", use_container_width=True)

# --- AI EXPERT ---
elif menu == "AI Expert":
    st.markdown("<h1>🤖 AI Expert Assistant</h1>", unsafe_allow_html=True)
    
    # Display chat history
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # FIX: Use STREAMLIT NATIVE SPACING COMPONENTS (not CSS margins!)
    st.write("")           # Creates actual vertical space
    st.divider()          # Creates actual horizontal line
    st.write("")          # Creates actual vertical space
    
    # Chat Input - placed AFTER spacing
    if prompt := st.chat_input("Ask about your garden or hydroponic system..."):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        time.sleep(0.5)
        response = get_bot_response(prompt)
        
        st.session_state.chat_history.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response)

# --- SETTINGS ---
elif menu == "Settings":
    st.markdown("<h1>⚙️ Account Settings</h1>", unsafe_allow_html=True)
    
    # Container with border to separate settings
    with st.container(border=True):
        st.markdown("### 👤 User Profile")
        st.text_input("Display Name", value="Demo User")
        st.text_input("Email Address", value="demo@greenflow.com")
        
        st.markdown("### 🔔 Preferences")
        # Text visibility is fixed via global CSS
        st.checkbox("Receive weekly plant care tips via email", value=True)
        st.checkbox("Enable SMS alerts for water levels", value=False)
        
    st.markdown("---")
    
    # Reset Button - with proper styling
    if st.button("Reset Application Data", use_container_width=True):
        st.session_state.clear()
        st.rerun()
