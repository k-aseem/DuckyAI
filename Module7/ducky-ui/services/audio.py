import os
import threading
import wave
import asyncio

import pyaudio
import pygame
from dotenv import load_dotenv
from gtts import gTTS
from openai import OpenAI

from services import llm

# Load .env file
load_dotenv()

# Initialize the OpenAI client with the modern API pattern
client = OpenAI(
    api_key=os.getenv('OPENAI_API_KEY'),
    base_url=os.getenv('OPENAI_API_BASE_URL', 'https://api.openai.com/v1')
)

# Initialize pygame speech mixer with explicit parameters for robustness
pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=4096)


# Set up audio recording parameters
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000  # Whisper supports 16kHz for best results
CHUNK = 1024
RECORD_SECONDS = 5  # Adjust as needed
WAVE_OUTPUT_FILENAME = "data/audio/voice_chat.wav"


def record_audio():
    """
    Capture audio from the microphone and save it to a file.

    # AI Generation Prompt:
    # Write a Python function that records audio from the microphone for a given
    # duration and saves it as a .wav file using the PyAudio library.
    """
    audio = pyaudio.PyAudio()

    # Open stream
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)

    print("Recording...")

    frames = []

    # Record for the specified number of seconds
    for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("Finished recording.")

    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # Save the recorded data as a WAV file
    with wave.open(WAVE_OUTPUT_FILENAME, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))

    print(f"Audio saved to {WAVE_OUTPUT_FILENAME}")


def transcribe_audio():
    """
    Transcribe the recorded audio file using OpenAI's Whisper model.

    Returns:
        str: The transcription of the audio file.

    # AI Generation Prompt:
    # Write a Python function that reads an audio file from disk and uses OpenAI's
    # Whisper model to generate a transcription of the audio.
    """
    audio_file_path = WAVE_OUTPUT_FILENAME

    # Ensure the audio file exists
    if not os.path.exists(audio_file_path):
        raise FileNotFoundError(f"Audio file not found: {audio_file_path}")

    # Read the audio file
    with open(audio_file_path, "rb") as audio_file:
        transcription = asyncio.run(llm.transcribe_audio("whisper-1", audio_file))

    print(f"Transcription: {transcription}")
    
    return transcription


async def generate_gpt_response(prompt, messages=None):
    """
    Send transcribed text to GPT-4 for a response.

    Args:
        prompt (str): The prompt or input text.
        messages (list, optional): The context messages for the GPT-4 API.

    Returns:
        str: The GPT-4 response.

    # AI Generation Prompt:
    # Write a Python function that takes a prompt and an optional list of context messages,
    # sends it to GPT-4 using the OpenAI API, and returns the generated response.
    """
    if messages is None:
        messages = []

    # Add the prompt to the messages
    messages.append({"role": "user", "content": prompt})

    # Initialize full_response
    full_response = ""

    # Send the request to GPT-4 using the converse method from llm.py
    async for chunk in llm.converse(messages):
        print(chunk)
        full_response += chunk

    return full_response

def speak_text(text, lang="en"):
    """
    Convert text to speech using gTTS and play the audio file using pygame.

    Args:
        text (str): The text to be spoken.
        lang (str): Language for speech (default is "en" for English).
    """

    def _speak():
        try:
            print("Converting text to speech...")
            # Convert the text to speech
            tts = gTTS(text=text, lang=lang)
            filename = "speech_output.mp3"

            print("Saving audio file...")
            try:
                tts.save(filename)
                print(f"Saved audio file: {filename}")
            except OSError as e:
                print(f"Failed to save file due to OS error: {e}")
                return
            except Exception as e:
                print(f"Unexpected error when saving file: {e}")
                return

            if os.path.exists(filename):
                print(f"Saved audio file successfully: {filename}")
            else:
                print(f"Failed to save the audio file: {filename}")
                return  # If the file didn't save, exit the function

            # Load and play the speech using pygame
            print("Loading audio file...")
            pygame.mixer.music.load(filename)
            print("Playing audio...")
            pygame.mixer.music.play()

            # Wait for the audio to finish playing
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)

            print("Audio finished playing.")

            # Optionally, remove the file after playing
            os.remove(filename)
            print(f"Removed audio file: {filename}")
        except Exception as e:
            print(f"Error in speak_text: {e}")

    # Run the speech process in a separate thread to prevent blocking
    thread = threading.Thread(target=_speak)
    thread.daemon = True  # Mark thread as daemon so it exits when the app exits
    thread.start()
    thread.join()  # Ensure the thread completes before the program exits
