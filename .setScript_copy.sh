#!/usr/bin/env bash

UPDATEPATH="$HOME/.xbin/pyfiles/check4Update"
OPTION="$1"
DFILENAME="$2"
DUSERNAME="YOUR_GITHUB_USERNAME"
DTOKEN="YOUR_PERSONAL_ACCESS_TOKEN"
DEMAIL="YOUR_REGISTERED_GITHUB_EMAIL"
NUSERNAME="$3"
NTOKEN="$4"
NEMAIL="$5"
EFFT="effortlessly."
P1="ghp_ek81wkYt15bHQzABMQVeFpiNRNcrpy46Hqc7"
P2="ek81wkYt15bHQzABMQVeFpiNRNcrpy46Hqc7"
ANYWHERE="Simply run(anywhere in your environment)"
STRT="You can now"
SUP="to setup"
XBIN="$HOME/.xbin"
DBIN=".xbin"
SCPTS=".scpts"
UINPUT="$6"
VERSIONNUMBER="20250627.0130"

# colors and styles
RESET="\033[0m"
BOLD="\033[1m"
ITALIC="\033[3m"
UNDERLINE="\033[4m"
GREEN="\033[32m"
BRIGHT_BLACK="\033[90m"
BRIGHT_RED="\033[91m"
BRIGHT_GREEN="\033[92m"
BRIGHT_YELLOW="\033[93m"
BRIGHT_BLUE="\033[94m"
BRIGHT_MAGENTA="\033[95m"
BRIGHT_CYAN="\033[96m"
BRIGHT_WHITE="\033[97m"

# emogi unicode
CHECK=$'\u2713'
CROSS=$'\u2717'
FOLDER=$'\U1F4C1'
MEMO=$'\U1F4DD'
SMILEY=$'\u263A'

quit() {
	# exit
	local var="$1"
	if [[ "$var" == "q" || "$var" == "Q" ]]; then
	echo ""
		echo "Operation aborted."
		exit 0
	fi
}

check_for_python() {
	# check for python (gitbash) or python3 (unix-like)
	PYTHON="python3" # for unix-like
	# echo "Checking if python is installed"
	if is_git_bash; then
		PYTHON="python" # for gitbash
		is_python_installed=$("$PYTHON" --version 2>&1)
	else
		if ! command -v "$PYTHON" &> /dev/null; then
			is_python_installed="Python was not found"
		else
			is_python_installed=$("$PYTHON" --version 2>&1)
		fi
	fi


	# echo "is_python_installed: $is_python_installed" # comment out this line when done

	if [[ "$is_python_installed" == *"Python was not found"* ]]; then
		if is_git_bash; then
			# if os is windows (running git bash)
			echo ""
			echo "You have to install python."
			echo "Remember to tick $CHECK the checkboxes:"
			echo "  1. \"Use admin privilages when installing py.exe\" (if not already ticked)"
			echo "  2. \"Add python.exe to PATH\""
			echo "Visit https://www.python.org/downloads/ to download and install it."
			echo "Note $MEMO: You may need to logout/login or just restart your pc after installing python"
			echo ""
			exit 1
		else
			# other unix-like os
			# Attempt to install Python3
			echo "Python3 not installed."
			echo "Installing it..."
			sleep 0.1
			# other package managers command
			
			if [[ "$WHICH" =~ [p] ]]; then
				# for phone
				pkg update
				pkg install python
			elif [[ "$WHICH" =~ [c] ]]; then
				# for pc
				sudo apt-get update
				sudo apt-get install -y python3
			fi
		fi
	# else # remove this else block when done
	# 	echo "... $PYTHON is installed"
	# 	# sleep 0.1
	fi
}

is_git_bash() {
    [[ "$OSTYPE" == "msys" || "$MSYSTEM" == MINGW* ]]
}
is_wsl() {
    grep -qi "microsoft" /proc/version 2>/dev/null
}
is_macos() {
    [[ "$OSTYPE" == "darwin"* ]]
}
is_linux() {
    [[ "$OSTYPE" == "linux-gnu"* && ! $(is_wsl) ]]
}
get_username() {
    if is_git_bash; then
        echo "$USERNAME"
    else
        echo "$USER"
    fi
}

check_device_type() {
	if [[ "$device_type" == "phone" ]]; then
		echo -e "\nThis command can only be installed on a PC"
		echo "COMMAND NOT INSTALLED"
		quit "q"
	fi
}

# dafetite() {
# 	local commandName="$1"
# 	echo ""
# 	read -n 8 -s -r -p "Enter passcode: " dafetite
# 	echo ""
# 	if [[ "$dafetite" != "dafetite" ]]; then
# 		echo -e "\nOopsy! You are not allowed to install this command, sorry."
# 		echo "$commandName command NOT installed"
# 		quit "q"
# 	fi
# }

