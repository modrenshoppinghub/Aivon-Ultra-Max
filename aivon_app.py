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
        padding: 12px; border-radius: 8px; font-weight: bold;
        text-decoration: none; margin-top: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. FIXED PDF GENERATION FUNCTION ---
def create_pdf(text, topic):
    pdf = FPDF()
    pdf.add_page()
    
    # Header
    pdf.set_font("Arial", "B", 22)
    pdf.cell(200, 15, txt="AIVON STRATEGIC REPORT 2026", ln=True, align='C')
    pdf.ln(5)
    
    # Topic
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, txt=f"Strategy Topic: {topic}", ln=True, align='L')
    pdf.ln(10)
    
    # Body (Clean text handling for Latin-1)
    pdf.set_font("Arial", "", 12)
    clean_text = text.encode('latin-1', 'replace').decode('latin-1')
    pdf.multi_cell(0, 10, txt=clean_text)
    
    # Footer Section
    pdf.ln(20)
    pdf.set_draw_color(0, 242, 255)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(5)
    
    pdf.set_font("Arial", "B", 10)
    pdf.cell(0, 10, txt="Business Contact: msubhanalmani1199@gmail.com | WhatsApp: 03229270513", ln=True, align='C')
    
    # .output(dest='S') returns bytes directly in modern fpdf2
    return pdf.output()

# --- 3. SIDEBAR ---
with st.sidebar:
    st.markdown("<h1 style='color: #00f2ff;'>💠 Aivon Core v3.0</h1>", unsafe_allow_html=True)
    st.write("● WhatsApp: **03229270513**")
    st.divider()
    
    groq_api = st.text_input("🔑 Enterprise API Key", type="password")
    
    st.divider()
    st.markdown("### 💎 Manage Subscription")
    plan = st.selectbox("Select Plan:", ["Free Trial", "Starter ($10)", "Professional ($25)", "Enterprise ($50)"])
    
    payoneer_url = "https://link.payoneer.com/Token?t=08188776795A4054A03D813DC3816C08&src=prq"
    
    if plan != "Free Trial":
        st.markdown(f'<a href="{payoneer_url}" target="_blank" class="pay-btn">💳 Pay for {plan}</a>', unsafe_allow_html=True)

# --- 4. MAIN DASHBOARD ---
st.markdown('<div class="main-title">AIVON ULTRA MAX</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">BEYOND ARTIFICIAL INTELLIGENCE</div>', unsafe_allow_html=True)

topic = st.text_input("🚀 Strategic Topic:", placeholder="e.g., Future of AI in Tourism 2026")
execute_btn = st.button("EXECUTE NEURAL GENERATION")

if execute_btn:
    if not groq_api:
        st.error("Please enter Groq API Key.")
    elif not topic:
        st.warning("Please enter a topic.")
    else:
        try:
            with st.status("🧠 Processing...", expanded=True) as status:
                aivon_llm = LLM(model="groq/llama-3.3-70b-versatile", api_key=groq_api)
                
                # HD Image
                encoded_topic = urllib.parse.quote(topic)
                image_url = f"https://pollinations.ai/p/{encoded_topic}?width=1920&height=1080&model=flux&enhance=true"
                st.image(image_url, caption=f"Neural Vision: {topic}", use_container_width=True)
                
                # AI Research
                researcher = Agent(role='Global Strategist', goal=f'2026 intelligence report on {topic}', backstory="Lead Strategist.", llm=aivon_llm)
                task = Task(description=f"Deep analysis of {topic}.", expected_output="Markdown Report.", agent=researcher)
                crew = Crew(agents=[researcher], tasks=[task])
                result = crew.kickoff()
                
                status.update(label="✅ Ready!", state="complete")

            st.divider()
            st.markdown(f'<div class="report-card">{result.raw}</div>', unsafe_allow_html=True)
            
            # PDF Download Button
            pdf_data = create_pdf(str(result.raw), topic)
            st.download_button(
                label="📥 Download Professional PDF Report",
                data=pdf_data,
                file_name=f"Aivon_Report_{topic.replace(' ', '_')}.pdf",
                mime="application/pdf"
            )

        except Exception as e:
            st.error(f"Error: {e}")
