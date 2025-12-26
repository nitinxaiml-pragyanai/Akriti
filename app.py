import streamlit as st
import random
import time

# --- SAFETY CHECK: TRY IMPORTS ---
try:
    import requests
    from groq import Groq
except ImportError as e:
    st.error(f"🚨 MISSING LIBRARY: {e}")
    st.info("Please run this command in your terminal:  pip install requests groq streamlit")
    st.stop()

# ==========================================
# 1. CONFIGURATION & THEME ENGINE
# ==========================================
st.set_page_config(
    page_title="AKRITI OMEGA",
    page_icon="👑",
    layout="wide"
)

# FIXED CSS: Dark Theme + Transparent Footer + White Text
st.markdown("""
<style>
    /* 1. MAIN BACKGROUND */
    .stApp {
        background: linear-gradient(180deg, #020024 0%, #090979 35%, #00d4ff 100%);
        background-attachment: fixed;
    }
    
    /* 2. TEXT VISIBILITY FIX */
    h1, h2, h3, h4, h5, p, label, span, div {
        color: #ffffff !important;
    }
    
    /* 3. FILE UPLOADER (Fixing the White Box) */
    [data-testid="stFileUploaderDropzone"] {
        background-color: rgba(0, 0, 0, 0.6) !important;
        border: 1px dashed #00d4ff !important;
        border-radius: 15px;
    }
    [data-testid="stFileUploaderDropzone"] div {
        color: white !important;
    }
    [data-testid="stFileUploaderDropzone"] button {
        background: rgba(255, 255, 255, 0.1) !important;
        color: white !important;
        border: 1px solid white !important;
    }

    /* 4. INPUTS & DROPDOWNS */
    .stTextInput > div > div > input {
        background-color: rgba(0, 0, 0, 0.6) !important;
        color: white !important;
        border: 1px solid rgba(255,255,255,0.3);
    }
    div[data-baseweb="select"] > div {
        background-color: rgba(0, 0, 0, 0.6) !important;
        color: white !important;
        border: 1px solid rgba(255,255,255,0.3) !important;
    }
    div[data-baseweb="select"] svg { fill: white !important; }
    
    /* Dropdown Options */
    ul[data-testid="stSelectboxVirtualDropdown"] { background-color: #001f3f !important; }
    li[role="option"]:hover { background-color: #00d4ff !important; color: black !important; }

    /* 5. BUTTONS */
    div.stButton > button {
        background: linear-gradient(90deg, #FF0099, #493240) !important;
        border: 1px solid rgba(255,255,255,0.2) !important;
        color: white !important;
        font-weight: bold !important;
    }

    /* 6. GLASSMORPHIC FOOTER (Transparent & Premium) */
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background: rgba(0, 0, 0, 0.3);
        backdrop-filter: blur(8px); /* The Glass Effect */
        -webkit-backdrop-filter: blur(8px);
        border-top: 1px solid rgba(255,255,255,0.1);
        color: rgba(255,255,255,0.7) !important;
        text-align: center;
        padding: 12px;
        font-size: 13px;
        letter-spacing: 1.5px;
        z-index: 9999;
    }
    .block-container { padding-bottom: 100px; }
    #MainMenu, footer, header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. BACKEND LOGIC
# ==========================================

def get_groq_key():
    # Safely try to get key, return None if missing
    try: return st.secrets["GROQ_API_KEY"]
    except: return None

def expand_prompt_with_ai(short_prompt, api_key):
    if not short_prompt: return ""
    if not api_key:
        st.warning("⚠️ API Key missing in `.streamlit/secrets.toml`. Prompt expansion skipped.")
        return short_prompt
        
    try:
        client = Groq(api_key=api_key)
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are an expert visual prompt engineer. Expand the user's short idea into a detailed, artistic image generation prompt (max 50 words)."},
                {"role": "user", "content": f"Expand this: '{short_prompt}'"}
            ],
            temperature=0.7, max_tokens=150
        )
        return completion.choices[0].message.content
    except Exception as e:
        st.error(f"AI Error: {e}")
        return short_prompt

def fetch_image(url):
    try:
        r = requests.get(url, timeout=15)
        if r.status_code == 200: return r.content
    except: return None

def upload_to_pollinations(uploaded_file):
    # Uploads image to get a URL for the Remix feature
    try:
        files = {'file': uploaded_file.getvalue()}
        # Note: This endpoint returns the URL of the uploaded image
        response = requests.post('https://image.pollinations.ai/upload', files=files)
        if response.status_code == 200:
            return response.text.strip()
        else:
            st.error("Upload failed. Server might be busy.")
            return None
    except Exception as e:
        st.error(f"Connection Error: {e}")
        return None

# ==========================================
# 3. UI LAYOUT
# ==========================================
if 'create_prompt' not in st.session_state: st.session_state.create_prompt = ""
if 'remix_prompt' not in st.session_state: st.session_state.remix_prompt = ""
groq_key = get_groq_key()

st.title("👑 AKRITI OMEGA")
st.caption("Samrion Intelligence Visual Engine")

tab1, tab2 = st.tabs(["✨ GENERATE", "🌪️ REMIX"])

# --- TAB 1: GENERATE ---
with tab1:
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Settings Row
    c1, c2, c3 = st.columns(3)
    with c1:
        # We separate the "Label" from the "Value" for the API
        model_choice = st.selectbox("Model", ["Flux (High Quality)", "Turbo (Fast)"])
        model_api = "flux" if "Flux" in model_choice else "turbo"
        
    with c2:
        ratio = st.selectbox("Ratio", ["Square (1:1)", "Portrait (9:16)", "Landscape (16:9)"])
        width, height = (1024, 1024) if "Square" in ratio else (768, 1344) if "Portrait" in ratio else (1344, 768)
        
    with c3:
        style = st.selectbox("Style", ["Realistic", "Anime", "3D Render", "Cyberpunk", "Oil Painting", "None"])

    # Prompt Row
    col_input, col_btn = st.columns([4, 1])
    with col_input:
        st.session_state.create_prompt = st.text_input("Vision", value=st.session_state.create_prompt, placeholder="A futuristic city made of glass...", label_visibility="collapsed")
    with col_btn:
        if st.button("✨ AI Expand", use_container_width=True):
            with st.spinner("Thinking..."):
                st.session_state.create_prompt = expand_prompt_with_ai(st.session_state.create_prompt, groq_key)
                st.rerun()

    if st.button("🚀 IGNITE", type="primary", use_container_width=True):
        if st.session_state.create_prompt:
            # Construct Final Prompt
            final_prompt = st.session_state.create_prompt
            if style != "None":
                final_prompt += f", {style} style, 8k resolution, highly detailed"
            
            # URL Construction
            seed = random.randint(0, 99999)
            image_url = f"https://image.pollinations.ai/prompt/{final_prompt}?width={width}&height={height}&seed={seed}&nologo=true&model={model_api}"
            
            st.image(image_url, caption="Generated Result", use_container_width=True)
            
            # Download Logic
            img_data = fetch_image(image_url)
            if img_data:
                st.download_button("⬇️ SAVE IMAGE", data=img_data, file_name=f"akriti_{seed}.jpg", mime="image/jpeg", use_container_width=True)

# --- TAB 2: REMIX ---
with tab2:
    st.markdown("<br>", unsafe_allow_html=True)
    c_img, c_ctrl = st.columns(2)
    
    with c_img:
        uploaded = st.file_uploader("Upload Base", type=["jpg", "png"])
        if uploaded:
            st.image(uploaded, caption="Original", use_container_width=True)
            
    with c_ctrl:
        st.session_state.remix_prompt = st.text_input("Transformation", value=st.session_state.remix_prompt, placeholder="Make it look like a sketch...")
        
        if st.button("🌪️ REMIX NOW", type="primary", use_container_width=True):
            if uploaded and st.session_state.remix_prompt:
                with st.status("Processing remix...", expanded=True):
                    st.write("📤 Uploading image...")
                    base_url = upload_to_pollinations(uploaded)
                    
                    if base_url:
                        st.write("🎨 Applying style...")
                        seed = random.randint(0, 99999)
                        # Pollinations Remix URL Pattern
                        remix_url = f"https://image.pollinations.ai/prompt/{st.session_state.remix_prompt}?image={base_url}&seed={seed}&nologo=true&model=flux"
                        
                        st.image(remix_url, caption="Remixed Result", use_container_width=True)
                        
                        r_data = fetch_image(remix_url)
                        if r_data:
                            st.download_button("⬇️ SAVE REMIX", data=r_data, file_name=f"remix_{seed}.jpg", mime="image/jpeg")

# FOOTER
st.markdown("""
<div class="footer">
    POWERED BY SAMRION INTELLIGENCE &nbsp;|&nbsp; © 2026 SAMRION AI INFRASTRUCTURE &nbsp;|&nbsp; FOUNDER: NITIN RAJ
</div>
""", unsafe_allow_html=True)