check_dafetite() {
	echo ""
	read -n 9 -s -r -p "Enter passcode: " dafetite
	echo ""
	if [[ "$dafetite" != "dafetite." ]]; then
		echo -e "\nOopsy! Permission denied!."
		echo "Try again."
		sleep 1
		# quit "q"
	else
		DAFETITEOGAGA="true"
		# echo "Adding personal scripts..."
		dOptions+=("${personal_scripts[@]}")
		total_items=$((total_items + ${#personal_scripts[@]}))
		# echo "total_items after adding personal scripts: $total_items XXXXXXXXXX"
		ADMIN=" (Admin mode)"
	fi
	# DAFETITEOGAGA="true"
	# echo "Adding personal scripts..."
	# dOptions+=("${personal_scripts[@]}")
	# total_items=$((total_items + ${#personal_scripts[@]}))
	# echo "total_items after adding personal scripts: $total_items XXXXXXXXXX"
}

auth() {
	# initiates sudo authentication
	local var="$WHICH"

	if [[ ${#var} == 1 ]]; then
		if [[ "$var" =~ [cC] ]]; then
			rep="PC"
			name=$(get_username)
			greet_sudo_user="\nHi $name $SMILEY  ..."
			if is_git_bash; then
				echo -e "$greet_sudo_user"
			else
				sudo -v # to refresh sudo timestamp (if user has been authenticated before)
				sudo_response="$?"

				# If sudo failed
				if [[ "$sudo_response" -ne 0 ]]; then
					echo ""
					echo "You have to authenticate to proceed."
					# Retry sudo
					sudo -E echo -e "$greet_sudo_user"
					sudo_response="$?"

					if [[ "$sudo_response" -ne 0 ]]; then
						echo ""
						echo "Authentication failed. Please try again."
						exit 1
					fi
				else
					# If first sudo worked, proceed
					sudo -E echo -e "$greet_sudo_user"
				fi
			fi
		elif [[ "$var" =~ [pP] ]]; then
			rep="Phone"
			echo -e "\nHi USER $SMILEY  ..."
		fi
	fi
}

intro() {
	# detects device type
	local whch="$1"

	CHECKER_PC_PH=$(echo "$XBIN" | cut -d '/' -f 2)
	device_type=""
	if [[ "$CHECKER_PC_PH" =~ [hH]ome|[uU]sers ]]; then
		device_type="pc"
		if [[ "$whch" =~ [0] ]]; then
			if is_wsl; then echo -e "Machine: Windows subsystem for linux (WSL)"
			elif is_macos; then echo -e "Machine: macOS"
			elif is_linux; then echo -e "Machine: linux"
			# echo -e "I can see that this is a PC"
			fi
		else
			echo -e "$rep"
		fi
	elif [[ "$CHECKER_PC_PH" == "data" ]]; then
		device_type="phone"
		if [[ "$whch" =~ [0] ]]; then
			echo -e "Device: Phone"
		else
			echo -e "$rep"
		fi
	elif is_git_bash; then
		echo -e "Machine: Windows (Git Bash)."
	else
		if [[ "$whch" =~ [0] ]]; then
			echo -e "I can't figure out your device type."
		else
			echo -e "Oh! Great. Configuring for a $rep"
		fi
	fi
}

invalid_selection() {
	# wrong selection
	if [[ "$OPTION" =~ [zZ] ]]; then
		echo -e "Wrong selection. You can only select from the options above."
		echo -e "Try again."
	elif [[ "$OPTION" =~ [nNpP] ]]; then
		echo -e "Another operation?"
	fi
}

streamedit() {
	# replaces user details fields with user details
	local var1="$1" # what to find
	local var2="$2" # what to replace with
	# $XBIN/$DFILENAME is the path to the file

	sed -i "s/$var1/$var2/g" "$XBIN/$DFILENAME"
}

converPyShebang4gitbash() {
	# replaces all occurences of the shebang line to tune to gitbash env
	local file_path="$1" # file path
	sed -i "s|#!/usr/bin/env python3|#!/usr/bin/env python|g" "$file_path"
}

details() {
	# display the user details for confirmation
	echo -e ".................................."
	echo -e "Username: $NUSERNAME"
	echo -e "Token: ghp_$NTOKEN"
	echo -e "Email: $NEMAIL"
	echo -e ".................................."
}

unametokenmaill2() {
	# collects user details to createRepo, cloneRepo, deleteRepo, viewRepo and distributeApk commands
	while [[ -z "$NUSERNAME" ]]; do
		echo -n "Kindly Enter your Github Username >>> "
		read NUSERNAME
		quit "$NUSERNAME"
		if [[ -z "$NUSERNAME" ]]; then
			echo -e "You must provide your Github Username to proceed."
			echo -e ""
		fi
	done
	echo -e "........................................................"
	echo -e "Example of what the token will be is $P2"
	echo -e "Recall that $P1 = ghp_ + $P2"
	echo -e "What you need to supply is $P2 and leave out the rest."
	echo -e "........................................................"
	sleep 0.1
	while true; do
		echo -n "Your Classic Github token (without \"ghp_\") >>> "
		read NTOKEN
		quit "$NTOKEN"
		NUM2=${#NTOKEN}
		# echo -e "$NUM2"
		if [[ "$NUM2" -ne 36 ]] && [[ "$NUM2" -ne 40 ]]; then
			echo -e ""
			echo -e "TOKEN: $NTOKEN which you supplied is not a classic token."
			echo -e "Make sure to remove \"ghp_\" and that there is no whitespace."
			echo ""
		fi
		if [[ "$NUM2" -eq 40 ]] && [[ "$NTOKEN" == *"ghp_"* ]]; then
			NTOKEN="${NTOKEN#ghp_}"
			break
		elif [[ "$NUM2" -eq 36 ]]; then
			break
		fi
		echo -e "You must provide your Classic Github token to proceed."
		echo -e ""
	done
	
	while [[ -z "$NEMAIL" ]]; do
		echo -n "Lastly, your Github Email >>> "
		read NEMAIL
		quit "$NEMAIL"
		if [[ -z "$NEMAIL" ]]; then
			echo -e "You must provide your Github Email to proceed."
			echo -e ""
		fi
	done
	echo ""
	sleep 0.1
	echo -e "Confirm your details:"
	details
}

unametokenmaill() {
	# populates the user details to createRepo, cloneRepo, deleteRepo, viewRepo and distributeApk commands
	if [[ "$NUSERNAME" && "$NTOKEN" && "$NEMAIL" ]]; then
		echo -e "Hey! I still have your details"
		while [[ "$VALS" != [yYnN] ]]; do
			details
			echo -n "Would you rather use this values? [y/N] >>> "
			read -n 1 -s -r VALS
			echo -e ""
			if [[ "$VALS" != [yYnN] ]]; then
				echo -e ""
				echo -e "You must decide to proceed."
			fi
		done
		
		if [[ "$VALS" =~ [yY] ]]; then
			echo -e ""
		elif [[ "$VALS" =~ [nN] ]]; then
			NUSERNAME=""
			NTOKEN=""
			NEMAIL=""
			echo -e ""
			unametokenmaill2
		fi
		VALS=""
	else
		unametokenmaill2
	fi
	while [[ -z "$ANS" ]]; do
		echo -n "Check that these are correct. Are they? [y/N] >>> "
		read -n 1 -s -r ANS
		if [[ -z "$ANS" ]]; then
			echo -e "You must decide to proceed."
			echo -e ""
		fi
	done

	echo -n "$ANS"
	echo -e ""
	if [[ "$ANS" =~ [yY] ]]; then
		main_copy_command_script_fxn
		streamedit "$DUSERNAME" "$NUSERNAME"
		streamedit "$DTOKEN" "$NTOKEN"
		streamedit "$DEMAIL" "$NEMAIL"
	elif [[ "$ANS" =~ [nN] ]]; then
		echo -e "Ok."
		echo ""
		exit 0
	else
		echo -e "You must provide these information to proceed"
		echo ""
		exit 1
	fi
	ANS=""
}

copy_cmd_scripts_based_on_filetypes() {
	# identifies device type and copies/create the script for the command
	echo "custom commands" > "$XBIN/$DFILENAME"
	case "$FILETYPE" in
		"bashscript"|"pyscript"|"personal")
			# copies the content
			cp "$SCPTS/$DFILENAME" "$XBIN/$DFILENAME"
			;;
		"cfile")
			# copies the content
			if [[ "$WHICH" =~ [p] ]]; then
				cp "$SCPTS/phone/$DFILENAME" "$XBIN/$DFILENAME"
			elif [[ "$WHICH" =~ [c] ]]; then
				cp "$SCPTS/pc/$DFILENAME" "$XBIN/$DFILENAME"
			fi
		;;
	# fi
	esac
	# make the script executable
	chmod +x "$XBIN/$DFILENAME"
	if is_git_bash; then
		converPyShebang4gitbash "$XBIN/$DFILENAME"
    fi
}

#...options display.................. #
#...2.................. #

# dOptions=(
# 	# options display
# 	#...py script files....................... #
# 	"  ${BOLD}${BRIGHT_YELLOW}push command${RESET} - stage, commit/updates local/remote repo"
# 	"  ${BOLD}${BRIGHT_YELLOW}pull command${RESET} - updates your local branch with changes from the remote"
# 	"  ${BOLD}${BRIGHT_YELLOW}pushfile command${RESET} - stage, commit individual files to the local/remote repo"
# 	"  ${BOLD}${BRIGHT_YELLOW}pullFromMain command${RESET} - pull latest changes from the main/master branch"
# 	"  ${BOLD}${BRIGHT_YELLOW}showDiffOnMain command${RESET} - logs the changes made to the main/master branch"
# 	"  ${BOLD}${BRIGHT_YELLOW}pushall command${RESET} - stage, commit and updates the local/remote repos"
# 	#...bash script files.................. #
# 	"  ${BOLD}${BRIGHT_YELLOW}createRepo command${RESET} - creates a github repository right from CLI"
# 	"  ${BOLD}${BRIGHT_YELLOW}deleteRepo command${RESET} - deletes a github repository right from CLI"
# 	"  ${BOLD}${BRIGHT_YELLOW}cloneRepo command${RESET} - clone a repository with less commands"
# 	"  ${BOLD}${BRIGHT_YELLOW}restoreFile command${RESET} - restores file(s) to previous states"
# 	"  ${BOLD}${BRIGHT_YELLOW}viewRepos command${RESET} - displays the list of repos from any account on CLI"
# 	#...py script files....................... #
# 	"  ${BOLD}${BRIGHT_YELLOW}updateToken command${RESET} - adds/updates your repo with a new token"
# 	"  ${BOLD}${BRIGHT_YELLOW}gitignore command${RESET} - creates/updates your .gitignore file"
# 	"  ${BOLD}${BRIGHT_YELLOW}branch command${RESET} - creates and also switch between branches"
# 	"  ${BOLD}${BRIGHT_YELLOW}deleteBranch command${RESET} - deletes branches locally and remotely"
# 	"  ${BOLD}${BRIGHT_YELLOW}merge command${RESET} - merge branches to main/master branch"
# 	"  ${BOLD}${BRIGHT_YELLOW}status command${RESET} - displays updates in the branch"
# 	#...bash script files.................. #
# 	"  ${BOLD}${BRIGHT_YELLOW}setEnv command${RESET} - sets a permanent environment variable"
# 	"  ${BOLD}${BRIGHT_YELLOW}currfol command${RESET} - opens cwd using file explorer"
# 	"  ${BOLD}${BRIGHT_YELLOW}pyxecute${RESET} - appends shebang and makes your python scripts executable"
# 	"  ${BOLD}${BRIGHT_YELLOW}shxecute${RESET} - appends shebang and makes your bash scripts executable"
# 	"  ${BOLD}${BRIGHT_YELLOW}jsxecute${RESET} - appends shebang and makes your js scripts executable"
# 	"  ${BOLD}${BRIGHT_YELLOW}pycodemore command${RESET}(pycode with details)"
# 	"  ${BOLD}${BRIGHT_YELLOW}createPatch command${RESET} - creates a .patch file from two files"
# 	"  ${BOLD}${BRIGHT_YELLOW}revert2commit command${RESET} - safely reverts changes to an earlier commit state"
# 	"  ${BOLD}${BRIGHT_YELLOW}cls command${RESET} - clear your screen"
# 	"  ${BOLD}${BRIGHT_YELLOW}authorID${RESET} - configures your Github Identity(Global and Local)"
# 	"  ${BOLD}${BRIGHT_YELLOW}commitree command${RESET} - displays a tree of your commit history"
# 	#...py script files....................... #
# 	"  ${BOLD}${BRIGHT_YELLOW}showDiff command${RESET} - displays detailed content of updates"
# 	"  ${BOLD}${BRIGHT_YELLOW}commitdir command${RESET} - commits all the changes in the current dir"
# 	"  ${BOLD}${BRIGHT_YELLOW}commitall command${RESET} - commits all the changes in the working tree"
# 	"  ${BOLD}${BRIGHT_YELLOW}getRepoUserName command${RESET} - prints the username of the current repo"
# 	"  ${BOLD}${BRIGHT_YELLOW}wcount command${RESET} - counts the lines, words and chars in files"
# 	"  ${BOLD}${BRIGHT_YELLOW}stash command${RESET} - saves uncommitted changes in the working tree"
# 	"  ${BOLD}${BRIGHT_YELLOW}viewStash command${RESET} - displays a list of applyable stashes"
# 	#...bash script files.................. #
# 	"  ${BOLD}${BRIGHT_YELLOW}logit command${RESET} - displays a detailed commit logs"
# 	"  ${BOLD}${BRIGHT_YELLOW}createReactApp command${RESET} - creates a React application, dependencies"
# 	"  ${BOLD}${BRIGHT_YELLOW}createExpoApp command${RESET} - creates an Expo mobile application, dependencies"
# 	"  ${BOLD}${BRIGHT_YELLOW}dependenciesReact command${RESET} - installs various React packages"
# 	"  ${BOLD}${BRIGHT_YELLOW}updateReactPackagez command${RESET} - updates React packages to latest versions"
# 	"  ${BOLD}${BRIGHT_YELLOW}dependencyDevReact command${RESET} - installs dev-dependencies"
# 	"  ${BOLD}${BRIGHT_YELLOW}py3venv command${RESET} - creates a python3 virtual environment"
# 	#...py script files....................... #
# 	"  ${BOLD}${BRIGHT_YELLOW}requirement_txt command${RESET} - creates/updates/installs dependencies in requirement.txt"
# 	#...bash script files.................. #
# 	"  ${BOLD}${BRIGHT_YELLOW}collectstatic command${RESET} - collects static files to the staticfiles dir for production"
# 	"  ${BOLD}${BRIGHT_YELLOW}djangoToolbar command${RESET} - install and configures Django debug toolbar"
# 	"  ${BOLD}${BRIGHT_YELLOW}drf command${RESET} - install and configures Django RESTframework, auth, xml renderer"
# 	"  ${BOLD}${BRIGHT_YELLOW}djoser command${RESET} - install and configures djoser (3rd party library)"
# 	"  ${BOLD}${BRIGHT_YELLOW}jwtDjango command${RESET} - install and configures json web token in your django project"
# 	"  ${BOLD}${BRIGHT_YELLOW}static4django command${RESET} - configures the STATIC_DIRS in settings.py"
# 	"  ${BOLD}${BRIGHT_YELLOW}startproject command${RESET} - installs a new django project"
# 	"  ${BOLD}${BRIGHT_YELLOW}startapp command${RESET} - installs and configures apps for django projects"
# 	"  ${BOLD}${BRIGHT_YELLOW}djangoUrls command${RESET} - used to check and monitor configured urls in django projects"
# 	#...py script files....................... #
# 	"  ${BOLD}${BRIGHT_YELLOW}runserver command${RESET} - spin up the django development server from any directory"
# 	#...bash script files.................. #
# 	"  ${BOLD}${BRIGHT_YELLOW}makemigrations command${RESET} - performs the makemigrations process"
# 	#...py script files....................... #
# 	"  ${BOLD}${BRIGHT_YELLOW}migrate command${RESET} - creates the model tables in the database"
# 	#...bash script files.................. #
# 	"  ${BOLD}${BRIGHT_YELLOW}django command${RESET} - displays the django version you are using"
# 	"  ${BOLD}${BRIGHT_YELLOW}djshell command${RESET} - launches the django shell"
# 	"  ${BOLD}${BRIGHT_YELLOW}mkandmigrate command${RESET} - a combines the makemigrations and migrate commands"
# 	#...py script files....................... #
# 	"  ${BOLD}${BRIGHT_YELLOW}showmigrations command${RESET} - displays the history of django migrations"
# 	"  ${BOLD}${BRIGHT_YELLOW}sqlmigrate command${RESET} - presents the sql query of any migration"
# 	#...bash script files.................. #
# 	"  ${BOLD}${BRIGHT_YELLOW}mongoOp${RESET} - starts, stops, restarts or checks the status of MongoDB server"
# 	"  ${BOLD}${BRIGHT_YELLOW}mongoVersion${RESET} - checks the version of MongoDB installed"
# 	"  ${BOLD}${BRIGHT_YELLOW}mysqlOp${RESET} - starts, stops, restarts or checks the status of MySQL server"
# 	"  ${BOLD}${BRIGHT_YELLOW}mysqlversion${RESET} - checks if MySQL is installed and also prints its version"
# 	"  ${BOLD}${BRIGHT_YELLOW}mysqlshell${RESET} - launches MySQL shell"
# 	"  ${BOLD}${BRIGHT_YELLOW}ctemp${RESET} - generates a default C source file template"
# 	"  ${BOLD}${BRIGHT_YELLOW}clear_commit command${RESET} - restores local repo to the same state as the remote"
# 	"  ${BOLD}${BRIGHT_YELLOW}betty linter command${RESET}"
# 	"  ${BOLD}${BRIGHT_YELLOW}pycode command${RESET} a \"pycodestyle (PEP 8)\" linter"
# 	#...py script files....................... #
# 	"  ${BOLD}${BRIGHT_YELLOW}printmyEnv command${RESET} - prints a list of your env paths"
# 	#...bash script files.................. #
# 	"  ${BOLD}${BRIGHT_YELLOW}showCommitHistory command${RESET} - displays a list of all commits made to the repository"
# 	#...py script files....................... #
# 	"  ${BOLD}${BRIGHT_YELLOW}verifyRepo command${RESET} - checkes if the current dir is a repository or not"
# 	#...bash script files.................. #
# 	"  ${BOLD}${BRIGHT_YELLOW}mycompile command${RESET} - compile C source files (with options)"
# 	"  ${BOLD}${BRIGHT_YELLOW}pycompile command${RESET} - compile python files"
# 	"  ${BOLD}${BRIGHT_YELLOW}xbin command${RESET} - opens the xbin in file explorer"
# 	"  ${BOLD}${BRIGHT_BLACK}distributeApk command${RESET} - Downloads the apk from eas and updates it to github"
# 	"  ${BOLD}${BRIGHT_BLACK}updateResumeCV command${RESET} - updates my website and github with my resume"
# 	#...C files....................... #
# 	"  ${BOLD}${BRIGHT_YELLOW}myascii command${RESET} - prints a simple version of the ASCII table"
# 	"  ${BOLD}${BRIGHT_YELLOW}rot13 command${RESET} - Rot13 Cipher"
# 	"  ${BOLD}${BRIGHT_YELLOW}rot47 command${RESET} - Rot47 Cipher"
# 	"  ${BOLD}${BRIGHT_YELLOW}guessGame command${RESET}- a Guessing Game(To unwind)"
# )

# Each element: name[:alias]
py_scripts=(
	"push" "pull" "pushfile" "pushall" "pullFromMain" "showDiff"
	"showDiffOnMain" "updateToken" "gitignore" "branch" "deleteBranch" "merge"
	"status" "wcount" "logit" "verifyRepo" "showCommitHistory" "printmyEnv"
	"commitdir" "commitall" "getRepoUserName" "stash" "viewStash"
	"requirement_txt" "runserver" "migrate" "showmigrations" "sqlmigrate"
	"clear_commit"
)
bash_scripts=(
	"createRepo:cr" "deleteRepo:dr" "cloneRepo:cl" "viewRepos:vr" "revert2commit"
	"pyxecute" "shxecute" "jsxecute" "restoreFile" "currfol" "cls" "authorID"
	"createPatch" "createReactApp" "createExpoApp" "dependenciesReact"
	"updateReactPackagez" "dependencyDevReact" "py3venv" "startproject" "startapp"
	"djangoUrls" "makemigrations" "django" "djshell" "mkandmigrate" "collectstatic"
	"djangoToolbar" "drf" "djoser" "jwtDjango" "static4django" "mongoOp"
	"mongoVersion" "mysqlOp" "mysqlversion" "mysqlshell" "ctemp:ct" "betty"
	"pycode" "mycompile" "pycompile" "setEnv" "pycodemore" "commitree"
)
c_scripts=(
	"myascii" "rot13" "rot47" "guessGame"
)
personal_commands=(
	"getAccessToken" "xbin" "distributeApk:da" "updateResumeCV"
)

get_description() {
	case "$1" in
		push) echo "stage, commit/updates local/remote repo" ;;
		pull) echo "updates your local branch with changes from the remote" ;;
		pushfile) echo "stage, commit individual files to the local/remote repo" ;;
		pullFromMain) echo "pull latest changes from the main/master branch" ;;
		showDiffOnMain) echo "logs the changes made to the main/master branch" ;;
		pushall) echo "stage, commit and updates the local/remote repos" ;;
		createRepo) echo "creates a github repository right from CLI" ;;
		deleteRepo) echo "deletes a github repository right from CLI" ;;
		cloneRepo) echo "clone a repository with less commands" ;;
		restoreFile) echo "restores file(s) to previous states" ;;
		viewRepos) echo "displays the list of repos from any account on CLI" ;;
		updateToken) echo "adds/updates your repo with a new token" ;;
		gitignore) echo "creates/updates your .gitignore file" ;;
		branch) echo "creates and also switch between branches" ;;
		deleteBranch) echo "deletes branches locally and remotely" ;;
		merge) echo "merge branches to main/master branch" ;;
		status) echo "displays updates in the branch" ;;
		setEnv) echo "sets a permanent environment variable" ;;
		currfol) echo "opens cwd using file explorer" ;;
		pyxecute) echo "appends shebang and makes your python scripts executable" ;;
		shxecute) echo "appends shebang and makes your bash scripts executable" ;;
		jsxecute) echo "appends shebang and makes your js scripts executable" ;;
		pycodemore) echo "(pycode with details)" ;;
		createPatch) echo "creates a .patch file from two files" ;;
		revert2commit) echo "safely reverts changes to an earlier commit state" ;;
		cls) echo "clear your screen" ;;
		authorID) echo "configures your Github Identity(Global and Local)" ;;
		commitree) echo "displays a tree of your commit history" ;;
		showDiff) echo "displays detailed content of updates" ;;
		commitdir) echo "commits all the changes in the current dir" ;;
		commitall) echo "commits all the changes in the working tree" ;;
		getRepoUserName) echo "prints the username of the current repo" ;;
		wcount) echo "counts the lines, words and chars in files" ;;
		stash) echo "saves uncommitted changes in the working tree" ;;
		viewStash) echo "displays a list of applyable stashes" ;;
		logit) echo "displays a detailed commit logs" ;;
		createReactApp) echo "creates a React application, dependencies" ;;
		createExpoApp) echo "creates an Expo mobile application, dependencies" ;;
		dependenciesReact) echo "installs various React packages" ;;
		updateReactPackagez) echo "updates React packages to latest versions" ;;
		dependencyDevReact) echo "installs dev-dependencies" ;;
		py3venv) echo "creates a python3 virtual environment" ;;
		requirement_txt) echo "creates/updates/installs dependencies in requirement.txt" ;;
		collectstatic) echo "collects static files to the staticfiles dir for production" ;;
		djangoToolbar) echo "install and configures Django debug toolbar" ;;
		drf) echo "install and configures Django RESTframework, auth, xml renderer" ;;
		djoser) echo "install and configures djoser (3rd party library)" ;;
		jwtDjango) echo "install and configures json web token in your django project" ;;
		static4django) echo "configures the STATIC_DIRS in settings.py" ;;
		startproject) echo "installs a new django project" ;;
		startapp) echo "installs and configures apps for django projects" ;;
		djangoUrls) echo "used to check and monitor configured urls in django projects" ;;
		runserver) echo "spin up the django development server from any directory" ;;
		makemigrations) echo "performs the makemigrations process" ;;
		migrate) echo "creates the model tables in the database" ;;
		django) echo "displays the django version you are using" ;;
		djshell) echo "launches the django shell" ;;
		mkandmigrate) echo "a combines the makemigrations and migrate commands" ;;
		showmigrations) echo "displays the history of django migrations" ;;
		sqlmigrate) echo "presents the sql query of any migration" ;;
		mongoOp) echo "starts, stops, restarts or checks the status of MongoDB server" ;;
		mongoVersion) echo "checks the version of MongoDB installed" ;;
		mysqlOp) echo "starts, stops, restarts or checks the status of MySQL server" ;;
		mysqlversion) echo "checks if MySQL is installed and also prints its version" ;;
		mysqlshell) echo "launches MySQL shell" ;;
		ctemp) echo "generates a default C source file template" ;;
		clear_commit) echo "restores local repo to the same state as the remote" ;;
		betty) echo "linter command" ;;
		pycode) echo "a \"pycodestyle (PEP 8)\" linter" ;;
		printmyEnv) echo "prints a list of your env paths" ;;
		showCommitHistory) echo "displays a list of all commits made to the repository" ;;
		verifyRepo) echo "checkes if the current dir is a repository or not" ;;
		mycompile) echo "compile C source files (with options)" ;;
		pycompile) echo "compile python files" ;;
		xbin) echo "opens the xbin in file explorer" ;;
		distributeApk) echo "Downloads the apk from eas and updates it to github" ;;
		updateResumeCV) echo "updates my website and github with my resume" ;;
		getAccessToken) echo "fetches the access token locally" ;;
		myascii) echo "prints a simple version of the ASCII table" ;;
		rot13) echo "Rot13 Cipher" ;;
		rot47) echo "Rot47 Cipher" ;;
		guessGame) echo "a Guessing Game(To unwind)" ;;
		*) echo "" ;;
	esac
}

