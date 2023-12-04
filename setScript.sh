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

#...functions .................. #

#..................... #
# calculate_sum() 
# {
#     local sum=$(( $1 + $2 ))
#     result=$sum
# }
# calculate_sum 5 3
# echo "Sum: $result"
#..................... #

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
		elif [[ "$var" =~ [qQ] ]]; then
			echo ""
			echo -e "Ok."
			exit 1
		else
			wrongput
		fi
	else
		wrongput
	fi
}

wrongput()
{
	echo ""
	echo -e "Invalid input.\nThe options are [P/C/Q]"
	echo ""
	exit 1
}

Exit()
{
    if [[ -z "$OPTION" || $OPTION =~ [qQ] ]]; then
		if [[ $OPTION =~ [qQ] ]]; then
			echo ""
			echo -e "Cheers!"
		else
			echo -e "You must select an option"
		fi
		echo ""
		exit 1
	fi
}

empt()
{
	local var="$1"

	if [[ -z "$var" ]]; then
		echo ""
		echo -e "Field cannot be empty."
		echo ""
		exit 1
	fi
}

pchk()
{
	local NUM1=36
	local NUM2=${#NTOKEN}

	if [[ $NUM2 != $NUM1 ]]; then
		echo -e ""
		echo -e "TOKEN: $NTOKEN which you supplied is not a classic token."
		echo -e "Make sure to remove \"ghp_\" and there is no whitespace."
		echo ""
		exit 1
	fi
}

streamedit()
{
	local var1="$1"
	local var2="$2"

	sed -i "s/$var1/$var2/g" "$SDIR/$DFILENAME"
}

unametokenmaill()
{
	local vname="$1"

	echo -n "Kindly Enter your Github Username >>> "
	read NUSERNAME
	empt "$NUSERNAME"
	echo -e "........................................................"
	echo -e "Example of what the token will be is $P2"
	echo -e "Recall that $P1 = ghp_ + $P2"
	echo -e "What you need to supply is $P2 and leave out the rest."
	echo -e "........................................................"
	echo -n "Your Classic Github token >>> "
	read NTOKEN
	pchk
	empt "$NTOKEN"
	echo -n "Lastly, your Github Email >>> "
	read NEMAIL
	empt "$NEMAIL"
	echo ""
	echo -e "Confirm your details:"
	echo -e ".................................."
	echo -e "Username: $NUSERNAME"
	echo -e "Token: ghp_$NTOKEN"
	echo -e "Email: $NEMAIL"
	echo -e ".................................."
	echo -n "Check that these are correct. Are they? [y/N] >>> "
	read ANS
	echo ""
	if [[ ${#ANS} =~ 1 && ("$ANS" =~ [yY]) ]]; then
		scptcpy
		streamedit "$DUSERNAME" "$NUSERNAME"
		streamedit "$DTOKEN" "$NTOKEN"
		streamedit "$DEMAIL" "$NEMAIL"
	elif [[ ${#ANS} =~ 1 && ("$ANS" =~ [nN]) ]]; then
		echo -e "Ok."
		echo ""
		exit 1
	else
		echo -e "You must provide these information to proceed"
		echo ""
		exit 1
	fi
}

cpfunc()
{
	if [[ "$FILETYPE" =~ "bashscript" || "$FILETYPE" =~ "pyscript" ]]; then
		# copies the content
		cp "$HODN/$DFILENAME" "$SDIR/$DFILENAME"
		# make the script executable
		chmod 744 $SDIR/$DFILENAME
	elif [[ "$FILETYPE" =~ "cfile" ]]; then
		# copies the content
		if [[ "$WHICH" =~ 'p' ]]; then
			cp "$HODN/phone/$DFILENAME" "$SDIR/$DFILENAME"
		elif [[ "$WHICH" =~ 'c' ]]; then
			cp "$HODN/pc/$DFILENAME" "$SDIR/$DFILENAME"
		fi
	fi
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
    #...bash script files.................. #
	"[0] - install and $SUP the \"betty\" code compliance checker command"
	"[1] - install and $SUP the \"pycodestyle (PEP 8)\" as \"pycode\" command"
	"[a] or [A] - $SUP push(sync) command"
	"[b] or [B] - $SUP pull command"
	"[c] or [C] - $SUP createRepo command(Without opening the github website)"
	"[d] or [D] - $SUP cloneRepo command"
	"[e] or [E] - $SUP source files compile command(with options)"
	"[f] or [F] - $SUP a default C source file template"
	"[g] or [G] - $SUP and use \"cls\" command to clear"
	"[h] or [H] - $SUP Github Author Identity(Global and Local) command"
	"[i] or [I] - $SUP \"pycodemore\" command(pycode with details)"
	"[j] or [J] - $SUP python file compile command"
	"[k] or [K] - $SUP curfol(current folder) command -opens it in file explorer"
	"[l] or [L] - $SUP pyxecute - appends shebang and makes your python files executable"
	# #...C files....................... #
	"[m] or [M] - $SUP a Guessing Game command(To unwind)"
	"[o] or [O] - $SUP a Rot13 Cipher command"
	"[r] or [R] - $SUP a Rot47 Cipher command"
	"[s] or [S] - $SUP a simple ASCII table command"
	# #...py script files....................... #
	"[t] or [T] - $SUP wcount - counts the lines, words and chars in files"
)

#...................................................... #
#...................................................... #

#...3.................. #
options()
{
	if [[ $OPTION =~ "0" ]]; then
		DFILENAME="betty"
		# RES="0"
	elif [[ $OPTION =~ "1" ]]; then
		DFILENAME="pycode"
		# RES="1"
	elif [[ $OPTION =~ [aA] ]]; then
		DFILENAME="push"
		# RES="a"
	elif [[ $OPTION =~ [bB] ]]; then
		DFILENAME="pull"
		# RES="b"
	elif [[ $OPTION =~ [cC] ]]; then
		DFILENAME="createRepo"
		# RES="c"
	elif [[ $OPTION =~ [dD] ]]; then
		DFILENAME="cloneRepo"
		# RES="d"
	elif [[ $OPTION =~ [eE] ]]; then
		DFILENAME="mycompile"
		# RES="e"
	elif [[ $OPTION =~ [fF] ]]; then
		DFILENAME="ctemp"
		# RES="f"
	elif [[ $OPTION =~ [gG] ]]; then
		DFILENAME="cls"
		# RES="g"
	elif [[ $OPTION =~ [hH] ]]; then
		DFILENAME="authorID"
		# RES="h"
	elif [[ $OPTION =~ [iI] ]]; then
		DFILENAME="pycodemore"
		# RES="i"
	elif [[ $OPTION =~ [jJ] ]]; then
		DFILENAME="pycompile"
		# RES="j"
	elif [[ $OPTION =~ [kK] ]]; then
		DFILENAME="curfol"
		# RES="k"
	elif [[ $OPTION =~ [lL] ]]; then
		DFILENAME="pyxecute"
		# RES="l"
	# ............................................................ #
	elif [[ $OPTION =~ [mM] ]]; then
		DFILENAME="guessGame"
		# RES="m"
	elif [[ $OPTION =~ [oO] ]]; then
		DFILENAME="rot13"
		# RES="o"
	elif [[ $OPTION =~ [rR] ]]; then
		DFILENAME="rot47"
		# RES="r"
	elif [[ $OPTION =~ [sS] ]]; then
		DFILENAME="myascii"
		# RES="s"
	# ............................................................ #
	elif [[ $OPTION =~ [tT] ]]; then
		DFILENAME="wcount"
		# RES="t"
	else
		echo -e "You can only choose from the options provided"
		exit 1
	fi

	#....tags............................. #
	
	if [[ $OPTION =~ [01abcdefghijklABCDEFGHIJKL] ]]; then
		FILETYPE="bashscript"
	elif [[ $OPTION =~ [morsMORS] ]]; then
		FILETYPE="cfile"
	elif [[ $OPTION =~ [tT] ]]; then
		FILETYPE="pyscript"
	fi
}

#...4.................. #
opertn()
{
	#...dir.................. #

	mkdir -p $SDIR

	#... command assignment.................. #

	if [[  -z "$OPTION" || ${#OPTION} =~ 1 ]]; then

		Exit
		options

		# if [[ $RES =~ "0" ]]; then
		# 	DFILENAME="betty"
		# elif [[ $RES =~ "1" ]]; then
		# 	DFILENAME="pycode"
		# elif [[ $RES =~ "a" ]]; then
		# 	DFILENAME="push"
		# elif [[ $RES =~ "b" ]]; then
		# 	DFILENAME="pull"
		# elif [[ $RES =~ "c" ]]; then
		# 	DFILENAME="createRepo"
		# elif [[ $RES =~ "d" ]]; then
		# 	DFILENAME="cloneRepo"
		# elif [[ $RES =~ "e" ]]; then
		# 	DFILENAME="mycompile"
		# elif [[ $RES =~ "f" ]]; then
		# 	DFILENAME="ctemp"
		# elif [[ $RES =~ "g" ]]; then
		# 	DFILENAME="cls"
		# elif [[ $RES =~ "h" ]]; then
		# 	DFILENAME="authorID"
		# elif [[ $RES =~ "i" ]]; then
		# 	DFILENAME="pycodemore"
		# elif [[ $RES =~ "j" ]]; then
		# 	DFILENAME="pycompile"
		# elif [[ $RES =~ "k" ]]; then
		# 	DFILENAME="curfol"
		# elif [[ $RES =~ "l" ]]; then
		# 	DFILENAME="pyxecute"
		# # ............................................................ #
		# elif [[ $RES =~ "m" ]]; then
		# 	DFILENAME="guessGame"
		# elif [[ $RES =~ "o" ]]; then
		# 	DFILENAME="rot13"
		# elif [[ $RES =~ "r" ]]; then
		# 	DFILENAME="rot47"
		# elif [[ $RES =~ "s" ]]; then
		# 	DFILENAME="myascii"
		# # ............................................................ #
		# elif [[ $RES =~ "t" ]]; then
		# 	DFILENAME="wcount"
		# # ............................................................ #
		# else
		# 	echo -e "You can only choose from the options provided"
		# 	exit 1
		# fi


		#...creating variable and profile.................. #
		#...creating bshell variable.................. #
		echo ""
		if [ ! -f "$HOME/.bashrc" ]; then
			touch "$HOME/.bashrc"
			echo "Creating bshell variable..."
		else
			echo "Variable bshell exists..."
		fi

		if ! grep -q "$DBIN" "$HOME/.bashrc"; then
			echo -e "Setting up bshell variable..."
			echo 'export PATH="$PATH:$HOME/'$(basename "$SDIR")'"' >> "$HOME/.bashrc"
		else
			echo -e "Bshell variable good..."
		fi

		#...creating zshell variable.................. #
		echo ""
		if [ ! -f "$HOME/.zshrc" ]; then
			touch "$HOME/.zshrc"
			echo "Creating zshell variable..."
		else
			echo "Zshell variable exists..."
		fi

		if ! grep -q "$DBIN" "$HOME/.zshrc"; then
			echo -e "Setting up zshell variable..."
			echo 'export PATH="$PATH:$HOME/'$(basename "$SDIR")'"' >> "$HOME/.zshrc"
		else
			echo -e "Zshell variable good..."
		fi

		#...creating Profile.................. #
		echo ""
		if [ ! -f "$HOME/.bash_profile" ]; then
			touch "$HOME/.bash_profile"
			echo "Creating profile..."
		else
			echo "Profile exists..."
		fi

		if ! grep -q  bashrc "$HOME/.bash_profile"; then
			echo -e "Setting up profile..."
			echo '[ -r ~/.bashrc ] && . ~/.bashrc ' >> "$HOME/.bash_profile"
		else
			echo -e "Profile good..."
		fi

		echo ""
		if [[ $OPTION =~ [01abeghijklmorstABEGHIJKLMORST] ]]; then
			scptcpy
		# if [[ $RES =~ "0" ]]; then
		# 	scptcpy
		# elif [[ $RES =~ "1" ]]; then
		# 	scptcpy "1"
		# elif [[ $RES =~ "a" ]]; then
		# 	scptcpy
		# elif [[ $RES =~ "b" ]]; then
		# 	scptcpy
		elif [[ $OPTION =~ [cc] ]]; then
			unametokenmaill "createRepoGeneral"
		elif [[ $OPTION =~ [dD] ]]; then
			unametokenmaill "cloneRepoGeneral"
		# elif [[ $RES =~ "e" ]]; then
		# 	scptcpy
		elif [[ $OPTION =~ [Ff] ]]; then
			echo -e "TEXT" >  $SDIR/C_template.c
			cp "$HODN/C_template.c" "$SDIR/C_template.c"
			scptcpy
		# elif [[ $RES =~ "g" ]]; then
		# 	scptcpy
		# elif [[ $RES =~ "h" ]]; then
		# 	scptcpy
		# elif [[ $RES =~ "i" ]]; then
		# 	scptcpy "i"
		# elif [[ $RES =~ "j" ]]; then
		# 	scptcpy
		# elif [[ $RES =~ "k" ]]; then
		# 	scptcpy
		# elif [[ $RES =~ "l" ]]; then
		# 	scptcpy
		# # ............................................................ #
		# elif [[ $RES =~ "m" ]]; then
		# 	scptcpy
		# elif [[ $RES =~ "o" ]]; then
		# 	scptcpy
		# elif [[ $RES =~ "r" ]]; then
		# 	scptcpy
		# elif [[ $RES =~ "s" ]]; then
		# 	scptcpy
		# # ............................................................ #
		# elif [[ $RES =~ "t" ]]; then
		# 	scptcpy
		fi

	else
		echo -e "Invalid! You must select an option"
		echo ""
		exit 1
	fi
}

#...5.................. #
scptcpy()
{
	local ZERO
	# local pyarname="$1"

	echo -e "Creating $DFILENAME as a command..."
	# cpfunc
	# for betty command installation
	if [[ $DFILENAME =~ "betty" ]]; then
		bLinter
		# ZERO="yes"
	# else
	# 	ZERO="no"

	# for pycodemore command installation
	elif [[ $DFILENAME =~ "pycode" || $DFILENAME =~ "pycodemore" || $FILETYPE =~ "pyscript" ]]; then
		cpfunc
		# Check if Python3 is installed
		if command -v python3 &> /dev/null; then
			echo "Python 3 is already installed."
		else
			# Attempt to install Python3
			echo "Installing Python3..."
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
		# elif [[ "$GO" =~ "go" ]]; then
		# cpfunc
		if [[ "$WHICH" =~ 'c' ]]; then
			# cpfunc
			# installation for pc
			sudo apt install pycodestyle
		elif [[ "$WHICH" =~ 'p' ]]; then
			# installation for phone
			pip install pycodestyle
		fi
	else
		# for other commands
		cpfunc
	# else
	# 	cp "$HODN/$DFILENAME" "$SDIR/$DFILENAME"
	fi

		# GO="go"
	# else
	# 	GO="dont"
	# fi

	# for python3 installation
	# if [[ "$FILETYPE" =~ "pyscript" || "$GO" =~ "go" ]]; then
	# 	# Check if Python3 is installed
	# 	if command -v python3 &> /dev/null; then
	# 		echo "Python 3 is already installed."
	# 	else
	# 		# Attempt to install Python3
	# 		echo "Installing Python3..."
	# 		# other package managers command
			
	# 		if [[ "$WHICH" =~ 'p' ]]; then
	# 			# for phone
	# 			pkg update
	# 			pkg install python
	# 		elif [[ "$WHICH" =~ 'c' ]]; then
	# 			# for pc
	# 			sudo apt-get update
	# 			sudo apt-get install -y python3
	# 		fi
	# 	fi
	# fi

	# # for betty command installation
	# if [[ $RES =~ "0" ]]; then
	# 	bLinter
	# 	# ZERO="yes"
	# # else
	# # 	ZERO="no"
	# fi
	
	# echo -e "Creating $DFILENAME as a command..."

	# creating the file
	# echo -e "TEXT" >  $SDIR/$DFILENAME
	# making the file an executable
	# chmod 744 $SDIR/$DFILENAME


	# installation for phone
	# if [[ "$WHICH" =~ 'p' ]]; then
	# 	# for betty
	# 	if [[ "$ZERO" =~ "yes" ]]; then
	# 		bLinter
	# 	# for pycode and pycodemore
	# 	elif [[ "$GO" =~ "go" ]]; then
	# 		cpfunc
	# 		pip install pycodestyle
	# 	else
	# 		# for other commands
	# 		cpfunc
	# 	fi

	# installation for pc
	# elif [[ "$WHICH" =~ 'c' ]]; then

	# for betty
	# if [[ "$ZERO" =~ "yes" ]]; then
	# 	bLinter
	# for pycode and pycodemore
	# elif [[ "$GO" =~ "go" ]]; then
	# 	cpfunc
	# 	if [[ "$WHICH" =~ 'c' ]]; then
	# 		# cpfunc
	# 		# installation for pc
	# 		sudo apt install pycodestyle
	# 	elif [[ "$WHICH" =~ 'p' ]]; then
	# 		# installation for phone
	# 		pip install pycodestyle
	# 	fi
	# else
	# 	# for other commands
	# 	cpfunc
	# 	fi
	# # else
	# # 	cp "$HODN/$DFILENAME" "$SDIR/$DFILENAME"
	# fi

	#...creating custom_commands to view all commands.................. #
	cp "$HODN/custom_commands" "$SDIR/custom_commands"
	chmod +x "$SDIR/custom_commands"
}

#...5a.................. #
bLinter()
{
	echo -e ""
	# pwd
	mkdir -p tempo
	# pwd
	cd tempo
	# pwd
	git clone https://github.com/alx-tools/Betty.git

	if [[ "$WHICH" =~ 'p' ]]; then
		echo -e ""
		git clone https://github.com/DafetiteOgaga/betty_wrapper.git
		cp betty_wrapper/phone-betty.sh betty_wrapper/phone-install.sh Betty
		echo -e ""
		cd Betty
		# pwd
		./phone-install.sh

	elif [[ "$WHICH" =~ 'c' ]]; then
		echo -e ""
		cd Betty
		# pwd
		sudo ./install.sh
	fi
	# pwd
	# cd 
	rm -rf ../../tempo
	# pwd
	cd ../../
	# pwd
}

#...6.................. #
instructn()
{
	echo -e "Now, RESTART YOUR TERMINAL or START A NEW SESSION."

	if [[ $DFILENAME =~ "betty" ]]; then
		echo -e "$STRT check your source files. $ANYWHERE: $DFILENAME <filename(s)>"
	elif [[ $DFILENAME =~ "pycode" ]]; then
		echo -e "$STRT check your python files. $ANYWHERE: $DFILENAME <filename(s)>"
	elif [[ $DFILENAME =~ "push" ]]; then
		echo -e "$STRT push(sync) to github. $ANYWHERE: $DFILENAME"
	elif [[ $DFILENAME =~ "pull" ]]; then
		echo -e "$STRT pull from github. $ANYWHERE: $DFILENAME"
	elif [[ $DFILENAME =~ "createRepo" ]]; then
		echo -e "$STRT create a github repo right from your terminal. $ANYWHERE: $DFILENAME"
	elif [[ $DFILENAME =~ "cloneRepo" ]]; then
		echo -e "$STRT clone repos from github. $ANYWHERE: $DFILENAME"
	elif [[ $DFILENAME =~ "mycompile" ]]; then
		echo -e "$STRT compile your files $EFFT $ANYWHERE: $DFILENAME <filename>"
	elif [[ $DFILENAME =~ "ctemp" ]]; then
		echo -e "$STRT create default C source file templates $EFFT $ANYWHERE: $DFILENAME <filename>"
	elif [[ $DFILENAME =~ "cls" ]]; then
		echo -e "$STRT clear your screen $EFFT $ANYWHERE: $DFILENAME"
	elif [[ $DFILENAME =~ "authorID" ]]; then
		echo -e "$STRT configure your GitHub identity both globally and locally within your environment $EFFT $ANYWHERE: $DFILENAME"
	elif [[ $DFILENAME =~ "pycodemore" ]]; then
		echo -e "$STRT check your python file with line details $EFFT $ANYWHERE: $DFILENAME <filename(s)>"
	elif [[ $DFILENAME =~ "pycompile" ]]; then
		echo -e "$STRT compile your python scripts to a .pyc $EFFT $ANYWHERE: $DFILENAME <filename(s)>"
	elif [[ $DFILENAME =~ "curfol" ]]; then
		echo -e "$STRT open your current working directory $EFFT $ANYWHERE: $DFILENAME"
	elif [[ $DFILENAME =~ "pyxecute" ]]; then
		echo -e "$STRT turn your file(s) to executable file(s) $EFFT $ANYWHERE: $DFILENAME <filename(s)>"
	# ............................................................ #
	elif [[ $DFILENAME =~ "guessGame" ]]; then
		echo -e "$STRT play guessing game $EFFT $ANYWHERE: $DFILENAME"
	elif [[ $DFILENAME =~ "rot13" ]]; then
		echo -e "$STRT encode and decode your texts with Rot13 $EFFT $ANYWHERE: $DFILENAME"
	elif [[ $DFILENAME =~ "rot47" ]]; then
		echo -e "$STRT encode and decode your texts with Rot47 $EFFT $ANYWHERE: $DFILENAME"
	elif [[ $DFILENAME =~ "myascii" ]]; then
		echo -e "$STRT check the ASCII table $EFFT $ANYWHERE: $DFILENAME"
	# ............................................................ #
	elif [[ $DFILENAME =~ "wcount" ]]; then
		echo -e "$STRT check the number of lines, words and characters in your file $EFFT $ANYWHERE: $DFILENAME <filename(s)>"
	fi
}


#........ start .......................... #

#........ intro .......................... #

intro "0"
echo -e "However, please go on and select your device:"
echo "[p] - Phone"
echo "[c] - PC"
echo "[q] - quit"
echo -n "Is this a phone or a pc? [P/C/Q] >>> "
read WHICH


#...main operation.................. #

#...options display.................. #

#...1.................. #
count=0
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
		
		for ((i = $start; i < $end && i < ${#dOptions[@]}; i++)); do
			echo -e "${dOptions[$i]}"
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
		# echo -e "count = $count"
		if [[ $count -gt 0 ]]; then
			echo ""
			opertn
			echo -e ""
			instructn
			echo -e ""
			echo -e "Last option entered: $OPTION"
			echo -e "Last command created: $DFILENAME"
			echo -e "Another operation?"
			echo -n "Select another option? [q] - quit >>> "
		else
			echo ""
			echo -n "What do you want to do? [q] - quit >>> "
		fi
		read -n 1 -s -r OPTION
		case $OPTION in
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
			0|1|a|b|c|d|e|f|g|h|i|j|k|l|m|o|r|s|t|A|B|C|D|E|F|G|H|I|J|K|L|M|O|R|S|T)
				echo -n "$OPTION"
				break
				;;
			q|Q)
				echo -n "$OPTION"
				Exit
				;;
		esac
	done

	# opertn

	((count++))
done

#........ finish .......................... #

echo -e "\ncompleted."
