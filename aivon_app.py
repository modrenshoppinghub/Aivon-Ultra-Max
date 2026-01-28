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
        font-family: 'Courier New', Courier, monospace;
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
    .price-tag { background: #111; padding: 15px; border-radius: 10px; border: 1px solid #7000ff; text-align: center; min-height: 220px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SIDEBAR (Payments & Navigation) ---
with st.sidebar:
    st.markdown("<h1 style='color: #00f2ff;'>💠 Aivon Core</h1>", unsafe_allow_html=True)
    st.write("● Status: **Online**")
    st.write("● App Mode: **Installed**")
    st.divider()
    
    groq_api = st.text_input("🔑 Groq API Key", type="password", help="Enter your Groq API key here")
    
    st.divider()
    st.markdown("### 💎 Manage Subscription")
    tier = st.selectbox("Current Tier:", ["Basic (Free)", "Pro ($19/mo)", "Elite ($49/mo)", "Enterprise ($100/Full)"])
    
    # Payoneer Enterprise Link
    payoneer_url = "https://link.payoneer.com/Token?t=08188776795A4054A03D813DC3816C08&src=prq"
    
    if "Enterprise" in tier:
        st.markdown(f'<a href="{payoneer_url}" target="_blank" class="pay-btn">💳 Pay $100 for Enterprise</a>', unsafe_allow_html=True)
    elif "Basic" in tier:
        st.success("Active: Free Trial (Limited)")
    else:
        st.info(f"Payment link for {tier} is being generated. Use Enterprise for now.")

    st.divider()
    if st.button("📱 Mobile/Windows Install"):
        st.info("Chrome/Edge: URL bar mein 'Install' icon par click karein.\n\nMobile: Browser menu se 'Add to Home Screen' select karein.")

# --- 3. MAIN DASHBOARD ---
st.markdown('<div class="main-title">AIVON ULTRA MAX 2026</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Automated Business Intelligence & Multimedia Engine</div>', unsafe_allow_html=True)

col_input, col_action = st.columns([4, 1])
with col_input:
    topic = st.text_input("🌐 Strategic Vision Input:", placeholder="Enter a trend or industry (e.g., Future of AI in Space)")
with col_action:
    st.write("##")
    execute_btn = st.button("🚀 EXECUTE")

if execute_btn:
    if not groq_api:
        st.error("Error: Please provide your Groq API Key in the sidebar.")
    elif not topic:
        st.warning("Warning: Please enter a topic to analyze.")
    else:
        try:
            with st.status("🛠️ Neural Agents Working...", expanded=True) as status:
                # 1. LLM Setup
                aivon_llm = LLM(model="groq/llama-3.3-70b-versatile", api_key=groq_api)
                
                # 2. Visual Generation
                st.write("🖼️ Creating 4K Cinematic Visual...")
                encoded_topic = urllib.parse.quote(topic)
                image_url = f"https://pollinations.ai/p/{encoded_topic}?width=1280&height=720&model=flux&seed=42"
                st.image(image_url, caption=f"Neural Projection: {topic}", use_container_width=True)
                
                # 3. Intelligence Agent Logic
                researcher = Agent(
                    role='Intelligence Officer',
                    goal=f'Generate 3 breakthrough insights for {topic} in 2026',
                    backstory="Global trend analyst specializing in exponential technologies.",
                    llm=aivon_llm,
                    allow_delegation=False
                )

                task = Task(
                    description=f"Analyze {topic} and provide a detailed brief including Executive Summary, 3 Insights, and Recommendations.",
                    expected_output="A structured Intelligence Brief in Markdown.",
                    agent=researcher
                )

                crew = Crew(agents=[researcher], tasks=[task])
                result = crew.kickoff()
                
                status.update(label="✅ Generation Complete!", state="complete")

            # --- 4. DISPLAY RESULTS & DOWNLOAD ---
            st.divider()
            st.markdown("### 🎬 Strategic Intelligence Report")
            st.markdown(f'<div class="report-card">{result.raw}</div>', unsafe_allow_html=True)
            
            # PDF/Text Download Button
            st.download_button(
                label="📥 Download This Report",
                data=str(result.raw),
                file_name=f"Aivon_Report_{topic.replace(' ', '_')}.txt",
                mime="text/plain"
            )

        except Exception as e:
            st.error(f"System Error: {e}")

# --- 5. MONETIZATION GRID ---
st.divider()
st.markdown("<h2 style='text-align: center;'>💼 Enterprise Monetization</h2>", unsafe_allow_html=True)
p_col1, p_col2, p_col3 = st.columns(3)

with p_col1:
    st.markdown('<div class="price-tag"><h3>Basic</h3><p>FREE</p><hr><ul><li>3 Daily Researches</li><li>Standard Images</li></ul></div>', unsafe_allow_html=True)
with p_col2:
    st.markdown('<div class="price-tag" style="border-color: #00f2ff;"><h3>Pro</h3><p>$19/mo</p><hr><ul><li>Unlimited Research</li><li>4K Neural Visuals</li></ul></div>', unsafe_allow_html=True)
with p_col3:
    st.markdown('<div class="price-tag"><h3>Elite</h3><p>$49/mo</p><hr><ul><li>Full Automation</li><li>Priority Support</li></ul></div>', unsafe_allow_html=True)

st.markdown("<p style='text-align: center; color: #555;'>Aivon Ultra Max © 2026 - Powered by Neural Intelligence</p>", unsafe_allow_html=True)
