import streamlit as st
import random
import requests
import time
from groq import Groq 

# ==========================================
# 1. CONFIGURATION & OMEGA THEME
# ==========================================
st.set_page_config(
    page_title="AKRITI OMEGA",
    page_icon="👑",
    layout="wide"
)

# THE NUCLEAR CSS (Forces Dark Mode Everywhere)
st.markdown("""
<style>
    /* 1. GLOBAL FONT & TEXT COLOR */
    .stApp, p, h1, h2, h3, h4, h5, label, span, div, button, li {
        font-family: 'Inter', sans-serif;
        color: #ffffff !important;
    }

    /* 2. BACKGROUND: DEEP SPACE IMPERIAL GRADIENT */
    .stApp {
        background: linear-gradient(180deg, #020024 0%, #090979 35%, #00d4ff 100%);
        background-attachment: fixed;
    }

    /* 3. FIX: FILE UPLOADER (The "White Box" Fix) */
    [data-testid="stFileUploader"] {
        background-color: rgba(0, 31, 63, 0.8);
        border-radius: 15px;
        padding: 20px;
        border: 1px dashed #00d4ff;
    }
    /* This forces the inner drag-drop zone to be transparent/dark */
    section[data-testid="stFileUploaderDropzone"] {
        background-color: rgba(0,0,0,0.3) !important;
    }
    /* This ensures the small text inside is white */
    [data-testid="stFileUploaderDropzone"] div, 
    [data-testid="stFileUploaderDropzone"] span, 
    [data-testid="stFileUploaderDropzone"] small {
        color: #ffffff !important;
    }

    /* 4. FIX: DROPDOWN MENUS (The "Invisible Option" Fix) */
    /* Forces the popup list to be Dark Blue */
    div[data-baseweb="popover"], div[data-baseweb="menu"], ul {
        background-color: #001f3f !important;
        border: 1px solid #00d4ff;
    }
    /* Forces options to be white */
    li[role="option"] {
        background-color: #001f3f !important;
        color: white !important;
    }
    /* Highlight color when hovering */
    li[role="option"]:hover {
        background-color: #00d4ff !important;
        color: black !important;
    }
    
    /* 5. FIX: INPUT BOXES & PLACEHOLDERS */
    .stTextInput > div > div > input {
        background-color: rgba(0,0,0,0.5) !important;
        color: white !important;
        border: 1px solid rgba(255,255,255,0.3);
        border-radius: 10px;
    }
    /* Makes "Describe your vision..." visible light gray */
    .stTextInput input::placeholder {
        color: rgba(200, 200, 200, 0.8) !important;
    }

    /* 6. TABS STYLE */
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
        color: #000000 !important;
        font-weight: bold;
    }

    /* 7. FOOTER STYLE */
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: rgba(0, 31, 63, 0.9);
        color: #888888 !important;
        text-align: center;
        padding: 10px;
        font-size: 12px;
        border-top: 1px solid #00d4ff;
        z-index: 999;
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

def expand_prompt_with_ai(short_prompt, api_key):
    if not short_prompt or not api_key: return None
    try:
        client = Groq(api_key=api_key)
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are an expert AI prompt engineer. Turn the user's short idea into a highly detailed, descriptive image prompt (lighting, texture, mood, 8k). Keep it one paragraph."},
                {"role": "user", "content": f"Expand: '{short_prompt}'"}
            ],
            temperature=0.7,
            max_tokens=300,
        )
        return completion.choices[0].message.content
    except: return None

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

tab_create, tab_remix = st.tabs(["✨ CREATE (Text-to-Image)", "🌪️ REMIX (Photo Editor)"])

# === TAB 1: CREATE ===
with tab_create:
    st.markdown("<br>", unsafe_allow_html=True)
    with st.expander("🎛️ CONTROL DECK (Settings)", expanded=True):
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

    st.markdown("#### ✍️ Describe your vision")
    col_p, col_b = st.columns([4, 1])
    with col_p:
        prompt_input = st.text_input("Enter idea...", value=st.session_state.create_prompt, key="create_input", placeholder="e.g. A golden temple")
        st.session_state.create_prompt = prompt_input
    with col_b:
        if st.button("✨ Magic Expand", key="magic_create_btn", use_container_width=True):
            if groq_key and st.session_state.create_prompt:
                with st.spinner("✨ AI is dreaming..."):
                    expanded = expand_prompt_with_ai(st.session_state.create_prompt, groq_key)
                    if expanded:
                        st.session_state.create_prompt = expanded
                        st.rerun()
            else: st.toast("⚠️ Key missing or empty prompt")

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🚀 IGNITE GENERATION", type="primary", use_container_width=True):
        if st.session_state.create_prompt:
            final_p = st.session_state.create_prompt + (f", {style} style" if style != "None" else "")
            url_p = final_p.replace(" ", "%20")
            seed = random.randint(0, 1000000)
            url = f"https://image.pollinations.ai/prompt/{url_p}?width={w}&height={h}&seed={seed}&nologo=true&model={model_code}"
            
            st.markdown(f"### ✨ Result")
            st.image(url, caption=f"{model} | {w}x{h}", use_container_width=True)
            with st.spinner("Preparing Download..."):
                data = fetch_image(url)
                if data: st.download_button("⬇️ DOWNLOAD HD", data, f"akriti_{seed}.jpg", "image/jpeg", use_container_width=True)

# === TAB 2: REMIX ===
with tab_remix:
    st.markdown("<br>", unsafe_allow_html=True)
    col_up, col_set = st.columns([1, 1], gap="large")
    with col_up:
        st.markdown("#### 1. Upload Photo")
        uploaded = st.file_uploader("", type=["jpg", "png", "jpeg"])
        if uploaded: st.image(uploaded, caption="Base", use_container_width=True)
    with col_set:
        st.markdown("#### 2. Describe Edit")
        col_rp, col_rb = st.columns([3, 1])
        with col_rp:
            remix_in = st.text_input("Change what?", value=st.session_state.remix_prompt, key="remix_in", placeholder="e.g. Make me a cyborg")
            st.session_state.remix_prompt = remix_in
        with col_rb:
             if st.button("✨ Expand", key="magic_remix", use_container_width=True):
                if groq_key and st.session_state.remix_prompt:
                    with st.spinner("AI thinking..."):
                        exp = expand_prompt_with_ai(f"Edit image: {st.session_state.remix_prompt}", groq_key)
                        if exp:
                            st.session_state.remix_prompt = exp
                            st.rerun()

        st.markdown("#### 3. Engine")
        r_model = st.selectbox("Engine", ["Flux-Realism", "Flux-Anime", "Flux-3D"])
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🌪️ REMIX PHOTO", type="primary", use_container_width=True):
            if uploaded and st.session_state.remix_prompt:
                with st.status("🌪️ Processing...", expanded=True):
                    base_url = upload_to_pollinations(uploaded)
                    if base_url:
                        p = st.session_state.remix_prompt.replace(" ", "%20")
                        seed = random.randint(0, 1000000)
                        url = f"https://image.pollinations.ai/prompt/{p}?image={base_url}&seed={seed}&nologo=true&model={r_model.lower()}"
                        st.image(url, caption="Remix", use_container_width=True)
                        data = fetch_image(url)
                        if data: st.download_button("⬇️ DOWNLOAD REMIX", data, f"remix_{seed}.jpg", "image/jpeg", use_container_width=True)

# ==========================================
# 5. COMPANY FOOTER
# ==========================================
st.markdown("""
<div class="footer">
    <p>© 2025 Samrion AI Infrastructure. Built by Nitin Raj. All Rights Reserved.</p>
</div>
""", unsafe_allow_html=True)
