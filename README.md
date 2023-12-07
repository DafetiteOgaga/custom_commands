# Custom Commands

![Device check Image](.intro.jpg)
![Main menu page 1](.main_menu.jpg)
![Main menu page 2](.main_menu2.jpg)

### Note: **You can view all your custom commands by running `custom_commands` on your terminal**

# Installation

1. ### **Clone the repository:**
   ```bash
   git clone https://github.com/DafetiteOgaga/custom_commands.git
   ```
2. ### **cd into the repository:**
   ```bash
   cd custom_commands
   ```
3. ### **Then, run:**
   ```bash
   ./setScript.sh
   ```
   ### **to access various commands that you can install on your computer/phone such as:**

   * #### custom_command (This command is installed automatically for you) - displays all the custom commands installed on your machine
   * push command - synchronse rather than just push
   * pull command - updates your local machine from remote
   * pushfile command - similar to "push" command but it updates the remote with individual file commit messages for good practice
   * createRepo command - creates a github repository right from the command line
   * cloneRepo command - clone a repository with less commands
   * betty linter command
   * pycode command - a pycodestyle (PEP 8) linter
   * curfol command - opens current working directory using file explorer
   * pyxecute - appends shebang and makes your python files executable
   * pycodemore command(pycode with details)
   * cls command - clear your screen
   * authorID - configures your Github Identity(Global and Local) on your local machine
   * wcount command - counts the lines, words and chars in files
   * ctemp command - generates a default C source file template
   * clear_commit command - clears the staging area and recent commits on your local machine
   * mycompile command - compile C source files (with options)
   * pycompile command - compile python files
   * myascii command - prints a simple version of the ASCII table
   * rot13 command - Rot13 Cipher
   * rot47 command - Rot47 Cipher
   * guessGame command- a Guessing Game(To unwind)

<br>

### Usage

Depending on the command, the usage instruction for that command is provided after its successful installation.

<br>

# Changelog
This file contains the notable changes made to the Custom Commands project.

<br>

## New
   - clear_commit command clears the local staging area and commits
   - pushfile command updates the remote with individual commits to each files
   - pyxecute can now make python scripts that has no .py extension into executables and still filter out non python files
   - Added the last choice of command and the command it created to the display
   - Added wcount command. calculates and output the number of lines, words and characters in your file
   - Added pyxecute command. Easily turns py scripts into executables
   - Added custom_commands as a command that displays all of the commands created so far
   - Added curfol command. This automatically opens the current working directory in file explorer
   - Added support for multiple arguments for pycode, pycodemore and pycompile commands
   - pycompile command that compiles python codes to .pyc executables
   - pycodemore command a detailed version of pycode (according to EP 8 conventions)
   - pycode command(a short for pycodestyle) for python code compliance according to PEP 8 conventions
   - Added betty linter command for source files
   - Added installations of betty linter and pycodestyle(PEP 8)
   - Added Support for 64-bit operating system computers
   - Added Support for AARCH64/ARM64 operating system for phones
   - Added Support for PC and Phone and device detection
   - Added Support for root user password request for PC
   - Added command to configure Github Author Identity Globally and/or Locally
   - Added sample screenshot of the menu when the script is executed
   - Added the git username and email feature locally to the create and clone repository commands (specific to the current working repository)
   - Added reminder to users not to create a repository within an existing repository
   - Added reminder to users not to clone into an existing repository
   - Added cls command to the list
   - Added quit option to push command
   - Moved the project to remote repository


## Changes
   - new updates and improvements implemented to the the program
   - pull and push commands has been updated for robust perfomances
   - Improved user experience with a little bit of animated display
   - Minor changes made to the script and display for effectiveness
   - pyxecute also appends the python3 shebang line to the first line of the script
   - pyxecute command now checks for the presence of py scripts and responds accordingly
   - Readme file was updated
   - "from" word was removed from the parting message after installation
   - Change to multiple display in pages and its navigation
   - Minor changes made to guessing game, rot13, rot47 and my ascii codes to enhance performance
   - clone and create repo commands now collect users information during installation
   - Changed the process of users having to open the clone and create repo scripts to manually input their details
   - Changed the simple ASCII table display
   - Changed default C template description
   - Removed emoji from Guessing game
   - Removed emoji from Rot47
   - Removed emoji from Rot13
   - Removed emoji from simple ASCII table


## Fixes
   - you don't have to enter your information twice anymore when running createRepo and/or cloneRepo anymore, in a single execution
   - "Next" and "Previous" choices no longer reinstall the previous command and clears off the screen, any information belonging to the previous command
   - Resolve issue of invalid path in ctemp command
   - Fixed bugs in createRepo command
   - Fixed scripts repetition for PCs and Phones
   - Fixed bugs in cloneRepo command
   - Fixed bugs preventing pycodemore command from working due to pycodestyle
   - Fixed bugs in "[n] option display and selection"
   - Fixed bugs in ctemp command
   - Fixed exec: format errors caused by variation in operating system architectures for both phones and computers
   - Commands creation now runs contineously until you quit the process
   - Source files and compilations has been removed from the operations for optimization
   - The authorID, create and clone repo commands now automatically configures local author during operation
   - You now have to provide your Username, token and email when creating create/clone repo commads
   - Repetition of codes in setscript has been removed to enhance robost performance 
   - Fixed and removed answer display before the start of the guessing game
   - Added execute permission for all user to the files.
   - Fixed response to wrong input entered by users during installation and command execution
   - Fixed option display to be limited to alphabets and not numbers
   - Removed repeated lines of codes that need not be




###### We Rise by Lifting Others.
