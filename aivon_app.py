import streamlit as st
import os
import urllib.parse
from crewai import Agent, Task, Crew, LLM

# --- SYSTEM SETTINGS ---
os.environ["OTEL_SDK_DISABLED"] = "true"

# --- 1. PWA & PRO UI DESIGN ---
st.set_page_config(
    page_title="Aivon Ultra Max | AI Business Engine", 
    layout="wide", 
    page_icon="💠"
)

st.markdown("""
    <head>
        <meta name="apple-mobile-web-app-capable" content="yes">
        <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
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
        background: #00f2ff; color: #000 !important; 
        padding: 12px; border-radius: 8px; font-weight: bold;
        text-decoration: none; margin-top: 10px;
    }
    .price-tag { background: #111; padding: 15px; border-radius: 10px; border: 1px solid #7000ff; text-align: center; min-height: 200px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SIDEBAR (Payments & Core) ---
with st.sidebar:
    st.markdown("<h1 style='color: #00f2ff;'>💠 Aivon Core</h1>", unsafe_allow_html=True)
    st.write("● Status: **Online**")
    st.write("● Mode: **Enterprise multimedia**")
    st.divider()
    
    groq_api = st.text_input("🔑 Groq API Key", type="password")
    
    st.divider()
    st.markdown("### 💎 Subscription Plans")
    plan = st.selectbox("Select your tier:", ["Basic (Free)", "Pro ($19/mo)", "Elite ($49/mo)", "Enterprise ($100/Full)"])
    
    # Payoneer Link for Enterprise Plan
    payoneer_url = "https://link.payoneer.com/Token?t=08188776795A4054A03D813DC3816C08&src=prq"
    
    if "Enterprise" in plan:
        st.markdown(f'<a href="{payoneer_url}" target="_blank" class="pay-btn">💳 Pay $100 via Payoneer</a>', unsafe_allow_html=True)
    elif "Basic" in plan:
        st.success("Currently active on Free Trial.")
    else:
        st.warning(f"Payment link for {plan} is being updated. Please use Enterprise for instant access.")
    
    st.caption("Note: After payment, send your receipt to support for activation.")
    
    st.divider()
    if st.button("📱 Install as App"):
        st.info("On Desktop: Click the 'Install' icon in your browser URL bar. \n\nOn Mobile: Tap '3 dots' -> 'Add to Home Screen'.")

# --- 3. MAIN DASHBOARD ---
st.markdown('<div class="main-title">AIVON ULTRA MAX 2026</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Multi-Platform Enterprise Business Intelligence</div>', unsafe_allow_html=True)

topic = st.text_input("🌐 Strategic Vision Topic:", placeholder="e.g., Impact of 6G on Global Economy")
execute_btn = st.button("🚀 EXECUTE FULL MULTIMEDIA GENERATION")

if execute_btn:
    if not groq_api:
        st.error("Please enter Groq API Key.")
    elif not topic:
        st.warning("Please enter a vision topic.")
    else:
        try:
            with st.status("🛠️ System Initializing Agents...", expanded=True) as status:
                # LLM & Agent Setup
                aivon_llm = LLM(model="groq/llama-3.3-70b-versatile", api_key=groq_api)
                
                # Image Logic
                encoded_topic = urllib.parse.quote(topic)
                image_url = f"https://pollinations.ai/p/{encoded_topic}?width=1280&height=720&model=flux"
                st.image(image_url, caption=f"Neural Asset: {topic}", use_container_width=True)
                
                # Intelligence Agent
                researcher = Agent(
                    role='Intelligence Officer', 
                    goal=f'Analyze {topic} for 2026 trends', 
                    backstory="Data Expert", 
                    llm=aivon_llm
                )
                
                task = Task(description=f"Generate 3 breakthrough insights for {topic}.", expected_output="A Detailed Intelligence Brief.", agent=researcher)
                
                crew = Crew(agents=[researcher], tasks=[task])
                result = crew.kickoff()
                
                status.update(label="✅ Analysis Complete!", state="complete")
            
            st.markdown("### 🎬 Intelligence Brief Output")
            st.markdown(f'<div class="report-card">{result.raw}</div>', unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"System Error: {e}")

# --- 4. PRICING GRID ---
st.divider()
st.markdown("<h2 style='text-align: center;'>💼 Enterprise Monetization</h2>", unsafe_allow_html=True)
p_col1, p_col2, p_col3 = st.columns(3)

with p_col1:
    st.markdown('<div class="price-tag"><h3>Basic</h3><p>FREE</p><ul><li>3 Daily Researches</li><li>Standard Images</li></ul></div>', unsafe_allow_html=True)
with p_col2:
    st.markdown('<div class="price-tag" style="border-color: #00f2ff;"><h3>Pro</h3><p>$19/mo</p><ul><li>Unlimited Research</li><li>4K Neural Visuals</li></ul></div>', unsafe_allow_html=True)
with p_col3:
    st.markdown('<div class="price-tag"><h3>Elite</h3><p>$49/mo</p><ul><li>Full Automation</li><li>Priority Support</li></ul></div>', unsafe_allow_html=True)
