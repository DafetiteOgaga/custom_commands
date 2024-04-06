#!/usr/bin/env python3

import subprocess, sys, time, os
from datetime import datetime
from .verify_repo_new import entry_point
from .my_prompt import main as prompt_1ch
from .colors import *
from pyfiles.configure_settings_py import compile_dir_list

# now = datetime.now() 
formatted_date_time = datetime.now().strftime("%H:%M:%S on %a %b %Y")

# [RED GREEN YELLOW MAGENTA BLUE CYAN]
# [BRIGHT_BLACK BRIGHT_RED BRIGHT_GREEN BRIGHT_YELLOW
# BRIGHT_BLUE BRIGHT_MAGENTA BRIGHT_CYAN BRIGHT_WHITE]
# [RESET BOLD ITALIC UNDERLINE BLINK REVERSE STRIKETHROUGH]


def backward_search():
	"""Generates the path to the repository in the child directory.

	Returns:
		str: path to root repository
	"""
	init_path = os.getcwd()
	if ".git" in os.listdir():
		root_repo = init_path
		return root_repo
	else:
		if init_path == '/':
			print()
			print("You don't seem to be in a git repository")
			print('Change into a repository and try again')
			print()
			sys.exit(1)
		os.chdir(os.pardir)
		return backward_search()


def write_to_file(ignore_list, delimiter: str, read: bool=False):
	"""Inserts the given lines into the .gitignore file.

	Args:
		ignore_list (list): list of path to append to file
		delimiter (str): delimiter
		read (bool, optional): indicats that the current process is
		extract the content of .gitignore file. Defaults to False.

	Returns:
		list: content of .gitignore file
	"""
	# set the file name to .gitignore
	filename = delimiter + '.gitignore'
	ignore_file = 1
	try:
		file_list = []
		with open(filename) as g:
			for line in g:
				file_list.append(line.strip())
	except FileNotFoundError:
		open(filename, 'w').close()
	if read:
		return file_list
	if filename not in file_list:
		ignore_file = 0
	with open(filename, 'a') as f:
		for k in ignore_list:
			k = k.split(delimiter)[1]
			if k not in file_list:
				f.write(k + '\n')
		if not ignore_file:
			f.write(filename + '\n')


try:
	current_dir_var = os.getcwd()
	root_repo = backward_search()
	pycache, venv = compile_dir_list(root_repo, venv=True)
	pycache = [i for i in pycache if not os.path.isfile(i) and i.split('/')[-1] == '__pycache__']
	delimiter = root_repo + os.sep
	gitignore_content = write_to_file([], '', read=True)
	pycache = [file for file in pycache if file.split(delimiter)[-1] not in gitignore_content]
	venv = [dir for dir in venv if dir.split(delimiter)[-1] not in gitignore_content]
except:
	print('...')


def gitignore():
	"""Initiates the gitignore operation
	"""
	auto_set_pycache1 = setup_gitignore()
	gitignore_resp(auto_set_pycache1, pycache)
	auto_set_pycache2 = setup_gitignore(pycache=venv, envFile=True)
	ret = gitignore_resp(auto_set_pycache2, venv)
	if ret == 'n':
		browse_files()
	print()
	print('Successful.')
	print('Check the root of your repository for the newly created/updated .gitignore file')


def setup_gitignore(pycache: list=pycache, envFile: bool=False):
	"""display the list of files/directories paths to append to the .gitignore file.

	Args:
		pycache (list, optional): list of __pycache__ in the project. Defaults to pycache.
		envFile (bool, optional): list of venv directories in the project. Defaults to False.

	Returns:
		str: user's selection
	"""
	mainVar = 'Setting up and/or Updating .gitignore file (For'
	var = '__pycache__ directories'
	if envFile:
		var = 'venv directories'
	if pycache == []:
		print(f'==> .gitignore file is upto date with "{var}"')
		time.sleep(.5)
		cont = input('Press Enter to continue...')
		return 'n'
	print()
	print(f'{mainVar} {var})')
	print('.'.rjust(len(mainVar)+len(var)+3, '.'))
	for index, filepath in enumerate(pycache):
		filepath = filepath.split(delimiter)[-1]
		print(f'{index+1}. {filepath}')
	print()
	print('[y] - To add this list to .gitignore file')
	print('Press any key to browse through this dir (and subdirs) and select files/dirs to ignore')
	print('[q] - To quit')
	print()
	auto_set_pycache = prompt_1ch('Make a choice >>> ')
	print()
	return auto_set_pycache