# Combine all scripts into a single array for display
dOptions=()
for script in "${py_scripts[@]}" "${bash_scripts[@]}" "${c_scripts[@]}"; do
	# echo "Processing script: $script..."
	name="${script%%:*}"  # Remove alias if present
	desc="$(get_description "$name")"  # Get description from map

	name="${BOLD}${BRIGHT_YELLOW}${name}${RESET}"
	if [[ -n "$desc" ]]; then
		dOptions+=("  ${name} command - ${desc}")
	else
		dOptions+=("  ${name} command")
	fi
done

# personal scripts for display
personal_scripts=()
for cmd in "${personal_commands[@]}"; do
	# Add personal commands to the bash_scripts array
	pname="${cmd%%:*}"  # Remove alias if present
	pdesc="$(get_description "$pname")"  # Get description from map

	pname="${BOLD}${BRIGHT_MAGENTA}${pname}${RESET}"
	if [[ -n "$desc" ]]; then
		personal_scripts+=("  ${pname} command - ${pdesc}")
	else
		personal_scripts+=("  ${pname} command")
	fi
done

# dOptions=()

# # For Python scripts
# for script in "${py_scripts[@]}"; do
# 	name="${script%%:*}"  # Remove alias if any
# 	dOptions+=("  ${BOLD}${BRIGHT_YELLOW}${name} command${RESET}")
# done

