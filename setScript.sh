#!/bin/bash

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


quit() {
	# exit
	local var="$1"
	if [[ "$var" == "q" || "$var" == "Q" ]]; then
	echo ""
		echo "Operation aborted."
		exit 0
	fi
}

check_device_type() {
	if [[ "$device_type" == "phone" ]]; then
		echo -e "\nThis command can only be installed on a PC"
		echo "COMMAND NOT INSTALLED"
		quit "q"
	fi
}

dafetite() {
	local commandName="$1"
	echo ""
	read -n 8 -s -r -p "Enter passcode: " dafetite
	echo ""
	if [[ "$dafetite" != "dafetite" ]]; then
		echo -e "\nOopsy! You are not allowed to install this command, sorry."
		echo "$commandName command NOT installed"
		quit "q"
	fi
}

auth() {
	# initiates sudo authentication
	local var="$WHICH"

	if [[ ${#var} == 1 ]]; then
		if [[ "$var" =~ [cC] ]]; then
			rep="PC"
			sudo -E echo -e "\nHi $USER 😊 ..."
		elif [[ "$var" =~ [pP] ]]; then
			rep="Phone"
			echo -e "\nHi USER 😊 ..."
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
		if [[ "$whch" =~ "0" ]]; then
			echo -e "I can see that this is a PC"
		else
			echo -e "$rep"
		fi
	elif [[ "$CHECKER_PC_PH" == "data" ]]; then
		device_type="phone"
		if [[ "$whch" =~ "0" ]]; then
			echo -e "I can see that this is a Phone"
		else
			echo -e "$rep"
		fi
	else
		if [[ "$whch" =~ "0" ]]; then
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
	local var1="$1"
	local var2="$2"

	sed -i "s/$var1/$var2/g" "$XBIN/$DFILENAME"
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
	# collects user details to createRepo, cloneRepo, deleteRepo and viewRepo commands
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
		echo -e "$NUM2"
		if [[ $NUM2 -ne 36 && $NUM2 -ne 40 ]]; then
			echo -e ""
			echo -e "TOKEN: $NTOKEN which you supplied is not a classic token."
			echo -e "Make sure to remove \"ghp_\" and that there is no whitespace."
			echo ""
		fi
		if [[ $NUM2 -eq 40 && "$NTOKEN" == *"ghp_"* ]]; then
			NTOKEN="${NTOKEN#ghp_}"
			break
		elif [[ $NUM2 -eq 36 ]]; then
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
	# populates the user details to createRepo, cloneRepo, deleteRepo and viewRepo commands
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

	echo ""
	if [[ "$ANS" =~ [yY] ]]; then
		scptcpy
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

cpfunc() {
	# identifies device type and cpoies appropriate code for command creation
	echo "custom commands" > "$XBIN/$DFILENAME"
	case "$FILETYPE" in
		"bashscript"|"pyscript")
			# copies the content
			cp "$SCPTS/$DFILENAME" "$XBIN/$DFILENAME"
			;;
		"cfile")
			# copies the content
			if [[ "$WHICH" =~ 'p' ]]; then
				cp "$SCPTS/phone/$DFILENAME" "$XBIN/$DFILENAME"
			elif [[ "$WHICH" =~ 'c' ]]; then
				cp "$SCPTS/pc/$DFILENAME" "$XBIN/$DFILENAME"
			fi
		;;
	# fi
	esac
	# make the script executable
	chmod +x $XBIN/$DFILENAME
}

#...options display.................. #
#...2.................. #

dOptions=(
	# options display
	#...py script files....................... #
	"  push command - stage, commit/updates local/remote repo"
	"  pull command - updates your local branch with changes from the remote"
	"  pushfile command - stage, commit individual files to the local/remote repo"
	"  pushall command - stage, commit and updates the local/remote repos"
	#...bash script files.................. #
	"  createRepo command - creates a github repository right from CLI"
	"  deleteRepo command - deletes a github repository right from CLI"
	"  cloneRepo command - clone a repository with less commands"

	"  restoreFile command - restores file(s) to previous states"

	"  viewRepos command - displays the list of repos from any account on CLI"
	#...py script files....................... #

	"  updateToken command - adds/updates your repo with a new token"

	"  gitignore command - creates/updates your .gitignore file"
	"  branch command - creates and also switch between branches"
	"  merge command - merge branches to main/master branch"
	"  status command - displays updates in the branch"
	#...bash script files.................. #
	"  setEnv command - sets a permanent environment variable"

	"  curfol command - opens cwd using file explorer"
	"  pyxecute - appends shebang and makes your python scripts executable"
	"  shxecute - appends shebang and makes your bash scripts executable"

	"  jsxecute - appends shebang and makes your js scripts executable"

	"  pycodemore command(pycode with details)"
	"  createPatch command - creates a .patch file from two files"
	"  rollback command - reverts the current branch to an earlier commit"
	"  cls command - clear your screen"
	"  authorID - configures your Github Identity(Global and Local)"
	"  commitree command - displays a tree of your commit history"
	#...py script files....................... #
	"  compareChange command - displays detailed content of updates"
	"  commitdir command - commits all the changes in the current dir"
	"  commitall command - commits all the changes in the working tree"

	"  getRepoUserName command - prints the username of the current repo"

	"  wcount command - counts the lines, words and chars in files"
	"  stash command - saves uncommitted changes in the working tree"
	"  viewStash command - displays a list of applyable stashes"
	"  logit command - displays a detailed commit logs"
	
	#...bash script files.................. #
	"  createReactApp command - creates a React application, dependencies"
	"  createExpoApp command - creates an Expo mobile application, dependencies"
	"  dependenciesReact command - installs various React packages"
	"  updateReactPackagez command - updates React packages to latest versions"
	"  dependencyDevReact command - installs dev-dependencies"

	"  py3venv command - creates a python3 virtual environment"
	#...py script files....................... #
	"  requirement_txt command - creates/updates/installs dependencies in requirement.txt"
	#...bash script files.................. #

	"  collectstatic command - collects static files to the staticfiles dir for production"

	"  djangoToolbar command - install and configures Django debug toolbar"
	"  drf command - install and configures Django RESTframework, auth, xml renderer"
	"  djoser command - install and configures djoser (3rd party library)"
	"  jwtDjango command - install and configures json web token in your django project"
	"  static4django command - configures the STATIC_DIRS in settings.py"

	"  startproject command - installs a new django project"
	"  startapp command - installs and configures apps for django projects"
	"  djangoUrls command - used to check and monitor configured urls in django projects"

	#...py script files....................... #
	"  runserver command - spin up the django development server from any directory"
	#...bash script files.................. #
	"  makemigrations command - performs the makemigrations process"
	#...py script files....................... #
	"  migrate command - creates the model tables in the database"
	#...bash script files.................. #
	"  django command - displays the django version you are using"
	"  djshell command - launches the django shell"
	"  mkandmigrate command - a combines the makemigrations and migrate commands"
	#...py script files....................... #
	"  showmigrations command - displays the history of django migrations"
	"  sqlmigrate command - presents the sql query of any migration"
	#...bash script files.................. #
	"  mysqlversion - checks if MySQL is installed and also prints its version"
	"  mysqlstartserver - starts MySQL server"
	"  mysqlstopserver - stops MySQL server"
	"  mysqlrestartserver - restarts MySQL server"
	"  mysqlstatus_server - displays the status of MySQL server"
	"  mysqlshell - launches MySQL shell"
	"  ctemp - generates a default C source file template"
	
	"  clear_commit command - restores local repo to the same state as the remote"
	"  betty linter command"
	"  pycode command a \"pycodestyle (PEP 8)\" linter"
	#...py script files....................... #
	"  printmyEnv command - prints a list of your env paths"
	"  show command - displays a list of all commits made to the repository"
	"  verifyRepo command - checkes if the current dir is a repository or not"
	#...bash script files.................. #
	"  mycompile command - compile C source files (with options)"
	"  pycompile command - compile python files"
	"  xbin command - opens the xbin in file explorer"
	"  updateResumeCV command - updates my website and github with my resume"
	#...C files....................... #
	"  myascii command - prints a simple version of the ASCII table"
	"  rot13 command - Rot13 Cipher"
	"  rot47 command - Rot47 Cipher"
	"  guessGame command- a Guessing Game(To unwind)"
)

category() {
	# reassigns the selection to a different number
	local type="$1"
	local value="$2"
	local btype="$3"
	if [[ "$type" == "p" ]]; then
		# python scripts
		new_value="$(( ($value) + 700 ))"
	elif [[ "$type" == "b" ]]; then
		# bash scripts
		new_value="$(( ($value) + 400 ))"
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
		new_value="$(( ($value) + 100 ))"
	fi
}
#...................................................... #
#...................................................... #

#...3.................. #
options() {
	# ...py script files.................................... #
	# assign file names
	case "$converted_selection" in
		0)
			DFILENAME="push"
			category p "$converted_selection"
			;;
		1)
			DFILENAME="pull"
			category p "$converted_selection"
			;;
		2)
			DFILENAME="pushfile"
			category p "$converted_selection"
			;;
		3)
			DFILENAME="pushall"
			category p "$converted_selection"
			;;
	
	# ...bash script files................................... #
		4)
			DFILENAME="createRepo"
			category b "$converted_selection" "cr"
			;;
		5)
			DFILENAME="deleteRepo"
			category b "$converted_selection" "dr"
			;;
		6)
			DFILENAME="cloneRepo"
			category b "$converted_selection" "cl"
			;;
		7)
			DFILENAME="restoreFile"
			category b "$converted_selection"
			;;
		8)
			DFILENAME="viewRepos"
			category b "$converted_selection" "vr"
			;;
		
	# ...py script files..................................... #
		9)
			DFILENAME="updateToken"
			category p "$converted_selection"
			;;
		10)
			DFILENAME="gitignore"
			category p "$converted_selection"
			;;
		11)
			DFILENAME="branch"
			category p "$converted_selection"
			;;
		12)
			DFILENAME="merge"
			category p "$converted_selection"
			;;
		13)
			DFILENAME="status"
			category p "$converted_selection"
			;;

	# ...bash script files................................... #
		14)
			DFILENAME="setEnv"
			category b "$converted_selection"
			;;
		15)
			DFILENAME="curfol"
			category b "$converted_selection"
			check_device_type
			;;
		16)
			DFILENAME="pyxecute"
			category b "$converted_selection"
			;;
		17)
			DFILENAME="shxecute"
			category b "$converted_selection"
			;;
		18)
			DFILENAME="jsxecute"
			category b "$converted_selection"
			;;
		19)
			DFILENAME="pycodemore"
			category b "$converted_selection"
			;;
		20)
			DFILENAME="createPatch"
			category b "$converted_selection"
			;;
		21)
			DFILENAME="rollback"
			category b "$converted_selection"
			;;
		22)
			DFILENAME="cls"
			category b "$converted_selection"
			;;
		23)
			DFILENAME="authorID"
			category b "$converted_selection"
			;;
		24)
			DFILENAME="commitree"
			category b "$converted_selection"
			;;
	
	# ...py script files..................................... #
		25)
			DFILENAME="compareChange"
			category p "$converted_selection"
			;;
		26)
			DFILENAME="commitdir"
			category p "$converted_selection"
			;;
		27)
			DFILENAME="commitall"
			category p "$converted_selection"
			;;
		28)
			DFILENAME="getRepoUserName"
			category p "$converted_selection"
			;;
		29)
			DFILENAME="wcount"
			category p "$converted_selection"
			;;
		30)
			DFILENAME="stash"
			category p "$converted_selection"
			;;
		31)
			DFILENAME="viewStash"
			category p "$converted_selection"
			;;
		32)
			DFILENAME="logit"
			category p "$converted_selection"
			;;
	
	# ...bash script files................................... #
		33)
			DFILENAME="createReactApp"
			category b "$converted_selection"
			;;
		34)
			DFILENAME="createExpoApp"
			category b "$converted_selection"
			;;
		35)
			DFILENAME="dependenciesReact"
			category b "$converted_selection"
			;;
		36)
			DFILENAME="updateReactPackagez"
			category b "$converted_selection"
			;;
		37)
			DFILENAME="dependencyDevReact"
			category b "$converted_selection"
			;;
		38)
			DFILENAME="py3venv"
			category b "$converted_selection"
			;;

		39)
			DFILENAME="requirement_txt"
			category p "$converted_selection"
			;;
		
		# ...bash script files................................... #
		40)
			DFILENAME="collectstatic"
			category b "$converted_selection"
			;;
		41)
			DFILENAME="djangoToolbar"
			category b "$converted_selection"
			;;
		42)
			DFILENAME="drf"
			category b "$converted_selection"
			;;
		43)
			DFILENAME="djoser"
			category b "$converted_selection"
			;;
		44)
			DFILENAME="jwtDjango"
			category b "$converted_selection"
			;;
		45)
			DFILENAME="static4django"
			category b "$converted_selection"
			;;

		46)
			DFILENAME="startproject"
			category b "$converted_selection"
			;;
		47)
			DFILENAME="startapp"
			category b "$converted_selection"
			;;
		48)
			DFILENAME="djangoUrls"
			category b "$converted_selection"
			;;
	
	# ...py script files..................................... #
		49)
			DFILENAME="runserver"
			category p "$converted_selection"
			;;

	# ...bash script files................................... #
		50)
			DFILENAME="makemigrations"
			category b "$converted_selection"
			;;
	
	# ...py script files..................................... #
		51)
			DFILENAME="migrate"
			category p "$converted_selection"
			;;
	
	# ...bash script files................................... #
		52)
			DFILENAME="django"
			category b "$converted_selection"
			;;
		53)
			DFILENAME="djshell"
			category b "$converted_selection"
			;;
		54)
			DFILENAME="mkandmigrate"
			category b "$converted_selection"
			;;

	#...py script files..................................... #
		55)
			DFILENAME="showmigrations"
			category p "$converted_selection"
			;;
		56)
			DFILENAME="sqlmigrate"
			category p "$converted_selection"
			;;

	# ...bash script files................................... #
		57)
			DFILENAME="mysqlversion"
			category b "$converted_selection"
			;;
		58)
			DFILENAME="mysqlstartserver"
			category b "$converted_selection"
			;;
		59)
			DFILENAME="mysqlstopserver"
			category b "$converted_selection"
			;;
		60)
			DFILENAME="mysqlrestartserver"
			category b "$converted_selection"
			;;
		61)
			DFILENAME="mysqlstatus_server"
			category b "$converted_selection"
			;;
		62)
			DFILENAME="mysqlshell"
			category b "$converted_selection"
			;;
		63)
			DFILENAME="ctemp"
			category b "$converted_selection" "ct"
			;;
	
	# ...py script files..................................... #
		64)
			DFILENAME="clear_commit"
			category p "$converted_selection"
			;;
		65)
			DFILENAME="betty"
			category b "$converted_selection"
			;;
		66)
			DFILENAME="pycode"
			category b "$converted_selection"
			;;

		67)
			DFILENAME="printmyEnv"
			category p "$converted_selection"
			;;
		68)
			DFILENAME="show"
			category p "$converted_selection"
			;;
		69)
			DFILENAME="verifyRepo"
			category p "$converted_selection"
			;;
	
	# ...bash script files................................... #
		70)
			DFILENAME="mycompile"
			category b "$converted_selection"
			;;
		71)
			DFILENAME="pycompile"
			category b "$converted_selection"
			;;
		72)
			DFILENAME="xbin"
			category b "$converted_selection"
			;;
		
		# ...py script files..................................... #
		73)
			DFILENAME="updateResumeCV"
			category p "$converted_selection"
			dafetite "$DFILENAME"
			;;
		74)
			DFILENAME="myascii"
			category c "$converted_selection"
			;;
		75)
			DFILENAME="rot13"
			category c "$converted_selection"
			;;
		76)
			DFILENAME="rot47"
			category c "$converted_selection"
			;;
		77)
			DFILENAME="guessGame"
			category c "$converted_selection"
			;;
	esac

	#....tags............................. #
	# checks the type of file in process
	case "$new_value" in
		[4-6][0-9][0-9]|11111|22222|33333|44444|55555)
			FILETYPE="bashscript"
			;;
		[1-3][0-9][0-9])
			FILETYPE="cfile"
			;;
		[7-9][0-9][0-9])
			FILETYPE="pyscript"
			;;
	esac
}