def gitignore_resp(auto_set_pycache: str, pycache: list):
	"""operates on the user response

	Args:
		auto_set_pycache (str): user's response
		pycache (list): list of __pycache__ directories in the project

	Returns:
		str: .
	"""
	root_list = []
	if auto_set_pycache.lower() == 'q':
		print('Cheers...')
		sys.exit(0)
	elif auto_set_pycache.lower() == 'y' or auto_set_pycache == '\n':
		for file in pycache:
			root_list.append(file)
		write_to_file(root_list, delimiter=delimiter)
	else:
		return 'n'

def browse_files():
	"""calls the function that allows the user browse through the
		current directory.
	"""
	root_list = []
	for file in os.listdir(root_repo):
		root_list.append(f'{root_repo}{os.sep}{file}')
	search_repo(root_list, delimiter=delimiter)



def print_stdout(stdout: str, index: int=0, serial_numbered: int=0):
	"""This function nicely colors and prints out the output stream the
		result of the argument passed to it

	Args:
		stdout (str): the string to print
		index (int, optional): Defaults to 0.
		serial_numbered (int, optional): Defaults to 0.

	Returns:
		int, list: index of the line and list of line substrings.
	"""
	print()

	if stdout == None:
		std_list = []
	else:
		std_list = (stdout.split("\n"))[:-1]
	i = 0
	for_untrack = 0
	for i, line in enumerate(std_list):
		time.sleep(.03)
		if '(use "git add <file>..." to include in what will be committed)' in line:
			print(f"::::: {line}{RESET}")
			for_untrack += 1
			continue
		elif 'fatal' in line and 'did not match any files' in line:
			continue
		elif 'no changes added to commit (use "git add" and/or "git commit -a")' in line:
			for_untrack = 0
		elif for_untrack == 1:
			line = f"{YELLOW}{line}{RESET}"
		if serial_numbered == 1:
			if not index:
				if line.startswith("*"):
					line = f"{i+1}. {BRIGHT_MAGENTA}{line}"
				else:
					line = f"{i+1}. {line}"
		if line.startswith("["):
			for j, char in enumerate(line):
				if char == "]":
					req_index = j+1
			branch_id = line[:req_index]
			color_branch_id = f"{BRIGHT_MAGENTA}{branch_id}{RESET}"
			line = color_branch_id + line[req_index:]

		# s - selected words
		# y - any half of the line
		# a - complete line
		# c - further processing
		# o - other
		# n - specific selection
		sep = "^¬^"
		words_list = [
			f"deleted by us:{sep}{BRIGHT_RED}{sep}s",
			f"remote:{sep}{BRIGHT_CYAN}{sep}s",
			f"deleted:{sep}{BRIGHT_RED}{sep}s",
			f"delete {sep}{BRIGHT_RED}{sep}s",
			f"create {sep}{BRIGHT_GREEN}{sep}s",
			f"rewrite {sep}{CYAN}{sep}s",
			f"rename {sep}{BRIGHT_YELLOW}{sep}s",
			f"both modified{sep}{BRIGHT_GREEN}{sep}s",
			f"modified:{sep}{BRIGHT_GREEN}{sep}s",
			f"On branch{sep}{BRIGHT_MAGENTA}{sep}y",
			f"Untracked files:{sep}{MAGENTA}{sep}a",
			f"error{sep}{BRIGHT_RED}{sep}a",
			f"Changes not staged for commit:{sep}{BLUE}{sep}a",
			f"Your branch is ahead of{sep}{BRIGHT_YELLOW}{sep}y",
			f"Changes to be committed:{sep}{YELLOW}{sep}a",
			f"changed{sep}{RESET}{sep}c",
			f"new file:{sep}{BRIGHT_CYAN}{sep}s",
			f"diff --git{sep}{UNDERLINE}{BOLD}{BRIGHT_BLUE}{sep}a",
			f"+{sep}{RESET}{sep}o",
			f"-{sep}{RESET}{sep}o",
			f"Switched to branch{sep}{BRIGHT_GREEN}{sep}y",
			f"Saved working directory and index state{sep}{BRIGHT_MAGENTA}{sep}n",
			f"Your branch is up to date with{sep}{YELLOW}{sep}y",
			f"No local changes to save{sep}{BRIGHT_GREEN}{sep}a",
			f"set up to track remote branch{sep}{RESET}{sep}m", # don't touch this line.
			f"working tree clean{sep}{BRIGHT_GREEN}{sep}d",
			f"Unmerged paths{sep}{BRIGHT_CYAN}{sep}a"
			]
		
		words_dict = {}
		for word in words_list:
			a_word, color, type = word.split(sep)
			words_dict[word] = len(a_word)

		for k, v in words_dict.items():
			c_word, color, type = k.split(sep)
		
			if c_word in line:
				if type == "a":
					line = f"{color}{line}{RESET}"
				elif type == "y":
					line = line[:v] + f"{color}{line[v:]}{RESET}"
				elif type == "m":
					br_name1, br_name2 = line.split(c_word)
					line = " ".join([(br_name1.split())[0], f"{BRIGHT_MAGENTA}{br_name1.split()[1]}{RESET}",
							c_word, f"{BRIGHT_MAGENTA}{(br_name2.split())[0]}{RESET}", (br_name2.split())[1],
							f"{BRIGHT_YELLOW}{(br_name2.split())[2]}{RESET}"])
					# line = " ".join([(br_name1.split())[0], f"{BRIGHT_MAGENTA}{br_name1.split()[1]}{RESET}", c_word, f"{BRIGHT_MAGENTA}{(br_name2.split())[0]}{RESET}", (br_name2.split())[1], f"{BRIGHT_YELLOW}{(br_name2.split())[2]}{RESET}"])
				elif type == "n":
					index = next((i for i, char in enumerate(line) if char == ":"), v)
					line = line[:v] + f"{color}{line[v:index]}{RESET}" + line[index:]
				elif type == "d":
					index = line.find(c_word)
					v = index + v
					line = line[:index] + f"{color}{line[index:v]}{RESET}" + line[v:]
				elif type == "o":
					if "--- a/" in line or "+++ b" in line or "@@" in line:
						pass
					elif line.startswith("+"):
						line = f"{GREEN}{line}{RESET}"
					elif line.startswith("-"):
						line = f"{RED}{line}{RESET}"
				elif type == "c":
					if "insertion" in line or "deletion" in line:
						if len(line.split(",")) == 3:
							file_part, insertions, deletions = line.split(",")
							num, str_file, change = file_part.split()
							change = f"{BRIGHT_BLUE}{change}{RESET}"
							file_part = " ".join([num, str_file, change])
							insertions = f"{BRIGHT_GREEN}{insertions}{RESET}"
							deletions = f"{BRIGHT_RED}{deletions}{RESET}"
							line = ",".join([file_part, insertions, deletions])
						elif len(line.split(",")) == 2:
							if "insertion" in line:
								file_part, insertions = line.split(",")
								num, str_file, change = file_part.split()
								change = f"{BRIGHT_BLUE}{change}{RESET}"
								file_part = " ".join([num, str_file, change])
								insertions = f"{BRIGHT_GREEN}{insertions}{RESET}"
								line = ",".join([file_part, insertions])
							elif "deletion" in line:
								file_part, deletions = line.split(",")
								num, str_file, change = file_part.split()
								change = f"{BRIGHT_BLUE}{change}{RESET}"
								file_part = " ".join([num, str_file, change])
								deletions = f"{BRIGHT_RED}{deletions}{RESET}"
								line = ",".join([file_part, deletions])
					line = line[:v] + f"{color}{line[v:]}{RESET}"
				elif type == "s":
					word = line[:v]
					color_word = f"{color}{word}{RESET}"
					remaining_words = line[v:]
					if "/" in line or "\\" in line: # and line[i] != line[-1]:
						slash_index = 0
						for i, char in enumerate(line):
							if (char == "/" or char == "\\") and char != line[-1]:
								slash_index = i+1
							if slash_index:
								file_name = f"{color}{line[slash_index:]}{RESET}"
								remaining_words = line[v:slash_index] + file_name
					else:
						remaining_words = f"{color}{remaining_words}{RESET}"
					line = color_word + remaining_words
					break
		print(f"::::: {line}{RESET}")
	print()
	return i+1, std_list