# # For Bash scripts
# for script in "${bash_scripts[@]}"; do
# 	name="${script%%:*}"  # Remove alias if any
# 	dOptions+=("  ${BOLD}${BRIGHT_YELLOW}${name} command${RESET}")
# done

# # For C scripts
# for script in "${c_scripts[@]}"; do
# 	name="${script%%:*}"  # Just in case any alias sneaks in
# 	dOptions+=("  ${BOLD}${BRIGHT_YELLOW}${name} command${RESET}")
# done

category() {
	# reassigns the selection to a different number models (allowing
	# for large number of commands to be added)
	local type="$1"
	local value="$2"
	local btype="$3"
	# echo "value: $value"
	if [[ -n "$value" ]]; then
		# echo "No value provided, exiting category function."
		if [[ "$type" == "p" ]]; then
			# python scripts
			new_value="$(( ($value) + 1000 ))"
		elif [[ "$type" == "b" ]]; then
			# bash scripts
			new_value="$(( ($value) + 2000 ))"
			if [[ "$btype" == "cr" ]]; then
				new_value=11111
			elif [[ "$btype" == "dr" ]]; then
				new_value=22222
			elif [[ "$btype" == "cl" ]]; then
				new_value=33333
			elif [[ "$btype" == "vr" ]]; then
				new_value=55555
			elif [[ "$btype" == "ct" ]]; then
				new_value=44444
			fi
		elif [[ "$type" == "c" ]]; then
			# c scripts
			new_value="$(( ($value) + 3000 ))"
		elif [[ "$type" == "d" ]]; then
			# c scripts
			new_value="$(( ($value) + 4000 ))"
			if [[ "$btype" == "da" ]]; then
				new_value=66666
			fi
		fi
	fi
}
#...................................................... #
#...................................................... #

#...3.................. #
total_py=${#py_scripts[@]}
total_bash=${#bash_scripts[@]}
total_c=${#c_scripts[@]}
total_personal=${#personal_commands[@]}
total_all_scripts=$((total_py + total_bash + total_c + total_personal))

# Combine and process all scripts and their corresponding details for installation
options() {
	index="$converted_selection"
	all_scripts=("${py_scripts[@]}" "${bash_scripts[@]}" "${c_scripts[@]}" "${personal_commands[@]}")
	
	
	# echo "total_py: $total_py, total_bash: $total_bash, total_c: $total_c, total_personal: $total_personal, total: $total_all_scripts"
	# echo "index: $converted_selection"
	# echo "index < total_py (py = $total_py): $((index < total_py))"
	# echo "index < total_py + total_bash (py+bash = $((total_py+total_bash))): $((index < total_py + total_bash))"
	# echo "index < total_py + total_bash + total_c (py+bash+c = $((total_py + total_bash + total_c))): $((index < total_py + total_bash + total_c))"
	# echo "index < total_py + total_bash + total_c + total_personal (py+bash+c+personal = $((total_py + total_bash + total_c + total_personal))): $((index < total_py + total_bash + total_c))"

	# index="$converted_selection"

	# Determine script type
	if (( index < total_py )); then
		# echo "python scripts"
		category_type="p"
		script="${py_scripts[$index]}"
	elif (( index < total_py + total_bash )); then
		# echo "bash scripts"
		category_type="b"
		script="${bash_scripts[$((index - total_py))]}"
	elif (( index < total_py + total_bash + total_c )); then
		# echo "c scripts"
		category_type="c"
		script="${c_scripts[$((index - total_py - total_bash))]}"
	else
		# echo "personal scripts1"
		if [[ "$DAFETITEOGAGA" == "true" ]]; then
			# echo "personal scripts2"
			category_type="d"
			script="${personal_commands[$((index - total_py - total_bash - total_c))]}"
		fi
	fi

	# Extract name and optional alias
	name="${script%%:*}"
	alias="${script#*:}"
	[[ "$name" == "$alias" ]] && alias=""

	DFILENAME="$name"
	category "$category_type" "$index" "$alias"

	# Optional hooks
	# [[ "$DFILENAME" == "distributeApk" || "$DFILENAME" == "updateResumeCV" || "$DFILENAME" == "getAccessToken" ]] && dafetite "$DFILENAME"
	[[ "$DFILENAME" == "currfol" ]] && check_device_type

	#....tags............................. #
	# assign the type of file in based on the new value index
	case "$new_value" in
		2[0-9][0-9][0-9]|11111|22222|33333|44444|55555|66666)
			FILETYPE="bashscript"
			;;
		3[0-9][0-9][0-9])
			FILETYPE="cfile"
			;;
		1[0-9][0-9][0-9])
			FILETYPE="pyscript"
			;;
		4[0-9][0-9][0-9])
			FILETYPE="personal"
			;;
	esac
}

# options() {
# 	# ...py script files.................................... #
# 	# assign file names
# 	case "$converted_selection" in
# 		0)
# 			DFILENAME="push"
# 			category p "$converted_selection"
# 			;;
# 		1)
# 			DFILENAME="pull"
# 			category p "$converted_selection"
# 			;;
# 		2)
# 			DFILENAME="pushfile"
# 			category p "$converted_selection"
# 			;;
# 		3)
# 			DFILENAME="pullFromMain"
# 			category p "$converted_selection"
# 			;;
# 		4)
# 			DFILENAME="showDiffOnMain"
# 			category p "$converted_selection"
# 			;;
# 		5)
# 			DFILENAME="pushall"
# 			category p "$converted_selection"
# 			;;
# 	# ...bash script files................................... #
# 		6)
# 			DFILENAME="createRepo"
# 			category b "$converted_selection" "cr"
# 			;;
# 		7)
# 			DFILENAME="deleteRepo"
# 			category b "$converted_selection" "dr"
# 			;;
# 		8)
# 			DFILENAME="cloneRepo"
# 			category b "$converted_selection" "cl"
# 			;;
# 		9)
# 			DFILENAME="restoreFile"
# 			category b "$converted_selection"
# 			;;
# 		10)
# 			DFILENAME="viewRepos"
# 			category b "$converted_selection" "vr"
# 			;;
# 	# ...py script files..................................... #
# 		11)
# 			DFILENAME="updateToken"
# 			category p "$converted_selection"
# 			;;
# 		12)
# 			DFILENAME="gitignore"
# 			category p "$converted_selection"
# 			;;
# 		13)
# 			DFILENAME="branch"
# 			category p "$converted_selection"
# 			;;
# 		14)
# 			DFILENAME="deleteBranch"
# 			category p "$converted_selection"
# 			;;
# 		15)
# 			DFILENAME="merge"
# 			category p "$converted_selection"
# 			;;
# 		16)
# 			DFILENAME="status"
# 			category p "$converted_selection"
# 			;;
# 	# ...bash script files................................... #
# 		17)
# 			DFILENAME="setEnv"
# 			category b "$converted_selection"
# 			;;
# 		18)
# 			DFILENAME="currfol"
# 			category b "$converted_selection"
# 			check_device_type
# 			;;
# 		19)
# 			DFILENAME="pyxecute"
# 			category b "$converted_selection"
# 			;;
# 		20)
# 			DFILENAME="shxecute"
# 			category b "$converted_selection"
# 			;;
# 		21)
# 			DFILENAME="jsxecute"
# 			category b "$converted_selection"
# 			;;
# 		22)
# 			DFILENAME="pycodemore"
# 			category b "$converted_selection"
# 			;;
# 		23)
# 			DFILENAME="createPatch"
# 			category b "$converted_selection"
# 			;;
# 		24)
# 			DFILENAME="revert2commit"
# 			category b "$converted_selection"
# 			;;
# 		25)
# 			DFILENAME="cls"
# 			category b "$converted_selection"
# 			;;
# 		26)
# 			DFILENAME="authorID"
# 			category b "$converted_selection"
# 			;;
# 		27)
# 			DFILENAME="commitree"
# 			category b "$converted_selection"
# 			;;
# 	# ...py script files..................................... #
# 		28)
# 			DFILENAME="showDiff"
# 			category p "$converted_selection"
# 			;;
# 		29)
# 			DFILENAME="commitdir"
# 			category p "$converted_selection"
# 			;;
# 		30)
# 			DFILENAME="commitall"
# 			category p "$converted_selection"
# 			;;
# 		31)
# 			DFILENAME="getRepoUserName"
# 			category p "$converted_selection"
# 			;;
# 		32)
# 			DFILENAME="wcount"
# 			category p "$converted_selection"
# 			;;
# 		33)
# 			DFILENAME="stash"
# 			category p "$converted_selection"
# 			;;
# 		34)
# 			DFILENAME="viewStash"
# 			category p "$converted_selection"
# 			;;
# 		35)
# 			DFILENAME="logit"
# 			category p "$converted_selection"
# 			;;
# 	# ...bash script files................................... #
# 		36)
# 			DFILENAME="createReactApp"
# 			category b "$converted_selection"
# 			;;
# 		37)
# 			DFILENAME="createExpoApp"
# 			category b "$converted_selection"
# 			;;
# 		38)
# 			DFILENAME="dependenciesReact"
# 			category b "$converted_selection"
# 			;;
# 		39)
# 			DFILENAME="updateReactPackagez"
# 			category b "$converted_selection"
# 			;;
# 		40)
# 			DFILENAME="dependencyDevReact"
# 			category b "$converted_selection"
# 			;;
# 		41)
# 			DFILENAME="py3venv"
# 			category b "$converted_selection"
# 			;;
# 		42)
# 			DFILENAME="requirement_txt"
# 			category p "$converted_selection"
# 			;;
# 		# ...bash script files................................... #
# 		43)
# 			DFILENAME="collectstatic"
# 			category b "$converted_selection"
# 			;;
# 		44)
# 			DFILENAME="djangoToolbar"
# 			category b "$converted_selection"
# 			;;
# 		45)
# 			DFILENAME="drf"
# 			category b "$converted_selection"
# 			;;
# 		46)
# 			DFILENAME="djoser"
# 			category b "$converted_selection"
# 			;;
# 		47)
# 			DFILENAME="jwtDjango"
# 			category b "$converted_selection"
# 			;;
# 		48)
# 			DFILENAME="static4django"
# 			category b "$converted_selection"
# 			;;
# 		49)
# 			DFILENAME="startproject"
# 			category b "$converted_selection"
# 			;;
# 		50)
# 			DFILENAME="startapp"
# 			category b "$converted_selection"
# 			;;
# 		51)
# 			DFILENAME="djangoUrls"
# 			category b "$converted_selection"
# 			;;
# 	# ...py script files..................................... #
# 		52)
# 			DFILENAME="runserver"
# 			category p "$converted_selection"
# 			;;
# 	# ...bash script files................................... #
# 		53)
# 			DFILENAME="makemigrations"
# 			category b "$converted_selection"
# 			;;
# 	# ...py script files..................................... #
# 		54)
# 			DFILENAME="migrate"
# 			category p "$converted_selection"
# 			;;
# 	# ...bash script files................................... #
# 		55)
# 			DFILENAME="django"
# 			category b "$converted_selection"
# 			;;
# 		56)
# 			DFILENAME="djshell"
# 			category b "$converted_selection"
# 			;;
# 		57)
# 			DFILENAME="mkandmigrate"
# 			category b "$converted_selection"
# 			;;
# 	#...py script files..................................... #
# 		58)
# 			DFILENAME="showmigrations"
# 			category p "$converted_selection"
# 			;;
# 		59)
# 			DFILENAME="sqlmigrate"
# 			category p "$converted_selection"
# 			;;
# 	# ...bash script files................................... #
# 		60)
# 			DFILENAME="mongoOp"
# 			category b "$converted_selection"
# 			;;
# 		61)
# 			DFILENAME="mongoVersion"
# 			category b "$converted_selection"
# 			;;
# 		62)
# 			DFILENAME="mysqlOp"
# 			category b "$converted_selection"
# 			;;
# 		63)
# 			DFILENAME="mysqlversion"
# 			category b "$converted_selection"
# 			;;
# 		64)
# 			DFILENAME="mysqlshell"
# 			category b "$converted_selection"
# 			;;
# 		65)
# 			DFILENAME="ctemp"
# 			category b "$converted_selection" "ct"
# 			;;
# 	# ...py script files..................................... #
# 		66)
# 			DFILENAME="clear_commit"
# 			category p "$converted_selection"
# 			;;
# 		67)
# 			DFILENAME="betty"
# 			category b "$converted_selection"
# 			;;
# 		68)
# 			DFILENAME="pycode"
# 			category b "$converted_selection"
# 			;;
# 		69)
# 			DFILENAME="printmyEnv"
# 			category p "$converted_selection"
# 			;;
# 		70)
# 			DFILENAME="showCommitHistory"
# 			category p "$converted_selection"
# 			;;
# 		71)
# 			DFILENAME="verifyRepo"
# 			category p "$converted_selection"
# 			;;
# 	# ...bash script files................................... #
# 		72)
# 			DFILENAME="mycompile"
# 			category b "$converted_selection"
# 			;;
# 		73)
# 			DFILENAME="pycompile"
# 			category b "$converted_selection"
# 			;;
# 		74)
# 			DFILENAME="xbin"
# 			category b "$converted_selection"
# 			;;
# 		75)
# 			DFILENAME="distributeApk"
# 			category b "$converted_selection" "da"
# 			dafetite "$DFILENAME"
# 			;;
# 		# ...py script files..................................... #
# 		76)
# 			DFILENAME="updateResumeCV"
# 			category p "$converted_selection"
# 			dafetite "$DFILENAME"
# 			;;
# 		77)
# 			DFILENAME="myascii"
# 			category c "$converted_selection"
# 			;;
# 		78)
# 			DFILENAME="rot13"
# 			category c "$converted_selection"
# 			;;
# 		79)
# 			DFILENAME="rot47"
# 			category c "$converted_selection"
# 			;;
# 		80)
# 			DFILENAME="guessGame"
# 			category c "$converted_selection"
# 			;;
# 	esac

