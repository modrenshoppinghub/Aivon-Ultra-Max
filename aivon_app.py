import streamlit as st
import os
import urllib.parse
from crewai import Agent, Task, Crew, LLM
from fpdf import FPDF

# --- 1. USER & KEY DATABASE ---
USER_DB = {
    "subhan": "almani1199",
    "admin": "aivon2026"
}
VALID_KEYS = ["AIVON-PRO-786", "FIVERR-GOLD-2026"]

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'user_role' not in st.session_state:
    st.session_state['user_role'] = "Basic"

# --- UI STYLING ---
st.set_page_config(page_title="Aivon Ultra Max", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #020202; color: #ffffff; }
    .main-title { text-align: center; color: #00f2ff; font-size: 50px; font-weight: bold; text-shadow: 0 0 20px #00f2ff; }
    .login-box { background: #0a0a0a; padding: 40px; border-radius: 20px; border: 1px solid #7000ff; max-width: 450px; margin: auto; }
    .stButton>button { background: linear-gradient(90deg, #00f2ff, #7000ff); color: white; border-radius: 12px; font-weight: bold; width: 100%; border: none; }
    </style>
    """, unsafe_allow_html=True)

# --- LOGIN PAGE ---
def show_login():
    st.markdown('<div style="height: 100px;"></div>', unsafe_allow_html=True)
    st.markdown('<div class="main-title">AIVON SECURE LOGIN</div>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="login-box">', unsafe_allow_html=True)
        user = st.text_input("Username")
        pwd = st.text_input("Password", type="password")
        if st.button("Enter Neural Engine"):
            if user in USER_DB and USER_DB[user] == pwd:
                st.session_state['logged_in'] = True
                st.rerun()
            else:
                st.error("Invalid Credentials")
        st.markdown('</div>', unsafe_allow_html=True)

# --- MAIN APP ---
def show_main():
    def create_pdf(text, topic):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B", 20)
        pdf.cell(200, 15, txt="AIVON STRATEGIC INTELLIGENCE", ln=True, align='C')
        pdf.ln(10)
        pdf.set_font("Arial", "", 12)
        # Fix for special characters
        clean_text = text.encode('latin-1', 'replace').decode('latin-1')
        pdf.multi_cell(0, 10, txt=clean_text)
        pdf.ln(20)
        pdf.cell(0, 10, txt="Contact: Aivonprobussines@gmail.com", ln=True, align='C')
        
        # FIXED LINE: Ensuring bytes format for Streamlit
        return bytes(pdf.output())

    with st.sidebar:
        st.title("💠 Aivon Control")
        st.write(f"Level: {st.session_state['user_role']}")
        if st.session_state['user_role'] == "Basic":
            key = st.text_input("License Key:")
            if st.button("Activate Pro"):
                if key in VALID_KEYS:
                    st.session_state['user_role'] = "Pro"
                    st.success("Unlocked!")
                    st.rerun()
        st.divider()
        groq_api = st.text_input("Groq API Key", type="password")
        if st.button("Sign Out"):
            st.session_state['logged_in'] = False
            st.rerun()

    st.markdown('<div class="main-title">AIVON ULTRA MAX</div>', unsafe_allow_html=True)
    topic = st.text_input("🚀 Research Topic:", placeholder="e.g., Virtual Tourism 2026")
    
    if st.button("GENERATE REPORT"):
        if not groq_api:
            st.error("Enter API Key in Sidebar")
        else:
            try:
                with st.status("🧬 Analyzing...", expanded=True):
                    aivon_llm = LLM(model="groq/llama-3.3-70b-versatile", api_key=groq_api)
                    encoded_topic = urllib.parse.quote(topic)
                    st.image(f"https://pollinations.ai/p/{encoded_topic}?width=1280&height=720&enhance=true")
                    
                    agent = Agent(role='Strategist', goal=f'2026 Report on {topic}', backstory="AI Pro", llm=aivon_llm)
                    task = Task(description=f"Detailed report on {topic}", expected_output="Markdown Report", agent=agent)
                    result = Crew(agents=[agent], tasks=[task]).kickoff()

                st.markdown(result.raw)
                
                # Fixed PDF download logic
                pdf_bytes = create_pdf(str(result.raw), topic)
                st.download_button(
                    label="📥 Download Strategic PDF",
                    data=pdf_bytes,
                    file_name=f"Aivon_{topic.replace(' ', '_')}.pdf",
                    mime="application/pdf"
                )
            except Exception as e:
                st.error(f"System Error: {e}")

if st.session_state['logged_in']:
    show_main()
else:
    show_login()
