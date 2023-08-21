#!/bin/bash

OPTION="$1"
DFILENAME="$2"
EFFT="effortlessly."
P1="ghp_ek81wkYt15bHQzABMQVeFpiNRNcrpy46Hqc7"
P2="ek81wkYt15bHQzABMQVeFpiNRNcrpy46Hqc7"
ANYWHERE="Simply run(from anywhere in your environment)"
STRT="You can now"
UN="YOUR_GUTHUB_USERNAME"
TK="YOUR_PERSONAL_ACCESS_TOKEN"
GM="YOUR_REGISTERED_GITHUB_EMAIL"
SUP="to setup"
SDIR=~/.my_cmds
TILDE=~"/"
SHOW=".my_cmds"
FILEPATH=~/$SHOW/.set


echo -e "\n.....Hey! ....."
mkdir -p $SDIR


#...options display.................. #

echo ""
#...Script files.................. #
echo -e "[a] or [A] - $SUP push(sync) command"
echo -e "[b] or [B] - $SUP pull command"
echo -e "[c] or [C] - $SUP create repo command(Without opening the github website)"
echo -e "[d] or [D] - $SUP clone repo command"
echo -e "[e] or [E] - $SUP compile command (with options including common flags)"
echo -e "[f] or [F] - $SUP a default C source file template"
echo -e "[g] or [G] - $SUP and use \"cls\" command to clear"
#...C files....................... #
echo -e "[h] or [H] - $SUP a Guessing Game command(To unwind)"
echo -e "[i] or [I] - $SUP a Rot13 Cipher command"
echo -e "[j] or [J] - $SUP a Rot47 Cipher command"
echo -e "[k] or [K] - $SUP a simple ASCII table command"
#................................. #
echo ""

echo -n "What do you want to do? [q] - quit >>> "
read OPTION


#...functions .................. #

Exit() 
{
    if [[ -z "$OPTION" || $OPTION =~ "q" || $OPTION =~ "Q" ]]; then
		if [[ $OPTION =~ "q" || $OPTION =~ "Q" ]]; then
			echo -e "Cheers!"
		else
			echo -e "You must select an option"
		fi
		echo ""
		exit 1
	fi
}

options()
{
	if [[ $OPTION =~ "a" || $OPTION =~ "A" ]]; then
		RES="a"
	elif [[ $OPTION =~ "b" || $OPTION =~ "B" ]]; then
		RES="b"
	elif [[ $OPTION =~ "c" || $OPTION =~ "C" ]]; then
		RES="c"
	elif [[ $OPTION =~ "d" || $OPTION =~ "D" ]]; then
		RES="d"
	elif [[ $OPTION =~ "e" || $OPTION =~ "E" ]]; then
		RES="e"
	elif [[ $OPTION =~ "f" || $OPTION =~ "F" ]]; then
		RES="f"
	elif [[ $OPTION =~ "g" || $OPTION =~ "G" ]]; then
		RES="g"
	# ............................................................ #
	elif [[ $OPTION =~ "h" || $OPTION =~ "H" ]]; then
		RES="h"
	elif [[ $OPTION =~ "i" || $OPTION =~ "I" ]]; then
		RES="i"
	elif [[ $OPTION =~ "j" || $OPTION =~ "J" ]]; then
		RES="j"
	elif [[ $OPTION =~ "k" || $OPTION =~ "K" ]]; then
		RES="k"
	fi

	#....tags............................. #
	
	if [[ $RES =~ "a" || $RES =~ "b" || $RES =~ "c" || $RES =~ "d" ||
		$RES =~ "e" || $RES =~ "f" || $RES =~ "g" ]]; then
		FILETYPE="script"
	elif [[ $RES =~ "h" || $RES =~ "i" || $RES =~ "j" || $RES =~ "k" ]]; then
		FILETYPE="cfile"
	fi
}

#..................... #
# calculate_sum() 
# {
#     local sum=$(( $1 + $2 ))
#     result=$sum
# }
# calculate_sum 5 3
# echo "Sum: $result"
#..................... #


#... command assignment.................. #

