import streamlit as st
import time
from datetime import datetime, timedelta
import random

# ==========================================
# 1. CONFIGURATION & ASSETS
# ==========================================
st.set_page_config(
    page_title="GreenFlow",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Merged Data: Plant Knowledge Base ---
PLANTS_DB = {
    "cherry_tomatoes": {
        "name": "Cherry Tomatoes",
        "days_to_harvest": 60,
        "icon": "🍅",
        "ph": "5.8-6.5",
        "tips": "Needs support stakes. Prune suckers for better yield."
    },
    "spinach": {
        "name": "Spinach",
        "days_to_harvest": 40,
        "icon": "🥬",
        "ph": "6.0-7.0",
        "tips": "Harvest outer leaves first to extend growth cycle."
    },
    "lettuce": {
        "name": "Lettuce",
        "days_to_harvest": 30,
        "icon": "🥗",
        "ph": "5.5-6.5",
        "tips": "Sensitive to heat. Keep water temp below 24°C."
    },
    "strawberry": {
        "name": "Strawberry",
        "days_to_harvest": 90,
        "icon": "🍓",
        "ph": "5.5-6.5",
        "tips": "Hand pollination may be required indoors."
    },
    "basil": {
        "name": "Basil",
        "days_to_harvest": 25,
        "icon": "🌿",
        "ph": "5.5-6.5",
        "tips": "Harvest frequently to prevent flowering."
    }
}

# --- Merged Data: Packages ---
PACKAGES = {
    'starter': {
        'name': 'Starter Kit (Balcony)',
        'price': 9999,
        'plants_count': 4,
        'area': '2x2 ft',
        'desc': 'Perfect for beginners. Includes pump, reservoir, and nutrients.'
    },
    'professional': {
        'name': 'Professional Setup',
        'price': 24999,
        'plants_count': 12,
        'area': '4x4 ft',
        'desc': 'High-yield system with automated lighting control.'
    },
    'commercial': {
        'name': 'Commercial System',
        'price': 59999,
        'plants_count': 30,
        'area': '8x8 ft',
        'desc': 'Full-scale farm setup with IoT monitoring capabilities.'
    }
}

# --- Merged Data: Chatbot Logic ---
BOT_RESPONSES = {
    'hello': 'Hello! Welcome to GreenFlow. How can I help you grow today?',
    'water': 'For , maintain pH between 5.5-6.5. Change water every 3-4 weeks.',
    'light': 'Most plants need 12-16 hours of LED light daily. Keep lights 12-24 inches away.',
    'ph': 'Ideal pH is usually 5.8-6.5. If too high, use pH Down; if too low, use pH Up.',
    'pest': 'Use organic neem oil spray. Ensure good air circulation to prevent mold.',
    'cost': 'Starter kits begin at ₹9,999. Check the "Store" tab for details.',
    'default': 'That is a great question! I recommend booking a consultation with our experts for specific advice.'
}

# ==========================================
# 2. SESSION STATE MANAGEMENT
# ==========================================
# Initialize "In-Memory Database"
if 'users_db' not in st.session_state:
    st.session_state.users_db = {"demo@greenflow.com": {"name": "Demo User", "password": "password123", "subscription": False}}
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'current_user' not in st.session_state:
    st.session_state.current_user = None
if 'user_garden' not in st.session_state:
    # Pre-populate with some data for demo
    st.session_state.user_garden = [
        {"type": "cherry_tomatoes", "planted_at": datetime.now() - timedelta(days=45)},
        {"type": "lettuce", "planted_at": datetime.now() - timedelta(days=10)},
        {"type": "basil", "planted_at": datetime.now() - timedelta(days=20)},
    ]
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = [{"role": "assistant", "content": "Hi! Ask me anything about your setup."}]

# ==========================================
# 3. HELPER FUNCTIONS
# ==========================================
def login_user(email, password):
    user = st.session_state.users_db.get(email)
    if user and user['password'] == password:
        st.session_state.logged_in = True
        st.session_state.current_user = user
        st.success("Login successful!")
        time.sleep(0.5)
        st.rerun()
    else:
        st.error("Invalid email or password")

def register_user(email, name, password):
    if email in st.session_state.users_db:
        st.error("User already exists!")
    else:
        st.session_state.users_db[email] = {"name": name, "password": password, "subscription": False}
        st.success("Account created! Please log in.")

def get_bot_response(user_input):
    user_input = user_input.lower()
    for key, response in BOT_RESPONSES.items():
        if key in user_input:
            return response
    return BOT_RESPONSES['default']

# ==========================================
# 4. MAIN UI LAYOUT
# ==========================================

# --- Sidebar Navigation ---
st.sidebar.title("🌿 GreenFlow")
if st.session_state.logged_in:
    st.sidebar.write(f"Welcome, **{st.session_state.current_user['name']}**!")
    menu = st.sidebar.radio("Navigate", ["Dashboard", "My Garden", "Store", "AI Expert", "Consultation", "Settings"])
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.current_user = None
        st.rerun()
else:
    menu = "Login"

# --- Page: LOGIN / REGISTER ---
if menu == "Login":
    st.title("Welcome to GreenFlow")
    st.subheader("Smart Farming for Urban Spaces")
    
    tab1, tab2 = st.tabs(["Login", "Register"])
    
    with tab1:
        with st.form("login_form"):
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Login")
            if submitted:
                login_user(email, password)
        st.info("Demo Account: demo@greenflow.com / password123")

    with tab2:
        with st.form("register_form"):
            new_name = st.text_input("Full Name")
            new_email = st.text_input("Email")
            new_pass = st.text_input("Password", type="password")
            reg_submitted = st.form_submit_button("Register")
            if reg_submitted:
                if new_name and new_email and new_pass:
                    register_user(new_email, new_name, new_pass)
                else:
                    st.warning("All fields are required.")

# --- Page: DASHBOARD ---
elif menu == "Dashboard":
    st.title("📊 System Overview")
    
    # Mock Sensor Data
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Temperature", "24°C", "1.2°C")
    with col2:
        st.metric("Humidity", "65%", "-2%")
    with col3:
        st.metric("Water pH", "6.2", "OK")
    with col4:
        st.metric("TDS / EC", "850 ppm", "Normal")

    st.markdown("### 🔔 Alerts")
    st.warning("⚠️ Tank water level is at 40%. Consider refilling in 2 days.")
    
    st.markdown("### 📈 Growth Trends")
    # Simple chart
    chart_data = {"Week": [1, 2, 3, 4], "Height (cm)": [5, 12, 18, 25]}
    st.line_chart(chart_data, x="Week", y="Height (cm)")

# --- Page: MY GARDEN ---
elif menu == "My Garden":
    st.title("🌱 My Garden Status")
    
    if not st.session_state.user_garden:
        st.info("Your garden is empty. Visit the Store to get started!")
    else:
        grid_cols = st.columns(3)
        for i, plant in enumerate(st.session_state.user_garden):
            plant_info = PLANTS_DB.get(plant['type'], {})
            
            # Calculate progress
            days_passed = (datetime.now() - plant['planted_at']).days
            total_days = plant_info.get('days_to_harvest', 60)
            progress = min(1.0, days_passed / total_days)
            
            with grid_cols[i % 3]:
                with st.container(border=True):
                    st.markdown(f"### {plant_info.get('icon', '🌱')} {plant_info.get('name', 'Unknown')}")
                    st.progress(progress, text=f"{days_passed}/{total_days} Days")
                    
                    if progress >= 1.0:
                        st.success("🎉 Ready to Harvest!")
                    else:
                        st.caption(f"Harvest in approx. {total_days - days_passed} days")
                    
                    with st.expander("Care Tips"):
                        st.write(f"**pH Range:** {plant_info.get('ph')}")
                        st.write(plant_info.get('tips'))

        # Add new plant interface
        st.markdown("---")
        st.subheader("Add New Plant")
        with st.form("add_plant"):
            new_plant_type = st.selectbox("Select Plant Type", list(PLANTS_DB.keys()), format_func=lambda x: PLANTS_DB[x]['name'])
            if st.form_submit_button("Plant Seed"):
                st.session_state.user_garden.append({
                    "type": new_plant_type,
                    "planted_at": datetime.now()
                })
                st.success(f"Added {PLANTS_DB[new_plant_type]['name']} to your garden!")
                time.sleep(1)
                st.rerun()

# --- Page: STORE ---
elif menu == "Store":
    st.title("🛒 Subscription Kits")
    st.write("Choose a package to start your sustainable farming journey.")
    
    cols = st.columns(3)
    for idx, (key, pkg) in enumerate(PACKAGES.items()):
        with cols[idx]:
            with st.container(border=True):
                st.header(pkg['name'])
                st.subheader(f"₹{pkg['price']:,}")
                st.write(f"**Plants:** {pkg['plants_count']}")
                st.write(f"**Area:** {pkg['area']}")
                st.write(pkg['desc'])
                if st.button(f"Buy {pkg['name']}", key=key):
                    st.balloons()
                    st.success(f"Thank you! The {pkg['name']} will be shipped to your address.")

# --- Page: AI EXPERT ---
elif menu == "AI Expert":
    st.title("🤖 GreenFlow Assistant")
    
    # Display chat history
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("Ask about pH, lighting, pests, or watering..."):
        # User message
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Bot response
        time.sleep(0.5) # Simulate thinking
        response_text = get_bot_response(prompt)
        
        st.session_state.chat_history.append({"role": "assistant", "content": response_text})
        with st.chat_message("assistant"):
            st.markdown(response_text)

# --- Page: CONSULTATION ---
elif menu == "Consultation":
    st.title("📞 Book an Expert")
    st.write("Need hands-on help? Schedule a visit.")
    
    with st.form("consultation_form"):
        c_name = st.text_input("Name", value=st.session_state.current_user['name'])
        c_phone = st.text_input("Phone Number")
        c_date = st.date_input("Preferred Date")
        c_reason = st.text_area("What do you need help with?")
        
        if st.form_submit_button("Book Appointment"):
            st.success("Booking Confirmed! Our team will contact you within 24 hours.")
            st.info(f"Ref ID: GF-{random.randint(1000,9999)}")

# --- Page: SETTINGS ---
elif menu == "Settings":
    st.title("⚙️ Account Settings")
    st.write(f"**Email:** {st.session_state.current_user.get('email', 'N/A')}")
    st.write(f"**Member Since:** {datetime.now().strftime('%B %Y')}")
    
    st.checkbox("Receive weekly plant care tips via email", value=True)
    st.checkbox("Enable SMS alerts for water levels", value=False)
    
    if st.button("Clear App Data (Reset Demo)"):
        st.session_state.clear()
        st.rerun()
# 1. CONFIGURATION (Must be the first Streamlit command)
st.set_page_config(
    page_title="GreenFlow",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. CUSTOM STYLE INJECTION (The "Fancy" Part)

import streamlit as st

# 1. Setup
st.set_page_config(layout="wide", page_title="GreenFlow | Premium Hydroponics")

# 2. Final Polished Styling
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;700&display=swap');

    /* --- MAIN APP AREA --- */
    .stApp { background: #FFFFFF !important; }
    
    html, body, [data-testid="stMarkdownContainer"] p {
        font-family: 'Outfit', sans-serif !important;
        color: #2D3436 !important;
    }

    .glass-card {
        background: #FFFFFF;
        border: 1px solid #E0E0E0;
        border-radius: 16px;
        padding: 25px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        margin-bottom: 20px;
    }

    h1, h2, h3 {
        font-family: 'Outfit', sans-serif !important;
        color: #1B5E20 !important;
    }

    /* --- SIDEBAR RE-DESIGN (Pure Black & High Contrast) --- */
    [data-testid="stSidebar"] {
        background-color: #000000 !important;
    }

    /* Target EVERY piece of text in the sidebar to be White */
    [data-testid="stSidebar"] *, 
    [data-testid="stSidebar"] p, 
    [data-testid="stSidebar"] small, 
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] div {
        color: #FFFFFF !important;
        font-family: 'Outfit', sans-serif !important;
    }

    /* Specifically target the radio button labels which often stay grey */
    [data-testid="stWidgetLabel"] p {
        color: #FFFFFF !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
    }

    /* Sidebar Divider */
    hr { border-top: 1px solid #333 !important; }

    /* Metric Styling */
    [data-testid="stMetricValue"] { color: #1B5E20 !important; font-weight: 700 !important; }

    /* Header padding */
    .block-container { padding-top: 2rem !important; }
    [data-testid="stHeader"] { background: transparent; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR CONTENT (Fixed Double Title) ---
# Removed st.markdown("# 🌿 GreenFlow") from here to avoid the double title
with st.sidebar:
    st.markdown("<p style='opacity:0.8; font-size:0.9rem;'>Premium Hydroponics OS</p>", unsafe_allow_html=True)
    st.divider()
    
    # Navigation
    menu = st.radio("MAIN MENU", ["Dashboard", "My Garden", "Store", "AI Expert", "Settings"])
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("<small>System Version 2.0.4</small>", unsafe_allow_html=True)

# --- MAIN PAGE CONTENT ---
st.markdown('<p style="color:#4CAF50; font-weight:700; letter-spacing:2px;">SYSTEM ONLINE</p>', unsafe_allow_html=True)
st.markdown('# GREENFLOW <span style="font-weight:300">INTELLIGENCE</span>', unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    st.markdown("""
    <div class="glass-card">
        <h3>🌱 Crop Health</h3>
        <p>Your cherry tomatoes are in the <b>flowering stage</b>. Light exposure is optimal.</p>
        <small style="color:#666;">Next Nutrient Flush: 2 Days</small>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown('<div class="glass-card"><h3>📊 Environment</h3>', unsafe_allow_html=True)
    st.metric("Room Temp", "24.5°C", "0.5°C")
    st.metric("Humidity", "62%", "-1%")
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="glass-card">
        <h3>🛡️ Alerts</h3>
        <p style="margin:0;">✅ Sensors: Active</p>
        <p style="margin:0;">✅ pH: 6.2</p>
        <p style="margin:0; color:#d32f2f; font-weight:bold;">⚠️ Reservoir: 40%</p>
    </div>
    """, unsafe_allow_html=True)
    /* --- SIDEBAR RE-DESIGN --- */
    [data-testid="stSidebar"] {
        background-color: #000000 !important;
    }

    /* Target text but EXCLUDE icons (Material Symbols) */
    [data-testid="stSidebar"] *:not(span[data-testid="stIconMaterial"]), 
    [data-testid="stSidebar"] p, 
    [data-testid="stSidebar"] label {
        color: #FFFFFF !important;
        font-family: 'Outfit', sans-serif !important;
    }

    /* Keep icons as the default Icon Font so they render correctly */
    [data-testid="stIconMaterial"] {
        font-family: 'Material Symbols Outlined' !important;
        color: #FFFFFF !important;
    }