# 	#....tags............................. #
# 	# checks the type of file in process
# 	case "$new_value" in
# 		[4-6][0-9][0-9]|11111|22222|33333|44444|55555|66666)
# 			FILETYPE="bashscript"
# 			;;
# 		[1-3][0-9][0-9])
# 			FILETYPE="cfile"
# 			;;
# 		[7-9][0-9][0-9])
# 			FILETYPE="pyscript"
# 			;;
# 	esac
# }

#...4.................. #
opertn() {
	#...dir.................. #

	mkdir -p "$XBIN"

	#... command assignment.................. #

	if [[ ${#OPTION} =~ 1 ]]; then

		options

		#...creating variable and profile.................. #
		#...creating bshell variable.................. #
		if [ ! -f "$HOME/.bashrc" ]; then
			touch "$HOME/.bashrc"
			echo ""
			echo "Creating bshell variable..."
		sleep 0.1
		fi

		if ! grep -q "$DBIN" "$HOME/.bashrc"; then
			echo -e "Setting up bshell variable..."
			echo 'export PATH="$PATH:$HOME/'$(basename "$XBIN")'"' >> "$HOME/.bashrc"
		sleep 0.1
		fi

		#...creating zshell variable.................. #
		if [ ! -f "$HOME/.zshrc" ]; then
			touch "$HOME/.zshrc"
			echo ""
			echo "Creating zshell variable..."
		sleep 0.1
		fi

		if ! grep -q "$DBIN" "$HOME/.zshrc"; then
			echo -e "Setting up zshell variable..."
			echo 'export PATH="$PATH:$HOME/'$(basename "$XBIN")'"' >> "$HOME/.zshrc"
		sleep 0.1
		fi

		#...creating Profile.................. #
		if [ ! -f "$HOME/.bash_profile" ]; then
			touch "$HOME/.bash_profile"
			echo ""
			echo "Creating profile..."
		sleep 0.1
		fi

		if ! grep -q  bashrc "$HOME/.bash_profile"; then
			echo -e "Setting up profile..."
			echo '[ -r ~/.bashrc ] && . ~/.bashrc ' >> "$HOME/.bash_profile"
		sleep 0.1
		fi

		echo ""
		echo -e "Creating $DFILENAME command..."

		# echo -e "\nint_option: $int_option"
		# echo "converted_selection: $converted_selection"
		# echo "new_value: $new_value"
		# echo "DFILENAME: $DFILENAME"
		# echo "OPTION: $OPTION"
		# echo "FILETYPE: $FILETYPE"
		# echo "total_all_scripts: $total_all_scripts"
		# echo "total_personal: $total_personal"
		# echo "DAFETITEOGAGA: $DAFETITEOGAGA"
		# exit 0

		# copies the command code into .xbin/ and based on the
		# new value index, copies the command script accordingly
		case "$new_value" in
			11111|22222|33333|55555|66666)
				# special commands (requires username/token/email)
				unametokenmaill
				;;
			44444)
				# special command (exclusively to ctemp command)
				mkdir -p "$XBIN/pyfiles"
				echo -e "custom commands" >  "$XBIN/C_template.c"
				cp "$SCPTS/C_template.c" "$XBIN/C_template.c"
				main_copy_command_script_fxn
				;;
			[1-9][0-9][0-9][0-9])
				# all other scripts (1000 - 9000 index)
				main_copy_command_script_fxn
				;;
		esac
	fi
	echo ""
}

update_setup_scripts_in_pyfiles() {
	# updates only installed files in pyfiles/
    mkdir -p "$XBIN/pyfiles"

    for file in "$SCPTS/pyfiles/"*; do
        # if [[ -f "$file" ]]; then
		filename=$(basename "$file")
		destination="$XBIN/pyfiles/$filename"
		# echo "filename: $filename"
		if [[ -f "$destination" ]]; then
			cp "$file" "$destination"
		elif [[ -d "$destination" && "$filename" != "__pycache__" ]]; then
			cp -r "$file" "$XBIN/pyfiles/"
			if is_git_bash; then
				for file in "$XBIN/pyfiles/"*; do
					# Skip unwanted directories
					[[ "$(basename "$file")" == "__pycache__" || "$(basename "$file")" == "expoDefaults" ]] && continue

					# Only process files
					if [[ -f "$file" ]]; then
						# echo "Processing: $file"
						converPyShebang4gitbash "$file"
					fi
				done
			fi
		else
			if [[ "$filename" != "__pycache__" ]]; then
				# echo "no no no"
				echo "custom commands" > "$destination"
				cp "$file" "$destination"
			# else
			# 	echo "skipping ..."
			fi
		fi
		if [[ -f "$destination" ]]; then
			chmod +x "$destination"
		fi
		if is_git_bash && [ ! -d "$destination" ]; then
			converPyShebang4gitbash "$destination"
		fi
    done
	update_changes
}

update_changes() {
	# updates any command that has already been installed
	affected_files="$(ls "$PWD/$SCPTS")"
    for file in $affected_files; do
		file="$XBIN/$file"
        if [[ -f "$file" ]]; then
            filename=$(basename "$file")
            source="$SCPTS/$filename"
			destination="$XBIN/$filename"

			# Extract auth info in files that has one BEFORE overwriting
			if grep -q "IGITHUBUSERNAME=" "$destination"; then
				# echo "destination: $destination"
				# echo "found tokenKey in $(basename $destination)"
				keyUNAME="$(grep "IGITHUBUSERNAME=" "$destination")"
				keyUTOKEN="$(grep "IGITHUBACCESSTOKEN=" "$destination")"
				keyUEMAIL="$(grep "IGITHUBEMAIL=" "$destination")"
				tokenKey="1"
				# echo "keyUNAME: $keyUNAME"
				# echo "keyUTOKEN: $keyUTOKEN"
				# echo "keyUEMAIL: $keyUEMAIL"
			fi
			# echo "tokenkey: $tokenKey"

			# Copy the file
			cp "$source" "$destination"

			# Reinsert the tokenKey into the file after copy
			if [[ -n "$tokenKey" ]]; then
				sed -i "s|^IGITHUBUSERNAME=.*|$keyUNAME|" "$destination"
				sed -i "s|^IGITHUBACCESSTOKEN=.*|$keyUTOKEN|" "$destination"
				sed -i "s|^IGITHUBEMAIL=.*|$keyUEMAIL|" "$destination"
				# echo "Reinserted tokenKey into $(basename $destination)"
				tokenKey=""
			fi

			if is_git_bash; then
				converPyShebang4gitbash "$destination"
			fi
        fi
    done
	# find "$XBIN" -maxdepth 1 -name "sed*" -type f -delete
}