def print_set_commit(var: str):
	"""This function prints information regarding the state of "Update README.md" setting.

	Args:
		var (str): string
	"""

	print("........................................................................................")
	if var.lower() == "unset":
		print('"Update README.md" is no longer your default commit message to all README.md files')
	elif var.lower() == "set":
		print('"Update README.md" is now your default commit message for all README.md files.')
	print('##### NOTE: CHANGES WILL TAKE EFFECT THE NEXT TIME YOU RUN THE "pushfile" command. #####')
	print("........................................................................................")


def pull():
	"""This function pulls and merges updates from the remote to the local branch
	"""

	print()
	print("#### pulling ...################################################")
	pull = subprocess.run(["git", "pull"], capture_output=True, text=True)
	if pull.returncode == 0:
		print_stdout(pull.stdout)
	elif "You have divergent branches and need to specify how to reconcile them" in pull.stderr\
			and "Need to specify how to reconcile divergent branches" in pull.stderr:
		rebase = subprocess.run(["git", "config", "pull.rebase", "true"])
		pull = subprocess.run(["git", "pull"], capture_output=True, text=True)
		if pull.returncode == 0:
			print_stdout(pull.stdout)
		elif pull.stdout:
			print_stdout(pull.stdout)
		elif pull.stderr:
			print_stdout(pull.stderr)
	elif pull.returncode > 0:
		print_stdout(pull.stderr)
	else:
		print("Oops! I got {}".format(pull.stderr))
		sys.exit()
	print("Pull successful...")
	print()


