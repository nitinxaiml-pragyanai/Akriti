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

# THE LEGENDARY CSS (Fixed for Visibility)
st.markdown("""
<style>
    /* GLOBAL TEXT VISIBILITY */
    .stApp, p, h1, h2, h3, h4, h5, label, span, div {
        color: #ffffff !important;
        font-family: 'Inter', sans-serif;
    }

    /* BACKGROUND: DEEP SPACE IMPERIAL */
    .stApp {
        background: linear-gradient(180deg, #020024 0%, #090979 35%, #00d4ff 100%);
        background-attachment: fixed;
    }

    /* CONTROL DECK (The new Menu) */
    div[data-testid="stExpander"] {
        background-color: rgba(0, 0, 0, 0.6);
        border: 1px solid #00d4ff;
        border-radius: 15px;
    }

    /* INPUTS */
    .stTextInput > div > div > input {
        background-color: rgba(255,255,255,0.1) !important;
        color: white !important;
        border: 1px solid rgba(255,255,255,0.2);
        border-radius: 10px;
    }

    /* BUTTONS */
    div.stButton > button {
        background: linear-gradient(45deg, #FF0099, #493240);
        border: none;
        color: white;
        font-weight: bold;
        transition: 0.3s;
    }
    div.stButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0 0 20px #FF0099;
    }

    /* HIDE STREAMLIT BRANDING */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. SESSION STATE (The Memory)
# ==========================================
if 'history' not in st.session_state:
    st.session_state.history = []

# ==========================================
# 3. HELPER FUNCTIONS
# ==========================================
def fetch_image(url):
    try:
        r = requests.get(url, timeout=5)
        if r.status_code == 200: return r.content
    except: return None

# ==========================================
# 4. THE CONTROL DECK (Main Screen Menu)
# ==========================================
st.title("👑 AKRITI OMEGA")
st.markdown("### The World's Most Advanced Visual Engine")

# WE USE COLUMNS INSTEAD OF SIDEBAR so you can see it!
st.markdown("---")
with st.expander("🎛️ CONTROL CENTER (Open for Settings)", expanded=True):
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.markdown("#### 🧠 AI Brain")
        model = st.selectbox("", ["Flux (Best)", "Flux-Realism", "Flux-Anime", "Flux-3D", "Turbo (Fast)"], label_visibility="collapsed")
        model_code = model.split(" ")[0].lower() # extracts 'flux', 'turbo' etc
        
    with c2:
        st.markdown("#### 📐 Aspect Ratio")
        ratio = st.selectbox("", ["Square (1:1)", "Portrait (9:16)", "Landscape (16:9)", "Wide (21:9)"], label_visibility="collapsed")
        
        # Smart Logic for Dimensions
        if "Square" in ratio: w, h = 1024, 1024
        elif "Portrait" in ratio: w, h = 768, 1344
        elif "Landscape" in ratio: w, h = 1344, 768
        elif "Wide" in ratio: w, h = 1536, 640

    with c3:
        st.markdown("#### 🎨 Style Preset")
        style = st.selectbox("", ["None", "Cyberpunk", "Studio Photo", "Oil Painting", "Pixar 3D", "Dark Fantasy"], label_visibility="collapsed")

st.markdown("---")

# ==========================================
# 5. INPUT SECTOR
# ==========================================
col_prompt, col_btn = st.columns([4, 1])

with col_prompt:
    prompt_text = st.text_input("Describe your vision...", placeholder="e.g. A futuristic glass temple in the clouds")
    negative = st.text_input("Negative Prompt (What to remove?)", placeholder="blur, ugly, bad hands, cartoon")

with col_btn:
    st.write("")
    st.write("")
    generate = st.button("🚀 IGNITE", type="primary", use_container_width=True)

# ==========================================
# 6. EXECUTION ENGINE
# ==========================================
if generate and prompt_text:
    
    # 1. BUILD THE MASTER PROMPT
    final_prompt = prompt_text
    if style != "None":
        final_prompt += f", {style} style"
    
    # Clean up for URL
    url_prompt = final_prompt.replace(" ", "%20")
    seed = random.randint(0, 1000000)
    
    # 2. GENERATE URL
    image_url = f"https://image.pollinations.ai/prompt/{url_prompt}?width={w}&height={h}&seed={seed}&nologo=true&model={model_code}"
    
    # 3. SHOW PREVIEW INSTANTLY
    st.markdown(f"### ✨ Result: {style if style != 'None' else 'Custom'}")
    
    # Use a container to make it look framed
    with st.container():
        st.image(image_url, caption=f"{model} | {w}x{h}", use_container_width=True)
    
    # 4. BACKGROUND DOWNLOAD FETCH
    with st.spinner("💾 Preparing High-Res File..."):
        img_data = fetch_image(image_url)
        if img_data:
            c_dl1, c_dl2 = st.columns(2)
            with c_dl1:
                st.download_button("⬇️ DOWNLOAD NOW", data=img_data, file_name=f"akriti_{seed}.jpg", mime="image/jpeg", use_container_width=True)
            with c_dl2:
                st.success("✅ Ready to Save")
            
            # Save to History
            st.session_state.history.insert(0, {"data": img_data, "prompt": final_prompt})

# ==========================================
# 7. GALLERY (Recent Works)
# ==========================================
if len(st.session_state.history) > 0:
    st.markdown("---")
    st.markdown("### 🕰️ Recent Creations")
    
    # Show last 3 images in columns
    h_cols = st.columns(3)
    for i, item in enumerate(st.session_state.history[:3]):
        with h_cols[i]:
            st.image(item['data'], use_container_width=True)
            st.caption(item['prompt'][:30] + "...")
