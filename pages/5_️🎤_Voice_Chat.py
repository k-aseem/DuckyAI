import asyncio
import streamlit as st
import time
from services.audio import record_audio, transcribe_audio, generate_gpt_response, speak_text

st.set_page_config(
    page_title="Voice Chat",
    page_icon="🎤",
    layout="wide"
)

import helpers.sidebar

helpers.sidebar.show()

st.header("Voice Chat")

st.write("Get instant answers to your software development and coding questions using the microphone.")

# The UI should have a big red record button stating we will record for 5 seconds.
# When clicked, let's show a spinner stating we are processing the audio.
# If we click the button, we should record for 5 seconds and then transcribe the audio to text,
# send it to chatGPT and then speak the text asynchronously - all using the audio.py module and methods inside this project
if st.button("🔴 Record for 5 seconds", key="record_button"):
    with st.spinner("Recording audio for 5 seconds..."):
        record_audio()
    
    with st.spinner("Transcribing the recorded audio..."):
        transcription = transcribe_audio()

    st.write(f"Transcription: {transcription}")

    with st.spinner("Generating response..."):
        response = asyncio.run(generate_gpt_response(transcription))
        st.write(f"GPT Response: {response}")

    with st.spinner("Speaking the generated response..."):
        speak_text(response)
        


