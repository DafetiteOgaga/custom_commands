# Custom Commands

### `custom_command` is installed automatically for you - displays all the custom commands installed on your machine

### Git commands
   * push command - synchronse rather than just push
   * pull command - updates your local branch with changes from remote
   * pushfile command - similar to "push" command but it stages and commits files individually then updates the remote. To skip a file from being staged and committed type "pass".<br>
   Note: you can set and remove "Update README.md" as your default commit message for all README.md files
   * pushall command - similar to "push" command but it stages and commits all changes in the working in one operation
   * createRepo command - creates a github repository right from the command line without having to enter your details everytime
   * cloneRepo command - displays the list of repositories and clone them from any account right from the command line. Collaboration has never been more interesting!
   * deleteRepo command - deletes a github repository right from the command line.<br>
   NOTE: THIS COMMAND IS TO BE USED WITH CAUTION, any repository deleted CANNOT be reversed.
   * restoreFile command - restores individual file(s) to previous states
   * gitignore command - creates/updates your .gitignore file by navigating to any file/directory to select and/or update them to your .gitignore file.<br>
   Note: This command auto detect \_\_pycache\_\_ and virtual environment directories
   * branch command - creates and setup new branches on the remote and switch between them locally
   * merge command - merges changes in the current branch to main/master branch.<br>
   Note: keeps commit history linear, preventing 3way merge
   * status command - displays information about tracked, untracked, committed and uncommitted changes in the branch
   * revert2commit command - safely reverts the current branch to an older commit instance but with a new revert commit without disrupting the commit history
   * authorID - configures your Github Identity (Globally and Locally) on your local machine
   * commitree command - displays a tree of your commit history
   * compareChange command - displays the content of uncommited changes on the working tree of the current branch
   * commitdir command - commits all the changes in the working directory to the repository
   * commitall command - just like commitdir but commits all the changes in the working tree instead
   * stash command - saves uncommitted changes in the working tree for the curent branch
   * viewStash command - displays a list of all the stash in all branches and can be applied to the current branch
   * logit command - displays a detailed log of your commits with their branches
   * clear_commit command - restores your working tree to the same state as your remote
   * show command - displays a list of all commits made to the selected repository
   * verifyRepo command - checkes if the current dir is a repository or not
   * viewRepos command - displays the list of repositories from any account right from the command line. Bringing the information to you on the go!
   * getRepoUserName command - prints the username of the current repository
   * updateToken command - adds/stores and updates a new github token and swap it with the old (expired) token in your local repository
   * distributeApk command - updates the versioning and distributing my
   altaviz mobile app accordingly i.e making it available for updates and
   downloads

### Djando commands
   * startproject command - creates a new django project
   * startapp command - creates and configures django apps for projects within any django project
   * runserver command - spins up the django development server from any directory.<br>
   Note: Provided, there is atleast one django project in the current working directory or its subdirectories, it will find and spin it.
   * makemigrations command - performs the makemigrations process
   * migrate command - creates the model tables in the database (migrate process)
   * requirement_txt command - creates, updates and install the dependencies in the requirement.txt file
   * drf command - install and configures Django RESTframework, token authentication, xml renderer.<br>
   It also configures a models.py, serializers.py, views.py and urls.py for a basic Bookstore application with all the necessary API endpoints
   * djoser command - install and configures djoser for use with drf with all its basic API endpoints
   * jwtDjango command - install and configures json web token (simple JWT) for use in your django project with the token generation and refresh API endpoints
   * djangoToolbar command - install and configures Django's debug toolbar
   * static4django command - configures the STATIC_DIRS in settings.py for static files
   * djshell command - launches the django shell
   * mkandmigrate command - a combination of the makemigrations and migrate in one command
   * showmigrations command - displays the history of migrations within an app or all the apps in a project
   * sqlmigrate command - displays list of all mirations and presents the sql query of the selected item
   * django command - displays the django version you are using
   * djangoUrls command - displays the list and details of all configured urls in your django project.
   * collectstatic command - collects static files to the staticfiles dir for production in django applications.

### Javascript commands
   * createReactApp command - creates a React application and installs dependencies
   * createExpoApp command - creates an Expo mobile application, dependencies from the initial copy (i.e saving you installation time) and spin up the server automatically.
   * dependencyDevReact command - installs dependencies in development
   * updateReactPackagez command - updates React packages to their latest versions
   * dependencyDevReact command - installs dev-dependencies

### Shell commands
   * pyxecute - prepends the python3 shebang line to your script and gives it the execute permission
   * shxecute - works just like pyxecute but for bash scripts
   * jsxecute - works just like pyxecute but for javascripts
   * curfol command - opens current working directory in the file explorer
   * cls command - clears your screen
   * wcount command - counts the lines, words and chars in files and prints it to display
   * createPatch command - creates a .patch file
   * printmyEnv command - prints a list of your env paths
   * setEnv command - sets environment variable for all sessions

### MySQL commands
   * mysqlOp - starts, stops, restarts and checks the status of MySQL server
   * mysqlversion - checks if MySQL is installed and also prints its version
   * mysqlshell - launches MySQL shell

### Betty command
   * betty linter command for C programming language

### Python commands
   * py3venv command - creates a python3 virtual environment in the current working directory
   * pycode command - a pycodestyle (PEP 8) linter for python programming language
   * pycodemore command - this is pycode but with more details
   * pycompile command - compile python files

### C commands
   * ctemp command - generates a default source file template for C programming
   * mycompile command - compile C source files.<br>
   Note: you can stop at the preprocessing, compile, assembly or linking stages and also set different level of standards
   * myascii command - prints a simple version of the ASCII table
   * rot13 command - Rot13 Cipher
   * rot47 command - Rot47 Cipher
   * guessGame command- a Guessing Game(To unwind)

### MongoDB command
   * mongoOp command - starts, stops, restarts and checks the status of
   the server
   * mongoVersion - checks if MongoDB is installed and also prints its version


   ###### *We Rise by Lifting Others.*
