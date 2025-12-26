import streamlit as st
import random
import requests
import time

# ==========================================
# 1. CONFIGURATION & DARK THEME FIXES
# ==========================================
st.set_page_config(
    page_title="AKRITI SPEED",
    page_icon="⚡",
    layout="wide"
)

st.markdown("""
<style>
    /* 1. GLOBAL TEXT COLOR = WHITE */
    .stApp, p, h1, h2, h3, h4, label, span, div {
        color: #ffffff !important;
    }

    /* 2. MAIN BACKGROUND (Royal Blue) */
    .stApp {
        background: linear-gradient(135deg, #001f3f 0%, #003366 50%, #00509e 100%);
        background-attachment: fixed;
    }

    /* 3. SIDEBAR BACKGROUND (FIXED FOR WHITE MENU ISSUE) */
    section[data-testid="stSidebar"] {
        background-color: #001226 !important; /* Very Dark Blue */
        border-right: 1px solid #4da6ff;
    }
    
    /* Force Sidebar Text & Inputs to be Visible */
    section[data-testid="stSidebar"] p, section[data-testid="stSidebar"] span {
        color: #ffffff !important;
    }
    section[data-testid="stSidebar"] div[data-baseweb="select"] > div {
        background-color: rgba(255,255,255,0.1) !important;
        color: white !important;
    }

    /* 4. INPUT BOXES (Glass Style) */
    .stTextInput > div > div > input, .stNumberInput > div > div > input {
        background: rgba(0, 80, 158, 0.3) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        color: #ffffff !important;
        border-radius: 10px;
    }

    /* 5. BUTTONS */
    div.stButton > button {
        background: linear-gradient(90deg, #00c6ff, #0072ff);
        color: white;
        border: none;
        padding: 0.6rem 1.2rem;
        border-radius: 8px;
        font-weight: bold;
    }
    
    /* 6. STATUS BOX COLOR FIX */
    div[data-testid="stStatusWidget"] {
        background-color: #001f3f !important;
        border: 1px solid #4da6ff;
    }

    /* HIDE JUNK */
    #MainMenu, footer, header {visibility: hidden;}
    
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. HELPER FUNCTIONS
# ==========================================
def fetch_image_bytes(url):
    """Downloads image in background without freezing app"""
    try:
        response = requests.get(url, timeout=10) # 10s timeout to prevent hanging
        if response.status_code == 200:
            return response.content
        return None
    except:
        return None

# ==========================================
# 3. SIDEBAR (THE COCKPIT)
# ==========================================
with st.sidebar:
    st.title("⚙️ SETTINGS")
    
    # Model Selector
    st.markdown("### 🧠 AI Model")
    model_choice = st.selectbox(
        "Choose Engine:",
        ["Turbo (Fastest)", "Flux (Best Quality)", "Flux-Realism", "Flux-Anime", "Flux-3D"]
    )
    
    model_map = {
        "Turbo (Fastest)": "turbo",
        "Flux (Best Quality)": "flux",
        "Flux-Realism": "flux-realism",
        "Flux-Anime": "flux-anime",
        "Flux-3D": "flux-3d"
    }
    selected_model = model_map[model_choice]
    
    if selected_model == "turbo":
        st.success("⚡ Speed: ~3 Seconds")
    else:
        st.warning("🐢 Speed: ~15-30 Seconds")

    st.markdown("---")
    
    # Size
    width = st.slider("Width", 512, 2048, 1024, step=64)
    height = st.slider("Height", 512, 2048, 1024, step=64)
    
    st.markdown("---")
    # Seed
    use_random = st.checkbox("Random Seed", value=True)
    seed_input = st.number_input("Custom Seed", value=42, disabled=use_random)
    final_seed = random.randint(0, 1000000) if use_random else int(seed_input)

# ==========================================
# 4. MAIN SCREEN
# ==========================================
st.title("AKRITI SPEED")
st.markdown("### The Instant Imagination Engine")

# Input
col1, col2 = st.columns([4, 1])
with col1:
    prompt = st.text_input("Describe your vision...", placeholder="e.g. Iron Man in Bihar")
with col2:
    st.write("")
    st.write("")
    if st.button("✨ Enhance"):
        if prompt:
            prompt += ", 8k resolution, cinematic lighting, masterpiece"
            st.toast("✨ Prompt Enhanced!")

if st.button("🚀 GENERATE", type="primary"):
    if prompt:
        clean_prompt = prompt.replace(" ", "%20")
        
        # 1. SHOW LOADING
        with st.status("🎨 Starting Engine...", expanded=True) as status:
            st.write("📡 Connecting to Satellite...")
            
            # Construct URL
            image_url = f"https://image.pollinations.ai/prompt/{clean_prompt}?width={width}&height={height}&seed={final_seed}&nologo=true&model={selected_model}"
            
            # 2. INSTANT PREVIEW (Don't wait for download)
            st.write("⚡ Streaming Pixels...")
            status.update(label="STREAMING STARTED", state="complete", expanded=False)

        # Show the image via URL immediately (Browser handles loading)
        st.image(image_url, caption=f"Seed: {final_seed}", use_container_width=True)
        
        # 3. BACKGROUND DOWNLOAD (Optional)
        # We only try to fetch the file for the button AFTER showing the image
        with st.spinner("Preparing Download Link..."):
            img_data = fetch_image_bytes(image_url)
            
            if img_data:
                st.download_button(
                    label="⬇️ DOWNLOAD HD FILE",
                    data=img_data,
                    file_name=f"akriti_{final_seed}.jpg",
                    mime="image/jpeg"
                )
            else:
                st.warning("⚠️ Preview only (Download timed out, but you can screenshot!)")
                
    else:
        st.warning("⚠️ Enter a prompt first.")
