from google import genai
from google.genai import types
import streamlit as st


def ask_llm(prompt, model="gemini-2.5-flash"):
    # Get API key from Streamlit secrets
    api_key = st.secrets.get("GEMINI_API_KEY")

    if not api_key:
        return "⚠️ Missing API key. Please set GEMINI_API_KEY in Streamlit Secrets."

    client = genai.Client(api_key=api_key)

    try:
        response = client.models.generate_content(
            model=model,
            contents=prompt
        )
        return response.text.strip()
    except Exception as e:
        return f"⚠️ Gemini API Error: {str(e)}"


# ---------------------------
# Helper functions for app.py
# ---------------------------

def generate_greeting(name: str) -> str:
    """Generate a friendly greeting for the candidate."""
    return f"Hello {name}, welcome to your interview session! Let's get started."


def get_candidate_questions(tech_stack: str):
    """Generate technical interview questions using Gemini AI, fallback if it fails."""
    prompt = f"""
    You are an interviewer. Generate 5 concise technical interview questions
    based on the candidate's skills: {tech_stack}.
    Each question should be on a new line.
    """

    response = ask_llm(prompt)

    if response.startswith("⚠️"):   # API failure
        return response
    else:
        return [q.strip("-•1234567890. ") for q in response.split("\n") if q.strip()]
