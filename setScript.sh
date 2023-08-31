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
ANYWHERE="Simply run(from anywhere in your environment)"
STRT="You can now"
SUP="to setup"
SDIR="$HOME/.xbin"
DBIN=".xbin"
HODN=".scpts"
DEL1="$HOME/.my_cmds"
DEL2="$HOME/dafCom"


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


#...options display.................. #
#...options display.................. #
options=(
    #...Script files.................. #
	"[a] or [A] - $SUP push(sync) command"
	"[b] or [B] - $SUP pull command"
	"[c] or [C] - $SUP create repo command(Without opening the github website)"
	"[d] or [D] - $SUP clone repo command"
	"[e] or [E] - $SUP compile command (with options including common flags)"
	"[f] or [F] - $SUP a default C source file template"
	"[g] or [G] - $SUP and use \"cls\" command to clear"
	"[h] or [H] - $SUP Github Author Identity(Global and Local) command"
	# #...C files....................... #
	"[i] or [I] - $SUP a Guessing Game command(To unwind)"
	"[j] or [J] - $SUP a Rot13 Cipher command"
	"[k] or [K] - $SUP a Rot47 Cipher command"
	"[l] or [L] - $SUP a simple ASCII table command"
)
#...................................................... #
#...................................................... #
intro()
{
	local whch="$1"

	# echo ""
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
#...................................................... #
#...................................................... #
intro "0"
echo -e "However, please go on and select your device:"
echo "[p] - Phone"
echo "[c] - PC"
echo "[q] - quit"
echo -n "Is this a phone or a pc? [P/C/Q] >>> "
read WHICH

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

#...................................................... #
#...................................................... #
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
    
    for ((i = $start; i < $end && i < ${#options[@]}; i++)); do
        echo -e "${options[$i]}"
    done

    echo ""
    echo -e "More options"
    if (( $page > 1 )); then
        echo "[p] - Previous Page"
    fi
    
    if (( $end < ${#options[@]} )); then
        echo "[n] - Next Page"
    fi
    
    echo "[q] - Quit"
    echo ""
    echo -n "What do you want to do? [q] - quit >>> "
    read -n 1 -s -r OPTION
    case $OPTION in
        n|N)
            if (( $end < ${#options[@]} )); then
                ((page++))
            fi
            ;;
        p|P)
            if (( $page > 1 )); then
                ((page--))
            fi
            ;;
        a|b|c|d|e|f|g|h|i|j|k|l|A|B|C|D|E|F|G|H|I|J|K|L)
			echo -n "$OPTION"
            break
            ;;
		q|Q)
			echo -n "$OPTION"
            Exit
            ;;
    esac
done
#...options display.................. #
#...options display.................. #


#...dir.................. #

mkdir -p $SDIR

echo ""
# <<<<<<< HEAD
# =======
#...Script files.................. #
# echo -e "[a] or [A] - $SUP push(sync) command"
# echo -e "[b] or [B] - $SUP pull command"
# echo -e "[c] or [C] - $SUP create repo command(Without opening github website)"
# echo -e "[d] or [D] - $SUP clone repo command"
# echo -e "[e] or [E] - $SUP compile command (with options including common flags)"
# echo -e "[f] or [F] - $SUP a default C source file template"
# echo -e "[g] or [G] - $SUP and use \"cls\" command to clear"
# echo -e "[h] or [H] - $SUP Github Author Identity(Global and Local) command"
#...C files....................... #
# echo -e "[i] or [I] - $SUP a Guessing Game command(To unwind)"
# echo -e "[j] or [J] - $SUP a Rot13 Cipher command"
# echo -e "[k] or [K] - $SUP a Rot47 Cipher command"
# echo -e "[l] or [L] - $SUP a simple ASCII table command"
#................................. #
# echo ""

# echo -n "What do you want to do? [q] - quit >>> "
# read OPTION
# >>>>>>> e5cf2fc59e0dc6788fc5a4c54599813068bdd8f5


#...functions .................. #

scptcpy()
{
	cp "$HODN/$DFILENAME" "$SDIR/$DFILENAME"
}

Ccpy()
{
	cp "$HODN/$DFILENAME.c" "$SDIR/$DFILENAME.c"
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
	echo -n "Chech that these are correct. Are they? [y/N] >>> "
	read ANS
	echo ""
	if [[ ${#ANS} =~ 1 && ("$ANS" =~ [yY]) ]]; then
		cp "$HODN/$vname" "$SDIR/$DFILENAME"
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

options()
{
	if [[ $OPTION =~ [aA] ]]; then
		RES="a"
	elif [[ $OPTION =~ [bB] ]]; then
		RES="b"
	elif [[ $OPTION =~ [cC] ]]; then
		RES="c"
	elif [[ $OPTION =~ [dD] ]]; then
		RES="d"
	elif [[ $OPTION =~ [eE] ]]; then
		RES="e"
	elif [[ $OPTION =~ [fF] ]]; then
		RES="f"
	elif [[ $OPTION =~ [gG] ]]; then
		RES="g"
	elif [[ $OPTION =~ [hH] ]]; then
		RES="h"
	# ............................................................ #
	elif [[ $OPTION =~ [iI] ]]; then
		RES="i"
	elif [[ $OPTION =~ [jJ] ]]; then
		RES="j"
	elif [[ $OPTION =~ [kK] ]]; then
		RES="k"
	elif [[ $OPTION =~ [lL] ]]; then
		RES="l"
	fi

	#....tags............................. #
	
	if [[ $RES =~ [abcdefgh] ]]; then
		FILETYPE="script"
	elif [[ $RES =~ [ijkl] ]]; then
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
	elif [[ $RES =~ "h" ]]; then
		DFILENAME="authorID"
	# ............................................................ #
	elif [[ $RES =~ "i" ]]; then
		DFILENAME="guessGame"
	elif [[ $RES =~ "j" ]]; then
		DFILENAME="rot13"
	elif [[ $RES =~ "k" ]]; then
		DFILENAME="rot47"
	elif [[ $RES =~ "l" ]]; then
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

	#...remove old dir.................. #
	# echo ""
	# if [ ! -f "$DEL2" ]; then
	# 	echo -e "Nothing to backup1"
	# else
	# 	cp $DEL2/* "$SDIR"
	# 	mv "$DEL2" "$HOME/.${(basename ${DEL2})}_backup_$(date +"%Y-%m-%d %H:%M:%S")"
	# 	echo "Old dir1 backed up..."
	# fi

	# if [ ! -f "$DEL1" ]; then
	# 	echo -e "Nothing to backup2"
	# else
	# 	cp $DEL1/* "$SDIR"
	# 	mv "$DEL1" "$HOME/${(basename ${DEL1})}_backup_$(date +"%Y-%m-%d %H:%M:%S")"
	# 	echo "Old dir2 backed up..."
	# fi
	#...remove old dir.................. #


	echo ""
	if [[ $RES =~ "a" ]]; then
		scptcpy
	elif [[ $RES =~ "b" ]]; then
		scptcpy
	elif [[ $RES =~ "c" ]]; then
		unametokenmaill "createRepoGeneral"
	elif [[ $RES =~ "d" ]]; then
		unametokenmaill "cloneRepoGeneral"
	elif [[ $RES =~ "e" ]]; then
		scptcpy
	elif [[ $RES =~ "f" ]]; then
		echo -e "TEXT" >  $SDIR/C_template.c
		cp "$HODN/C_template.c" "$SDIR/C_template.c"
		scptcpy
	elif [[ $RES =~ "g" ]]; then
		scptcpy
	elif [[ $RES =~ "h" ]]; then
		scptcpy
	# ............................................................ #
	elif [[ $RES =~ "i" ]]; then
		Ccpy
	elif [[ $RES =~ "j" ]]; then
		Ccpy
	elif [[ $RES =~ "k" ]]; then
		Ccpy
	elif [[ $RES =~ "l" ]]; then
		Ccpy
	fi


	#....make............................. #

	if [[ $FILETYPE =~ "cfile" ]]; then
		make $SDIR/$DFILENAME
		echo ""
	fi


	#...instructions(how to use).................. #	

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
	elif [[ $RES =~ "h" ]]; then
		echo -e "$STRT configure your GitHub identity both globally and locally within your environment $EFFT $ANYWHERE: $DFILENAME"
	# ............................................................ #
	elif [[ $RES =~ "i" ]]; then
		echo -e "$STRT play guessing game $EFFT $ANYWHERE: $DFILENAME"
	elif [[ $RES =~ "j" ]]; then
		echo -e "$STRT encode and decode your texts with Rot13 $EFFT $ANYWHERE: $DFILENAME"
	elif [[ $RES =~ "k" ]]; then
		echo -e "$STRT encode and decode your texts with Rot47 $EFFT $ANYWHERE: $DFILENAME"
	elif [[ $RES =~ "l" ]]; then
		echo -e "$STRT check the ASCII table $EFFT $ANYWHERE: $DFILENAME"
	fi


	echo -e "\ncompleted."
else
	echo -e "Invalid! You must select an option"
	echo ""
	exit 1
fi
