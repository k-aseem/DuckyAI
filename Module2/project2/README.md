# Project 2 Guidance

I suggest the following approach to completing this set of exercises:

* Have a look at the reading and the example tfidf_example python script to get a sense of what the tfidf function does and how it works.

* Using the `project2_chat` notebook, complete the unsupervised learning exercise in the `project2` notebook.

* Using the `project2_chat` notebook, complete the supervised learning exercise in the `project2` notebook.

* Follow instructions in the project description as to how to create and submit the assessable ZIP file.


# Tip: Creating a zip file

Creating a zip file that includes only specific files from a folder can be done via command line on both Windows and Mac. Here are the instructions:

### For Windows Users (Using 7-Zip)

1. **Install 7-Zip:**
   - If you don't have 7-Zip installed, download and install it from [7-Zip's official website](https://www.7-zip.org/).

2. **Open Command Prompt:**
   - Search for `cmd` in the Start menu and open Command Prompt.

3. **Navigate to the Parent Directory:**
   - Use the `cd` command to go to the parent directory of the `project2` folder. For example:
     ```bash
     cd path\to\parent\directory
     ```
   - Replace `path\to\parent\directory` with the actual path.

4. **Create the Zip File:**
   - Execute the following command:
     ```bash
     7z a -tzip project2_submission.zip .\project2\project2.ipynb .\project2\project2_chat.ipynb
     ```
   - This command creates `project2_submission.zip` containing only `project2.ipynb` and `project2_chat.ipynb` from the `project2` folder.

### For macOS Users

1. **Open Terminal:**
   - You can find Terminal in your Applications under Utilities, or search for it using Spotlight.

2. **Navigate to the Parent Directory:**
   - Use the `cd` command to change to the directory that contains the `project2` folder. For example:
     ```bash
     cd /path/to/parent/directory
     ```
   - Replace `/path/to/parent/directory` with the actual path.

3. **Create the Zip File:**
   - Use the `zip` command to create the zip file:
     ```bash
     zip project2_submission.zip project2/project2.ipynb project2/project2_chat.ipynb
     ```
   - This command adds the `project2.ipynb` and `project2_chat.ipynb` files from the `project2` folder to a new zip file named `project2_submission.zip`.

In both cases, you'll end up with a `project2_submission.zip` file in the parent directory of `project2`, containing only the specified `.ipynb` files.
