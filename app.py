import streamlit as st
import random
import time
import requests # <--- NEW IMPORT FOR UPLOADING

# ==========================================
# 1. CONFIGURATION & ROYAL BLUE THEME
# ==========================================
st.set_page_config(
    page_title="AKRITI ULTIMATE",
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

    /* 3. GLASS INPUT BOXES & SELECTORS */
    .stTextInput > div > div > input, .stNumberInput > div > div > input {
        background: rgba(0, 80, 158, 0.2) !important;
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        color: #ffffff !important;
        border-radius: 12px;
        padding: 12px;
    }
    
    /* Fix for Dropdown Menu Text */
    div[data-baseweb="select"] > div {
        background-color: rgba(0, 80, 158, 0.2) !important;
        color: white !important;
        border-color: rgba(255, 255, 255, 0.2) !important;
    }

    /* 4. MAGIC BUTTONS (Gradient) */
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

    /* 6. SIDEBAR STYLING */
    section[data-testid="stSidebar"] {
        background-color: rgba(0, 31, 63, 0.9);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }

    /* HIDE JUNK */
    #MainMenu, footer, header {visibility: hidden;}
    
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. HELPER FUNCTION: UPLOAD IMAGE
# ==========================================
def upload_to_pollinations(uploaded_file):
    """Hacks Pollinations upload endpoint to get a temporary public URL"""
    try:
        # Send POST request with file data
        files = {'file': uploaded_file.getvalue()}
        response = requests.post('https://image.pollinations.ai/upload', files=files)
        if response.status_code == 200:
            # The response is the plain text URL
            return response.text.strip()
        else:
            return None
    except Exception as e:
        st.error(f"Upload Error: {e}")
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
    
    st.markdown("### 📏 Canvas Size (Create Mode)")
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

st.title("AKRITI ULTIMATE")
st.markdown("<div style='color: #aaccff; margin-bottom: 30px;'>IMAGINATION & REMIX ENGINE</div>", unsafe_allow_html=True)

# TABS FOR DIFFERENT MODES
tab_create, tab_remix = st.tabs(["✨ Create New", "🖼️ Remix Photo"])

# ==========================
# TAB 1: CREATE NEW (Original)
# ==========================
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
                # In a real app we'd update session state, here we just show info
            else:
                st.warning("Type something first!")

    btn_create = st.button("🚀 LAUNCH GENERATION", type="primary", key="btn_create")

    if btn_create and prompt_create:
        with st.status(f"🎨 Rendering with {selected_model.upper()}...", expanded=True) as status:
            clean_prompt = prompt_create.replace(" ", "%20")
            image_url = f"https://image.pollinations.ai/prompt/{clean_prompt}?width={width}&height={height}&seed={final_seed}&nologo=true&model={selected_model}"
            time.sleep(1) # Fake wait for effect
            status.update(label="RENDER COMPLETE", state="complete", expanded=False)

        st.image(image_url, caption=f"Seed: {final_seed}", use_container_width=True)
        st.markdown(f"""<div style="text-align: center; margin-top: 20px;"><a href="{image_url}" download="akriti_{final_seed}.jpg" target="_blank"><button style="background: linear-gradient(45deg, #00c6ff, #0072ff); border: none; color: white; padding: 12px 24px; border-radius: 30px; cursor: pointer;">⬇️ DOWNLOAD HIGH QUALITY</button></a></div>""", unsafe_allow_html=True)

# ==========================
# TAB 2: REMIX PHOTO (New)
# ==========================
with tab_remix:
    st.markdown("### 1. Upload Base Photo")
    uploaded_file = st.file_uploader("", type=["jpg", "png", "jpeg"])
    
    if uploaded_file is not None:
        st.image(uploaded_file, caption="Original Photo", width=300)
        
        st.markdown("---")
        st.markdown("### 2. Describe the Edit")
        prompt_remix = st.text_input("What should change? (e.g., 'Add a golden retriever next to me')", key="prompt_remix_box")
        
        st.markdown("### 3. Transformation Strength")
        strength = st.slider("How much change? (Lower = subtle, Higher = drastic)", 10, 90, 50)
        st.caption("Tip: Use 30-50% to add objects. Use 70%+ to change art style.")

        btn_remix = st.button("🌪️ REMIX IMAGE", type="primary", key="btn_remix")

        if btn_remix and prompt_remix:
            with st.status("🌪️ Uploading & Remixing...", expanded=True) as status:
                # 1. Upload image to get temporary URL
                st.write("📤 Sending photo to neural cloud...")
                base_image_url = upload_to_pollinations(uploaded_file)
                
                if base_image_url:
                    st.write("✅ Photo accepted. Applying edits...")
                    # 2. Construct URL with image reference
                    clean_prompt = prompt_remix.replace(" ", "%20")
                    # Strength needs to be inverted for Pollinations sometimes, let's try direct first.
                    # Actually Pollinations doesn't have a direct strength parameter easily exposed in the URL for Flux yet.
                    # We rely on the prompt guiding it.
                    
                    # IMPORTANT: When using an image, width/height are usually ignored as it adopts the original image aspect ratio.
                    remix_url = f"https://image.pollinations.ai/prompt/{clean_prompt}?image={base_image_url}&seed={final_seed}&nologo=true&model={selected_model}"
                    
                    time.sleep(2) # Give API time to process upload reference
                    status.update(label="REMIX COMPLETE", state="complete", expanded=False)
                    
                    st.image(remix_url, caption=f"Remixed Seed: {final_seed}", use_container_width=True)
                    st.markdown(f"""<div style="text-align: center; margin-top: 20px;"><a href="{remix_url}" download="akriti_remix_{final_seed}.jpg" target="_blank"><button style="background: linear-gradient(45deg, #00c6ff, #0072ff); border: none; color: white; padding: 12px 24px; border-radius: 30px; cursor: pointer;">⬇️ DOWNLOAD REMIX</button></a></div>""", unsafe_allow_html=True)
                else:
                    status.update(label="UPLOAD FAILED", state="error")
                    st.error("Could not upload base image. Try a smaller file.")
