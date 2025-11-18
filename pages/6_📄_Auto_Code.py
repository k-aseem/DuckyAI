import asyncio
import os

import streamlit as st
from asyncio import sleep

import helpers.sidebar
import helpers.util
from aitools_autogen.blueprint_project9 import ReactComponentBlueprint  # Changed import
from aitools_autogen.config import llm_config_openai as llm_config
from aitools_autogen.utils import clear_working_dir
from streamlit_file_browser import st_file_browser

# Set the configuration for the Streamlit page
st.set_page_config(
    page_title="Auto Code",
    page_icon="📄",
    layout="wide"
)

# Show the sidebar
helpers.sidebar.show()

# Initialize the blueprint in the session state if it doesn't exist
if st.session_state.get("blueprint", None) is None:
    st.session_state.blueprint = ReactComponentBlueprint()  # Changed class

# Define an asynchronous function to run the blueprint
async def run_blueprint(seed: int = 42) -> str:
    await sleep(3)  # Simulate a delay
    llm_config["seed"] = seed  # Set the seed for the LLM configuration
    await st.session_state.blueprint.initiate_work(message=task)  # Initiate the blueprint work
    return st.session_state.blueprint.summary_result  # Return the summary result

# Display the file browser if the directory exists
if os.path.exists('aitools_autogen/coding'):
    st.markdown('# Generated Code')
    event = st_file_browser("aitools_autogen/coding", key='A')

# Create two columns for input and options
blueprint_ctr, parameter_ctr = st.columns(2, gap="large")
with blueprint_ctr:
    st.markdown("# Run Blueprint")
    # Input for the web app idea
    idea = st.text_input("Enter a web app idea to generate React components:",  # Changed input
                         value="Pomodoro Timer")
    # Button to start the agents
    agents = st.button("Start the Agents!", type="primary")

with parameter_ctr:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("### Other Options")
    # Button to clear the autogen cache
    clear = st.button("Clear the autogen cache...&nbsp; ⚠️", type="secondary")
    # Input for the seed value
    seed = st.number_input("Enter a seed for the random number generator:", value=42)

# Container to display results
results_ctr = st.empty()

# Clear the cache if the button is clicked
if clear:
    with results_ctr:
        st.status("Clearing the agent cache...")
        clear_working_dir(".cache", "*")
        st.status("Cache cleared!")

# Run the agents if the button is clicked
if agents:
    with results_ctr:
        st.status("Running the Blueprint...")

    # Define the task message
    task = f"""
            I want to generate React components for a web app idea: 
            {idea}
            """

    # Run the blueprint and get the result
    text = asyncio.run(run_blueprint(seed=seed))
    st.balloons()

    # Display the result
    with results_ctr:
        st.markdown(text)