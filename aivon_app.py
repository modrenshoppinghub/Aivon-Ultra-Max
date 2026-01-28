import streamlit as st
import os
import urllib.parse
from crewai import Agent, Task, Crew, LLM
from fpdf import FPDF

# --- SYSTEM SETTINGS ---
os.environ["OTEL_SDK_DISABLED"] = "true"

# --- 1. PWA & PRO UI DESIGN ---
st.set_page_config(
    page_title="Aivon Ultra Max | Global AI Engine", 
    layout="wide", 
    page_icon="💠"
)

st.markdown("""
    <style>
    .stApp { background-color: #050505; color: #ffffff; }
    .main-title { text-align: center; color: #00f2ff; font-size: 50px; font-weight: bold; text-shadow: 0 0 20px #00f2ff; }
    .sub-title { text-align: center; color: #7000ff; font-size: 20px; margin-bottom: 30px; letter-spacing: 2px; }
    .report-card { 
        background: rgba(10, 10, 10, 0.9); 
        padding: 30px; border-radius: 20px; 
        border: 2px solid #00f2ff; 
        box-shadow: 0 0 30px rgba(0, 242, 255, 0.2);
        color: #e0e0e0; line-height: 1.6;
    }
    .stButton>button {
        background: linear-gradient(90deg, #00f2ff, #7000ff);
        color: white; border: none; padding: 20px; font-size: 18px; font-weight: bold; border-radius: 15px;
        width: 100%; transition: 0.5s; cursor: pointer;
    }
    .stButton>button:hover { transform: scale(1.02); box-shadow: 0 0 40px #7000ff; }
    .pay-btn {
        display: block; width: 100%; text-align: center;
        background: #00f2ff; color: #000 !important; 
        padding: 15px; border-radius: 10px; font-weight: bold;
        text-decoration: none; margin-top: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. PDF GENERATION FUNCTION ---
def create_pdf(text, topic):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 20)
    pdf.cell(200, 10, txt="AIVON STRATEGIC REPORT 2026", ln=True, align='C')
    pdf.ln(10)
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, txt=f"Topic: {topic}", ln=True, align='L')
    pdf.ln(5)
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 10, txt=text)
    return pdf.output(dest='S').encode('latin-1')

# --- 3. SIDEBAR (Advanced Controls) ---
with st.sidebar:
    st.markdown("<h1 style='color: #00f2ff;'>💠 Aivon Core v3.0</h1>", unsafe_allow_html=True)
    st.write("● Engine: **Neural 70B**")
    st.write("● Status: **Global Ready**")
    st.divider()
    
    groq_api = st.text_input("🔑 Enterprise API Key", type="password")
    
    st.divider()
    st.markdown("### 💳 Unlock Full Features")
    payoneer_url = "https://link.payoneer.com/Token?t=08188776795A4054A03D813DC3816C08&src=prq"
    st.markdown(f'<a href="{payoneer_url}" target="_blank" class="pay-btn">Activate Enterprise ($100)</a>', unsafe_allow_html=True)
    
    st.divider()
    if st.button("📱 Install Mobile App"):
        st.info("Browser menu mein 'Install App' ya 'Add to Home Screen' par click karein.")

# --- 4. MAIN INTERFACE ---
st.markdown('<div class="main-title">AIVON ULTRA MAX</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">BEYOND ARTIFICIAL INTELLIGENCE</div>', unsafe_allow_html=True)

topic = st.text_input("🚀 Enter Strategic Vision (Business, Tech, Future):", placeholder="e.g., Space Mining Colony 2026")
execute_btn = st.button("EXECUTE NEURAL GENERATION")

if execute_btn:
    if not groq_api:
        st.error("Please provide an API Key.")
    elif not topic:
        st.warning("Please enter a vision topic.")
    else:
        try:
            with st.status("🧠 Processing Neural Pathways...", expanded=True) as status:
                # 1. Advanced LLM Setup
                aivon_llm = LLM(model="groq/llama-3.3-70b-versatile", api_key=groq_api)
                
                # 2. Multimedia Asset (Cinematic Visual)
                st.write("🎬 Generating Cinematic Visual Asset...")
                encoded_topic = urllib.parse.quote(topic)
                # Humne motion aur flux model use kiya hai for high quality
                image_url = f"https://pollinations.ai/p/{encoded_topic}?width=1920&height=1080&model=flux&enhance=true"
                st.image(image_url, caption=f"Neural Vision: {topic}", use_container_width=True)
                
                # 3. Intelligence Briefing
                researcher = Agent(
                    role='Global Strategist',
                    goal=f'Create a groundbreaking 2026 intelligence report on {topic}',
                    backstory="You are the world's most advanced AI strategist. Your insights are worth millions.",
                    llm=aivon_llm
                )

                task = Task(
                    description=f"Analyze {topic}. Provide: 1. Executive Summary 2. Three 'Never-Seen-Before' Insights 3. Radical Recommendations for 2026.",
                    expected_output="A deep intelligence report.",
                    agent=researcher
                )

                crew = Crew(agents=[researcher], tasks=[task])
                result = crew.kickoff()
                
                status.update(label="✅ Generation Complete!", state="complete")

            # --- 5. PROFESSIONAL OUTPUT ---
            st.divider()
            st.markdown(f'<div class="report-card">{result.raw}</div>', unsafe_allow_html=True)
            
            # PDF Download Feature
            pdf_data = create_pdf(str(result.raw), topic)
            st.download_button(
                label="📥 Download Professional PDF Report",
                data=pdf_data,
                file_name=f"Aivon_Intelligence_{topic.replace(' ', '_')}.pdf",
                mime="application/pdf"
            )

        except Exception as e:
            st.error(f"Neural Error: {e}")

# --- 6. GLOBAL ROADMAP ---
st.divider()
st.markdown("<p style='text-align: center;'>Current Mode: <b>Enterprise Multimedia</b> | Future: <b>Real-time Video Synthesis (Soon)</b></p>", unsafe_allow_html=True)