#...4.................. #
opertn() {
	#...dir.................. #

	mkdir -p $XBIN

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
		echo -e "Creating $DFILENAME as a command..."
		# copies the command code into .xbin/
		case "$new_value" in
			11111|22222|33333|55555)
				unametokenmaill
				;;
			44444)
				echo -e "custom commands" >  $XBIN/C_template.c
				cp "$SCPTS/C_template.c" "$XBIN/C_template.c"
				scptcpy
				;;
			[1-9][0-9][0-9])
				scptcpy
				;;
		esac
	fi
	echo ""
}

pyfiles() {
	# echo "Updating pyfiles..."
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
		else
			if [[ "$filename" != "__pycache__" ]]; then
				echo "no no no"
				echo "custom commands" > "$destination"
				cp "$file" "$destination"
			# else
			# 	echo "skipping ..."
			fi
		fi
		if [[ -f "$destination" ]]; then
			chmod +x $destination
		fi
    done
	update_changes
}

update_changes() {
	# updates any command that has already been installed
	affected_files="$(ls $PWD/$SCPTS)"
    for file in $affected_files; do
		file="$XBIN/$file"
        if [[ -f "$file" ]]; then
            filename=$(basename "$file")
            source="$SCPTS/$filename"
			destination="$XBIN/$filename"
			cp "$source" "$destination"
        fi
    done
}

