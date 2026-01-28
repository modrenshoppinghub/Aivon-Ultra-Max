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
    .price-box {
        background: #111; padding: 15px; border-radius: 10px; border: 1px solid #7000ff; text-align: center; margin-bottom: 10px;
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

# --- 3. SIDEBAR (Payments & Control) ---
with st.sidebar:
    st.markdown("<h1 style='color: #00f2ff;'>💠 Aivon Core v3.0</h1>", unsafe_allow_html=True)
    st.write("● Status: **Enterprise Ready**")
    st.divider()
    
    groq_api = st.text_input("🔑 Enterprise API Key", type="password")
    
    st.divider()
    st.markdown("### 💎 Choose Your Plan")
    
    # Updated Cheaper Pricing Tiers
    plan = st.selectbox("Select Tier:", ["Basic (Free Trial)", "Starter ($10)", "Professional ($25)", "Enterprise ($50)"])
    
    # Payoneer Link (User can pay any amount via your request link)
    payoneer_url = "https://link.payoneer.com/Token?t=08188776795A4054A03D813DC3816C08&src=prq"
    
    if plan == "Basic (Free Trial)":
        st.info("Limited to 2 researches per day.")
    else:
        st.success(f"Unlock {plan} features now!")
        st.markdown(f'<a href="{payoneer_url}" target="_blank" class="pay-btn">💳 Pay for {plan}</a>', unsafe_allow_html=True)
        st.caption("Payment ke baad screenshot support ko bhejien.")

    st.divider()
    if st.button("📱 Install Mobile App"):
        st.info("Browser menu se 'Add to Home Screen' select karein.")

# --- 4. MAIN INTERFACE ---
st.markdown('<div class="main-title">AIVON ULTRA MAX</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">NEXT-GEN BUSINESS INTELLIGENCE</div>', unsafe_allow_html=True)

topic = st.text_input("🚀 Strategic Topic (Industry, Tech, or Business):", placeholder="e.g., Future of Renewable Energy in Pakistan")
execute_btn = st.button("GENERATE NEURAL ASSETS")

if execute_btn:
    if not groq_api:
        st.error("Please enter your Groq API Key.")
    elif not topic:
        st.warning("Please enter a topic.")
    else:
        try:
            with st.status("🧠 Processing...", expanded=True) as status:
                # LLM Setup
                aivon_llm = LLM(model="groq/llama-3.3-70b-versatile", api_key=groq_api)
                
                # Visual Asset
                encoded_topic = urllib.parse.quote(topic)
                image_url = f"https://pollinations.ai/p/{encoded_topic}?width=1920&height=1080&model=flux&enhance=true"
                st.image(image_url, caption=f"Neural Vision: {topic}", use_container_width=True)
                
                # Intelligence Agent
                researcher = Agent(
                    role='Global Strategist',
                    goal=f'Create a high-value 2026 intelligence report on {topic}',
                    backstory="Top-tier data analyst for global enterprises.",
                    llm=aivon_llm
                )

                task = Task(
                    description=f"Deep analysis of {topic}. Include Executive Summary, 3 Insights, and 2026 Recommendations.",
                    expected_output="Professional Markdown Report.",
                    agent=researcher
                )

                crew = Crew(agents=[researcher], tasks=[task])
                result = crew.kickoff()
                
                status.update(label="✅ Success!", state="complete")

            # Display Results
            st.divider()
            st.markdown(f'<div class="report-card">{result.raw}</div>', unsafe_allow_html=True)
            
            # PDF Download
            pdf_data = create_pdf(str(result.raw), topic)
            st.download_button(
                label="📥 Download Professional PDF",
                data=pdf_data,
                file_name=f"Aivon_Report_{topic.replace(' ', '_')}.pdf",
                mime="application/pdf"
            )

        except Exception as e:
            st.error(f"Error: {e}")

# --- 5. PRICING GRID ---
st.divider()
p_col1, p_col2, p_col3 = st.columns(3)
with p_col1:
    st.markdown('<div class="price-box"><h3>Starter</h3><p>$10</p><p>Standard Research</p></div>', unsafe_allow_html=True)
with p_col2:
    st.markdown('<div class="price-box" style="border-color:#00f2ff"><h3>Pro</h3><p>$25</p><p>HD Multimedia</p></div>', unsafe_allow_html=True)
with p_col3:
    st.markdown('<div class="price-box"><h3>Enterprise</h3><p>$50</p><p>Full PDF Access</p></div>', unsafe_allow_html=True)
