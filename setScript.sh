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
SDIR="$HOME/.xbin"
DBIN=".xbin"
HODN=".scpts"
UINPUT="$6"


quit()
{
	local var="$1"
	if [[ "$var" == "q" || "$var" == "Q" ]]; then
	echo ""
		echo "Operation aborted."
		exit 0
	fi
}

auth()
{
	local var="$WHICH"

	if [[ ${#var} == 1 ]]; then
		if [[ "$var" =~ [cC] ]]; then
			rep="PC"
			sudo -E echo -e "\n.....Hi $USER! ....."
		elif [[ "$var" =~ [pP] ]]; then
			rep="Phone"
			echo -e "\n.....Hi USER! ....."
		fi
	fi
}

invalid_selection()
{
	if [[ "$OPTION" =~ [zZ] ]]; then
		echo -e "Wrong selection. You can only select from the options above."
		echo -e "Try again."
	elif [[ "$OPTION" =~ [nNpP] ]]; then
		echo -e "Another operation?"
	fi
}

streamedit()
{
	local var1="$1"
	local var2="$2"

	sed -i "s/$var1/$var2/g" "$SDIR/$DFILENAME"
}

details()
{
	echo -e ".................................."
	echo -e "Username: $NUSERNAME"
	echo -e "Token: ghp_$NTOKEN"
	echo -e "Email: $NEMAIL"
	echo -e ".................................."
}

unametokenmaill2()
{
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
	pass=10
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

unametokenmaill()
{
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

cpfunc()
{
	echo "custom commands" > "$SDIR/$DFILENAME"
	if [[ "$FILETYPE" =~ "bashscript" || "$FILETYPE" =~ "pyscript" ]]; then
		# copies the content
		cp "$HODN/$DFILENAME" "$SDIR/$DFILENAME"
	elif [[ "$FILETYPE" =~ "cfile" ]]; then
		# copies the content
		if [[ "$WHICH" =~ 'p' ]]; then
			cp "$HODN/phone/$DFILENAME" "$SDIR/$DFILENAME"
		elif [[ "$WHICH" =~ 'c' ]]; then
			cp "$HODN/pc/$DFILENAME" "$SDIR/$DFILENAME"
		fi
	fi
	# make the script executable
	chmod +x $SDIR/$DFILENAME
}

intro()
{
	local whch="$1"

	CHECKER_PC_PH=$(echo "$SDIR" | cut -d '/' -f 2)
	if [[ "$CHECKER_PC_PH" =~ [hH]ome|[uU]sers ]]; then
		if [[ "$whch" =~ "0" ]]; then
			echo -e "I can see that this is a PC"
		else
			echo -e "Configuring for a $rep"
		fi
	elif [[ "$CHECKER_PC_PH" == "data" ]]; then
		if [[ "$whch" =~ "0" ]]; then
			echo -e "I can see that this is a Phone"
		else
			echo -e "Configuring for a $rep"
		fi
	else
		if [[ "$whch" =~ "0" ]]; then
			echo -e "I can't figure out your type of device"
		else
			echo -e "Oh! Great. Configuring for a $rep"
		fi
	fi
}

#...options display.................. #
#...2.................. #

dOptions=(
	#...py script files....................... #
	"  push command - synchronse rather than just push"
	"  pull command - updates your local machine from remote"
	"  pushfile command - updates the remote with individual file commit messages"
	#...bash script files.................. #
	"  createRepo command - creates a github repository right from CLI"
	"  deleteRepo command - deletes a github repository right from CLI"
	"  cloneRepo command - clone a repository with less commands"
	"  viewRepos command - displays the list of repos from any account right from CLI"
	"  betty linter command"
	"  pycode command a \"pycodestyle (PEP 8)\" linter"
	"  curfol command - opens cwd using file explorer"
	"  pyxecute - appends shebang and makes your python files executable"
	"  pycodemore command(pycode with details)"
	"  cls command - clear your screen"
	"  authorID - configures your Github Identity(Global and Local) on your machine"
	#...py script files....................... #
	"  wcount command - counts the lines, words and chars in files"
    #...bash script files.................. #
	"  ctemp - generates a default C source file template"
	#...py script files....................... #
	"  clear_commit command - clears unstaged and recent commits on your machine"
	#...bash script files.................. #
	"  mycompile command - compile C source files (with options)"
	"  pycompile command - compile python files"
	#...C files....................... #
	"  myascii command - prints a simple version of the ASCII table"
	"  rot13 command - Rot13 Cipher"
	"  rot47 command - Rot47 Cipher"
	"  guessGame command- a Guessing Game(To unwind)"
	
	
)

category()
{
	local type="$1"
	local value="$2"
	local btype="$3"
	if [[ "$type" == "p" ]]; then
		new_value="$(( ($value) + 700 ))"
	elif [[ "$type" == "b" ]]; then
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
		new_value="$(( ($value) + 100 ))"
	fi
}
#...................................................... #
#...................................................... #

#...3.................. #
options()
{
	# ...py script files.................................... #
	if [[ "$converted_selection" == 0 ]]; then
		DFILENAME="push"
		category p "$converted_selection"
	elif [[ "$converted_selection" == 1 ]]; then
		DFILENAME="pull"
		category p "$converted_selection"
	elif [[ "$converted_selection" == 2 ]]; then
		DFILENAME="pushfile"
		category p "$converted_selection"
	# ...bash script files................................... #
	elif [[ "$converted_selection" == 3 ]]; then
		DFILENAME="createRepo"
		category b "$converted_selection" "cr"
	elif [[ "$converted_selection" == 4 ]]; then
		DFILENAME="deleteRepo"
		category b "$converted_selection" "dr"
	elif [[ "$converted_selection" == 5 ]]; then
		DFILENAME="cloneRepo"
		category b "$converted_selection" "cl"
	elif [[ "$converted_selection" == 6 ]]; then
		DFILENAME="viewRepos"
		category b "$converted_selection" "vr"
	elif [[ "$converted_selection" == 7 ]]; then
		DFILENAME="betty"
		category b "$converted_selection"
	elif [[ "$converted_selection" == 8 ]]; then
		DFILENAME="pycode"
		category b "$converted_selection"
	elif [[ "$converted_selection" == 9 ]]; then
		DFILENAME="curfol"
		category b "$converted_selection"
	elif [[ "$converted_selection" == 10 ]]; then
		DFILENAME="pyxecute"
		category b "$converted_selection"
	elif [[ "$converted_selection" == 11 ]]; then
		DFILENAME="pycodemore"
		category b "$converted_selection"
	elif [[ "$converted_selection" == 12 ]]; then
		DFILENAME="cls"
		category b "$converted_selection"
	elif [[ "$converted_selection" == 13 ]]; then
		DFILENAME="authorID"
		category b "$converted_selection"
	# ...py script files..................................... #
	elif [[ "$converted_selection" == 14 ]]; then
		DFILENAME="wcount"
		category p "$converted_selection"
	# ...bash script files................................... #
	elif [[ "$converted_selection" == 15 ]]; then
		DFILENAME="ctemp"
		category b "$converted_selection" "ct"
	# ...py script files..................................... #
	elif [[ "$converted_selection" == 16 ]]; then
		DFILENAME="clear_commit"
		category p "$converted_selection"
	# ...bash script files................................... #
	elif [[ "$converted_selection" == 17 ]]; then
		DFILENAME="mycompile"
		category b "$converted_selection"
	elif [[ "$converted_selection" == 18 ]]; then
		DFILENAME="pycompile"
		category b "$converted_selection"
	# ...C files............................................. #
	elif [[ "$converted_selection" == 19 ]]; then
		DFILENAME="myascii"
		category c "$converted_selection"
	elif [[ "$converted_selection" == 20 ]]; then
		DFILENAME="rot13"
		category c "$converted_selection"
	elif [[ "$converted_selection" == 21 ]]; then
		DFILENAME="rot47"
		category c "$converted_selection"
	elif [[ "$converted_selection" == 22 ]]; then
		DFILENAME="guessGame"
		category c "$converted_selection"
	fi

	#....tags............................. #
	
	if [[ "$new_value" =~ [4-6][0-9][0-9]|11111|22222|33333|44444|55555 ]]; then
		FILETYPE="bashscript"
	elif [[ "$new_value" =~ [1-3][0-9][0-9] ]]; then
		FILETYPE="cfile"
	elif [[ "$new_value" =~ [7-9][0-9][0-9] ]]; then
		FILETYPE="pyscript"
	fi
}

#...4.................. #
opertn()
{
	#...dir.................. #

	mkdir -p $SDIR

	#... command assignment.................. #

	if [[ ${#OPTION} =~ 1 ]]; then

		options

		#...creating variable and profile.................. #
		#...creating bshell variable.................. #
		echo ""
		if [ ! -f "$HOME/.bashrc" ]; then
			touch "$HOME/.bashrc"
			echo "Creating bshell variable..."
		else
			echo "Variable bshell exists..."
		sleep 0.1
		fi

		if ! grep -q "$DBIN" "$HOME/.bashrc"; then
			echo -e "Setting up bshell variable..."
			echo 'export PATH="$PATH:$HOME/'$(basename "$SDIR")'"' >> "$HOME/.bashrc"
		else
			echo -e "Bshell variable good..."
		sleep 0.1
		fi

		#...creating zshell variable.................. #
		echo ""
		if [ ! -f "$HOME/.zshrc" ]; then
			touch "$HOME/.zshrc"
			echo "Creating zshell variable..."
		else
			echo "Zshell variable exists..."
		sleep 0.1
		fi

		if ! grep -q "$DBIN" "$HOME/.zshrc"; then
			echo -e "Setting up zshell variable..."
			echo 'export PATH="$PATH:$HOME/'$(basename "$SDIR")'"' >> "$HOME/.zshrc"
		else
			echo -e "Zshell variable good..."
		sleep 0.1
		fi

		#...creating Profile.................. #
		echo ""
		if [ ! -f "$HOME/.bash_profile" ]; then
			touch "$HOME/.bash_profile"
			echo "Creating profile..."
		else
			echo "Profile exists..."
		sleep 0.1
		fi

		if ! grep -q  bashrc "$HOME/.bash_profile"; then
			echo -e "Setting up profile..."
			echo '[ -r ~/.bashrc ] && . ~/.bashrc ' >> "$HOME/.bash_profile"
		else
			echo -e "Profile good..."
		sleep 0.1
		fi

		echo -e ""
		echo -e "Creating $DFILENAME as a command..."
		echo -e ""
		
		if [[ "$new_value" =~ ^(11111|22222|33333|55555)$ ]]; then
			unametokenmaill
		elif [[ "$new_value" == 44444 ]]; then
			echo -e "custom commands" >  $SDIR/C_template.c
			cp "$HODN/C_template.c" "$SDIR/C_template.c"
			scptcpy
		elif [[ "$new_value" =~ [1-9][0-9][0-9] ]]; then
			scptcpy
		fi
	fi
	echo ""
}

pyfiles() {
    mkdir -p "$SDIR/pyfiles"

    for file in "$HODN/pyfiles/"*; do
        if [[ -f "$file" ]]; then
            filename=$(basename "$file")
            destination="$SDIR/pyfiles/$filename"

            if [[ -f "$destination" ]]; then
                cp "$file" "$destination"
            else
                echo "custom commands" > "$destination"
				cp "$file" "$destination"
            fi
        fi
    done
}


#...5.................. #
scptcpy()
{
	sleep 0.1
	# for betty command installation
	if [[ $DFILENAME =~ "betty" ]]; then
		bLinter

	# for pycodemore command installation
	elif [[ $DFILENAME =~ "pycode" || $DFILENAME =~ "pycodemore" || $FILETYPE =~ "pyscript" ]]; then
		pyfiles
		cpfunc
		# Check if Python3 is installed
		if command -v python3 &> /dev/null; then
			echo "Python 3 is already installed."
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
	echo "custom commands" > "$SDIR/custom_commands"
	cp "$HODN/custom_commands" "$SDIR/custom_commands"
	chmod +x "$SDIR/custom_commands"
}

#...5a.................. #
bLinter()
{
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
instructn()
{
	echo -e "Now, RESTART YOUR TERMINAL or START A NEW SESSION."
	sleep 0.1

	if [[ $DFILENAME == "betty" ]]; then
		echo -e "$STRT check your source files. $ANYWHERE: $DFILENAME <filename(s)>"
	elif [[ $DFILENAME == "pycode" ]]; then
		echo -e "$STRT check your python files. $ANYWHERE: $DFILENAME <filename(s)>"
	elif [[ $DFILENAME == "push" ]]; then
		echo -e "$STRT push(sync) to github. $ANYWHERE: $DFILENAME"
	elif [[ $DFILENAME == "pull" ]]; then
		echo -e "$STRT pull from github. $ANYWHERE: $DFILENAME"
	elif [[ $DFILENAME == "createRepo" ]]; then
		echo -e "$STRT create a github repo right from your terminal. $ANYWHERE: $DFILENAME"
	elif [[ $DFILENAME == "deleteRepo" ]]; then
		echo -e "$STRT delete a github repo right from your terminal. $ANYWHERE: $DFILENAME"
	elif [[ $DFILENAME == "cloneRepo" ]]; then
		echo -e "$STRT clone repos from github. $ANYWHERE: $DFILENAME"
	elif [[ $DFILENAME == "viewRepos" ]]; then
		echo -e "$STRT view the public repos of any github account. $ANYWHERE: $DFILENAME"
	elif [[ $DFILENAME == "mycompile" ]]; then
		echo -e "$STRT compile your files $EFFT $ANYWHERE: $DFILENAME <filename>"
	elif [[ $DFILENAME == "ctemp" ]]; then
		echo -e "$STRT create default C source file templates $EFFT $ANYWHERE: $DFILENAME <filename>"
	elif [[ $DFILENAME == "cls" ]]; then
		echo -e "$STRT clear your screen $EFFT $ANYWHERE: $DFILENAME"
	elif [[ $DFILENAME == "authorID" ]]; then
		echo -e "$STRT configure your GitHub identity both globally and locally within your environment $EFFT $ANYWHERE: $DFILENAME"
	elif [[ $DFILENAME == "pycodemore" ]]; then
		echo -e "$STRT check your python file with line details $EFFT $ANYWHERE: $DFILENAME <filename(s)>"
	elif [[ $DFILENAME == "pycompile" ]]; then
		echo -e "$STRT compile your python scripts to a .pyc $EFFT $ANYWHERE: $DFILENAME <filename(s)>"
	elif [[ $DFILENAME == "curfol" ]]; then
		echo -e "$STRT open your current working directory $EFFT $ANYWHERE: $DFILENAME"
	elif [[ $DFILENAME == "pyxecute" ]]; then
		echo -e "$STRT turn your file(s) to executable file(s) $EFFT $ANYWHERE: $DFILENAME <filename(s)>"
	# ............................................................ #
	elif [[ $DFILENAME == "guessGame" ]]; then
		echo -e "$STRT play guessing game $EFFT $ANYWHERE: $DFILENAME"
	elif [[ $DFILENAME == "rot13" ]]; then
		echo -e "$STRT encode and decode your texts with Rot13 $EFFT $ANYWHERE: $DFILENAME"
	elif [[ $DFILENAME == "rot47" ]]; then
		echo -e "$STRT encode and decode your texts with Rot47 $EFFT $ANYWHERE: $DFILENAME"
	elif [[ $DFILENAME == "myascii" ]]; then
		echo -e "$STRT check the ASCII table $EFFT $ANYWHERE: $DFILENAME"
	# ............................................................ #
	elif [[ $DFILENAME == "wcount" ]]; then
		echo -e "$STRT check the number of lines, words and characters in your file $EFFT $ANYWHERE: $DFILENAME <filename(s)>"
	elif [[ $DFILENAME == "clear_commit" ]]; then
		echo -e "$STRT unstage your files, clear commit messages on your local machine(provided, you are yet to push to remote). Revert to the same state as your remote $EFFT $ANYWHERE: $DFILENAME"
	elif [[ $DFILENAME == "pushfile" ]]; then
		echo -e "$STRT stage and commit individual files before pushing them all to remote $EFFT $ANYWHERE: $DFILENAME <filename(s)>"
	
	sleep 0.1
	fi
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
    items_per_page=8

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
