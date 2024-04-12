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
   ### **After installation you can access various commands on your computer/phone such as:**

   * #### custom_command (This command is installed automatically for you) - displays all the custom commands installed on your machine
   * push command - synchronse rather than just push
   * pull command - updates your local branch with changes from remote
   * pushfile command - similar to "push" command but it stages and commits files individually then updates the remote. To skip a file from being staged and committed type "pass". 
   (Note: you can set and remove "Update README.md" as your default commit message for all README.md files)
   * pushall command - similar to "push" command but it stages and commits changes in the working tree

   * createRepo command - creates a github repository right from the command line
   * deleteRepo command - deletes a github repository right from the command line. NOTE: THIS COMMAND IS TO BE USED WITH CAUTION, any repository deleted CANNOT be reversed.
   * cloneRepo command - displays the list of repositories and clone them from any account right from the command line. Collaboration has never been more interesting!

   * restoreFile command - restores file(s) to previous states

   * viewRepos command - displays the list of repositories from any account right from the command line. Bringing the information to you on the go!
   * betty linter command
   * pycode command - a pycodestyle (PEP 8) linter

   * gitignore command - creates/updates your .gitignore file by navigating to any file/directory to select and/or update them to your .gitignore file

   * branch command - creates, setup the branch on the remote and switch between local branches
   * merge command - merges changes in the current branch to main/master branch. Note: keeps commit history linear, preventing 3way merge
   * status command - displays information about tracked and untracked changes in the branch

   * curfol command - opens current working directory using file explorer
   * pyxecute - appends shebang and makes your python files executable
   * shxecute - works just like pyxecute but for bash scripts

   * jsxecute - works just like pyxecute but for js scripts

   * pycodemore command(pycode with details)
   * createPatch command - creates a .patch file
   * rollback command - reverts the current branch to an older commit instance
   * cls command - clear your screen
   * authorID - configures your Github Identity(Global and Local) on your local machine
   * commitree command - displays a tree of your commit history

   * compareChanges command - displays the content of uncommited changes on the working tree
	* commitdir command - commits all the changes in the current dir
	* commitall command - just like commitdir but commits all the changes in the working tree instead
   * wcount command - counts the lines, words and chars in files
   * stash command - saves uncommitted changes in the working tree for the curent branch
	* viewStash command - displays a list of all stashed changes in all branches and can be applied to the current branch
	* logit command - displays a detailed log of your commits with their branches

   * py3venv command - creates a python3 virtual environment in the cwd
   * djangoToolbar command - install and configures Django debug toolbar
   * drf command - install and configures Django RESTframework and its authentication token functionality
   * djoser command - install and configures djoser for use with drf authentication token functionality
   * jwtDjango command - install and configures json web token for use in your django project
   * static4django command - configures the STATIC_DIRS in settings.py for non-app dirs

	* startproject command - creates a new django project
	* startapp command - creates django apps for projects within any django project
	* runserver command - spins up the django development server from any directory"
   Note: Provided, there is atleast one django project in the current working directory, it will find it and spin it.
	* makemigrations command - performs the makemigrations process
	* migrate command - creates the model tables in the database
	* django command - displays the django version you are using
	* djshell command - launches the django shell
	* mkandmigrate command - a combination of the makemigrations and migrate commands
	* showmigrations command - displays the history of migrations within an app or all the apps in a project
	* sqlmigrate command - presents the sql query of any migration
   * requirement_txt command - creates, updates and install the dependencies in the requirement.txt file

   * mysqlversion - checks if MySQL is installed and also prints its version
	* mysqlstartserver - starts MySQL server
	* mysqlstopserver - stops MySQL server
	* mysqlrestartserver - restarts MySQL server
	* mysqlstatus_server - displays the status of MySQL server
	* mysqlshell - launches MySQL shell

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

#### Depending on the command, the usage instruction for that command is provided after its successful installation.

<br>

### Contributing
#### I welcome contributions from the community! If you'd like to contribute to Custom commands, please follow these steps:

- Fork this repository.
- Create a new branch for your feature or bug fix.
- Commit your changes and push to your fork.
- Submit a pull request to this repository.

<br>

# Changelog
This file contains the notable changes made to the Custom Commands project.


## New
   - jsxecute
   - restoreFile
   - djangoToolbar
   - jwtDjango
   - static4django
   - djoser
   - drf

## Changes
   - Added the list of endpoints created by drf, jwtDjango and djoser to the the displayed text after installation
   - changed compareChanges command to compareChange command
   - django config commands now display the specific changes made to the settings and urls files
   - added support for DRF-xml rednderer configuration, separated DRF-auth configuration from DRF config in DRF command
   - implemented app-level urls.py auto creation and urls configuration were added in startapp command
   - gitignore now auto add all \_\_pychache\_\_ files and venv dirs if you choose to
   - [More](https://github.com/DafetiteOgaga/custom_commands/blob/master/changes.md)


## Fixes
   - handled the case where a user tries to install and configure a django project without initially installing an app
   - fixed the DRF module error for runserver, sqlmigrate commanda
   - handled moduleNotFound error in migrate command
   - minor bug fixes to: djshell, makemigrations, mkandmigrate, static4django
   - [More](https://github.com/DafetiteOgaga/custom_commands/blob/master/fixes.md)




###### *We Rise by Lifting Others.*
