import streamlit as st
from prompt_utils import generate_greeting, get_candidate_questions
import os

# ---------------------------
# Streamlit Page Setup
# ---------------------------
st.set_page_config(page_title="TalentScout Hiring Assistant", layout="centered")
st.title("🤖 TalentScout - Hiring Assistant Chatbot")

# ---------------------------
# Initialize session state
# ---------------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "submitted" not in st.session_state:
    st.session_state.submitted = False
if "questions" not in st.session_state:
    st.session_state.questions = []
if "answers" not in st.session_state:
    st.session_state.answers = {}
if "debug_info" not in st.session_state:
    st.session_state.debug_info = ""

# ---------------------------
# Candidate Details Form
# ---------------------------
with st.form("candidate_form"):
    st.subheader("👤 Candidate Details")
    full_name = st.text_input("Full Name")
    email = st.text_input("Email Address")
    phone = st.text_input("Phone Number")
    experience = st.slider("Years of Experience", 0, 30, 1)
    position = st.text_input("Desired Position")
    location = st.text_input("Current Location")
    tech_stack = st.text_input("Tech Stack / Skills (e.g., Python, ML, SQL)")

    submitted = st.form_submit_button("Start Interview")

# ---------------------------
# Handle Form Submission
# ---------------------------
if submitted:
    st.session_state.submitted = True
    st.session_state.chat_history = []
    st.session_state.answers = {}

    # Chat introduction
    st.session_state.chat_history.append(("bot", generate_greeting(full_name)))
    st.session_state.chat_history.append(("user", f"My tech stack includes: {tech_stack}"))
    st.session_state.chat_history.append(("bot", "Great! Let me ask you a few technical questions."))

    # Get AI-generated questions
    questions = get_candidate_questions(tech_stack)

    if isinstance(questions, str) and questions.startswith("⚠️"):
        st.session_state.debug_info = questions
        st.session_state.questions = []
    else:
        st.session_state.questions = questions
        st.session_state.debug_info = "✅ Questions generated successfully from Gemini AI."

# ---------------------------
# Display Chat & Questions
# ---------------------------
if st.session_state.submitted:
    for role, msg in st.session_state.chat_history:
        if role == "bot":
            st.markdown(f"**🤖 {msg}**")
        else:
            st.markdown(f"> {msg}")

    # Debug info (for API messages)
    if st.session_state.debug_info:
        st.info(st.session_state.debug_info)

    # Show questions
    if st.session_state.questions:
        st.subheader("📝 Your Answers:")
        for i, question in enumerate(st.session_state.questions):
            answer = st.text_area(f"{i+1}. {question}", key=f"answer_input_{i}")
            st.session_state.answers[question] = answer
    else:
        st.warning("⚠️ No AI-generated questions available. Please check your Gemini API key.")

    # Submit button
    if st.button("Submit Answers"):
        st.success("✅ Thank you! Your answers have been recorded.")
        st.subheader("📋 Your Responses:")
        for q, a in st.session_state.answers.items():
            st.markdown(f"**Q:** {q}")
            st.markdown(f"**A:** {a if a else '*No answer provided*'}")