def push(file_list: list):
	"""This function takes a list as argument and Updates the
		remote with the changes on the local machine.

	Args:
		file_list (list): list of files in the current working directory
	"""

	print("#### pushing ...################################################")
	push = subprocess.run(["git", "push"])
	if push.returncode == 0:
		print()
		print('Changes has been pushed to remote.')
		# print("The file(s)/folder(s): {} are in the working tree.".format([xfile for xfile in file_list]))
	elif push.stdout:
		print_stdout(push.stdout)
	elif push.stderr:
		print_stdout(push.stderr)
	else:
		print("Oops! I got {}".format(push.stderr))
		sys.exit()


def add_commit_all(type: str="current", commit_message: str=""):
	"""This function stages and commits all changes made on the working tree
		with just a message.

	Args:
		type (str, optional): Defaults to "current".
		commit_message (str, optional): Defaults to "".
	"""
	while True:
		if len(sys.argv) > 1:
			commit_message = (sys.argv)[1]
			break
		if commit_message:
			pass
		else:
			commit_message = input("Provide a commit message. [q] to quit >>> ")
		quit(commit_message)
		if commit_message != "":
			break
		print("You have to provide a commit message.")
	print("#### staging and committing ...################################")
	if type == "current":
		# stage changes in current directories ####
		subprocess.run(["git", "add", "."])
	elif type == "all":
		# stage changes in all directories ########
		subprocess.run(["git", "add", "-A"])
	commit = subprocess.run(["git", "commit", "-m", commit_message], capture_output=True, text=True)
	if commit.returncode == 0:
		print_stdout(commit.stdout)
		print('"{}" successfully committed to files.'.format(commit_message))
	elif commit.stdout:
		print_stdout(commit.stdout)
	elif commit.stderr:
		print_stdout(commit.stderr)


