import streamlit as st
import os
import urllib.parse
from crewai import Agent, Task, Crew, LLM

# --- SYSTEM SETTINGS ---
os.environ["OTEL_SDK_DISABLED"] = "true"

# --- 1. PRO UI & DESIGN ---
st.set_page_config(page_title="Aivon Ultra Max | AI Business Engine", layout="wide", page_icon="💠")

st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #ffffff; }
    .main-title { text-align: center; color: #00f2ff; font-size: 50px; font-weight: bold; text-shadow: 0 0 15px #00f2ff; }
    .sub-title { text-align: center; color: #7000ff; font-size: 20px; margin-bottom: 30px; }
    .report-card { 
        background: rgba(255, 255, 255, 0.05); 
        padding: 25px; border-radius: 20px; 
        border: 1px solid #00f2ff; 
        box-shadow: 0 0 20px rgba(0, 242, 255, 0.3);
        margin-top: 20px;
        white-space: pre-wrap;
    }
    .stButton>button {
        background: linear-gradient(45deg, #00f2ff, #7000ff);
        color: white; border: none; padding: 18px; font-weight: bold; border-radius: 12px;
        width: 100%; transition: 0.3s;
    }
    .stButton>button:hover { transform: scale(1.02); box-shadow: 0 0 20px #00f2ff; }
    .price-tag { background: #1a1a1a; padding: 15px; border-radius: 10px; border: 1px solid #7000ff; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SIDEBAR ---
with st.sidebar:
    st.markdown("<h1 style='color: #00f2ff;'>💠 Aivon Core</h1>", unsafe_allow_html=True)
    st.write("● Status: **Online**")
    st.write("● Mode: **Enterprise Multimedia**")
    st.divider()
    
    groq_api = st.text_input("🔑 Groq API Key", type="password", help="Enter your Groq key.")
    
    st.divider()
    st.markdown("### 💰 Subscription Status")
    st.info("Current Plan: **FREE TRIAL**")
    
    # Apna real Stripe link yahan dalein
    stripe_url = "https://buy.stripe.com/test_demo" 
    if st.button("⭐ Upgrade to Pro"):
        st.markdown(f'<a href="{stripe_url}" target="_blank" style="text-decoration:none; color:white; background:#00f2ff; padding:10px; border-radius:5px; display:block; text-align:center;">Pay with Stripe</a>', unsafe_allow_html=True)

# --- 3. MAIN DASHBOARD ---
st.markdown('<div class="main-title">AIVON ULTRA MAX 2026</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">The Future of AI-Driven Business Intelligence</div>', unsafe_allow_html=True)

col_main = st.columns([1, 4, 1])
with col_main[1]:
    topic = st.text_input("🌐 Strategic Vision Input:", placeholder="Enter a trend (e.g., Future of AI Tourism)")
    execute_btn = st.button("🚀 EXECUTE FULL MULTIMEDIA GENERATION")

if execute_btn:
    if not groq_api:
        st.error("Please provide Groq API Key.")
    elif not topic:
        st.warning("Please enter a topic.")
    else:
        try:
            with st.status("🛠️ Initializing Neural Agents...", expanded=True) as status:
                # Agent LLM Setup
                aivon_llm = LLM(model="groq/llama-3.3-70b-versatile", api_key=groq_api)
                
                # Visual Asset
                st.write("🖼️ Generating Cinematic Visual Asset...")
                encoded_topic = urllib.parse.quote(topic)
                image_url = f"https://pollinations.ai/p/{encoded_topic}?width=1280&height=720&model=flux&nologo=true"
                st.image(image_url, caption=f"AI Visual for: {topic}", use_container_width=True)
                
                # Crew Setup
                researcher = Agent(
                    role='Intelligence Officer', 
                    goal=f'Analyze {topic} for 2026 trends', 
                    backstory="Data Expert", 
                    llm=aivon_llm,
                    allow_delegation=False
                )
                
                task1 = Task(
                    description=f"Research 3 breakthrough insights for {topic}.", 
                    expected_output="An Intelligence Brief.", 
                    agent=researcher
                )
                
                crew = Crew(agents=[researcher], tasks=[task1])
                result = crew.kickoff()
                
                status.update(label="✅ Analysis Complete!", state="complete")
                
            # Results display
            st.divider()
            st.markdown("### 🎬 Analysis Report")
            st.markdown(f'<div class="report-card">{result.raw}</div>', unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"Error: {e}")

# --- 4. PRICING ---
st.divider()
p_col1, p_col2, p_col3 = st.columns(3)
with p_col2:
    st.markdown('<div class="price-tag"><h3>Pro Plan</h3><p>$19/mo</p><ul><li>Unlimited AI Research</li><li>4K Visual Assets</li></ul></div>', unsafe_allow_html=True)
