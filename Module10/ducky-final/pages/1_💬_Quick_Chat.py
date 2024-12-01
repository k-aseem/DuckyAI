import streamlit as st
import asyncio
from services import prompts
from helpers import util
from pdf2image import convert_from_path
from PIL import Image

st.set_page_config(
    page_title="Quick Chat",
    page_icon="💬",
    layout="wide"
)

import helpers.sidebar

helpers.sidebar.show()

# Header and description
st.header("Quick Chat")
st.write("Get instant answers to your coding and software development questions.")

# Session state initialization
if "messages" not in st.session_state:
    initial_messages = [{"role": "system",
                         "content": prompts.quick_chat_system_prompt()}]
    st.session_state.messages = initial_messages

if "ask_book_checkbox" not in st.session_state:
    st.session_state.ask_book_checkbox = False

# Checkbox for book context
st.session_state.ask_book_checkbox = st.checkbox("Use The Pragmatic Programmer as context.", value=st.session_state.ask_book_checkbox)

# Display messages from session state
for message in [m for m in st.session_state.messages if m["role"] != "system"]:
    avatar = "🔎" if message["role"] == "evidence" else None
    if avatar:
        with st.chat_message(message["role"], avatar=avatar):
            page_number = message["page_number"]
            with st.expander(f"See page {page_number}", expanded=False):
                if isinstance(message["content"], Image.Image):
                    st.image(message["content"], caption=f"Page {page_number}")
                else:
                    st.write(message["content"], unsafe_allow_html=True)
    else:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Function to extract PDF page as an image
def extract_pdf_page_as_image(pdf_path, page_number):
    try:
        images = convert_from_path(pdf_path, dpi=200, first_page=page_number, last_page=page_number)
        return images[0] if images else None
    except Exception as e:
        st.error(f"Error extracting PDF page as an image: {e}")
        return None

# Function to handle conversation
async def chat(messages, prompt):
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        try:
            messages = await util.run_conversation(messages, message_placeholder)
            st.session_state.messages = messages
        except Exception as e:
            st.error(f"An error occurred during conversation: {e}")
    print("Ask book checkbox: False")
    return messages

# Function to handle semantic search and evidence retrieval
async def ask_book(messages, prompt):
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            relevant_documents = await util.semantic_search(messages, prompt)

            # Extract context and page number
            if relevant_documents:
                relevant_documents_text = relevant_documents.get('context', "")
                page_number = relevant_documents.get('page_number', None)
            else:
                relevant_documents_text = ""
                page_number = None

            prompt = prompts.semantic_search_prompt(prompt, relevant_documents_text)
            # Create a system message for the prompt context
            context_message = {"role": "system", "content": prompt}
            messages.append(context_message)

            message_placeholder = st.empty()
            messages = await util.run_conversation(messages, message_placeholder)

            # Extract PDF page and convert it to an image
            if page_number is not None:
                pdf_path = "data/ThePragmaticProgrammer.pdf"
                page_image = extract_pdf_page_as_image(pdf_path, page_number)

                if page_image:
                    messages.append({
                        "role": "evidence",
                        "content": page_image,
                        "page_number": page_number
                    })

            st.session_state.messages = messages
        except Exception as e:
            st.error(f"An error occurred during the semantic search or page extraction process: {e}")

    print("Ask book checkbox: True")
    return messages


# React to user prompt
if prompt := st.chat_input("Ask a coding question..."):
    try:
        st.session_state.messages.append({"role": "user", "content": prompt})

        if st.session_state.ask_book_checkbox:
            asyncio.run(ask_book(st.session_state.messages, prompt))
        else:
            asyncio.run(chat(st.session_state.messages, prompt))
            
        st.rerun()
    except Exception as e:
        st.error(f"An error occurred while processing the user prompt: {e}")
    
