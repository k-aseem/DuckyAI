import streamlit as st
import asyncio
import io
import os
import pathlib
from os.path import isfile, join
import pandas as pd
import helpers.sidebar
import helpers.util
import services.prompts
import services.llm
import helpers.util

st.set_page_config(
    page_title="Generate Code",
    page_icon="📄",
    layout="wide"
)

helpers.sidebar.show()

# Initialize session state for the code editor and button states
if "code" not in st.session_state:
    st.session_state.code = ""
if "explanation" not in st.session_state:
    st.session_state.explanation = ""
if "active_button" not in st.session_state:
    st.session_state.active_button = ""

st.header("🛠️ Get help with your code!")

# Create columns for buttons
col1, col2, col3, col4 = st.columns([0.1, 0.1, 0.1, 0.9])

with col1:
    review_clicked = st.button("Review", key="review_button",
                               help="Review the code",
                               disabled=(st.session_state.active_button == "review"))

with col2:
    debug_clicked = st.button("Debug", key="debug_button",
                              help="Debug the code",
                              disabled=(st.session_state.active_button == "debug"))

with col3:
    modify_clicked = st.button("Modify", key="modify_button",
                               help="Modify the code",
                               disabled=(st.session_state.active_button == "modify"))

with col4:
    reset_clicked = st.button("Reset", key="reset_button",
                              help="Reset the code",
                              disabled=(st.session_state.active_button == "reset"))


# Text area for code input
text_area_code = st.text_area("Code Editor", value=st.session_state.code,
                              placeholder="Paste your python code here...",
                              height=200, key="text_area_code_editor")

async def get_response(prompt):
    conversation = services.llm.create_conversation_starter(prompt)
    response = ""
    async for chunk in services.llm.converse(conversation):
        response += chunk
    return response

if review_clicked:
    st.session_state.active_button = "review"
    st.rerun()

if debug_clicked:
    st.session_state.active_button = "debug"
    st.rerun()

if modify_clicked:
    st.session_state.active_button = "modify"
    st.rerun()

if reset_clicked:
    st.session_state.active_button = "reset"
    st.session_state.code = ""
    st.session_state.explanation = ""
    st.rerun()

if st.session_state.active_button == "review":
    review_prompt = services.prompts.review_prompt(text_area_code)
    with st.spinner("Thinking..."):
        review_response = asyncio.run(get_response(review_prompt))
    
    # Extract the explanation from the response
    parts = review_response.split("```")
    if len(parts) >= 3:
        explanation = parts[2].strip()
    else:
        explanation = review_response

    # Update the session state with the explanation
    st.session_state.explanation = explanation
    # st.rerun()

if st.session_state.active_button == "debug":
    # Move the 'Error message' markdown to immediately before the chat input
    debug_error_string = st.chat_input("Enter the error message (optional):")
    if debug_error_string:
        debug_prompt = services.prompts.debug_prompt(debug_error_string, text_area_code)
        with st.spinner("Thinking..."):
            debug_response = asyncio.run(get_response(debug_prompt))
        
        # Extract the code and explanation from the response
        parts = debug_response.split("```")
        if len(parts) >= 3:
            debugged_code = parts[1].strip()
            # Remove the language identifier if present
            if debugged_code.startswith("python"):
                debugged_code = debugged_code[len("python"):].strip()
            explanation = parts[2].strip()
        else:
            debugged_code = debug_response
            explanation = ""

        # Update the session state with the debugged code and explanation
        st.session_state.code = debugged_code
        st.session_state.explanation = explanation
        st.rerun()


if st.session_state.active_button == "modify":
    modification_instructions = st.chat_input("Enter modification instructions")
    if modification_instructions:
        modify_prompt = services.prompts.modify_code_prompt(modification_instructions, text_area_code)
        with st.spinner("Thinking..."):
            modify_response = asyncio.run(get_response(modify_prompt))
        
        # Extract the modified code and explanation from the response
        parts = modify_response.split("```")
        if len(parts) >= 3:
            modified_code = parts[1].strip()
            # Remove the language identifier if present
            if modified_code.startswith("python"):
                modified_code = modified_code[len("python"):].strip()
            explanation = parts[2].strip()
        else:
            modified_code = modify_response
            explanation = ""

        # Update the session state with the modified code and explanation
        st.session_state.code = modified_code
        st.session_state.explanation = explanation
        st.rerun()

# Display the explanation below the text area
if st.session_state.explanation:
    st.subheader("Explanation")
    st.markdown(st.session_state.explanation)