#...5.................. #
scptcpy() {
	# copies pymanage and configure_settings_py to .xbin
	if [[ ! -f "$XBIN/pymanage" || ! -f "$XBIN/configure_settings_py.py" ]]; then
		cp "$SCPTS/pymanage" "$XBIN/pymanage"
		cp "$SCPTS/pyfiles/configure_settings_py.py" "$XBIN/pyfiles/configure_settings_py.py"
		cp "$SCPTS/pyfiles/check_db.py" "$XBIN/pyfiles/check_db.py"
		# check_db.py
	fi
	if [[ ! -d "$XBIN/pyfiles/expoDefaults" && "$DFILENAME"=~"createExpoApp" ]]; then
		mkdir -p "$XBIN/pyfiles/expoDefaults"
		cp -r "$SCPTS/pyfiles/expoDefaults" "$XBIN/pyfiles/"
	fi
	pyfiles
	sleep 0.1
	# for betty command installation
	if [[ $DFILENAME =~ "betty" ]]; then
		bLinter

	# for pyscripts/pycodemore/pycode command installation
	elif [[ $DFILENAME =~ "pycode" || $DFILENAME =~ "pycodemore" || $FILETYPE =~ "pyscript" ]]; then
		cpfunc
		# Check if Python3 is installed
		if command -v python3 &> /dev/null; then
			echo "..."
			sleep 0.1
		else
			# Attempt to install Python3
			echo "Installing Python3..."
			sleep 0.1
			# other package managers command
			
			if [[ "$WHICH" =~ 'p' ]]; then
				# for phone
				pkg update
				pkg install python
			elif [[ "$WHICH" =~ 'c' ]]; then
				# for pc
				sudo apt-get update
				sudo apt-get install -y python3
			fi
		fi

		if [[ $DFILENAME =~ "pycode" || $DFILENAME =~ "pycodemore" ]]; then
			if [[ "$WHICH" =~ 'c' ]]; then
				# installation for pc
				sudo apt install pycodestyle
			elif [[ "$WHICH" =~ 'p' ]]; then
				# installation for phone
				pip install pycodestyle
			fi
		fi
	else
		# for other commands
		cpfunc
	fi

	#...creating custom_commands to view all commands.................. #
	echo "custom commands" > "$XBIN/custom_commands"
	cp "$SCPTS/custom_commands" "$XBIN/custom_commands"
	chmod +x "$XBIN/custom_commands"
}

