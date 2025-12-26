import streamlit as st
import random
import requests
import time

# ==========================================
# 1. CONFIGURATION & OMEGA THEME
# ==========================================
st.set_page_config(
    page_title="AKRITI OMEGA",
    page_icon="👑",
    layout="wide"
)

# THE FIX FOR INVISIBLE DROPDOWNS
st.markdown("""
<style>
    /* 1. GLOBAL TEXT & FONT */
    .stApp, p, h1, h2, h3, h4, h5, label, span, div {
        color: #ffffff !important;
        font-family: 'Inter', sans-serif;
    }

    /* 2. BACKGROUND: DEEP SPACE IMPERIAL */
    .stApp {
        background: linear-gradient(180deg, #020024 0%, #090979 35%, #00d4ff 100%);
        background-attachment: fixed;
    }

    /* 3. DROPDOWN MENU FIX (The Invisible Text Fix) */
    /* Forces the popup list to be Dark Blue so white text is visible */
    div[data-baseweb="popover"], div[data-baseweb="menu"], ul {
        background-color: #001f3f !important;
    }
    li[role="option"] {
        background-color: #001f3f !important;
        color: white !important;
    }
    /* The selected option in the closed box */
    div[data-baseweb="select"] > div {
        background-color: rgba(255,255,255,0.1) !important;
        color: white !important;
        border: 1px solid rgba(255,255,255,0.2);
    }

    /* 4. TABS STYLE */
    .stTabs [data-baseweb="tab-list"] {
        gap: 20px;
        background-color: rgba(0,0,0,0.3);
        padding: 15px;
        border-radius: 20px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: rgba(255,255,255,0.05);
        border-radius: 10px;
        border: 1px solid rgba(255,255,255,0.1);
        padding: 10px 30px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #00d4ff !important;
        color: #000000 !important; /* Black text on active tab */
        font-weight: bold;
    }

    /* 5. INPUTS & BUTTONS */
    .stTextInput > div > div > input {
        background-color: rgba(0,0,0,0.5) !important;
        color: white !important;
        border: 1px solid #00d4ff;
        border-radius: 10px;
    }
    div.stButton > button {
        background: linear-gradient(45deg, #FF0099, #493240);
        border: none;
        color: white;
        font-weight: bold;
        transition: 0.3s;
    }
    div.stButton > button:hover {
        transform: scale(1.02);
        box-shadow: 0 0 20px #FF0099;
    }

    /* HIDE JUNK */
    #MainMenu, footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. HELPER FUNCTIONS
# ==========================================
def fetch_image(url):
    try:
        r = requests.get(url, timeout=8)
        if r.status_code == 200: return r.content
    except: return None

def upload_to_pollinations(uploaded_file):
    try:
        files = {'file': uploaded_file.getvalue()}
        response = requests.post('https://image.pollinations.ai/upload', files=files)
        if response.status_code == 200: return response.text.strip()
    except: return None

# ==========================================
# 3. MAIN INTERFACE
# ==========================================
st.title("👑 AKRITI OMEGA")
st.markdown("### The Ultimate Visual Engine")

# TABS: CREATE vs REMIX
tab_create, tab_remix = st.tabs(["✨ CREATE (Text-to-Image)", "🌪️ REMIX (Photo Editor)"])

# ==========================================
# TAB 1: CREATE (The Control Deck)
# ==========================================
with tab_create:
    st.markdown("<br>", unsafe_allow_html=True)
    
    # CONTROL DECK
    with st.expander("🎛️ CONTROL DECK (Settings)", expanded=True):
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown("#### 🧠 Brain")
            model = st.selectbox("Model", ["Flux (Best)", "Flux-Realism", "Flux-Anime", "Flux-3D", "Turbo (Fast)"], label_visibility="collapsed")
            model_code = model.split(" ")[0].lower()
        with c2:
            st.markdown("#### 📐 Size")
            ratio = st.selectbox("Ratio", ["Square (1:1)", "Portrait (9:16)", "Landscape (16:9)", "Wide (21:9)"], label_visibility="collapsed")
            if "Square" in ratio: w, h = 1024, 1024
            elif "Portrait" in ratio: w, h = 768, 1344
            elif "Landscape" in ratio: w, h = 1344, 768
            elif "Wide" in ratio: w, h = 1536, 640
        with c3:
            st.markdown("#### 🎨 Style")
            style = st.selectbox("Style", ["None", "Cyberpunk", "Cinematic", "Oil Painting", "Pixar 3D", "Dark Fantasy"], label_visibility="collapsed")

    # INPUT AREA
    col_p, col_b = st.columns([4, 1])
    with col_p:
        prompt = st.text_input("Describe your vision...", placeholder="e.g. A golden temple in the clouds")
    with col_b:
        st.write("")
        st.write("")
        btn_gen = st.button("🚀 IGNITE", type="primary", use_container_width=True)

    # GENERATION LOGIC
    if btn_gen and prompt:
        final_prompt = prompt
        if style != "None": final_prompt += f", {style} style"
        
        url_prompt = final_prompt.replace(" ", "%20")
        seed = random.randint(0, 1000000)
        image_url = f"https://image.pollinations.ai/prompt/{url_prompt}?width={w}&height={h}&seed={seed}&nologo=true&model={model_code}"
        
        st.markdown(f"### ✨ Result: {style if style != 'None' else 'Custom'}")
        st.image(image_url, caption=f"{model} | {w}x{h}", use_container_width=True)
        
        with st.spinner("💾 Preparing Download..."):
            img_data = fetch_image(image_url)
            if img_data:
                st.download_button("⬇️ DOWNLOAD HD", data=img_data, file_name=f"akriti_{seed}.jpg", mime="image/jpeg", use_container_width=True)

# ==========================================
# TAB 2: REMIX (The Photo Editor)
# ==========================================
with tab_remix:
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_upload, col_settings = st.columns([1, 1])
    
    with col_upload:
        st.markdown("#### 1. Upload Photo")
        uploaded_file = st.file_uploader("", type=["jpg", "png", "jpeg"])
        if uploaded_file:
            st.image(uploaded_file, caption="Base Image", use_container_width=True)

    with col_settings:
        st.markdown("#### 2. Describe Changes")
        remix_prompt = st.text_input("What to change?", placeholder="e.g. Make me look like a cyborg")
        st.markdown("#### 3. AI Model")
        remix_model = st.selectbox("Remix Engine", ["Flux-Realism", "Flux-Anime", "Flux-3D"], index=0)
        
        st.write("")
        btn_remix = st.button("🌪️ REMIX PHOTO", type="primary", use_container_width=True)

    # REMIX LOGIC
    if btn_remix and uploaded_file and remix_prompt:
        with st.status("🌪️ Uploading & Processing...", expanded=True) as status:
            st.write("📤 Sending to Neural Cloud...")
            base_url = upload_to_pollinations(uploaded_file)
            
            if base_url:
                st.write("🎨 Applying Magic...")
                clean_p = remix_prompt.replace(" ", "%20")
                seed = random.randint(0, 1000000)
                # Remix URL (Note: Dimensions usually adapt to source image)
                remix_url = f"https://image.pollinations.ai/prompt/{clean_p}?image={base_url}&seed={seed}&nologo=true&model={remix_model.lower()}"
                
                status.update(label="REMIX COMPLETE", state="complete", expanded=False)
                
                st.image(remix_url, caption=f"Remix by Akriti", use_container_width=True)
                
                with st.spinner("💾 Fetching File..."):
                    remix_data = fetch_image(remix_url)
                    if remix_data:
                        st.download_button("⬇️ DOWNLOAD REMIX", data=remix_data, file_name=f"akriti_remix_{seed}.jpg", mime="image/jpeg", use_container_width=True)
            else:
                st.error("Upload Failed. Try a smaller image.")
