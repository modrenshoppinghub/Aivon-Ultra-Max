import streamlit as st
import os
import urllib.parse
from crewai import Agent, Task, Crew, LLM

# --- SYSTEM SETTINGS ---
os.environ["OTEL_SDK_DISABLED"] = "true"

# --- 1. PWA & PRO UI DESIGN ---
# Is section se app mobile aur windows par installable ban jati hai
st.set_page_config(
    page_title="Aivon Ultra Max | AI Business Engine", 
    layout="wide", 
    page_icon="💠"
)

st.markdown("""
    <head>
        <meta name="apple-mobile-web-app-capable" content="yes">
        <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="apple-touch-icon" href="https://pollinations.ai/p/ai_icon?width=180&height=180">
    </head>
    <style>
    .stApp { background-color: #050505; color: #ffffff; }
    .main-title { text-align: center; color: #00f2ff; font-size: 45px; font-weight: bold; text-shadow: 0 0 15px #00f2ff; }
    .sub-title { text-align: center; color: #7000ff; font-size: 18px; margin-bottom: 25px; }
    .report-card { 
        background: rgba(255, 255, 255, 0.05); 
        padding: 20px; border-radius: 15px; 
        border: 1px solid #00f2ff; 
        box-shadow: 0 0 15px rgba(0, 242, 255, 0.2);
        white-space: pre-wrap;
    }
    .stButton>button {
        background: linear-gradient(45deg, #00f2ff, #7000ff);
        color: white; border: none; padding: 15px; font-weight: bold; border-radius: 10px;
        width: 100%; transition: 0.3s;
    }
    .pay-btn {
        display: block; width: 100%; text-align: center;
        background: #ff4b4b; color: white !important; 
        padding: 12px; border-radius: 8px; font-weight: bold;
        text-decoration: none; margin-top: 10px;
    }
    .price-tag { background: #111; padding: 15px; border-radius: 10px; border: 1px solid #7000ff; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SIDEBAR (Payments & Core) ---
with st.sidebar:
    st.markdown("<h1 style='color: #00f2ff;'>💠 Aivon Core</h1>", unsafe_allow_html=True)
    st.write("● Status: **Online**")
    st.write("● Version: **2.0 (PWA Ready)**")
    st.divider()
    
    groq_api = st.text_input("🔑 Groq API Key", type="password")
    
    st.divider()
    st.markdown("### 💎 Pro Subscription")
    st.write("Unlock 2026 Strategy Reports & 4K Visuals.")
    
    # PAYONEER LINK INTEGRATION
    payoneer_url = "https://link.payoneer.com/Token?t=08188776795A4054A03D813DC3816C08&src=prq"
    
    st.markdown(f'<a href="{payoneer_url}" target="_blank" class="pay-btn">💳 Pay $100 via Payoneer</a>', unsafe_allow_html=True)
    st.caption("Note: After payment, features will be unlocked within 2 hours.")
    
    st.divider()
    if st.button("📱 How to Install as App?"):
        st.info("Desktop: Click the 'Install' icon in your browser URL bar. \n\nMobile: Tap '3 dots' -> 'Add to Home Screen'.")

# --- 3. MAIN DASHBOARD ---
st.markdown('<div class="main-title">AIVON ULTRA MAX 2026</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Multi-Platform Enterprise Intelligence</div>', unsafe_allow_html=True)

topic = st.text_input("🌐 Enter Strategic Vision Topic:", placeholder="e.g., Future of Mars Tourism")
execute_btn = st.button("🚀 GENERATE MULTIMEDIA REPORT")

if execute_btn:
    if not groq_api:
        st.error("Please enter Groq API Key in sidebar.")
    elif not topic:
        st.warning("Please enter a topic.")
    else:
        try:
            with st.status("🛠️ System Initializing...", expanded=True) as status:
                # LLM Setup
                aivon_llm = LLM(model="groq/llama-3.3-70b-versatile", api_key=groq_api)
                
                # Image Logic
                encoded_topic = urllib.parse.quote(topic)
                image_url = f"https://pollinations.ai/p/{encoded_topic}?width=1280&height=720&model=flux"
                st.image(image_url, caption=f"Neural Visual: {topic}", use_container_width=True)
                
                # Agent Logic
                researcher = Agent(role='Analyst', goal=f'Analyze {topic}', backstory="Expert", llm=aivon_llm)
                task = Task(description=f"Detailed report on {topic}", expected_output="Text report", agent=researcher)
                
                crew = Crew(agents=[researcher], tasks=[task])
                result = crew.kickoff()
                
                status.update(label="✅ Success!", state="complete")
            
            st.markdown(f'<div class="report-card">{result.raw}</div>', unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"Error: {e}")

# --- 4. MULTI-PLATFORM FOOTER ---
st.divider()
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("🍏 **iOS / Apple**\n\nAdd to Home Screen via Safari.")
with col2:
    st.markdown("🤖 **Android / Play Store**\n\nInstall via Chrome PWA.")
with col3:
    st.markdown("💻 **Windows / Mac**\n\nInstall via Edge/Chrome Desktop.")