if [[  -z "$OPTION" || ${#OPTION} =~ 1 ]]; then

	Exit
	options

	if [[ $RES =~ "a" ]]; then
		DFILENAME="push"
	elif [[ $RES =~ "b" ]]; then
		DFILENAME="pull"
	elif [[ $RES =~ "c" ]]; then
		DFILENAME="createRepo"
	elif [[ $RES =~ "d" ]]; then
		DFILENAME="cloneRepo"
	elif [[ $RES =~ "e" ]]; then
		DFILENAME="mycompile"
	elif [[ $RES =~ "f" ]]; then
		DFILENAME="ctemp"
	elif [[ $RES =~ "g" ]]; then
		DFILENAME="cls"
	# ............................................................ #
	elif [[ $RES =~ "h" ]]; then
		DFILENAME="guessGame"
	elif [[ $RES =~ "i" ]]; then
		DFILENAME="rot13"
	elif [[ $RES =~ "j" ]]; then
		DFILENAME="rot47"
	elif [[ $RES =~ "k" ]]; then
		DFILENAME="myascii"
	else
		echo -e "You can only choose from the options provided"
		exit 1
	fi

	
	#....C/script............................. #

	echo -e "\nCreating $DFILENAME as a command..."

	if [[ $FILETYPE =~ "script" ]]; then
		echo -e "TEXT" >  $SDIR/$DFILENAME
		chmod 744 $SDIR/$DFILENAME
	elif [[ $FILETYPE =~ "cfile" ]]; then
		echo -e "TEXT" >  $SDIR/$DFILENAME.c
	fi


	#...creating variable and profile.................. #

	if ! grep -q .my_cmds ~/.bashrc; then
		echo -e "Setting up variable..."
		echo 'export PATH="$PATH:~/.my_cmds"' >> ~/.bashrc
	else
		echo -e "Variable good..."
	fi

	if ! grep -q  bashrc ~/.bash_profile; then
		echo -e "Setting up profile...\n"
		echo '[ -r ~/.bashrc ] && . ~/.bashrc ' >> ~/.bash_profile
	else
		echo -e "Profile good..."
	fi


	echo ""

	if [[ $RES =~ "a" ]]; then
		cp ".scpts/$DFILENAME" "$SDIR/$DFILENAME"
	elif [[ $RES =~ "b" ]]; then
		cp ".scpts/$DFILENAME" "$SDIR/$DFILENAME"
	elif [[ $RES =~ "c" ]]; then
		cp ".scpts/createRepoGeneral" "$SDIR/$DFILENAME"
	elif [[ $RES =~ "d" ]]; then
		cp ".scpts/cloneRepoGeneral" "$SDIR/$DFILENAME"
	elif [[ $RES =~ "e" ]]; then
		cp ".scpts/mycompile" "$SDIR/$DFILENAME"
	elif [[ $RES =~ "f" ]]; then
		echo -e "TEXT" >  $SDIR/C_template.c
		cp ".scpts/C_template.c" "$SDIR/C_template.c"
		cp ".scpts/defaultCTemplate" "$SDIR/$DFILENAME"
	elif [[ $RES =~ "g" ]]; then
		cp ".scpts/cls" "$SDIR/$DFILENAME"
	# ............................................................ #
	elif [[ $RES =~ "h" ]]; then
		cp ".scpts/1_edxGuessGame.c" "$SDIR/$DFILENAME.c"
	elif [[ $RES =~ "i" ]]; then
		cp ".scpts/1_my_rot13.c" "$SDIR/$DFILENAME.c"
	elif [[ $RES =~ "j" ]]; then
		cp ".scpts/1_my_rot47.c" "$SDIR/$DFILENAME.c"
	elif [[ $RES =~ "k" ]]; then
		cp ".scpts/1_my_ascii.c" "$SDIR/$DFILENAME.c"
	fi


	#....make............................. #

	if [[ $FILETYPE =~ "cfile" ]]; then
		make $SDIR/$DFILENAME
	fi


	#...instructions(how to use).................. #	

	echo ""
	echo -e "Now, RESTART YOUR TERMINAL or START A NEW SESSION."

	if [[ $RES =~ "a" ]]; then
		echo -e "$STRT push(sync) to github. $ANYWHERE: $DFILENAME"
	elif [[ $RES =~ "b" ]]; then
		echo -e "$STRT pull from github. $ANYWHERE: $DFILENAME"
	elif [[ $RES =~ "c" ]]; then
		echo -e "$STRT create a github repo right from your terminal. $ANYWHERE: $DFILENAME"
	elif [[ $RES =~ "d" ]]; then
		echo -e "$STRT clone repos from github. $ANYWHERE: $DFILENAME"
	elif [[ $RES =~ "e" ]]; then
		echo -e "$STRT compile your files $EFFT $ANYWHERE: $DFILENAME <filename>"
	elif [[ $RES =~ "f" ]]; then
		echo -e "$STRT create default C source file templates $EFFT $ANYWHERE: $DFILENAME <filename>"
	elif [[ $RES =~ "g" ]]; then
		echo -e "$STRT clear your screen $EFFT $ANYWHERE: $DFILENAME"
	# ............................................................ #
	elif [[ $RES =~ "h" ]]; then
		echo -e "$STRT play guessing game $EFFT $ANYWHERE: $DFILENAME"
	elif [[ $RES =~ "i" ]]; then
		echo -e "$STRT encode and decode your texts with Rot13 $EFFT $ANYWHERE: $DFILENAME"
	elif [[ $RES =~ "j" ]]; then
		echo -e "$STRT encode and decode your texts with Rot47 $EFFT $ANYWHERE: $DFILENAME"
	elif [[ $RES =~ "k" ]]; then
		echo -e "$STRT check the ASCII table $EFFT $ANYWHERE: $DFILENAME"
	fi


	#...more instructions(how to configure).................. #

	if [[ $OPTION =~ "c" || $OPTION =~ "C" || $OPTION =~ "d" || $OPTION =~ "D" ]]; then
		echo ""
		echo -e "ONE more step. RUN: vi $TILDE$SHOW/$DFILENAME"
		echo -e "When you open the file, you will replace \"$UN\" with your Github Username."
		echo -e "You will also replace \"$TK\" with your classic token."
		echo -e "Example of what the token will be is $P2 and not $P1"
		echo -e "Therefore $P1 = ghp_ + $P2"
		echo -e "What you need to supply is $P2 and leave out the rest."
		echo -e "Remember to equally replace $GM with your Registered Github Account Email."
	fi

	echo -e "\ncompleted."

else
	echo -e "Invalid! You must select an option"
	echo ""
	exit 1
fi