def quit(val):
	"""
	This function stops and exit the program.
	"""

	if val.lower() == "q":
		print()
		print("Cheers.")
		sys.exit()


def clear_staged_and_commit():
	"""This function will unstage and clears the recent changes made on the
		local branch and revert it to the recent state of the remote
	"""

	print()
	sure = prompt_1ch("""You will lose all the recent changes on your local branch
Are you sure that you want to proceed? [y/N] >>> """)
	print()
	if sure.lower() == "y":
		current_branch = subprocess.run(["git", "branch", "--show-current"], capture_output=True, text=True)
		fetch = subprocess.run(["git", "fetch", "origin", current_branch.stdout.strip()], capture_output=True, text=True)
		clear = subprocess.run(["git", "reset", "--hard", f"origin/{current_branch.stdout.strip()}"])
		print("Revert successful...")
		print("Recent changes on this branch cleaned.")
		print("Most recent state of the remote has been restored to the working tree of this branch.")
	else:
		print("Operation aborted.")
	print()
	sys.exit()

def git_status(action: int=0):
	"""This function displays the current changes made to the working tree compared to that in the 
		repositories

	Args:
		action (int, optional): Defaults to 0.

	Returns:
		int: 1 for success, 0 for failure
	"""
	status = subprocess.run(["git", "status"], capture_output=True, text=True)
	if status.stdout:
		if action == 0:
			print_stdout(status.stdout)
		else:
			if "working tree clean" in status.stdout:
				print("Working tree is the same as last commit. No changes to save.")
				return 1
			else:
				return 0
	elif status.stderr:
		print_stdout(status.stderr)


def collect_input(num: int, string: str):
	"""This function processes the choice from branch or stash selection and
		returnes an integer value of the choice

	Args:
		num (int): integer
		string (str): string

	Returns:
		int: choice number
	"""
	while True:
		# single input function needed here
		if string == "branch_list":
			item = prompt_1ch('Select a branch to switch to. [q] to quit >>> ')
			quit(item)
		elif string == "stash":
			print(F"{RED}NOTE: IF YOU QUIT. YOUR STASH WILL NOT BE APPLIED TO THIS BRANCH.{RESET}")
			item = prompt_1ch('Select the stash you wish to apply. [q] to quit >>> ')
			quit(item)
		if item.isdecimal() and int(item) > 0 and int(item) <= num:
			item = int(item)
			break
		print()
		if string == "branch_list":
			print("You should enter the number corresponding to the branch name.")
		elif string == "stash":
			print("You should enter the number corresponding to the stash you want to apply.")
	return item


def view_branch(action: int=0, new_branch=""):
	"""This function:
		1. displays a list of available branches in the repository
		2. extracts the main or master branch depending on what the repository uses
		3. prevents you from creating already existing branch
		4. prevents you from recreating the branch you are in
		5. extraccts the current branch
		6. checkes whether you are not in the main or master branch before proceeding to stash your changes

	Args:
		action (int, optional): Defaults to 0.
		new_branch (str, optional): Defaults to "".

	Returns:
		str: branch name
	"""
	# view branch
	branch_list = subprocess.run(["git", "branch"], capture_output=True, text=True)
	selection = ""
	if action == 0:
		# list branches
		num, returned_list = print_stdout(branch_list.stdout, serial_numbered=1)
		item = collect_input(num, "branch_list")
		item = item - 1
		selection = (returned_list[item]).strip()
		return  selection
	elif new_branch == "main":
		# get main branch
		for line in (branch_list.stdout).split("\n"):
			if "main" in line or "master" in line:
				if line.startswith("*"):
					main = (line.strip("*")).strip()
				else:
					main = line.strip()
		return main
	elif new_branch:
		for line in (branch_list.stdout).split("\n"):
			if line.strip() == new_branch.strip():
				print(f"The branch {new_branch} already exist.")
				quit("q")
			if line.startswith("*"):
				if (line.strip("*").strip()) == new_branch.strip():
					print(f"You are currently on this branch({new_branch}).")
					quit("q")
	elif action == 100:
		for line in (branch_list.stdout).split("\n"):
			if line.startswith("*"):
				current_branch = (line.strip("*")).strip()
				return  current_branch
	elif action > 0:
		for line in (branch_list.stdout).split("\n"):
			if line.startswith("*") and (("master" not in line) or ("main" not in line)):
				stash(action)
				break