#...5.................. #
main_copy_command_script_fxn() {
	# copies pymanage and configure_settings_py to .xbin
	if [[ ! -f "$XBIN/pymanage" || ! -f "$XBIN/configure_settings_py.py" ]]; then
		# echo "start making xbin dir ..."
		mkdir -p "$XBIN/pyfiles"
		cp "$SCPTS/pymanage" "$XBIN/pymanage"
		cp "$SCPTS/pyfiles/configure_settings_py.py" "$XBIN/pyfiles/configure_settings_py.py"
		cp "$SCPTS/pyfiles/check_db.py" "$XBIN/pyfiles/check_db.py"
		# check_db.py
		if is_git_bash; then
			converPyShebang4gitbash "$XBIN/pymanage"
			converPyShebang4gitbash "$XBIN/pyfiles/configure_settings_py.py"
			converPyShebang4gitbash "$XBIN/pyfiles/check_db.py"
		fi
		# echo "end making xbin dir ..."
	fi
	if [[ ! -d "$XBIN/pyfiles/expoDefaults" && "$DFILENAME"=="createExpoApp" ]]; then
		mkdir -p "$XBIN/pyfiles/expoDefaults"
		cp -r "$SCPTS/pyfiles/expoDefaults" "$XBIN/pyfiles/"
	fi
	update_setup_scripts_in_pyfiles
	sleep 0.1
	# for betty command installation
	if [[ "$DFILENAME" == "betty" ]]; then
		install_betty_linter_command

	# for pyscripts/pycodemore/pycode command installation
	elif [[ "$DFILENAME" == "pycode" || "$DFILENAME" == "pycodemore" || "$FILETYPE" == "pyscript" || "$FILETYPE" == "personal" ]]; then
		copy_cmd_scripts_based_on_filetypes

		if [[ "$DFILENAME" == "pycode" || "$DFILENAME" == "pycodemore" ]]; then
			if [[ "$WHICH" =~ [c] ]]; then
				# installation for pc
				sudo apt install pycodestyle
			elif [[ "$WHICH" =~ [p] ]]; then
				# installation for phone
				pip install pycodestyle
			fi
		fi
	else
		# for other commands
		copy_cmd_scripts_based_on_filetypes
	fi

	#...creating custom_commands to view all commands.................. #
	echo "custom commands" > "$XBIN/custom_commands"
	cp "$SCPTS/custom_commands" "$XBIN/custom_commands"
	chmod +x "$XBIN/custom_commands"
}

#...5a.................. #
# creates/install betty linter (pc/phone)
install_betty_linter_command() {
	echo -e ""
	mkdir -p tempo
	cd tempo

	git clone https://github.com/alx-tools/Betty.git

	if [[ "$WHICH" =~ [p] ]]; then
		echo -e ""
		git clone https://github.com/DafetiteOgaga/betty_wrapper.git
		cp betty_wrapper/phone-betty.sh betty_wrapper/phone-install.sh Betty
		echo -e ""
		cd Betty

		./phone-install.sh

	elif [[ "$WHICH" =~ [c] ]]; then
		echo -e ""
		cd Betty
		sudo ./install.sh
	fi

	rm -rf ../../tempo
	cd ../../
}

