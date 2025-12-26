import streamlit as st
import random
import requests
import time
from groq import Groq # Import Groq for the Magic Expand feature

# ==========================================
# 1. CONFIGURATION & OMEGA THEME
# ==========================================
st.set_page_config(
    page_title="AKRITI OMEGA",
    page_icon="👑",
    layout="wide"
)

# THE LEGENDARY CSS (Fixed for Visibility & UI Issues)
st.markdown("""
<style>
    /* 1. GLOBAL FONT & DEFAULT TEXT COLOR */
    .stApp, p, h1, h2, h3, h4, h5, label, span, div, button {
        font-family: 'Inter', sans-serif;
        color: #ffffff; /* Default white text */
    }

    /* 2. BACKGROUND: DEEP SPACE IMPERIAL GRADIENT */
    .stApp {
        background: linear-gradient(180deg, #020024 0%, #090979 35%, #00d4ff 100%);
        background-attachment: fixed;
    }

    /* =========================================
       3. UI FIXES (Addressing your screenshot)
       ========================================= */
    
    /* FIX 1: FILE UPLOADER VISIBILITY */
    /* Makes the dropzone dark so the white text is readable */
    [data-testid="stFileUploader"] > div > div {
        background-color: rgba(0, 80, 158, 0.3) !important;
        border: 1px dashed #00d4ff;
        border-radius: 10px;
    }
    /* Ensures the text inside is white and visible */
    [data-testid="stFileUploader"] div, [data-testid="stFileUploader"] span, [data-testid="stFileUploader"] small {
        color: #ffffff !important;
    }

    /* FIX 2: TEXT INPUT PLACEHOLDER VISIBILITY */
    /* Makes the placeholder text (e.g., "Describe your vision...") a visible light gray */
    .stTextInput input::placeholder, .stTextArea textarea::placeholder {
        color: rgba(255, 255, 255, 0.7) !important;
    }
    /* Standard input box styling */
    .stTextInput > div > div > input {
        background-color: rgba(255,255,255,0.1) !important;
        color: white !important;
        border: 1px solid rgba(255,255,255,0.2);
        border-radius: 10px;
    }

    /* FIX 3: DROPDOWN MENU VISIBILITY */
    /* Forces popup menus to be dark blue so white text is visible */
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

    /* =========================================
       4. COMPONENT STYLING
       ========================================= */

    /* TABS */
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

    /* BUTTONS (Neon Gradient) */
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

    /* HIDE STREAMLIT UI */
    #MainMenu, footer, header {visibility: hidden;}
    
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. HELPER FUNCTIONS & AI BRAIN
# ==========================================

# --- Securely Load API Key ---
def get_groq_key():
    """Tries to get the Groq API key from secrets."""
    try:
        return st.secrets["GROQ_API_KEY"]
    except (FileNotFoundError, KeyError):
        return None

# --- The New AI Prompt Engineer ---
def expand_prompt_with_ai(short_prompt, api_key):
    """Uses Groq (Llama 3.1) to expand a short prompt into a detailed one."""
    if not short_prompt: return ""
    if not api_key: return "⚠️ API Key Missing for Magic Expand."
    
    try:
        client = Groq(api_key=api_key)
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant", # Very fast model
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert AI prompt engineer for image generation models like Flux and Midjourney. Your task is to take a user's short, simple idea and expand it into a detailed, descriptive prompt that will yield a high-quality, visually rich image. Add details about style, lighting, composition, textures, and mood. Keep it to one paragraph. Do not add conversational text."
                },
                {
                    "role": "user",
                    "content": f"Expand this idea into a detailed image prompt: '{short_prompt}'"
                }
            ],
            temperature=0.7,
            max_tokens=300,
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Error expanding prompt: {str(e)}"

# --- Existing Image Functions ---
def fetch_image(url):
    """Downloads the image data from a URL."""
    try:
        r = requests.get(url, timeout=10)
        if r.status_code == 200: return r.content
    except: return None

def upload_to_pollinations(uploaded_file):
    """Uploads an image to get a temporary URL for remixing."""
    try:
        files = {'file': uploaded_file.getvalue()}
        response = requests.post('https://image.pollinations.ai/upload', files=files)
        if response.status_code == 200: return response.text.strip()
    except: return None

# ==========================================
# 3. STATE MANAGEMENT (For Magic Expand)
# ==========================================
# We use session state to store the prompt so it can be updated by the AI
if 'create_prompt' not in st.session_state:
    st.session_state.create_prompt = ""
if 'remix_prompt' not in st.session_state:
    st.session_state.remix_prompt = ""

groq_key = get_groq_key()

# ==========================================
# 4. MAIN INTERFACE
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

    # INPUT AREA WITH MAGIC EXPAND
    st.markdown("#### ✍️ Describe your vision")
    col_p, col_b = st.columns([4, 1])
    with col_p:
        # Input is bound to session state
        prompt_input = st.text_input("Enter a short idea...", value=st.session_state.create_prompt, key="create_input", placeholder="e.g. A golden temple")
        st.session_state.create_prompt = prompt_input # Update state on change

    with col_b:
        # Magic Expand Button
        if st.button("✨ Magic Expand", key="magic_create_btn", help="Use AI to turn your short idea into a detailed prompt.", use_container_width=True):
            if not groq_key:
                 st.error("🔑 Groq API Key not found in secrets.")
            elif st.session_state.create_prompt:
                with st.spinner("✨ Expanding your idea with AI..."):
                    expanded_text = expand_prompt_with_ai(st.session_state.create_prompt, groq_key)
                    st.session_state.create_prompt = expanded_text # Update the state
                    st.rerun() # Rerun to show new text in input box
            else:
                 st.toast("⚠️ Please type an idea first!", icon="✍️")

    st.markdown("<br>", unsafe_allow_html=True)
    btn_gen = st.button("🚀 IGNITE GENERATION", type="primary", use_container_width=True)

    # GENERATION LOGIC
    if btn_gen and st.session_state.create_prompt:
        final_prompt = st.session_state.create_prompt
        if style != "None": final_prompt += f", {style} style"
        
        url_prompt = final_prompt.replace(" ", "%20")
        seed = random.randint(0, 1000000)
        # Using a free reliable endpoint proxy for Pollinations
        image_url = f"https://image.pollinations.ai/prompt/{url_prompt}?width={w}&height={h}&seed={seed}&nologo=true&model={model_code}"
        
        st.markdown(f"### ✨ Result")
        with st.container():
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
    
    col_upload, col_settings = st.columns([1, 1], gap="large")
    
    with col_upload:
        st.markdown("#### 1. Upload Photo")
        uploaded_file = st.file_uploader("", type=["jpg", "png", "jpeg"])
        if uploaded_file:
            st.image(uploaded_file, caption="Base Image", use_container_width=True, style={'border-radius':'15px'})

    with col_settings:
        st.markdown("#### 2. Describe Changes")
        
        # Input Area with Magic Expand
        col_rp, col_rb = st.columns([3, 1])
        with col_rp:
            remix_input = st.text_input("What to change?", value=st.session_state.remix_prompt, key="remix_input", placeholder="e.g. Make me a cyborg")
            st.session_state.remix_prompt = remix_input

        with col_rb:
             if st.button("✨ Expand", key="magic_remix_btn", help="Use AI to detail your edit.", use_container_width=True):
                if not groq_key:
                     st.error("🔑 Groq API Key missing.")
                elif st.session_state.remix_prompt:
                    with st.spinner("✨ AI is thinking..."):
                        expanded_text = expand_prompt_with_ai(f"Based on an image, make this edit: {st.session_state.remix_prompt}", groq_key)
                        st.session_state.remix_prompt = expanded_text
                        st.rerun()
                else:
                     st.toast("⚠️ Please type an edit first!", icon="✍️")

        st.markdown("#### 3. AI Model")
        remix_model = st.selectbox("Remix Engine", ["Flux-Realism", "Flux-Anime", "Flux-3D"], index=0, key="remix_model")
        
        st.markdown("<br>", unsafe_allow_html=True)
        btn_remix = st.button("🌪️ REMIX PHOTO", type="primary", use_container_width=True)

    # REMIX LOGIC
    if btn_remix and uploaded_file and st.session_state.remix_prompt:
        with st.status("🌪️ Uploading & Processing...", expanded=True) as status:
            st.write("📤 Sending to Neural Cloud...")
            base_url = upload_to_pollinations(uploaded_file)
            
            if base_url:
                st.write("🎨 Applying Magic...")
                clean_p = st.session_state.remix_prompt.replace(" ", "%20")
                seed = random.randint(0, 1000000)
                remix_url = f"https://image.pollinations.ai/prompt/{clean_p}?image={base_url}&seed={seed}&nologo=true&model={remix_model.lower()}"
                
                status.update(label="REMIX COMPLETE", state="complete", expanded=False)
                
                st.markdown(f"### 🌪️ Remix Result")
                st.image(remix_url, caption=f"Remix by Akriti", use_container_width=True)
                
                with st.spinner("💾 Fetching File..."):
                    remix_data = fetch_image(remix_url)
                    if remix_data:
                        st.download_button("⬇️ DOWNLOAD REMIX", data=remix_data, file_name=f"akriti_remix_{seed}.jpg", mime="image/jpeg", use_container_width=True)
            else:
                st.error("Upload Failed. Try a smaller image.")
