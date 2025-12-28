import streamlit as st
import random
import time

# --- 1. ROBUST DEPENDENCY CHECK ---
try:
    import requests
    from groq import Groq
except ImportError as e:
    st.error(f"🚨 SYSTEM ERROR: Missing Library '{e.name}'")
    st.info(f"Run this command to fix:  pip install requests groq streamlit")
    st.stop()

# ==========================================
# 2. APP CONFIGURATION & STYLING
# ==========================================
st.set_page_config(
    page_title="AKRITI ",
    page_icon="👑",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ULTRA-PREMIUM CSS SUITE
st.markdown("""
<style>
    /* 1. BACKGROUND ENGINE */
    .stApp {
        background: linear-gradient(180deg, #020024 0%, #090979 35%, #00d4ff 100%);
        background-attachment: fixed;
    }
    
    /* 2. TEXT & FONT ENGINE */
    h1, h2, h3, h4, h5, p, label, span, div, li {
        color: #ffffff !important;
        font-family: 'Helvetica Neue', sans-serif;
    }
    
    /* 3. COMPONENT: FILE UPLOADER */
    [data-testid="stFileUploaderDropzone"] {
        background-color: rgba(0, 0, 0, 0.6) !important;
        border: 2px dashed #00d4ff !important;
        border-radius: 15px;
        transition: all 0.3s ease;
    }
    [data-testid="stFileUploaderDropzone"]:hover {
        background-color: rgba(0, 0, 0, 0.8) !important;
        border-color: #FF0099 !important;
    }
    [data-testid="stFileUploaderDropzone"] button {
        background: rgba(255, 255, 255, 0.1) !important;
        color: white !important;
        border: 1px solid white !important;
    }

    /* 4. COMPONENT: INPUTS & DROPDOWNS */
    .stTextInput > div > div > input {
        background-color: rgba(0, 0, 0, 0.6) !important;
        color: white !important;
        border: 1px solid rgba(255,255,255,0.3);
        border-radius: 8px;
    }
    div[data-baseweb="select"] > div {
        background-color: rgba(0, 0, 0, 0.6) !important;
        color: white !important;
        border: 1px solid rgba(255,255,255,0.3) !important;
        border-radius: 8px;
    }
    div[data-baseweb="select"] svg { fill: white !important; }
    
    /* Dropdown Menu Items */
    ul[data-testid="stSelectboxVirtualDropdown"] { background-color: #001f3f !important; }
    li[role="option"]:hover { background-color: #00d4ff !important; color: black !important; }

    /* 5. COMPONENT: BUTTONS */
    div.stButton > button {
        background: linear-gradient(90deg, #FF0099, #493240) !important;
        border: 1px solid rgba(255,255,255,0.2) !important;
        color: white !important;
        font-weight: 700 !important;
        text-transform: uppercase;
        letter-spacing: 1px;
        transition: transform 0.1s;
    }
    div.stButton > button:active {
        transform: scale(0.98);
    }

    /* 6. COMPONENT: FOOTER */
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background: rgba(0, 0, 0, 0.5);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border-top: 1px solid rgba(255,255,255,0.1);
        color: rgba(255,255,255,0.8) !important;
        text-align: center;
        padding: 15px;
        font-size: 12px;
        letter-spacing: 2px;
        z-index: 9999;
    }
    .block-container { padding-bottom: 120px; }
    #MainMenu, footer, header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. CORE INTELLIGENCE FUNCTIONS
# ==========================================

def get_groq_key():
    try: return st.secrets["GROQ_API_KEY"]
    except: return None

def expand_prompt_with_ai(short_prompt, api_key):
    if not short_prompt: return ""
    if not api_key:
        st.toast("⚠️ API Key missing in secrets. Using raw prompt.", icon="⚠️")
        return short_prompt
        
    try:
        client = Groq(api_key=api_key)
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are a visual prompt expert. Convert the user's idea into a highly detailed, artistic image prompt with lighting and texture details. Keep it under 60 words."},
                {"role": "user", "content": f"Enhance this concept: '{short_prompt}'"}
            ],
            temperature=0.7, max_tokens=200
        )
        return completion.choices[0].message.content
    except Exception as e:
        st.error(f"AI Expansion Failed: {e}")
        return short_prompt

def get_image_bytes(url):
    """
    TRIPLE RETRY ENGINE:
    Tries 3 times to fetch the image. Includes headers to avoid being blocked.
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    
    max_retries = 3
    for attempt in range(1, max_retries + 1):
        try:
            # 60 second timeout is plenty for 1280px images
            response = requests.get(url, headers=headers, timeout=60)
            if response.status_code == 200:
                return response.content
        except requests.exceptions.RequestException:
            pass # Fail silently and try again
        
        time.sleep(2) # Wait 2 seconds before retry
    
    return None

def upload_to_pollinations(uploaded_file):
    try:
        files = {'file': uploaded_file.getvalue()}
        response = requests.post('https://image.pollinations.ai/upload', files=files)
        if response.status_code == 200:
            return response.text.strip()
        else:
            return None
    except:
        return None

# ==========================================
# 4. USER INTERFACE
# ==========================================

# Initialize Session State
if 'create_prompt' not in st.session_state: st.session_state.create_prompt = ""
if 'remix_prompt' not in st.session_state: st.session_state.remix_prompt = ""
groq_key = get_groq_key()

st.title(" AKRITI ")
st.caption("Samrion Intelligence | Visual Engine v4.0")

# Tabs
tab1, tab2 = st.tabs(["✨ GENERATE", "🌪️ REMIX"])

# --- TAB 1: CREATION ENGINE ---
with tab1:
    st.markdown("<br>", unsafe_allow_html=True)
    
    # CONTROL PANEL
    with st.container():
        c1, c2, c3 = st.columns(3)
        with c1:
            model_choice = st.selectbox("Model Engine", ["Flux (High Detail)", "Turbo (Speed)"])
            model_api = "flux" if "Flux" in model_choice else "turbo"
            
        with c2:
            ratio = st.selectbox("Frame Ratio", ["Square (1:1)", "Portrait (9:16)", "Landscape (16:9)"])
            # === SAFE RESOLUTION LOCK ===
            # These resolutions are tested to be safe from 504 Timeouts
            if "Square" in ratio: width, height = 1280, 1280
            elif "Portrait" in ratio: width, height = 768, 1280
            elif "Landscape" in ratio: width, height = 1280, 768
            
        with c3:
            style = st.selectbox("Artistic Style", ["Realistic", "Anime", "Cyberpunk", "Oil Painting", "3D Render", "Dark Fantasy", "None"])

    # PROMPT ENGINE
    st.markdown("<br>", unsafe_allow_html=True)
    col_input, col_btn = st.columns([4, 1])
    with col_input:
        st.session_state.create_prompt = st.text_input("Creative Vision", value=st.session_state.create_prompt, placeholder="A futuristic city made of gold and glass...", label_visibility="collapsed")
    with col_btn:
        if st.button("✨ Enhance", use_container_width=True, help="Use AI to improve your prompt"):
            with st.spinner("Injecting Creativity..."):
                st.session_state.create_prompt = expand_prompt_with_ai(st.session_state.create_prompt, groq_key)
                st.rerun()

    # GENERATION BUTTON
    st.write("")
    if st.button("🚀 IGNITE GENERATION", type="primary", use_container_width=True):
        if not st.session_state.create_prompt:
            st.warning("⚠️ Please enter a prompt first.")
        else:
            # 1. Prompt Engineering
            final_prompt = st.session_state.create_prompt
            # We force '8k' keyword for texture, even if actual resolution is 1280p
            final_prompt += ", 8k resolution, photorealistic, masterpiece, sharp focus, highly detailed"
            if style != "None":
                final_prompt += f", {style} style"
            
            seed = random.randint(0, 999999)
            image_url = f"https://image.pollinations.ai/prompt/{final_prompt}?width={width}&height={height}&seed={seed}&nologo=true&model={model_api}"
            
            # 2. Execution
            with st.status("Processing Request...", expanded=True) as status:
                st.write("📡 Connecting to Neural Cloud...")
                img_data = get_image_bytes(image_url)
                
                if img_data:
                    status.update(label="✅ Render Complete", state="complete", expanded=False)
                    st.image(img_data, caption=f"Generated Result (Seed: {seed})", use_container_width=True)
                    
                    st.download_button(
                        label="⬇️ DOWNLOAD HD ASSET",
                        data=img_data,
                        file_name=f"akriti_{seed}.jpg",
                        mime="image/jpeg",
                        use_container_width=True
                    )
                else:
                    status.update(label="❌ Network Timeout", state="error")
                    st.error("The server is currently overloaded. Please wait 10 seconds and try again.")
                    st.caption(f"Debug URL (Click to view in browser): [Link]({image_url})")

# --- TAB 2: REMIX ENGINE ---
with tab2:
    st.markdown("<br>", unsafe_allow_html=True)
    c_img, c_ctrl = st.columns(2)
    
    with c_img:
        uploaded = st.file_uploader("Upload Source Image", type=["jpg", "png", "jpeg"])
        if uploaded:
            st.image(uploaded, caption="Source", use_container_width=True)
            
    with c_ctrl:
        st.session_state.remix_prompt = st.text_input("Transformation Command", value=st.session_state.remix_prompt, placeholder="Example: Make it look like a pencil sketch")
        
        st.write("")
        if st.button("🌪️ ACTIVATE REMIX", type="primary", use_container_width=True):
            if uploaded and st.session_state.remix_prompt:
                with st.status("Remixing Reality...", expanded=True) as status:
                    st.write("📤 Uploading source matrix...")
                    base_url = upload_to_pollinations(uploaded)
                    
                    if base_url:
                        st.write("🎨 Applying neural style transfer...")
                        seed = random.randint(0, 999999)
                        # Remix safe resolution
                        remix_url = f"https://image.pollinations.ai/prompt/{st.session_state.remix_prompt}?image={base_url}&seed={seed}&nologo=true&model=flux&width=1280&height=1280"
                        
                        img_data = get_image_bytes(remix_url)
                        
                        if img_data:
                            status.update(label="✅ Remix Complete", state="complete", expanded=False)
                            st.image(img_data, caption="Remix Result", use_container_width=True)
                            st.download_button("⬇️ DOWNLOAD REMIX", data=img_data, file_name=f"remix_{seed}.jpg", mime="image/jpeg", use_container_width=True)
                        else:
                            st.error("Remix failed. The prompt might be too complex for the current server load.")
                    else:
                        st.error("Failed to upload source image.")

# FOOTER
st.markdown("""
<div class="footer">
    POWERED BY SAMRION INTELLIGENCE &nbsp;|&nbsp; © 2026 SAMRION AI INFRASTRUCTURE &nbsp;|&nbsp; FOUNDER: NITIN RAJ
</div>
""", unsafe_allow_html=True)
