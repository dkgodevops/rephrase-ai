"""Streamlit Web UI for Smart Grammar & Tone Rewriter.
"""

import os
import streamlit as st
from dotenv import load_dotenv
from rewriter import TONE_DESCRIPTIONS, rewrite_text

# Load .env
load_dotenv()

st.set_page_config(
    page_title="RephraseAI - Smart Tone & Grammar Rewriter",
    page_icon="✍️",
    layout="wide",
)

# Custom header
st.title("✍️ RephraseAI - Smart Tone & Grammar Rewriter")
st.caption("Powered by Google Gemini • Elevate your writing with structured AI suggestions")

# Sidebar Configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    
    env_api_key = os.getenv("GEMINI_API_KEY", "")
    api_key_input = st.text_input(
        "Gemini API Key",
        value=env_api_key,
        type="password",
        help="Get a free API key at https://aistudio.google.com/. Can also be set in .env file."
    )
    
    selected_tone = st.selectbox(
        "Select Target Tone",
        options=list(TONE_DESCRIPTIONS.keys()),
        index=0
    )
    st.info(TONE_DESCRIPTIONS[selected_tone])
    
    model_choice = st.selectbox(
        "Model",
        options=["gemini-3.8-flash", "gemini-3.5-flash", "gemini-3.1-flash-lite"],
        index=0
    )
    
    st.markdown("---")
    st.markdown("### 💡 Quick Examples")
    preset_col1, preset_col2 = st.columns(2)
    sample_text = ""
    
    if preset_col1.button("Work Email"):
        st.session_state["input_text"] = (
            "hey there im writing this to tell you that we cant make it to the "
            "client sync meeting because of some unexpected stuff that happened today, "
            "so sorry about that let me know when we can reschedule"
        )
        
    if preset_col2.button("Follow Up"):
        st.session_state["input_text"] = (
            "did you get a chance to look at the docs i sent over last week? "
            "i really need your approval asap so we dont get delayed with the launch"
        )

# Main UI layout: Two columns
col_input, col_output = st.columns(2, gap="medium")

with col_input:
    st.subheader("Original Text")
    
    default_val = st.session_state.get("input_text", "")
    user_input = st.text_area(
        "Enter or paste your text below:",
        value=default_val,
        height=260,
        placeholder="Type or paste draft text here..."
    )
    
    word_count_orig = len(user_input.split()) if user_input.strip() else 0
    st.caption(f"Word count: {word_count_orig}")
    
    submit_btn = st.button("🚀 Rewrite & Polish", type="primary", use_container_width=True)

with col_output:
    st.subheader("Rewritten Version")
    
    if submit_btn:
        if not user_input.strip():
            st.warning("Please enter some text first.")
        elif not api_key_input:
            st.error("Please provide a Gemini API Key in the sidebar or your .env file.")
        else:
            with st.spinner("Polishing grammar and adapting tone..."):
                try:
                    result = rewrite_text(
                        text=user_input,
                        tone=selected_tone,
                        api_key=api_key_input,
                        model_name=model_choice
                    )
                    
                    st.success(f"Tone Applied: **{result.tone_applied}**")
                    st.text_area(
                        "Result:",
                        value=result.rewritten_text,
                        height=200,
                        key="output_area"
                    )
                    
                    word_count_rewritten = len(result.rewritten_text.split())
                    diff = word_count_rewritten - word_count_orig
                    diff_str = f"+{diff}" if diff > 0 else f"{diff}"
                    st.caption(f"Word count: {word_count_rewritten} ({diff_str} words)")

                    # Detailed improvements breakdown
                    with st.expander("🔍 See What Changed & Why", expanded=True):
                        st.markdown("**Key Improvements Made:**")
                        for imp in result.improvements:
                            st.markdown(f"- {imp}")
                        
                        st.markdown(f"**Readability Note:** *{result.readability_note}*")

                except Exception as e:
                    st.error(f"Error during rewrite: {str(e)}")
    else:
        st.info("Click **Rewrite & Polish** on the left to see the AI output here.")
