import streamlit as st
from backend.prompt_manager import get_system_prompt
from backend.memory import ChatMemory
from backend.gemini_client import generate_response

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Financial Advisor GenAI",
    layout="wide",
    page_icon="💰"
)

# ---------------- CUSTOM CSS (EXTREME UI) ----------------
st.markdown("""
<style>

html, body, [class*="css"]  {
    font-family: 'Segoe UI', sans-serif;
}

.stApp {
    background: linear-gradient(135deg,#0f172a,#020617);
    color:white;
}

.main-title {
    font-size:48px;
    font-weight:700;
    text-align:center;
    background: linear-gradient(90deg,#22c55e,#06b6d4);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.chat-bubble-user {
    background:#1e293b;
    padding:14px;
    border-radius:14px;
    margin:8px 0;
}

.chat-bubble-ai {
    background:#020617;
    border:1px solid #22c55e;
    padding:14px;
    border-radius:14px;
    margin:8px 0;
}

.sidebar-title {
    font-size:22px;
    font-weight:bold;
    color:#22c55e;
}

</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR DASHBOARD ----------------
with st.sidebar:
    st.markdown('<p class="sidebar-title">💰 Finance Control Panel</p>', unsafe_allow_html=True)

    risk_profile = st.selectbox(
        "Select Risk Profile",
        ["Beginner", "Moderate Investor", "Aggressive Trader"]
    )

    investment_goal = st.selectbox(
        "Investment Goal",
        ["Wealth Growth", "Retirement", "Passive Income", "Emergency Fund"]
    )

    st.divider()

    st.info("This AI gives educational financial guidance only.")

# ---------------- TITLE ----------------
st.markdown('<p class="main-title">Financial Advisor GenAI</p>', unsafe_allow_html=True)

# ---------------- SESSION MEMORY ----------------
if "memory" not in st.session_state:
    st.session_state.memory = ChatMemory()

memory = st.session_state.memory

# ---------------- SYSTEM PROMPT ----------------
system_prompt = get_system_prompt()

# Add dynamic persona
system_prompt += f"\nUser Risk Profile: {risk_profile}\nInvestment Goal: {investment_goal}"

# ---------------- CHAT HISTORY ----------------
for msg in memory.get_history():
    if msg["role"] == "user":
        st.markdown(f'<div class="chat-bubble-user">🧑 {msg["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="chat-bubble-ai">🤖 {msg["content"]}</div>', unsafe_allow_html=True)

# ---------------- INPUT ----------------
user_input = st.chat_input("Ask financial questions...")

if user_input:

    memory.add_user(user_input)

    st.markdown(f'<div class="chat-bubble-user">🧑 {user_input}</div>', unsafe_allow_html=True)

    with st.spinner("📊 AI analyzing market strategy..."):

        reply = generate_response(
            system_prompt,
            user_input,
            memory.get_history()
        )

    st.markdown(f'<div class="chat-bubble-ai">🤖 {reply}</div>', unsafe_allow_html=True)

    memory.add_bot(reply)