import streamlit as st
import random
import requests
from groq import Groq

# ==========================================
# 1. CONFIGURATION & THEME ENGINE
# ==========================================
st.set_page_config(
    page_title="AKRITI OMEGA",
    page_icon="👑",
    layout="wide"
)

# THE ROBUST CSS PATCH
st.markdown("""
<style>
    /* 1. SAFER FONT RESET (Doesn't break icons) */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* 2. BACKGROUND: DEEP SPACE */
    .stApp {
        background: linear-gradient(180deg, #020024 0%, #090979 35%, #00d4ff 100%);
        background-attachment: fixed;
    }
    
    /* 3. TEXT COLOR FORCE (White) */
    h1, h2, h3, p, span, div, label {
        color: #ffffff !important;
    }

    /* =========================================
       CRITICAL UI FIXES
       ========================================= */
       
    /* FIX: PREVENT FOOTER OVERLAP */
    /* Adds empty space at the bottom of the scrollable area */
    .block-container {
        padding-bottom: 120px !important;
    }

    /* FIX: THE EXPANDER (Settings Box) */
    div[data-testid="stExpander"] {
        background-color: rgba(0, 0, 0, 0.6) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 10px;
        color: white !important;
    }
    /* Fixes the "keyboard_arrow_down" glitch by ignoring icon styling */
    div[data-testid="stExpander"] summary span {
        font-family: 'Inter', sans-serif !important;
    }
    div[data-testid="stExpander"] svg {
        fill: white !important; /* White Arrow */
    }

    /* FIX: FILE UPLOADER (The "Browse" Button) */
    [data-testid="stFileUploader"] {
        background-color: rgba(0, 0, 0, 0.3);
        border: 1px dashed #00d4ff;
        border-radius: 15px;
        padding: 20px;
    }
    /* Target the internal white button specifically */
    [data-testid="stFileUploader"] button {
        background-color: rgba(0, 0, 0, 0.5) !important; /* Dark background */
        color: white !important;
        border: 1px solid rgba(255,255,255,0.3) !important;
    }
    [data-testid="stFileUploader"] section {
        background-color: transparent !important;
    }

    /* FIX: MAGIC EXPAND BUTTON */
    div.stButton > button {
        background: linear-gradient(90deg, #FF0099, #493240) !important;
        border: 1px solid rgba(255,255,255,0.2) !important;
        color: white !important;
        font-weight: bold !important;
    }
    div.stButton > button:hover {
        transform: scale(1.02);
        box-shadow: 0 0 15px #FF0099;
    }

    /* FIX: INPUT FIELDS */
    .stTextInput > div > div > input {
        background-color: rgba(0, 0, 0, 0.6) !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }

    /* =========================================
       THE FOOTER
       ========================================= */
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background: transparent;
        color: rgba(255,255,255,0.8);
        text-align: center;
        padding: 15px;
        font-size: 14px;
        z-index: 9999;
        pointer-events: none; /* Allows clicking through if needed */
        text-shadow: 2px 2px 5px black; /* Ensures visibility */
        font-weight: 500;
    }
    
    #MainMenu, footer, header {visibility: hidden;}
    
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. HELPER FUNCTIONS
# ==========================================

def get_groq_key():
    try: return st.secrets["GROQ_API_KEY"]
    except: return None

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
# 3. STATE & UI
# ==========================================
if 'create_prompt' not in st.session_state: st.session_state.create_prompt = ""
if 'remix_prompt' not in st.session_state: st.session_state.remix_prompt = ""
groq_key = get_groq_key()

st.title("👑 AKRITI OMEGA")
st.markdown("### The Ultimate Visual Engine")

tab_create, tab_remix = st.tabs(["✨ CREATE", "🌪️ REMIX"])

# === TAB 1: CREATE ===
with tab_create:
    st.markdown("<br>", unsafe_allow_html=True)
    
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

    col_p, col_b = st.columns([4, 1])
    with col_p:
        st.session_state.create_prompt = st.text_input("Describe your vision...", value=st.session_state.create_prompt, key="c_input", placeholder="e.g. A golden temple in clouds")
    with col_b:
        st.write("") 
        if st.button("✨ Magic Expand", key="magic_c", use_container_width=True):
            if groq_key and st.session_state.create_prompt:
                with st.spinner("✨ Enhancing..."):
                    st.session_state.create_prompt = expand_prompt_with_ai(st.session_state.create_prompt, groq_key)
                    st.rerun()

    st.write("")
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
        st.session_state.remix_prompt = st.text_input("What to change?", value=st.session_state.remix_prompt, key="r_input", placeholder="e.g. Make me a cyborg")
        
        if st.button("✨ Magic Expand", key="magic_r"):
            if groq_key and st.session_state.remix_prompt:
                with st.spinner("✨ Enhancing..."):
                    st.session_state.remix_prompt = expand_prompt_with_ai(st.session_state.remix_prompt, groq_key)
                    st.rerun()
                    
        remix_model = st.selectbox("Remix Engine", ["flux-realism", "flux-anime", "flux-3d"])
        
        st.write("")
        if st.button("🌪️ REMIX PHOTO", type="primary", use_container_width=True):
            if uploaded_file and st.session_state.remix_prompt:
                with st.status("Processing...", expanded=True):
                    base_url = upload_to_pollinations(uploaded_file)
                    if base_url:
                        url = f"https://image.pollinations.ai/prompt/{st.session_state.remix_prompt.replace(' ', '%20')}?image={base_url}&seed={random.randint(0,1000)}&nologo=true&model={remix_model}"
                        st.image(url, caption="Remix", use_container_width=True)
                        data = fetch_image(url)
                        if data: st.download_button("⬇️ DOWNLOAD REMIX", data=data, file_name="remix.jpg", mime="image/jpeg")

st.markdown("""
<div class="footer">
    <p>⚡ Powered by Samrion Intelligence | © 2026 Samrion AI Infrastructure | Founder: Nitin Raj</p>
</div>
""", unsafe_allow_html=True)