#...5a.................. #
bLinter() {
	# creates/install betty linter
	echo -e ""
	mkdir -p tempo
	cd tempo

	git clone https://github.com/alx-tools/Betty.git

	if [[ "$WHICH" =~ 'p' ]]; then
		echo -e ""
		git clone https://github.com/DafetiteOgaga/betty_wrapper.git
		cp betty_wrapper/phone-betty.sh betty_wrapper/phone-install.sh Betty
		echo -e ""
		cd Betty

		./phone-install.sh

	elif [[ "$WHICH" =~ 'c' ]]; then
		echo -e ""
		cd Betty
		sudo ./install.sh
	fi

	rm -rf ../../tempo
	cd ../../
}

#...6.................. #
instructn() {
	# instructions
	echo -e "Now, RESTART YOUR TERMINAL or START A NEW SESSION."
	sleep 0.1
	case "$DFILENAME" in
		"betty")
			echo -e "$STRT check your source files. $ANYWHERE: $DFILENAME <filename(s)>"
			;;
		"pycode")
			echo -e "$STRT check your python files. $ANYWHERE: $DFILENAME <filename(s)>"
			;;
		"push")
			echo -e "$STRT push(sync) to github. $ANYWHERE: $DFILENAME"
			;;
		"pull")
			echo -e "$STRT pull from github. $ANYWHERE: $DFILENAME"
			;;
		"createRepo")
			echo -e "$STRT create a github repo right from your terminal. $ANYWHERE: $DFILENAME"
			;;
		"deleteRepo")
			echo -e "$STRT delete a github repo right from your terminal. $ANYWHERE: $DFILENAME"
			;;
		"cloneRepo")
			echo -e "$STRT clone repos from github. $ANYWHERE: $DFILENAME"
			;;
		"viewRepos")
			echo -e "$STRT view the public repos of any github account. $ANYWHERE: $DFILENAME"
			;;
		"mycompile")
			echo -e "$STRT compile your files $EFFT $ANYWHERE: $DFILENAME <filename>"
			;;
		"ctemp")
			echo -e "$STRT create default C source file templates $EFFT $ANYWHERE: $DFILENAME <filename>"
			;;
		"cls")
			echo -e "$STRT clear your screen $EFFT $ANYWHERE: $DFILENAME"
			;;
		"authorID")
			echo -e "$STRT configure your GitHub identity both globally and locally within your environment $EFFT $ANYWHERE: $DFILENAME"
			;;
		"pycodemore")
			echo -e "$STRT check your python file with line details $EFFT $ANYWHERE: $DFILENAME <filename(s)>"
			;;
		"pycompile")
			echo -e "$STRT compile your python scripts to a .pyc $EFFT $ANYWHERE: $DFILENAME <filename(s)>"
			;;
		"curfol")
			echo -e "$STRT open your current working directory $EFFT $ANYWHERE: $DFILENAME"
			;;
	# ............................................................ #
		"guessGane")
			echo -e "$STRT play guessing game $EFFT $ANYWHERE: $DFILENAME"
			;;
		"rot13")
			echo -e "$STRT encode and decode your texts with Rot13 $EFFT $ANYWHERE: $DFILENAME"
			;;
		"rot47")
			echo -e "$STRT encode and decode your texts with Rot47 $EFFT $ANYWHERE: $DFILENAME"
			;;
		"myascii")
			echo -e "$STRT check the ASCII table $EFFT $ANYWHERE: $DFILENAME"
			;;
	# ............................................................ #
		"wcount")
			echo -e "$STRT check the number of lines, words and characters in your file $EFFT $ANYWHERE: $DFILENAME <filename(s)>"
			;;
		"clear_commit")
			echo -e "$STRT unstage your files, clear commit messages on your local machine(provided, you are yet to push to remote). Revert to the same state as your remote $EFFT $ANYWHERE: $DFILENAME"
			;;
		"pushfile")
			echo -e "$STRT stage and commit individual files before pushing them all to remote $EFFT $ANYWHERE: $DFILENAME <filename(s)>"
			;;
	# ............................................................ #
		"pushall")
			echo -e "$STRT stage and commit all files in the working tree before pushing them all to remote $EFFT $ANYWHERE: $DFILENAME"
			;;
		"branch")
			echo -e "$STRT create and switch branches $EFFT $ANYWHERE:"
			echo -e "$DFILENAME <filename(s)> - to create an new branch"
			echo -e "$DFILENAME - to switch branches"
			;;
		"merge")
			echo -e "$STRT easily merge changesin a branch to main/master branch $EFFT $ANYWHERE: $DFILENAME"
			;;
		"status")
			echo -e "$STRT view tracked and untracked file(s) in the working tree $EFFT $ANYWHERE: $DFILENAME"
			;;
		"pyxecute"|"shxecute"|"jsxecute")
			echo -e "$STRT adds shebang and turn your file(s) to executable file(s) $EFFT $ANYWHERE: $DFILENAME <filename(s)>"
			;;
		"createPatch")
			echo -e "$STRT patch files $EFFT $ANYWHERE: $DFILENAME <main file> <updated file>"
			;;
		"rollback")
			echo -e "$STRT revert to a previous commit instance $EFFT $ANYWHERE: $DFILENAME"
			;;
		"commitree")
			echo -e "$STRT view a graphical commit history $EFFT $ANYWHERE: $DFILENAME"
			;;
		"compareChange")
			echo -e "$STRT view uncommitted changes in the working tree compared to the repository $EFFT $ANYWHERE: $DFILENAME"
			;;
		"commitdir")
			echo -e "$STRT commit changes in the current directory to the repository $EFFT $ANYWHERE: $DFILENAME"
			;;
		"commitall")
			echo -e "$STRT commit changes in the working directory to the repository $EFFT $ANYWHERE: $DFILENAME"
			;;
		"stash")
			echo -e "$STRT stash (save changes) in the current branch $EFFT $ANYWHERE: $DFILENAME"
			;;
		"viewStash")
			echo -e "$STRT view and apply stash to the current branch $EFFT $ANYWHERE: $DFILENAME"
			;;
		"logit")
			echo -e "$STRT view the detailed log history of your commits $EFFT $ANYWHERE: $DFILENAME"
			;;
		"printmyEnv")
			echo -e "$STRT view a list of your env paths $EFFT $ANYWHERE: $DFILENAME"
			;;
		"show")
			echo -e "$STRT view your commit history $EFFT $ANYWHERE: $DFILENAME"
			;;
		"verifyRepo")
			echo -e "$STRT verify that you are in a repository $EFFT $ANYWHERE: $DFILENAME"
			;;

		"startproject")
			echo -e "$STRT start/create a django project $EFFT $ANYWHERE: $DFILENAME <project name>"
			echo -e "Note: You must either have django installed on your machine or in a virtual environment"
			;;
		"startapp")
			echo -e "$STRT create django app(s) $EFFT $ANYWHERE: $DFILENAME <app name(s)"
			;;
		"runserver")
			echo -e "$STRT spin up your django server $EFFT $ANYWHERE: $DFILENAME"
			echo -e "Note: You can also pass a port number argument to the command, if you wish to spin it with a different port number"
			echo -e "I.e $DFILENAME <port number>"
			;;
		"makemigrations")
			echo -e "$STRT make/create django migration scripts that will be used to create tables in your database $EFFT $ANYWHERE: $DFILENAME"
			echo -e "Note: You can also pass specific app name(s) as argument for streamlined operations"
			echo -e "I.e $DFILENAME <app name(s)>"
			;;
		"migrate")
			echo -e "$STRT migrate your model setups to create tables in your database $EFFT $ANYWHERE: $DFILENAME"
			echo -e "Note: You can equally pass any string as argument to select options to migrate to"
			echo -e "I.e $DFILENAME <string>"
			;;
		"django")
			echo -e "$STRT can verify that you have django installed via its version $EFFT $ANYWHERE: $DFILENAME"
			;;
		"djshell")
			echo -e "$STRT enter into the django shell for further processing. $ANYWHERE: $DFILENAME"
			;;
		"mkandmigrate")
			echo -e "$STRT can perform the makemigrations and migrate operations with just a command. $ANYWHERE: $DFILENAME"
			;;
		"showmigrations")
			echo -e "$STRT display and observe the history of your migration operations $EFFT $ANYWHERE: $DFILENAME"
			echo -e "Note: You can also pass any string as argument for streamlined operation"
			echo -e "I.e $DFILENAME <string>"
			;;
		"sqlmigrate")
			echo -e "$STRT check the sql query of your model table $EFFT $ANYWHERE: $DFILENAME <app name> <migration filename>"
			;;
		"py3venv")
			echo -e "$STRT create python3 venvs $EFFT $ANYWHERE: $DFILENAME"
			;;
		"requirement_txt")
			echo -e "$STRT create, update or install the dependencies in the requirements.txt file $EFFT $ANYWHERE: $DFILENAME"
			;;
		"gitignore")
			echo -e "$STRT create or update the .gitignore file by navigating through your repository $EFFT $ANYWHERE: $DFILENAME"
			;;
	
		"mysqlversion")
			echo -e "$STRT check if you have MySQL installed on your machine and prints its version $EFFT $ANYWHERE: $DFILENAME"
			;;
		"mysqlstartserver")
			echo -e "$STRT spin up MySQL server $EFFT $ANYWHERE: $DFILENAME"
			;;
		"mysqlstopserver")
			echo -e "$STRT stop MySQL server $EFFT $ANYWHERE: $DFILENAME"
			;;
		"mysqlrestartserver")
			echo -e "$STRT restart MySQL server $EFFT $ANYWHERE: $DFILENAME"
			;;
		"mysqlstatus_server")
			echo -e "$STRT check the status of MySQL server $EFFT $ANYWHERE: $DFILENAME"
			;;
		"mysqlshell")
			echo -e "$STRT launch MySQL shell $EFFT $ANYWHERE: $DFILENAME"
			;;
		"drf")
			echo -e "$STRT install and configure django RESTframework and its authentication token functionality $EFFT $ANYWHERE: $DFILENAME"
			;;
		"djoser")
			echo -e "$STRT install and configure djoser and use it with drf authentication token $EFFT $ANYWHERE: $DFILENAME"
			;;
		"jwtDjango")
			echo -e "$STRT install and configure jwt in your django project $EFFT $ANYWHERE: $DFILENAME"
			;;
		"static4django")
			echo -e "$STRT configure the STATIC_DIRS in the setting.py $EFFT $ANYWHERE: $DFILENAME"
			;;
		"djangoToolbar")
			echo -e "$STRT install and configure django debug toolbars in setting.py urls.py $EFFT $ANYWHERE: $DFILENAME"
			;;
		"restoreFile")
			echo -e "$STRT restore your file(s) to previous states $EFFT $ANYWHERE: $DFILENAME <filename(s)>"
			;;
		"getRepoUserName")
			echo -e "$STRT printn the username of any repo $EFFT $ANYWHERE: $DFILENAME"
			;;
		"createReactApp")
			echo -e "$STRT create a React app $EFFT $ANYWHERE: $DFILENAME <filename>"
			;;
		"createExpoApp")
			echo -e "$STRT create an Expo Mobile app $EFFT $ANYWHERE: $DFILENAME <filename>"
			;;
		"dependenciesReact")
			echo -e "$STRT installs various dependencies $EFFT $ANYWHERE: $DFILENAME"
			;;
		"dependencyDevReact")
			echo -e "$STRT installs the specified dependency $EFFT $ANYWHERE: $DFILENAME"
			;;
		"updateReactPackagez")
			echo -e "$STRT updates all packages that has new releases $EFFT $ANYWHERE: $DFILENAME"
			;;
		"updateToken")
			echo -e "$STRT add/update your local credentials with a new token $EFFT $ANYWHERE: $DFILENAME"
			;;
		"xbin")
			echo -e "$STRT the .xbin directory in file explorer $EFFT $ANYWHERE: $DFILENAME"
			;;
		"updateResumeCV")
			echo -e "$STRT updates my website and github with my CV and Resume located in my google drive $EFFT $ANYWHERE: $DFILENAME"
			;;
		"djangoUrls")
			echo -e "$STRT start checking and monitoring all the configured urls in your django projects $EFFT $ANYWHERE: $DFILENAME"
			;;
		"setEnv")
			echo -e "$STRT set a permanent environmental variable $EFFT $ANYWHERE: $DFILENAME"
			;;
		"collectstatic")
			echo -e "$STRT collect static files into staticfiles dir for production $EFFT $ANYWHERE: $DFILENAME"
			;;
		esac
	sleep 0.1
}


