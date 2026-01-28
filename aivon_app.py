import streamlit as st
import os
import urllib.parse
from crewai import Agent, Task, Crew, LLM
from fpdf import FPDF

# --- 1. USER & KEY DATABASE ---
# Aap yahan naye clients add kar sakte hain
USER_DB = {
    "admin": "aivon2026",
    "subhan": "almani1199",
    "client_fiverr": "order123"
}

# Unique Keys jo aap bech sakte hain
VALID_KEYS = ["AIVON-PRO-786", "AIVON-PRO-999", "AIVON-PRO-1122", "FIVERR-GOLD-2026"]

# Session State
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'user_role' not in st.session_state:
    st.session_state['user_role'] = "Basic"
if 'username' not in st.session_state:
    st.session_state['username'] = ""

# --- 2. CONFIG & UI ---
st.set_page_config(page_title="Aivon Ultra Max | Global Engine", layout="wide", page_icon="💠")

st.markdown("""
    <style>
    .stApp { background-color: #020202; color: #ffffff; }
    .main-title { text-align: center; color: #00f2ff; font-size: 50px; font-weight: bold; text-shadow: 0 0 20px #00f2ff; }
    .login-box { background: #0a0a0a; padding: 40px; border-radius: 20px; border: 1px solid #7000ff; max-width: 450px; margin: auto; box-shadow: 0 0 30px #7000ff33; }
    .report-card { background: rgba(20, 20, 20, 0.9); padding: 30px; border-radius: 20px; border-left: 5px solid #00f2ff; line-height: 1.8; color: #e0e0e0; }
    .stButton>button { background: linear-gradient(90deg, #00f2ff, #7000ff); color: white; border-radius: 12px; font-weight: bold; height: 50px; width: 100%; border: none; }
    .stButton>button:hover { transform: scale(1.02); box-shadow: 0 0 20px #00f2ff; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. LOGIN PAGE ---
def show_login():
    st.markdown('<div style="height: 100px;"></div>', unsafe_allow_html=True)
    st.markdown('<div class="main-title">AIVON SECURE LOGIN</div>', unsafe_allow_html=True)
    st.markdown('<div class="login-box">', unsafe_allow_html=True)
    user = st.text_input("Username")
    pwd = st.text_input("Password", type="password")
    if st.button("Enter Neural Engine"):
        if user in USER_DB and USER_DB[user] == pwd:
            st.session_state['logged_in'] = True
            st.session_state['username'] = user
            st.rerun()
        else:
            st.error("Invalid Credentials. Access Denied.")
    st.markdown('</div>', unsafe_allow_html=True)

# --- 4. MAIN APPLICATION ---
def show_main():
    # PDF Generator Function
    def create_pdf(text, topic):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B", 20)
        pdf.set_text_color(0, 180, 255)
        pdf.cell(200, 15, txt="AIVON STRATEGIC INTELLIGENCE", ln=True, align='C')
        pdf.ln(10)
        pdf.set_font("Arial", "B", 14)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(200, 10, txt=f"Report Topic: {topic}", ln=True, align='L')
        pdf.ln(5)
        pdf.set_font("Arial", "", 12)
        clean_text = text.encode('latin-1', 'replace').decode('latin-1')
        pdf.multi_cell(0, 10, txt=clean_text)
        pdf.ln(20)
        pdf.set_draw_color(0, 180, 255)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(5)
        pdf.set_font("Arial", "B", 10)
        pdf.cell(0, 10, txt="Business: Aivonprobussines@gmail.com", ln=True, align='C')
        return pdf.output()

    # Sidebar
    with st.sidebar:
        st.markdown(f"<h2 style='color:#00f2ff;'>💠 Hello, {st.session_state['username'].title()}</h2>", unsafe_allow_html=True)
        st.write(f"Access Level: **{st.session_state['user_role']}**")
        st.divider()

        if st.session_state['user_role'] == "Basic":
            st.markdown("### 🔓 Upgrade to PRO")
            key = st.text_input("Enter License Key:")
            if st.button("Activate Neural Pro"):
                if key in VALID_KEYS:
                    st.session_state['user_role'] = "Pro"
                    # Note: Original code list removal is local, in production you'd use a database.
                    st.success("PRO Features Unlocked!")
                    st.rerun()
                else:
                    st.error("Key Invalid or Expired")
            
            st.divider()
            payoneer_url = "https://link.payoneer.com/Token?t=08188776795A4054A03D813DC3816C08&src=prq"
            st.markdown(f'<a href="{payoneer_url}" target="_blank" style="text-decoration:none;"><div style="background:#00f2ff; color:#000; padding:10px; border-radius:8px; text-align:center; font-weight:bold;">BUY PRO KEY ($10)</div></a>', unsafe_allow_html=True)

        st.divider()
        groq_api = st.text_input("Groq API Key", type="password")
        if st.button("Sign Out"):
            st.session_state['logged_in'] = False
            st.rerun()

    # Dashboard
    st.markdown('<div class="main-title">AIVON ULTRA MAX</div>', unsafe_allow_html=True)
    st.write(f"Account: {st.session_state['user_role']} | System Status: Online")

    topic = st.text_input("🚀 Strategic Vision Topic:", placeholder="e.g., Future of Solar Tech 2026")
    
    if st.button("GENERATE INTELLIGENCE ASSETS"):
        if not groq_api:
            st.error("Please enter your Groq API Key in the sidebar.")
        elif not topic:
            st.warning("Please enter a topic.")
        else:
            try:
                with st.status("🧬 Synthesizing Data...", expanded=True) as status:
                    # AI Core
                    aivon_llm = LLM(model="groq/llama-3.3-70b-versatile", api_key=groq_api)
                    
                    # Image Engine
                    encoded_topic = urllib.parse.quote(topic)
                    img_url = f"https://pollinations.ai/p/{encoded_topic}?width=1280&height=720&enhance=true&seed=42"
                    st.image(img_url, caption=f"Neural Projection: {topic}", use_container_width=True)
                    
                    # Agent Research
                    researcher = Agent(role='Global Strategist', goal=f'Deep 2026 report on {topic}', backstory="Advanced AI Analyst.", llm=aivon_llm)
                    task = Task(description=f"Detailed analysis of {topic} for 2026.", expected_output="Professional Markdown Report.", agent=researcher)
                    crew = Crew(agents=[researcher], tasks=[task])
                    result = crew.kickoff()
                    
                    status.update(label="✅ Generation Complete!", state="complete")

                st.divider()
                st.markdown(f'<div class="report-card">{result.raw}</div>', unsafe_allow_html=True)
                
                # PDF Asset
                pdf_data = create_pdf(str(result.raw), topic)
                st.download_button(label="📥 Download Strategic PDF", data=pdf_data, file_name=f"Aivon_{topic.replace(' ', '_')}.pdf", mime="application/pdf")
                
            except Exception as e:
                st.error(f"Engine Error: {e}")

# --- 5. RUN SYSTEM ---
if st.session_state['logged_in']:
    show_main()
else:
    show_login()
