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
   * pull command - updates your local branch with changes from remote
   * pushfile command - similar to "push" command but it stages and commits files individually then updates the remote. To skip a file from being staged and committed type "pass". 
   (Note: you can set and remove "Update README.md" as your default commit message for all README.md files)
   * pushall command - similar to "push" command but it stages and commits changes in the working tree

   * createRepo command - creates a github repository right from the command line
   * deleteRepo command - deletes a github repository right from the command line. NOTE: THIS COMMAND IS TO BE USED WITH CAUTION, any repository deleted CANNOT be reversed.
   * cloneRepo command - displays the list of repositories and clone them from any account right from the command line. Collaboration has never been more interesting!
   * viewRepos command - displays the list of repositories from any account right from the command line. Bringing the information to you on the go!
   * betty linter command
   * pycode command - a pycodestyle (PEP 8) linter

   * branch command - creates, setup the branch on the remote and switch between local branches
   * merge command - merges changes in the current branch to main/master branch. Note: keeps commit history linear, preventing 3way merge
   * status command - displays information about tracked and untracked changes in the branch

   * curfol command - opens current working directory using file explorer
   * pyxecute - appends shebang and makes your python files executable
   * shxecute - works just like pyxecute but for bash scripts
   * pycodemore command(pycode with details)
   * createPatch command - creates a .patch file
   * rollback command - reverts the current branch to an older commit instance
   * cls command - clear your screen
   * authorID - configures your Github Identity(Global and Local) on your local machine
   * commitree command - displays a tree of your commit history

   * compare command - displays the content of uncommited changes on the working tree
	* commitdir command - commits all the changes in the current dir
	* commitall command - just like commitdir but commits all the changes in the working tree instead
   * wcount command - counts the lines, words and chars in files
   * stash command - saves uncommitted changes in the working tree for the cuurent branch
	* viewStash command - displays a list of all stashed changes in all branches and can be applied to the current branch
	* logit command - displays a detailed log of your commits with their branches

   * py3venv command - creates a python3 virtual environment in the cwd"
	* startproject command - creates a new django project"
	* startapp command - creates django apps for projects within any django project"
	* runserver command - spins up the django development server from any directory"
   Note: Provided, there is atleast one django project in the current working directory, it will find it and spin it.
	* makemigrations command - performs the makemigrations process"
	* migrate command - creates the model tables in the database"
	* django command - displays the django version you are using"
	* djshell command - launches the django shell"
	* mkandmigrate command - a combination of the makemigrations and migrate commands"
	* showmigrations command - displays the history of migrations within an app or all the apps in a project"
	* sqlmigrate command - presents the sql query of any migration"

   * ctemp command - generates a default C source file template
   
   * clear_commit command - clears the staging area and recent commits on your local machine
   * printmyEnv command - prints a list of your env paths
	* show command - displays a list of all commits made to the selected repository
	* verifyRepo command - checkes if the current dir is a repository or not

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
   - startproject creates a new django project
   - startapp creates a new django app within a django project
   - runserver will spin up the development server right from any directory
   - makemigrations creates migrations
   - migrate will map the created tables to the database
   - django displays the django version currently in use(within a venv or without), validating the presence of django
   - djshell launches the django interactive shell
   - mkandmigrate combines the makemigrations and migrate commands to save time during development
   - showmigrations displays the migrations in all or any of the selected app
   - sqlmigrate presents the sql query of the migration you select
   - py3venv creates a venv without worrying about all the arguments
   - verifyRepo to checkes if the current dir is a repository or not
   - show - displays a list of all commits made to the current repository
   - printmyEnv to prints a list of your env paths
   - logit command - displays a detailed log of your commits with their branches
   - viewStash command - displays a list of all stashed changes in all branches and can be applied to the current branch
   - stash - saves uncommitted changes in the working tree for that branch
   - commitall to commits all the changes in the working tree
   - commitdir to commits all the changes in the current dir
   - compare - displays the content of uncommited changes on the working tree
   - commitree to see a tree of your commit history
   - rollback command - reverts the current branch to an older commit instance
   - createPatch command - creates a .patch file using the changes between the two files provided as arguments
   - shxecute to appends shebang and makes your bash files executable
   - status command to displays information about tracked and untracked files/changes in the branch
   - merge command to merges changes in the current branch to main/master branch. prevents 3way merge by setting the history linear and then put the branch ahead of the master, allowing for a fast forward merge
   - branch command to creates, sets up the branch on the remote and also switch between local branches
   - pushall command to stage, commit and updates the local/remote repos with changes in the working tree
   - pushfile commands will now skip already staged and committed files during usage. making the use of "pushfile *" more robust
   - added viewRepos command - you can now view any github repositories right from you CLI
   - deleteRepo command - checks and deletes github repositories
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
   - curfol now works on ubuntu and wsl-ubuntu
   - you can now skip files from being committed when using pushfile
   - majority of the display/output now commes with text coloring
   - deleting your repo is now much flexible as all you have to is select the number corresponding to the repo from the display me listing all of your repos
   - error of "... divergent branches ... reconcile divergent branches" has been fixed for all pull processes
   - massive improvements made to cloneRepo command. All you now need to clone your repo is just to run the command. It displays all your private and public repositories, giving you the option of cloning any of them with the selection menu. To clone another person's public repo, you only need the username. Collaboration has never been more interesting, you can now do so easily using this command
   - you can now observe the progress of setting up auto commit message for README.md files via a progress bar
   - added the ability to set "Update README.md" as your default commit message to all README.md files
   - new updates and general improvements to the the program
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
   - minor bug fixes made to setScript, cloneRepo and createRepo commands
   - every prompt that require single character as response are now auto executing soon as the character is provided
   - you don't have to enter your information twice anymore when running createRepo and/or cloneRepo anymore in the same session
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
