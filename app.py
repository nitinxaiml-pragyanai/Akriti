import streamlit as st
import random
import time
import requests
from io import BytesIO

# ==========================================
# 1. CONFIGURATION & ROYAL BLUE THEME
# ==========================================
st.set_page_config(
    page_title="AKRITI ",
    page_icon="🎨",
    layout="wide"
)

st.markdown("""
<style>
    /* 1. FORCE WHITE TEXT EVERYWHERE */
    .stApp, p, h1, h2, h3, h4, label, .stMarkdown, .stWrite, .stRadio, span, div[data-baseweb="select"] > div, .stTabs button {
        color: #ffffff !important;
    }

    /* 2. ROYAL BLUE IMPERIAL BACKGROUND */
    .stApp {
        background: linear-gradient(135deg, #001f3f 0%, #003366 50%, #00509e 100%);
        background-attachment: fixed;
    }

    /* 3. GLASS INPUT BOXES */
    .stTextInput > div > div > input, .stNumberInput > div > div > input {
        background: rgba(0, 80, 158, 0.2) !important;
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        color: #ffffff !important;
        border-radius: 12px;
        padding: 12px;
    }
    
    /* 4. MAGIC BUTTONS */
    div.stButton > button {
        background: linear-gradient(90deg, #00c6ff, #0072ff);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 1.2rem;
        font-weight: bold;
        transition: transform 0.2s;
        width: 100%;
    }
    div.stButton > button:hover {
        transform: scale(1.02);
        box-shadow: 0 0 15px rgba(0, 114, 255, 0.6);
    }
    
    /* DOWNLOAD BUTTON SPECIFIC */
    div.stDownloadButton > button {
        background: linear-gradient(90deg, #ff007f, #ff4081);
        color: white;
        border-radius: 30px;
    }

    /* 5. TAB STYLING */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background-color: rgba(0, 31, 63, 0.5);
        padding: 10px;
        border-radius: 15px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px;
        padding: 10px 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    .stTabs [aria-selected="true"] {
        background-color: #0072ff !important;
        color: white !important;
    }

    /* HIDE JUNK */
    #MainMenu, footer, header {visibility: hidden;}
    
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. HELPER FUNCTIONS
# ==========================================
def upload_to_pollinations(uploaded_file):
    """Hacks Pollinations upload endpoint"""
    try:
        files = {'file': uploaded_file.getvalue()}
        response = requests.post('https://image.pollinations.ai/upload', files=files)
        if response.status_code == 200:
            return response.text.strip()
        return None
    except Exception as e:
        return None

def fetch_image_bytes(url):
    """Downloads image to RAM for user download"""
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.content
        return None
    except:
        return None

# ==========================================
# 3. SIDEBAR CONTROLS
# ==========================================
with st.sidebar:
    st.title("⚙️ STUDIO CONTROLS")
    st.markdown("---")
    
    st.markdown("### 🧠 AI Model")
    model_choice = st.selectbox(
        "Choose Engine:",
        ["Flux (Standard)", "Flux-Realism (Photo)", "Flux-Anime (Cartoon)", "Flux-3D (Render)", "Turbo (Fastest)"]
    )
    
    model_map = {
        "Flux (Standard)": "flux",
        "Flux-Realism (Photo)": "flux-realism",
        "Flux-Anime (Cartoon)": "flux-anime",
        "Flux-3D (Render)": "flux-3d",
        "Turbo (Fastest)": "turbo"
    }
    selected_model = model_map[model_choice]
    st.info(f"Active: {selected_model.upper()}")
    st.markdown("---")
    
    st.markdown("### 📏 Canvas Size")
    width = st.slider("Width (px)", 256, 2048, 1024, step=64)
    height = st.slider("Height (px)", 256, 2048, 1024, step=64)
    
    st.markdown("---")
    st.markdown("### 🧬 DNA (Seed)")
    use_random_seed = st.checkbox("Randomize DNA", value=True)
    seed_input = st.number_input("Custom Seed ID", value=42, disabled=use_random_seed)
    final_seed = random.randint(0, 1000000) if use_random_seed else int(seed_input)

# ==========================================
# 4. MAIN INTERFACE
# ==========================================

st.title("AKRITI FINAL")
st.markdown("<div style='color: #aaccff; margin-bottom: 30px;'>IMAGINATION & REMIX ENGINE</div>", unsafe_allow_html=True)

tab_create, tab_remix = st.tabs(["✨ Create New", "🖼️ Remix Photo"])

# === TAB 1: CREATE NEW ===
with tab_create:
    col1, col2 = st.columns([3, 1])
    with col1:
        prompt_create = st.text_input("Describe your vision...", key="prompt_create_box")
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("✨ MAGIC EXPAND", key="magic_create"):
            modifiers = ["highly detailed", "8k resolution", "cinematic lighting", "masterpiece"]
            extras = ", ".join(random.sample(modifiers, 2))
            if prompt_create:
                st.info(f"Enhanced: {extras}")
            else:
                st.warning("Type something first!")

    btn_create = st.button("🚀 LAUNCH GENERATION", type="primary", key="btn_create")

    if btn_create and prompt_create:
        with st.status(f"🎨 Rendering with {selected_model.upper()}...", expanded=True) as status:
            clean_prompt = prompt_create.replace(" ", "%20")
            # 1. Generate URL
            image_url = f"https://image.pollinations.ai/prompt/{clean_prompt}?width={width}&height={height}&seed={final_seed}&nologo=true&model={selected_model}"
            
            # 2. Fetch Bytes (Real Download logic)
            st.write("📥 Fetching high-quality data...")
            img_data = fetch_image_bytes(image_url)
            
            status.update(label="RENDER COMPLETE", state="complete", expanded=False)

        if img_data:
            # 3. Show Preview
            st.image(img_data, caption=f"Seed: {final_seed}", use_container_width=True)
            
            # 4. Real Download Button
            st.download_button(
                label="⬇️ DOWNLOAD IMAGE (HD)",
                data=img_data,
                file_name=f"akriti_{final_seed}.jpg",
                mime="image/jpeg",
                key="dl_create"
            )
        else:
            st.error("Connection failed. Please try again.")

# === TAB 2: REMIX PHOTO ===
with tab_remix:
    st.markdown("### 1. Upload Base Photo")
    uploaded_file = st.file_uploader("", type=["jpg", "png", "jpeg"])
    
    if uploaded_file is not None:
        st.image(uploaded_file, caption="Original Photo", width=300)
        
        st.markdown("### 2. Describe Edit")
        prompt_remix = st.text_input("What to change?", key="prompt_remix_box")
        
        btn_remix = st.button("🌪️ REMIX IMAGE", type="primary", key="btn_remix")

        if btn_remix and prompt_remix:
            with st.status("🌪️ Processing Remix...", expanded=True) as status:
                st.write("📤 Uploading base layer...")
                base_image_url = upload_to_pollinations(uploaded_file)
                
                if base_image_url:
                    st.write("🎨 Applying neural edits...")
                    clean_prompt = prompt_remix.replace(" ", "%20")
                    remix_url = f"https://image.pollinations.ai/prompt/{clean_prompt}?image={base_image_url}&seed={final_seed}&nologo=true&model={selected_model}"
                    
                    # Fetch Bytes for Download
                    st.write("📥 Finalizing pixels...")
                    remix_data = fetch_image_bytes(remix_url)
                    
                    status.update(label="REMIX COMPLETE", state="complete", expanded=False)
                    
                    if remix_data:
                        st.image(remix_data, caption=f"Remixed Seed: {final_seed}", use_container_width=True)
                        st.download_button(
                            label="⬇️ DOWNLOAD REMIX",
                            data=remix_data,
                            file_name=f"akriti_remix_{final_seed}.jpg",
                            mime="image/jpeg",
                            key="dl_remix"
                        )
                    else:
                        st.error("Failed to fetch final image.")
                else:
                    st.error("Upload failed.")