try:
	current_branch_name = view_branch(action=100)
except:
	print('...')


def create_or_switch_branch(branch_name: str=None, new_branch_name: str=None):
	"""This function:
		1. creates a local branch
		2. sets up the local branch remotely i.e providing access to remotely
			synchronize between the local branch and its remote branch
		3. switches to the newly created branch

	Args:
		branch_name (str, optional): branch name. Defaults to None.
		new_branch_name (str, optional): new_branch_name. Defaults to None.
	"""
	if new_branch_name:
		# creates new branch
		create = subprocess.run(["git", "branch", new_branch_name], capture_output=True, text=True)
		if create.stdout:
			print_stdout(create.stdout)
		elif create.stderr:
			print_stdout(create.stderr)
		setup_branch = subprocess.run(["git", "push", "-u", "origin", new_branch_name], capture_output=True, text=True)
		print_stdout(setup_branch.stdout)
		print_stdout(setup_branch.stderr)
		branch_name = new_branch_name
	# commit the recent changes
	
	# print(f"commit before switching from {CYAN}{current_branch_name}{RESET} to {BRIGHT_MAGENTA}{branch_name}{RESET} at {formatted_date_time}")
	# commit_message = f"committed before switching from {current_branch_name} to {branch_name} at {formatted_date_time}"
	# print()
	# add_commit_all(type="all", commit_message=commit_message)
	
	# switch to next/new branch
	switch_branch = subprocess.run(["git", "checkout", branch_name], capture_output=True, text=True)
	if switch_branch.stderr:
		print_stdout(switch_branch.stderr)
	else:
		print_stdout(switch_branch.stdout)

def auto_apply_stash():
	"""This function automatically apply the most recent stash to the current
		branch
	"""
	# auto apply stashed updates
	auto_stash = subprocess.run(["git", "stash", "apply"], capture_output=True, text=True)
	if auto_stash.stdout:
		print_stdout(auto_stash.stdout)
	elif auto_stash.stderr:
		print_stdout(auto_stash.stderr)


def stash(action: int=0):
	"""This function commits or stashes(according to users wish) the changes made in the working tree that has not
		been commited with either:
		1. an auto generated message containing the branch name and time or
		2. specified commit or stash message provided by the user

	Args:
		action (int, optional): Defaults to 0.
	"""
	# now = datetime.now()
	# formatted_date_time = now.strftime("%H:%M:%S on %a %b %Y")

	# stash changes
	# current_branch_name = view_branch(action=100)
	default_commit_message = f"commit for {BRIGHT_MAGENTA}{current_branch_name}{RESET} at {formatted_date_time}"
	default_stash_message = f"stashed at {formatted_date_time}"
	resp = ""
	message = ""
	changes = git_status(action=1)
	while True:
		# single letter response needed
		print()
		if action == 0:
			if not changes:
				print(f"How do you want to handle changes in {current_branch_name}?")
				print("[v] to see change(s) - [d] to see content of change(s) - [q] to quit ")
				resp = prompt_1ch("commit[c] or stash[s]? [c/s] >>> ")
				quit(resp)
				if resp.lower() == "c":
					response = prompt_1ch("Use default commit message? [y/N] [q] to quit >>> ")
					quit(response)
					if response.lower() == "y" or response == "":
						message = default_commit_message
					elif response.lower() == "n":
						message = input("Enter your commit message. [q] to quit >>> ")
						quit(message)
					print("Invalid response.")
				elif resp.lower() == "s":
					response = prompt_1ch("Use default stash message? [y/N] [q] to quit >>> ")
					quit(response)
					if response.lower() == "y" or response == "":
						message = default_stash_message
					elif response.lower() == "n":
						message = input("Enter your stash message. [q] to quit >>> ")
						quit(message)
					print("Invalid response.")
				elif resp.lower() == "v":
					git_status()
					print()
				elif resp.lower() == "d":
					diff()
					print()
				if message:
					break
			else:
				break
		else:
			message = default_stash_message
			break
	print()
	if not changes:
		print("::::: Checking for local changes in the branch ...")
		if resp.lower() == "c" and message:
			add_commit_all("all", message)
		elif resp.lower() == "s":
			to_stash = subprocess.run(["git", "stash", "save", message], capture_output=True, text=True)
			if to_stash.stdout:
				print_stdout(to_stash.stdout, index=1)
				print_stdout(to_stash.stderr)
			elif to_stash.stderr:
				print_stdout(to_stash.stderr)