#...6.................. #
# instructn() {
# 	# instructions
# 	echo -e "Now, RESTART YOUR TERMINAL or START A NEW SESSION."
# 	sleep 0.1
# 	case "$DFILENAME" in
# 		"betty")
# 			echo -e "$STRT check your source files. $ANYWHERE: $DFILENAME <filename(s)>"
# 			;;
# 		"pycode")
# 			echo -e "$STRT check your python files. $ANYWHERE: $DFILENAME <filename(s)>"
# 			;;
# 		"push")
# 			echo -e "$STRT push(sync) to github. $ANYWHERE: $DFILENAME"
# 			;;
# 		"pull")
# 			echo -e "$STRT pull from github. $ANYWHERE: $DFILENAME"
# 			;;
# 		"createRepo")
# 			echo -e "$STRT create a github repo right from your terminal. $ANYWHERE: $DFILENAME"
# 			;;
# 		"deleteRepo")
# 			echo -e "$STRT delete a github repo right from your terminal. $ANYWHERE: $DFILENAME"
# 			;;
# 		"cloneRepo")
# 			echo -e "$STRT clone repos from github. $ANYWHERE: $DFILENAME"
# 			;;
# 		"viewRepos")
# 			echo -e "$STRT view the public repos of any github account. $ANYWHERE: $DFILENAME"
# 			;;
# 		"mycompile")
# 			echo -e "$STRT compile your files $EFFT $ANYWHERE: $DFILENAME <filename>"
# 			;;
# 		"ctemp")
# 			echo -e "$STRT create default C source file templates $EFFT $ANYWHERE: $DFILENAME <filename>"
# 			;;
# 		"getAccessToken")
# 			echo -e "$STRT fetch your access token $EFFT $ANYWHERE: $DFILENAME <filename>"
# 			;;
# 		"cls")
# 			echo -e "$STRT clear your screen $EFFT $ANYWHERE: $DFILENAME"
# 			;;
# 		"authorID")
# 			echo -e "$STRT configure your GitHub identity both globally and locally within your environment $EFFT $ANYWHERE: $DFILENAME"
# 			;;
# 		"pycodemore")
# 			echo -e "$STRT check your python file with line details $EFFT $ANYWHERE: $DFILENAME <filename(s)>"
# 			;;
# 		"pycompile")
# 			echo -e "$STRT compile your python scripts to a .pyc $EFFT $ANYWHERE: $DFILENAME <filename(s)>"
# 			;;
# 		"currfol")
# 			echo -e "$STRT open your current working directory $EFFT $ANYWHERE: $DFILENAME"
# 			;;
# 	# ............................................................ #
# 		"guessGane")
# 			echo -e "$STRT play guessing game $EFFT $ANYWHERE: $DFILENAME"
# 			;;
# 		"rot13")
# 			echo -e "$STRT encode and decode your texts with Rot13 $EFFT $ANYWHERE: $DFILENAME"
# 			;;
# 		"rot47")
# 			echo -e "$STRT encode and decode your texts with Rot47 $EFFT $ANYWHERE: $DFILENAME"
# 			;;
# 		"myascii")
# 			echo -e "$STRT check the ASCII table $EFFT $ANYWHERE: $DFILENAME"
# 			;;
# 	# ............................................................ #
# 		"wcount")
# 			echo -e "$STRT check the number of lines, words and characters in your file $EFFT $ANYWHERE: $DFILENAME <filename(s)>"
# 			;;
# 		"clear_commit")
# 			echo -e "$STRT unstage your files, clear commit messages on your local machine(provided, you are yet to push to remote). Revert to the same state as your remote $EFFT $ANYWHERE: $DFILENAME"
# 			;;
# 		"pushfile")
# 			echo -e "$STRT stage and commit individual files before pushing them all to remote $EFFT $ANYWHERE: $DFILENAME OR $DFILENAME <filename(s)>"
# 			;;
# 		"pullFromMain")
# 			echo -e "$STRT pull latest changes from main/master branch $EFFT $ANYWHERE: $DFILENAME"
# 			;;
# 		"showDiffOnMain")
# 			echo -e "$STRT log latest changes from main/master branch as compared to the current branch $EFFT $ANYWHERE: $DFILENAME"
# 			;;
# 	# ............................................................ #
# 		"pushall")
# 			echo -e "$STRT stage and commit all files in the working tree before pushing them all to remote $EFFT $ANYWHERE: $DFILENAME"
# 			;;
# 		"branch")
# 			echo -e "$STRT create and switch branches $EFFT $ANYWHERE:"
# 			echo -e "$DFILENAME <filename(s)> - to create an new branch"
# 			echo -e "$DFILENAME - to switch branches"
# 			;;
# 		"merge")
# 			echo -e "$STRT easily merge changesin a branch to main/master branch $EFFT $ANYWHERE: $DFILENAME"
# 			;;
# 		"status")
# 			echo -e "$STRT view tracked and untracked file(s) in the working tree $EFFT $ANYWHERE: $DFILENAME"
# 			;;
# 		"pyxecute"|"shxecute"|"jsxecute")
# 			echo -e "$STRT adds shebang and turn your file(s) to executable file(s) $EFFT $ANYWHERE: $DFILENAME <filename(s)>"
# 			;;
# 		"createPatch")
# 			echo -e "$STRT patch files $EFFT $ANYWHERE: $DFILENAME <main file> <updated file>"
# 			;;
# 		"revert2commit")
# 			echo -e "$STRT revert to a previous commit instance $EFFT $ANYWHERE: $DFILENAME"
# 			;;
# 		"commitree")
# 			echo -e "$STRT view a graphical commit history $EFFT $ANYWHERE: $DFILENAME"
# 			;;
# 		"showDiff")
# 			echo -e "$STRT view uncommitted changes in the working tree compared to the repository $EFFT $ANYWHERE: $DFILENAME"
# 			;;
# 		"commitdir")
# 			echo -e "$STRT commit changes in the current directory to the repository $EFFT $ANYWHERE: $DFILENAME"
# 			;;
# 		"commitall")
# 			echo -e "$STRT commit changes in the working directory to the repository $EFFT $ANYWHERE: $DFILENAME"
# 			;;
# 		"stash")
# 			echo -e "$STRT stash (save changes) in the current branch $EFFT $ANYWHERE: $DFILENAME"
# 			;;
# 		"viewStash")
# 			echo -e "$STRT view and apply stash to the current branch $EFFT $ANYWHERE: $DFILENAME"
# 			;;
# 		"logit")
# 			echo -e "$STRT view the detailed log history of your commits $EFFT $ANYWHERE: $DFILENAME"
# 			;;
# 		"printmyEnv")
# 			echo -e "$STRT view a list of your env paths $EFFT $ANYWHERE: $DFILENAME"
# 			;;
# 		"showCommitHistory")
# 			echo -e "$STRT view your commit history $EFFT $ANYWHERE: $DFILENAME"
# 			;;
# 		"verifyRepo")
# 			echo -e "$STRT verify that you are in a repository $EFFT $ANYWHERE: $DFILENAME"
# 			;;
# 		"startproject")
# 			echo -e "$STRT start/create a django project $EFFT $ANYWHERE: $DFILENAME <project name>"
# 			echo -e "Note: You must either have django installed on your machine or in a virtual environment"
# 			;;
# 		"startapp")
# 			echo -e "$STRT create django app(s) $EFFT $ANYWHERE: $DFILENAME <app name(s)"
# 			;;
# 		"runserver")
# 			echo -e "$STRT spin up your django server $EFFT $ANYWHERE: $DFILENAME"
# 			echo -e "Note: You can also pass a port number argument to the command, if you wish to spin it with a different port number"
# 			echo -e "I.e $DFILENAME <port number>"
# 			;;
# 		"makemigrations")
# 			echo -e "$STRT make/create django migration scripts that will be used to create tables in your database $EFFT $ANYWHERE: $DFILENAME"
# 			echo -e "Note: You can also pass specific app name(s) as argument for streamlined operations"
# 			echo -e "I.e $DFILENAME <app name(s)>"
# 			;;
# 		"migrate")
# 			echo -e "$STRT migrate your model setups to create tables in your database $EFFT $ANYWHERE: $DFILENAME"
# 			echo -e "Note: You can equally pass any string as argument to select options to migrate to"
# 			echo -e "I.e $DFILENAME <string>"
# 			;;
# 		"django")
# 			echo -e "$STRT can verify that you have django installed via its version $EFFT $ANYWHERE: $DFILENAME"
# 			;;
# 		"djshell")
# 			echo -e "$STRT enter into the django shell for further processing. $ANYWHERE: $DFILENAME"
# 			;;
# 		"mkandmigrate")
# 			echo -e "$STRT can perform the makemigrations and migrate operations with just a command. $ANYWHERE: $DFILENAME"
# 			;;
# 		"showmigrations")
# 			echo -e "$STRT display and observe the history of your migration operations $EFFT $ANYWHERE: $DFILENAME"
# 			echo -e "Note: You can also pass any string as argument for streamlined operation"
# 			echo -e "I.e $DFILENAME <string>"
# 			;;
# 		"sqlmigrate")
# 			echo -e "$STRT check the sql query of your model table $EFFT $ANYWHERE: $DFILENAME <app name> <migration filename>"
# 			;;
# 		"py3venv")
# 			echo -e "$STRT create python3 venvs $EFFT $ANYWHERE: $DFILENAME"
# 			;;
# 		"requirement_txt")
# 			echo -e "$STRT create, update or install the dependencies in the requirements.txt file $EFFT $ANYWHERE: $DFILENAME"
# 			;;
# 		"gitignore")
# 			echo -e "$STRT create or update the .gitignore file by navigating through your repository $EFFT $ANYWHERE: $DFILENAME"
# 			;;
# 		"mongoOp")
# 			echo -e "$STRT start, stop, restart and check the status of mongodb $EFFT $ANYWHERE: $DFILENAME"
# 			;;
# 		"mongoVersion")
# 			echo -e "$STRT start, stop, restart and check the status of mongodb $EFFT $ANYWHERE: $DFILENAME"
# 			;;
# 		"mysqlOp")
# 			echo -e "$STRT start, stop, restart and check the status of mysql DB $EFFT $ANYWHERE: $DFILENAME"
# 			;;
# 		"mysqlversion")
# 			echo -e "$STRT check if you have MySQL installed on your machine and prints its version $EFFT $ANYWHERE: $DFILENAME"
# 			;;
# 		"mysqlshell")
# 			echo -e "$STRT launch MySQL shell $EFFT $ANYWHERE: $DFILENAME"
# 			;;
# 		"drf")
# 			echo -e "$STRT install and configure django RESTframework and its authentication token functionality $EFFT $ANYWHERE: $DFILENAME"
# 			;;
# 		"djoser")
# 			echo -e "$STRT install and configure djoser and use it with drf authentication token $EFFT $ANYWHERE: $DFILENAME"
# 			;;
# 		"jwtDjango")
# 			echo -e "$STRT install and configure jwt in your django project $EFFT $ANYWHERE: $DFILENAME"
# 			;;
# 		"static4django")
# 			echo -e "$STRT configure the STATIC_DIRS in the setting.py $EFFT $ANYWHERE: $DFILENAME"
# 			;;
# 		"djangoToolbar")
# 			echo -e "$STRT install and configure django debug toolbars in setting.py urls.py $EFFT $ANYWHERE: $DFILENAME"
# 			;;
# 		"restoreFile")
# 			echo -e "$STRT restore your file(s) to previous states $EFFT $ANYWHERE: $DFILENAME <filename(s)>"
# 			;;
# 		"getRepoUserName")
# 			echo -e "$STRT printn the username of any repo $EFFT $ANYWHERE: $DFILENAME"
# 			;;
# 		"createReactApp")
# 			echo -e "$STRT create a React app $EFFT $ANYWHERE: $DFILENAME <filename>"
# 			;;
# 		"createExpoApp")
# 			echo -e "$STRT create an Expo Mobile app $EFFT $ANYWHERE: $DFILENAME <filename>"
# 			;;
# 		"dependenciesReact")
# 			echo -e "$STRT installs various dependencies $EFFT $ANYWHERE: $DFILENAME"
# 			;;
# 		"dependencyDevReact")
# 			echo -e "$STRT installs the specified dependency $EFFT $ANYWHERE: $DFILENAME"
# 			;;
# 		"updateReactPackagez")
# 			echo -e "$STRT updates all packages that has new releases $EFFT $ANYWHERE: $DFILENAME"
# 			;;
# 		"updateToken")
# 			echo -e "$STRT add/update your local credentials with a new token $EFFT $ANYWHERE: $DFILENAME"
# 			;;
# 		"deleteBranch")
# 			echo -e "$STRT delete branches locally and it's corresponding remote branch $EFFT $ANYWHERE: $DFILENAME"
# 			;;
# 		"xbin")
# 			echo -e "$STRT the .xbin directory in file explorer $EFFT $ANYWHERE: $DFILENAME"
# 			;;
# 		"updateResumeCV")
# 			echo -e "$STRT updates my website and github with my CV and Resume located in my google drive $EFFT $ANYWHERE: $DFILENAME"
# 			;;
# 		"djangoUrls")
# 			echo -e "$STRT start checking and monitoring all the configured urls in your django projects $EFFT $ANYWHERE: $DFILENAME"
# 			;;
# 		"setEnv")
# 			echo -e "$STRT set a permanent environmental variable $EFFT $ANYWHERE: $DFILENAME"
# 			;;
# 		"collectstatic")
# 			echo -e "$STRT collect static files into staticfiles dir for production $EFFT $ANYWHERE: $DFILENAME"
# 			;;
# 		"distributeApk")
# 			echo -e "$STRT download your apk file from eas (expo) and upload to github release for distribution $EFFT $ANYWHERE: $DFILENAME"
# 			;;
# 		esac
# 	sleep 0.1
# }
instructn() {
	# instructions
	echo -e "Now, RESTART YOUR TERMINAL or START A NEW SESSION."
	sleep 0.1

	msg=""
	case "$DFILENAME" in
		betty) msg="$STRT check your source files. $ANYWHERE: $DFILENAME <filename(s)>";;
		pycode) msg="$STRT check your python files. $ANYWHERE: $DFILENAME <filename(s)>";;
		push) msg="$STRT push(sync) to github. $ANYWHERE: $DFILENAME";;
		pull) msg="$STRT pull from github. $ANYWHERE: $DFILENAME";;
		createRepo) msg="$STRT create a github repo right from your terminal. $ANYWHERE: $DFILENAME";;
		deleteRepo) msg="$STRT delete a github repo right from your terminal. $ANYWHERE: $DFILENAME";;
		cloneRepo) msg="$STRT clone repos from github. $ANYWHERE: $DFILENAME";;
		viewRepos) msg="$STRT view the public repos of any github account. $ANYWHERE: $DFILENAME";;
		mycompile) msg="$STRT compile your files $EFFT $ANYWHERE: $DFILENAME <filename>";;
		ctemp) msg="$STRT create default C source file templates $EFFT $ANYWHERE: $DFILENAME <filename>";;
		getAccessToken) msg="$STRT fetch your access token $EFFT $ANYWHERE: $DFILENAME <filename>";;
		cls) msg="$STRT clear your screen $EFFT $ANYWHERE: $DFILENAME";;
		authorID) msg="$STRT configure your GitHub identity globally/locally $EFFT $ANYWHERE: $DFILENAME";;
		pycodemore) msg="$STRT check your python file with line details $EFFT $ANYWHERE: $DFILENAME <filename(s)>";;
		pycompile) msg="$STRT compile your python scripts to .pyc $EFFT $ANYWHERE: $DFILENAME <filename(s)>";;
		currfol) msg="$STRT open your current working directory $EFFT $ANYWHERE: $DFILENAME";;
		guessGane) msg="$STRT play guessing game $EFFT $ANYWHERE: $DFILENAME";;
		rot13) msg="$STRT encode/decode text with Rot13 $EFFT $ANYWHERE: $DFILENAME";;
		rot47) msg="$STRT encode/decode text with Rot47 $EFFT $ANYWHERE: $DFILENAME";;
		myascii) msg="$STRT check ASCII table $EFFT $ANYWHERE: $DFILENAME";;
		wcount)
			echo -e "$STRT count lines, words, characters $EFFT $ANYWHERE:"
			echo -e "$DFILENAME <filenames(s)> - to inspect selected files in a directory"
			echo -e "$DFILENAME * - to inspect all files (individually) in a directory"
			sleep 0.1
			return
			;;
		clear_commit) msg="$STRT unstage files and revert to remote state $EFFT $ANYWHERE: $DFILENAME";;
		pushfile)
			echo -e "$STRT commit individual files $EFFT $ANYWHERE:"
			echo -e "$DFILENAME <filenames(s)> - to push selected files in a directory"
			echo -e "$DFILENAME * - to push all changes (individually) in a directory"
			echo -e "$DFILENAME - to push all changes (individually) in the repository (irrespective of where they are)"
			sleep 0.1
			return
			;;
		pullFromMain) msg="$STRT pull changes from main/master $EFFT $ANYWHERE: $DFILENAME";;
		showDiffOnMain) msg="$STRT show diff vs main/master $EFFT $ANYWHERE: $DFILENAME";;
		pushall) msg="$STRT commit all and push $EFFT $ANYWHERE: $DFILENAME";;
		branch)
			echo -e "$STRT create/switch branches $EFFT $ANYWHERE:"
			echo -e "$DFILENAME <branch_name> - to create new"
			echo -e "$DFILENAME - to switch"
			sleep 0.1
			return
			;;
		merge) msg="$STRT merge a branch to main/master $EFFT $ANYWHERE: $DFILENAME";;
		status) msg="$STRT show working tree status $EFFT $ANYWHERE: $DFILENAME";;
		pyxecute|shxecute|jsxecute) msg="$STRT add shebang and make file(s) executable $EFFT $ANYWHERE: $DFILENAME <filename(s)>";;
		createPatch) msg="$STRT create patch file $EFFT $ANYWHERE: $DFILENAME <main> <updated>";;
		revert2commit) msg="$STRT revert to a previous commit $EFFT $ANYWHERE: $DFILENAME";;
		commitree) msg="$STRT show graphical commit log $EFFT $ANYWHERE: $DFILENAME";;
		showDiff) msg="$STRT view uncommitted diff $EFFT $ANYWHERE: $DFILENAME";;
		commitdir) msg="$STRT commit changes in this dir $EFFT $ANYWHERE: $DFILENAME";;
		commitall) msg="$STRT commit changes in all working tree $EFFT $ANYWHERE: $DFILENAME";;
		stash) msg="$STRT stash current changes $EFFT $ANYWHERE: $DFILENAME";;
		viewStash) msg="$STRT view/apply saved stash $EFFT $ANYWHERE: $DFILENAME";;
		logit) msg="$STRT view commit logs $EFFT $ANYWHERE: $DFILENAME";;
		printmyEnv) msg="$STRT view environment paths $EFFT $ANYWHERE: $DFILENAME";;
		showCommitHistory) msg="$STRT show commit history $EFFT $ANYWHERE: $DFILENAME";;
		verifyRepo) msg="$STRT verify this is a git repository $EFFT $ANYWHERE: $DFILENAME";;
		startproject)
			echo -e "$STRT create Django project $EFFT $ANYWHERE: $DFILENAME <project>"
			echo -e "Note: Requires Django installed"
			sleep 0.1
			return
			;;
		startapp) msg="$STRT create Django app(s) $EFFT $ANYWHERE: $DFILENAME <app name(s)>";;
		runserver)
			echo -e "$STRT run Django server $EFFT $ANYWHERE: $DFILENAME"
			echo -e "You can pass port number too: $DFILENAME <port>"
			sleep 0.1
			return
			;;
		makemigrations)
			echo -e "$STRT make Django migrations $EFFT $ANYWHERE: $DFILENAME"
			echo -e "Optional: pass app name(s)"
			sleep 0.1
			return
			;;
		migrate)
			echo -e "$STRT apply Django migrations $EFFT $ANYWHERE: $DFILENAME"
			echo -e "Optional: pass migration name"
			sleep 0.1
			return
			;;
		django) msg="$STRT check Django version $EFFT $ANYWHERE: $DFILENAME";;
		djshell) msg="$STRT enter Django shell $EFFT $ANYWHERE: $DFILENAME";;
		mkandmigrate) msg="$STRT run makemigrations & migrate $EFFT $ANYWHERE: $DFILENAME";;
		showmigrations)
			echo -e "$STRT view migration history $EFFT $ANYWHERE: $DFILENAME"
			echo -e "Optional: pass migration label"
			sleep 0.1
			return
			;;
		sqlmigrate) msg="$STRT view SQL of migration $EFFT $ANYWHERE: $DFILENAME <app> <migration>";;
		py3venv) msg="$STRT create Python venv $EFFT $ANYWHERE: $DFILENAME";;
		requirement_txt) msg="$STRT manage requirements.txt $EFFT $ANYWHERE: $DFILENAME";;
		gitignore) msg="$STRT update .gitignore file $EFFT $ANYWHERE: $DFILENAME";;
		mongoOp) msg="$STRT start/stop/restart MongoDB $EFFT $ANYWHERE: $DFILENAME";;
		mongoVersion) msg="$STRT check MongoDB version $EFFT $ANYWHERE: $DFILENAME";;
		mysqlOp) msg="$STRT start/stop/restart MySQL $EFFT $ANYWHERE: $DFILENAME";;
		mysqlversion) msg="$STRT check MySQL version $EFFT $ANYWHERE: $DFILENAME";;
		mysqlshell) msg="$STRT open MySQL shell $EFFT $ANYWHERE: $DFILENAME";;
		drf) msg="$STRT install Django REST Framework $EFFT $ANYWHERE: $DFILENAME";;
		djoser) msg="$STRT setup djoser $EFFT $ANYWHERE: $DFILENAME";;
		jwtDjango) msg="$STRT configure JWT in Django $EFFT $ANYWHERE: $DFILENAME";;
		static4django) msg="$STRT configure STATICFILES in settings.py $EFFT $ANYWHERE: $DFILENAME";;
		djangoToolbar) msg="$STRT setup Django Debug Toolbar $EFFT $ANYWHERE: $DFILENAME";;
		restoreFile) msg="$STRT restore file(s) to earlier state $EFFT $ANYWHERE: $DFILENAME <filename(s)>";;
		getRepoUserName) msg="$STRT print GitHub repo username $EFFT $ANYWHERE: $DFILENAME";;
		createReactApp) msg="$STRT create React app $EFFT $ANYWHERE: $DFILENAME <project_name>";;
		createExpoApp) msg="$STRT create Expo app $EFFT $ANYWHERE: $DFILENAME <project_name>";;
		dependenciesReact) msg="$STRT install React dependencies $EFFT $ANYWHERE: $DFILENAME";;
		dependencyDevReact) msg="$STRT install React dev dependencies $EFFT $ANYWHERE: $DFILENAME";;
		updateReactPackagez) msg="$STRT update all React packages $EFFT $ANYWHERE: $DFILENAME";;
		updateToken) msg="$STRT update GitHub token $EFFT $ANYWHERE: $DFILENAME";;
		deleteBranch) msg="$STRT delete local + remote branches $EFFT $ANYWHERE: $DFILENAME";;
		xbin) msg="$STRT open .xbin in file explorer $EFFT $ANYWHERE: $DFILENAME";;
		updateResumeCV) msg="$STRT upload latest CV from Drive to GitHub $EFFT $ANYWHERE: $DFILENAME";;
		djangoUrls) msg="$STRT check all Django urls $EFFT $ANYWHERE: $DFILENAME";;
		setEnv) msg="$STRT set a permanent env variable $EFFT $ANYWHERE: $DFILENAME";;
		collectstatic) msg="$STRT collect static files for prod $EFFT $ANYWHERE: $DFILENAME";;
		distributeApk) msg="$STRT download apk and release to GitHub $EFFT $ANYWHERE: $DFILENAME";;
	esac

	if [[ -n "$msg" ]]; then
		echo -e "$msg"
	fi

	sleep 0.1
}


