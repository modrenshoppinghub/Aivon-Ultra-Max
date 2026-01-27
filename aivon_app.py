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
    .price-tag { background: #1a1a1a; padding: 15px; border-radius: 10px; border: 1px solid #7000ff; text-align: center; min-height: 250px; }
    .pay-link { color: #00f2ff; font-weight: bold; text-decoration: none; border: 1px solid #00f2ff; padding: 5px 10px; border-radius: 5px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SIDEBAR (Core & Payments) ---
with st.sidebar:
    st.markdown("<h1 style='color: #00f2ff;'>💠 Aivon Core</h1>", unsafe_allow_html=True)
    st.write("● Status: **Online**")
    st.write("● Mode: **Enterprise Multimedia**")
    st.divider()
    
    groq_api = st.text_input("🔑 Groq API Key", type="password", help="Enter your Groq key.")
    
    st.divider()
    st.markdown("### 💰 Subscription Status")
    st.info("Current Plan: **FREE TRIAL**")
    
    # Yahan apna Stripe Payment link paste karein
    stripe_url = "https://buy.stripe.com/test_demo_link" 
    if st.button("⭐ Upgrade to Pro"):
        st.markdown(f'<p style="text-align:center;"><a href="{stripe_url}" target="_blank" class="pay-link">Click here to Pay Securely</a></p>', unsafe_allow_html=True)

# --- 3. MAIN DASHBOARD ---
st.markdown('<div class="main-title">AIVON ULTRA MAX 2026</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">The Future of AI-Driven Business Intelligence</div>', unsafe_allow_html=True)

col_main = st.columns([1, 4, 1])
with col_main[1]:
    topic = st.text_input("🌐 Strategic Vision Input:", placeholder="Enter a trend (e.g., AI-Driven Tourism 2026)")
    execute_btn = st.button("🚀 EXECUTE FULL MULTIMEDIA GENERATION")

if execute_btn:
    if not groq_api:
        st.error("Intelligence Core Offline: Please provide Groq API Key in the sidebar.")
    elif not topic:
        st.warning("Please define a Strategic Vision first.")
    else:
        try:
            with st.status("🛠️ Initializing Neural Agents...", expanded=True) as status:
                # PHASE 1: Visual Generation
                st.write("🖼️ Generating Cinematic Visual Asset...")
                encoded_topic = urllib.parse.quote(topic)
                image_url = f"https://pollinations.ai/p/{encoded_topic}?width=1280&height=720&model=flux&nologo=true"
                st.image(image_url, caption=f"AI Visual for: {topic}", use_container_width=True)
                
                # PHASE 2: LLM Configuration
                aivon_llm = LLM(
                    model="groq/llama-3.3-70b-versatile",
                    api_key=groq_api
                )
                
                # PHASE 3: AI Agents Setup
                researcher = Agent(
                    role='Intelligence Officer',
                    goal=f'Analyze {topic} for 2026 market trends',
                    backstory="Ex-CIA data analyst specializing in future tech trends.",
                    llm=aivon_llm,
                    allow_delegation=False
                )

                director = Agent(
                    role='Creative Director',
                    goal=f'Create a high-conversion video script for {topic}',
                    backstory="Award-winning filmmaker focused on viral AI content.",
                    llm=aivon_llm,
                    allow_delegation=False
                )

                task1 = Task(description=f"Research 3 breakthrough insights for {topic}.", expected_output="An Intelligence Brief.", agent=researcher)
                task2 = Task(description="Write a 60-second viral video script with scene descriptions.", expected_output="A production-ready Script.", agent=director)

                crew = Crew(agents=[researcher, director], tasks=[task1, task2])
                result = crew.kickoff()
                
                status.update(label="✅ Analysis Complete!", state="complete")

            # --- 4. DISPLAY RESULTS ---
            st.divider()
            res_col1, res_col2 = st.columns([1.5, 1])

            with res_col1:
                st.markdown("### 🎬 Production Storyboard")
                st.markdown(f'<div class="report-card">{result.raw}</div>', unsafe_allow_html=True)
                st.download_button("📥 Download Report", data=str(result.raw), file_name="Aivon_Report.txt")

            with res_col2:
                st.markdown("### 🖼️ Neural Visual")
                st.image(image_url, caption="Final AI Asset", use_container_width=True)
                st.success("4K Asset Ready for Export")

        except Exception as e:
            st.error(f"System Error: {e}")

# --- 5. PRICING SECTION ---
st.divider()
st.markdown("<h2 style='text-align: center;'>💼 Enterprise Monetization</h2>", unsafe_allow_html=True)
p_col1, p_col2, p_col3 = st.columns(3)

with p_col1:
    st.markdown('<div class="price-tag"><h3>Basic</h3><p>FREE</p><ul><li>3 Daily Researches</li><li>Standard Images</li></ul></div>', unsafe_allow_html=True)

with p_col2:
    st.markdown('<div class="price-tag" style="border-color: #00f2ff;"><h3>Pro</h3><p>$19/mo</p><ul><li>Unlimited Research</li><li>4K Neural Visuals</li></ul><br><small>Pay via Stripe Sidebar</small></div>', unsafe_allow_html=True)

with p_col3:
    st.markdown('<div class="price-tag"><h3>Elite</h3><p>$49/mo</p><ul><li>Full Automation</li><li>Priority Support</li></ul></div>', unsafe_allow_html=True)