def list_stashes():
	"""This function displays a list of saved stashes and applies the
		selected stash to the current branch
	"""
	# displays list of stashes
	stash = subprocess.run(["git", "stash", "list"], capture_output=True, text=True)
	if stash.stdout:
		num, returned_list = print_stdout(stash.stdout, serial_numbered=1)
		item = collect_input(num, "stash")
		item = item - 1
		selection = (((returned_list[item]).split(":"))[0]).strip()
		paths_list = entry_point(action="extraction")
		for item in paths_list:
			untrack = subprocess.run(["git", "rm", "-rf", item], capture_output=True, text=True)
			print_stdout(untrack.stdout)
			print_stdout(untrack.stderr)
		# apply stash
		stashed = subprocess.run(["git", "stash", "apply", selection], capture_output=True, text=True)
		if stashed.stdout:
			num, returned_list = print_stdout(stashed.stdout, index=1)
			print_stdout(stashed.stderr)
		elif stashed.stderr:
			print_stdout(stashed.stderr)
	elif stash.stderr:
		print_stdout(stash.stderr)


# branch entry point
def create_or_view_branches():
	"""display branches and creates a new on upon argument passed.
	"""
	args = sys.argv
	len_args = len(args)
	if len_args == 1:
		selection = view_branch()
		stash()
		create_or_switch_branch(selection)
		list_stashes()
		print()
	elif len_args == 2:
		# single input function needed here
		new_branch = (sys.argv)[1]
		view_branch(new_branch=new_branch, action=1)
		while True:
			print()
			create_branch = prompt_1ch(f'Create a branch "{new_branch}"? [y/N] [q] to quit >>> ')
			quit(create_branch)
			if create_branch.lower() == "y":
				break
			elif create_branch.lower() == "n":
				quit("q")
		view_branch(action=1)
		create_or_switch_branch("branch", new_branch)


# entry point for merge command
def merge_to_main_master():
	"""merge the current branch to the main/master branch
	"""
	# current_branch_name = view_branch(action=100)
	if current_branch_name == "main" or current_branch_name == "master":
		print(f"You are in {current_branch_name} branch.")
		print(f"Switch to the desired branch you want to merge to {current_branch_name}.")
		quit("q")
	while True:
		print()
		check = prompt_1ch("Are you sure that you want to merge this branch to main/master? [y/N] >>> ")
		if check.lower() == "y":
			break
		elif check.lower() == "n":
			quit("q")
		print()
		print("You must decide.")
	main = view_branch(new_branch="main", action=3)
	create_or_switch_branch(main)
	pull()
	create_or_switch_branch(current_branch_name)
	rebase = subprocess.run(["git", "rebase", main], capture_output=True, text=True)
	if rebase.stdout:
		print_stdout(rebase.stdout)
	elif rebase.stderr:
		print_stdout(rebase.stderr)
	create_or_switch_branch(main)
	merge = subprocess.run(["git", "merge", current_branch_name], capture_output=True, text=True)
	if merge.stdout:
		print_stdout(merge.stdout)
	elif merge.stderr:
		print_stdout(merge.stderr)
	push(file_list=[])
	# print(f"switching back to other branch")
	# create_or_switch_branch(current_branch_name)