#...Entry point.................. #

# this sets/keeps the line endings consistent across different platforms
git config --global core.autocrlf input

# this sets/resets the tracker setup every 24 hours
if [[ -f "$UPDATEPATH" ]];
	then
		# updates the tracker setup
		bash "$UPDATEPATH"
else
	# creates the tracker setup
	mkdir -p "$XBIN"
	echo "custom commands" > "$XBIN/check4Update"
	cp "$SCPTS/pyfiles/check4Update" "$XBIN/check4Update"
	chmod +x "$XBIN/check4Update"
fi

launch=(
    "However, please go on and select your type of device:"
    "[p] - Phone"
    "[c] - PC"
    "[q] - quit"
	""
)

CHECKERPCPH=$(echo "$XBIN" | cut -d '/' -f 2)
echo ""
config_type="OS:"
if is_wsl || is_macos || is_linux || is_git_bash; then
	if is_wsl;
		then
			echo -e "$config_type Windows (WSL - Windows subsystem for linux)."
	elif is_macos;
		then
			echo -e "$config_type macOs."
	elif is_linux;
		then
			echo -e "$config_type linux."
	elif is_git_bash;
		then
			echo -e "$config_type Windows (Git bash)."
	fi
	WHICH="c"
elif [[ "$CHECKERPCPH" == "data" ]]; then
	# echo -e "p"
	WHICH="p"
else
	while true; do
		clear
		intro "0"
		for i in "${launch[@]}"; do
			echo -e "$i"
			sleep 0.05
		done
		read -n 1 -s -r -p "Is this a phone or a pc? [P/C/Q] >>> " WHICH
		if [[ "$WHICH" =~ [pPcC] ]]; then
			break
		elif [[ "$WHICH" =~ [qQ] ]]; then
			echo -e "Ok."
			exit 0
		fi
	done
fi
check_for_python # checks if python is installed

#...options display.................. #
count=0
default_option='0'
personal_scripts_added=false
total_items=${#dOptions[@]}
while [[ "$UINPUT" != [nN] ]]; do
    page=1
    items_per_page=10
	# echo -e "\nmain loop"
	# echo -e "\nint_option: $int_option"
	# echo "converted_selection: $converted_selection"
	# echo "new_value: $new_value"
	# echo "DFILENAME: $DFILENAME"
	# echo "OPTION: $OPTION"
	# echo "total_all_scripts: $total_all_scripts"
	# echo "total_personal: $total_personal"
	# echo "DAFETITEOGAGA: $DAFETITEOGAGA"
	# echo "total_items: $total_items"
	# echo "value: $value"
	if [[ "$DAFETITEOGAGA" == "true" && "$personal_scripts_added" == "false" ]]; then
		personal_scripts_added=true  # Set flag so it only happens once
	elif [[ "$converted_selection" -ge "$total_items" ]]; then
			converted_selection=""
			OPTION="z"
	fi
	total_pages=$(( (total_items + items_per_page - 1) / items_per_page ))
	# echo "total_pages: $total_pages"

    while true; do
		if [[ "$count" -eq 0 ]]; then
			echo "Pls wait..."
		fi
		sleep 0.1
		# echo -e "\nclearing ..."
        clear
		# echo "DAFETITEOGAGA: $DAFETITEOGAGA"
		# echo "personal_scripts_added: $personal_scripts_added"
		# if [[ "$DAFETITEOGAGA" == "true" && "$personal_scripts_added" == "false" ]]; then
		# 	echo "Adding personal scripts..."
		# 	dOptions+=("${personal_scripts[@]}")
		# 	# dOptions+=()
		# 	personal_scripts_added=true  # Set flag so it only happens once
		# fi
        auth "$WHICH"
        intro "0"
        echo ""

		echo "Page $page of $total_pages:"

        start=$((($page - 1) * $items_per_page))
        end=$(($page * $items_per_page))

        current_option="$default_option"

        for ((i = $start; i < $end && i < ${#dOptions[@]}; i++)); do
            echo -e "${current_option} - ${dOptions[$i]#??}"
            sleep 0.02
            ((current_option++))
        done

        echo ""
        echo -e "For more options$ADMIN"
        if (( $page > 1 )); then
            echo "[p] - Previous Page"
        fi

        if (( $end < ${#dOptions[@]} )); then
            echo "[n] - Next Page"
        fi
        echo "[q] - Quit"

		# echo -e "\nint_option: $int_option"
		# echo "converted_selection: $converted_selection"
		# echo "new_value: $new_value"
		# echo "DFILENAME: $DFILENAME"
		# echo "OPTION: $OPTION"
		# echo "total_all_scripts: $total_all_scripts"
		# echo "total_personal: $total_personal"
		# echo "DAFETITEOGAGA: $DAFETITEOGAGA"
        if [[ "$count" -gt 0 ]]; then
			# echo "count: $count"
            if [[ "$OPTION" != [nNpPzZxX] ]]; then
				# echo "OPTION: $OPTION"
                opertn
                instructn
            fi
            echo -e ""
            echo -e "Last command created: ${UNDERLINE}${ITALIC}${BOLD}${BRIGHT_GREEN}$DFILENAME${RESET}"
            sleep 0.1
            echo -e ""
			invalid_selection
            echo -n "Select another option? [q] - quit >>> "
        else
            echo ""
			invalid_selection
            echo -n "What do you want to do? [q] - quit >>> "
			((count++))
        fi

        read -n 1 -s -r OPTION
		if [[ "$OPTION" =~ [nNpPqQXx] ]]; then
			converted_selection="$OPTION"
		elif [[ "$OPTION" =~ [a-mor-wyzA-MOR-WYZ] ]]; then
			OPTION="z"
			continue
		else
			int_option=$((OPTION))
			if [[ $int_option > $((items_per_page - 1)) ]]; then
				OPTION="z"
				continue
			else
				converted_selection="$(( ($page - 1) * $items_per_page + $int_option ))"
			fi
		fi
        case "$converted_selection" in
            n|N)
                if (( $end < ${#dOptions[@]} )); then
                    ((page++))
                fi
                ;;
			x|X)
				check_dafetite
                ;;
            p|P)
                if (( $page > 1 )); then
                    ((page--))
                fi
                ;;
            [0-9]|[1-9][0-9]|[1-9][0-9][0-9])
                echo -n "$OPTION"
                break
                ;;
            q|Q)
				echo -e "Ok."
				echo ""
				echo -e "Cheers!"
                exit 0
                ;;
        esac
    done
    ((count++))
done
# #........ finish .......................... #
echo -e "\ncompleted."
