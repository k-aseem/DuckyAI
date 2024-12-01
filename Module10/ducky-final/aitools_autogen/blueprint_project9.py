
from typing import Optional

from autogen import ConversableAgent

import aitools_autogen.utils
from aitools_autogen.blueprint import Blueprint
from aitools_autogen.config import llm_config_openai as llm_config, config_list_openai as config_list, WORKING_DIR
import os


# This Blueprint file defines the ReactComponentBlueprint class, which is responsible for generating React components,
# their corresponding styles, and unit tests based on a given web app idea. The blueprint uses multiple ConversableAgent
# instances to handle different aspects of the code generation process. The generated files are organized in a 
# component-based directory structure under the `src/components/<ComponentName>` directory.

# The blueprint performs the following steps:
# 1. Initializes the working directory.
# 2. Clears any existing files in the working directory.
# 3. Uses the requirements_agent to generate a summary of the requirements for the React components based on the provided web app idea.
# 4. Uses the react_component_agent to generate the React components based on the summarized requirements.
# 5. Uses the styling_agent to generate the corresponding styles for the React components.
# 6. Uses the testing_agent to generate unit tests for the React components.
# 7. Saves the generated files in the appropriate directories.
# 8. Summarizes the generated files and stores the summary result.

# The blueprint ensures that all generated files are placed in the correct directories and provides a summary of the generated code.


class ReactComponentBlueprint(Blueprint):

    def __init__(self, work_dir: Optional[str] = WORKING_DIR):
        super().__init__([], config_list=config_list, llm_config=llm_config)
        self._work_dir = work_dir or "code"
        self._summary_result: Optional[str] = None

    @property
    def summary_result(self) -> str | None:
        """The getter for the 'summary_result' attribute."""
        return self._summary_result

    @property
    def work_dir(self) -> str:
        """The getter for the 'work_dir' attribute."""
        return self._work_dir

    async def initiate_work(self, message: str):
        try:
            # Ensure the working directory exists
            if not os.path.exists(self._work_dir):
                os.makedirs(self._work_dir)

            aitools_autogen.utils.clear_working_dir(self._work_dir)
            agent0 = ConversableAgent("a0",
                                      max_consecutive_auto_reply=0,
                                      llm_config=False,
                                      human_input_mode="NEVER")

            requirements_agent = ConversableAgent("requirements_agent",
                                                  max_consecutive_auto_reply=6,
                                                  llm_config=llm_config,
                                                  human_input_mode="NEVER",
                                                  code_execution_config=False,
                                                  function_map=None,
                                                  system_message="""You are a helpful AI assistant.
                When given a web app idea, you will generate a summary of the requirements for React components.
                Output a summary in bullet point form for each component.
                Let's make it concise in markdown format.
                It should include short descriptions of props,
                and list expected possible states.
                Return `None` if the idea is not valid or cannot be summarized.
                """)

            react_component_agent = ConversableAgent("react_component_agent",
                                                     max_consecutive_auto_reply=6,
                                                     llm_config=llm_config,
                                                     human_input_mode="NEVER",
                                                     code_execution_config=False,
                                                     function_map=None,
                                                     system_message="""
            You are a frontend developer expert in React.
            You're writing React components based on the given description.

            When you receive a message, you should expect that message to describe the requirements of a React component.

            Let's use functional components and hooks for our implementation.
            All files must be generated in the src/components/<ComponentName> directory.

            Write a complete implementation covering all described requirements.
            Use multiple files in a directory structure that makes sense.
            Use React functional components and hooks.

            Create the components inside a `src/components/<ComponentName>` directory.
            The code using this generated code should not require additional modifications.

            You must indicate the script type in the code block.
            Do not suggest incomplete code which requires users to modify.
            Always put `// filename: src/components/<ComponentName>/<filename>` as the first line of each code block.

            Feel free to include multiple code blocks in one response. Do not ask users to copy and paste the result.
            """)

            styling_agent = ConversableAgent("styling_agent",
                                             max_consecutive_auto_reply=6,
                                             llm_config=llm_config,
                                             human_input_mode="NEVER",
                                             code_execution_config=False,
                                             function_map=None,
                                             system_message="""
            You are a frontend developer expert in CSS and styled-components.
            You're writing styles for React components based on the given description.

            When you receive a message, you should expect that message to describe the requirements of a React component.

            Write complete CSS or styled-components covering all described requirements.
            Use multiple files in a directory structure that makes sense.

            Create the styles inside a `src/components/<ComponentName>` directory.
            The code using this generated code should not require additional modifications.

            You must indicate the script type in the code block.
            Do not suggest incomplete code which requires users to modify.
            Always put `// filename: src/components/<ComponentName>/<filename>` as the first line of each code block.

            Feel free to include multiple code blocks in one response. Do not ask users to copy and paste the result.
            """)

            testing_agent = ConversableAgent("testing_agent",
                                             max_consecutive_auto_reply=6,
                                             llm_config=llm_config,
                                             human_input_mode="NEVER",
                                             code_execution_config=False,
                                             function_map=None,
                                             system_message="""
            You are a frontend developer expert in testing React components using Jest.
            You're writing unit tests for React components based on the given description.

            When you receive a message, you should expect that message to describe the requirements of a React component.

            Write complete unit tests covering all described requirements.
            Use multiple files in a directory structure that makes sense.

            Create the tests inside a `src/components/<ComponentName>` directory.
            The code using this generated code should not require additional modifications.

            You must indicate the script type in the code block.
            Do not suggest incomplete code which requires users to modify.
            Always put `// filename: src/components/<ComponentName>/<filename>` as the first line of each code block.

            Feel free to include multiple code blocks in one response. Do not ask users to copy and paste the result.
            """)

            print("#1")
            agent0.initiate_chat(requirements_agent, True, True, message=message)

            print("#2")
            component_description_message = agent0.last_message(requirements_agent)["content"]
            print(component_description_message)

            print("#3")
            agent0.initiate_chat(react_component_agent, True, True, message=component_description_message)

            print("#4")
            llm_message = agent0.last_message(react_component_agent)["content"]
            print(llm_message)
            aitools_autogen.utils.save_code_files(llm_message, self.work_dir)

            # Generate styles
            agent0.initiate_chat(styling_agent, True, True, message=component_description_message)
            styling_message = agent0.last_message(styling_agent)["content"]
            aitools_autogen.utils.save_code_files(styling_message, self.work_dir)

            # Generate tests
            agent0.initiate_chat(testing_agent, True, True, message=component_description_message)
            testing_message = agent0.last_message(testing_agent)["content"]
            aitools_autogen.utils.save_code_files(testing_message, self.work_dir)

            print("#5")
            self._summary_result = aitools_autogen.utils.summarize_files(self.work_dir)
        except Exception as e:
            print(f"An error occurred: {e}")
            self._summary_result = "An error occurred while generating the React components."