#........ start .......................... #

#........ intro .......................... #


launch=(
    "However, please go on and select your type of device:"
    "[p] - Phone"
    "[c] - PC"
    "[q] - quit"
	""
)
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

#...main operation.................. #
#...Entry point.................. #

#...options display.................. #

# #...1.................. #

count=0
default_option='0'  
while [[ "$UINPUT" != [nN] ]]; do
    page=1
    items_per_page=10

    while true; do
        clear
        auth $WHICH
        intro "1"
        echo ""
        echo "Page $page:"

        start=$((($page - 1) * $items_per_page))
        end=$(($page * $items_per_page))

        current_option=$default_option

        for ((i = $start; i < $end && i < ${#dOptions[@]}; i++)); do
            echo -e "${current_option} - ${dOptions[$i]#??}"
            sleep 0.02
            ((current_option++))
        done

        echo ""
        echo -e "For more options"
        if (( $page > 1 )); then
            echo "[p] - Previous Page"
        fi

        if (( $end < ${#dOptions[@]} )); then
            echo "[n] - Next Page"
        fi

        echo "[q] - Quit"

        if [[ $count -gt 0 ]]; then
            if [[ "$OPTION" != [nNpPzZ] ]]; then
                opertn
                instructn
            fi
            echo -e ""
            echo -e "Last command created: $DFILENAME"
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
		if [[ "$OPTION" =~ [nNpPqQ] ]]; then
			converted_selection="$OPTION"
		elif [[ "$OPTION" =~ [a-mor-zA-MOR-Z] ]]; then
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
