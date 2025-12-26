import streamlit as st
import random
import requests
import time
from groq import Groq 

# ==========================================
# 1. CONFIGURATION & THEME ENGINE
# ==========================================
st.set_page_config(
    page_title="AKRITI OMEGA",
    page_icon="👑",
    layout="wide"
)

# THE HIGH-CONTRAST CSS PATCH
st.markdown("""
<style>
    /* 1. GLOBAL FONT & COLOR */
    .stApp, p, h1, h2, h3, h4, h5, label, span, div, button, small {
        font-family: 'Inter', sans-serif;
        color: #ffffff !important;
    }

    /* 2. BACKGROUND: DEEP SPACE IMPERIAL GRADIENT */
    .stApp {
        background: linear-gradient(180deg, #020024 0%, #090979 35%, #00d4ff 100%);
        background-attachment: fixed;
    }

    /* =========================================
       3. CRITICAL UI VISIBILITY FIXES
       ========================================= */
    
    /* FIX 1: FILE UPLOADER (The "Invisible" Box Fix) */
    [data-testid="stFileUploader"] section {
        background-color: rgba(0, 31, 63, 0.8) !important; /* Dark Blue Background */
        border: 2px dashed #00d4ff;
        border-radius: 15px;
    }
    /* Force the small text inside uploader to be white */
    [data-testid="stFileUploader"] small {
        color: #e0e0e0 !important;
        opacity: 1 !important;
    }
    /* The button inside the uploader */
    [data-testid="stFileUploader"] button {
        background-color: rgba(255,255,255,0.1);
        border: 1px solid white;
    }

    /* FIX 2: INPUT PLACEHOLDERS (The "Camouflaged" Text Fix) */
    /* This makes the "e.g. Make me a cyborg" text visible */
    input::placeholder, textarea::placeholder {
        color: #cfcfcf !important; /* Bright Grey */
        opacity: 1 !important;
    }
    /* The input box itself */
    .stTextInput > div > div > input {
        background-color: rgba(0, 0, 0, 0.6) !important; /* Dark background */
        color: white !important; /* White typed text */
        border: 1px solid rgba(255,255,255,0.3);
    }

    /* FIX 3: DROPDOWN MENUS */
    /* Forces the popup list to be Dark Blue */
    div[data-baseweb="popover"], div[data-baseweb="menu"], ul {
        background-color: #001f3f !important;
    }
    li[role="option"] {
        background-color: #001f3f !important;
        color: white !important;
    }

    /* 4. COMPANY FOOTER */
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: rgba(0, 0, 0, 0.8);
        color: #888;
        text-align: center;
        padding: 10px;
        font-size: 12px;
        z-index: 999;
        pointer-events: none; /* Let clicks pass through */
    }

    /* HIDE STREAMLIT BRANDING */
    #MainMenu, footer, header {visibility: hidden;}
    
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. HELPER FUNCTIONS & AI BRAIN
# ==========================================

def get_groq_key():
    try: return st.secrets["GROQ_API_KEY"]
    except: return None

# --- Magic Expand (AI Prompting) ---
def expand_prompt_with_ai(short_prompt, api_key):
    if not short_prompt: return ""
    if not api_key: return "⚠️ API Key Missing."
    
    try:
        client = Groq(api_key=api_key)
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are an expert visual prompt engineer. Expand the user's short idea into a detailed, artistic image generation prompt. Keep it one paragraph."},
                {"role": "user", "content": f"Expand this idea: '{short_prompt}'"}
            ],
            temperature=0.7, max_tokens=300
        )
        return completion.choices[0].message.content
    except: return short_prompt

def fetch_image(url):
    try:
        r = requests.get(url, timeout=10)
        if r.status_code == 200: return r.content
    except: return None

def upload_to_pollinations(uploaded_file):
    try:
        files = {'file': uploaded_file.getvalue()}
        response = requests.post('https://image.pollinations.ai/upload', files=files)
        if response.status_code == 200: return response.text.strip()
    except: return None

# ==========================================
# 3. STATE MANAGEMENT
# ==========================================
if 'create_prompt' not in st.session_state: st.session_state.create_prompt = ""
if 'remix_prompt' not in st.session_state: st.session_state.remix_prompt = ""
groq_key = get_groq_key()

# ==========================================
# 4. MAIN INTERFACE
# ==========================================
st.title("👑 AKRITI OMEGA")
st.markdown("### The Ultimate Visual Engine")

tab_create, tab_remix = st.tabs(["✨ CREATE", "🌪️ REMIX"])

# === TAB 1: CREATE ===
with tab_create:
    st.markdown("<br>", unsafe_allow_html=True)
    
    # CONTROL DECK
    with st.expander("🎛️ SETTINGS (Model, Size, Style)", expanded=True):
        c1, c2, c3 = st.columns(3)
        with c1:
            model = st.selectbox("Model", ["Flux (Best)", "Flux-Realism", "Flux-Anime", "Flux-3D", "Turbo (Fast)"])
            model_code = model.split(" ")[0].lower()
        with c2:
            ratio = st.selectbox("Ratio", ["Square (1:1)", "Portrait (9:16)", "Landscape (16:9)", "Wide (21:9)"])
            if "Square" in ratio: w, h = 1024, 1024
            elif "Portrait" in ratio: w, h = 768, 1344
            elif "Landscape" in ratio: w, h = 1344, 768
            elif "Wide" in ratio: w, h = 1536, 640
        with c3:
            style = st.selectbox("Style", ["None", "Cyberpunk", "Cinematic", "Oil Painting", "Pixar 3D", "Dark Fantasy"])

    # INPUT & MAGIC EXPAND
    col_p, col_b = st.columns([4, 1])
    with col_p:
        prompt_input = st.text_input("Describe your vision...", value=st.session_state.create_prompt, key="c_input", placeholder="e.g. A golden temple in clouds")
        st.session_state.create_prompt = prompt_input
    with col_b:
        st.write("") 
        if st.button("✨ Magic Expand", key="magic_c", use_container_width=True):
            if groq_key and st.session_state.create_prompt:
                with st.spinner("✨ Enhancing..."):
                    st.session_state.create_prompt = expand_prompt_with_ai(st.session_state.create_prompt, groq_key)
                    st.rerun()

    if st.button("🚀 IGNITE GENERATION", type="primary", use_container_width=True):
        if st.session_state.create_prompt:
            final_p = st.session_state.create_prompt + (f", {style} style" if style != "None" else "")
            url = f"https://image.pollinations.ai/prompt/{final_p.replace(' ', '%20')}?width={w}&height={h}&seed={random.randint(0,1000)}&nologo=true&model={model_code}"
            
            st.image(url, caption="Generated by Akriti", use_container_width=True)
            data = fetch_image(url)
            if data: st.download_button("⬇️ DOWNLOAD HD", data=data, file_name="akriti.jpg", mime="image/jpeg", use_container_width=True)

# === TAB 2: REMIX ===
with tab_remix:
    st.markdown("<br>", unsafe_allow_html=True)
    c_up, c_set = st.columns(2)
    
    with c_up:
        uploaded_file = st.file_uploader("Upload Base Photo", type=["jpg", "png", "jpeg"])
        if uploaded_file: st.image(uploaded_file, caption="Base", use_container_width=True)

    with c_set:
        remix_in = st.text_input("What to change?", value=st.session_state.remix_prompt, key="r_input", placeholder="e.g. Make me a cyborg")
        st.session_state.remix_prompt = remix_in
        
        if st.button("✨ Magic Expand", key="magic_r"):
            if groq_key and st.session_state.remix_prompt:
                with st.spinner("✨ Enhancing..."):
                    st.session_state.remix_prompt = expand_prompt_with_ai(st.session_state.remix_prompt, groq_key)
                    st.rerun()
                    
        remix_model = st.selectbox("Remix Engine", ["flux-realism", "flux-anime", "flux-3d"])
        
        if st.button("🌪️ REMIX PHOTO", type="primary", use_container_width=True):
            if uploaded_file and st.session_state.remix_prompt:
                with st.status("Processing...", expanded=True):
                    base_url = upload_to_pollinations(uploaded_file)
                    if base_url:
                        url = f"https://image.pollinations.ai/prompt/{st.session_state.remix_prompt.replace(' ', '%20')}?image={base_url}&seed={random.randint(0,1000)}&nologo=true&model={remix_model}"
                        st.image(url, caption="Remix", use_container_width=True)
                        data = fetch_image(url)
                        if data: st.download_button("⬇️ DOWNLOAD REMIX", data=data, file_name="remix.jpg", mime="image/jpeg")

# COMPANY FOOTER
st.markdown("""
<div class="footer">
    <p>⚡ Powered by Samrion Intelligence | © 2025 Samrion Technologies | Founder: Nitin Raj</p>
</div>
""", unsafe_allow_html=True)