def diff(action: int=0):
	"""display detailed changes on the current branch compared to
		that in the repository

	Args:
		action (int, optional): Defaults to 0.
	"""
	diff_res = subprocess.run(["git", "diff"], capture_output=True, text=True)
	if diff_res.returncode == 0 and diff_res.stdout:
		print_stdout(diff_res.stdout)
	elif diff_res.stderr:
		print_stdout(diff_res.stderr)
	elif diff_res.stderr == "" and diff_res.stderr == "" and diff_res.returncode == 0:
		print()
		print("Nothing to show.")
		print("Your working directory is in the same state as your last commit.")
	elif diff_res.returncode > 0:
		print("Oops! I got:")
		print("{}".format(print_stdout(diff_res.stderr)))


def search_repo(repo_dir: list, delimiter: str, dir_path: str=None, repeat: int=0, child_dir: int=0):
	"""provides the mechanism to search and browse the current
		working directory

	Args:
		repo_dir (list): current working directory. begins with the
		root of the repository
		delimiter (str): delimiter
		dir_path (str, optional): Defaults to None.
		repeat (int, optional): Defaults to 0.
		child_dir (int, optional): Defaults to 0.

	Returns:
		list: list of selected paths
	"""
	subprocess.run(['clear'])
	dir = (os.sep).join((repo_dir[0]).split(os.sep)[:-1])
	if repeat and dir_path:
		dir = (os.sep).join(dir_path.split(os.sep)[:-1])
	if child_dir:
		dir = repo_dir[0]
		repo_dir = os.listdir(repo_dir[0])
	gitignore_content = write_to_file([], '', read=True)
	gitignore_content = [file.split(delimiter)[-1] for file in gitignore_content]
	repo_dir = [dir+f'{os.sep}'+file.split(delimiter)[-1] for file in repo_dir]
	repo_dir = [file for file in repo_dir if file.split(delimiter)[-1] not in gitignore_content]
	print(f'Browse through your file/dirs...')
	print()
	print(f'You are in: {os.path.basename(dir)}')
	print('.'*(len(os.path.basename(dir)) + 13))
	ignore_list = []
	count = 0
	dir_list = []
	for i in repo_dir:
		i = i.split(os.sep).pop()
		if i == '.git':
			continue
		print(f'{count + 1}. {i}')
		dir_list.append(i)
		count += 1
	print()
	selection = input('Make a selecion [q] - quit >>> ')
	if selection == '':
		return ignore_list
	quit(selection)
	cur_dir = ""
	try:
		selection = int(selection)
		item = dir_list[selection - 1]
	except ValueError:
		print("Invalid selection. Please enter a valid integer.")
		sys.exit(1)
	except IndexError:
		print("Selection is out of range. Please enter a valid number.")
		sys.exit(1)
	cur_dir = f'{dir}{os.sep}{item}'
	print()
	if os.path.isdir(cur_dir):
		print('[n] - to add the dir to .gitignore file')
		open_dir = prompt_1ch(f'You want to explore {item}? [y/N] [q] - quit >>> ')
		quit(open_dir)
		if open_dir.lower() == 'y':
			search_repo([cur_dir], delimiter=delimiter, child_dir=1)
		elif open_dir.lower() == 'n':
			if cur_dir not in ignore_list:
				ignore_list.append(cur_dir)
				del dir_list[selection - 1]
				if not dir_list:
					write_to_file(ignore_list, delimiter)
					return ignore_list
				search_repo(dir_list, delimiter=delimiter, dir_path=cur_dir, repeat=1)
		else:
			print()
			print("Invalid entry.")
			sys.exit(1)
	else:
		ignore_list.append(cur_dir)
		del dir_list[selection - 1]
		search_repo(dir_list, delimiter=delimiter, dir_path=cur_dir, repeat=1)
	if ignore_list:
		write_to_file(ignore_list, delimiter)
	return ignore_list

if current_dir_var:
    os.chdir(current_dir_var)
    