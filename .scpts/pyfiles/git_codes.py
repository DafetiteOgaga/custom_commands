#!/usr/bin/env python3

import subprocess, sys, os, time
from datetime import datetime
from pyfiles.verify_repo_new import entry_point
from pyfiles.my_prompt import main as prompt_1ch
from pyfiles.print import print_stdout, write_to_file, backward_search
from pyfiles.print import print_norm
from pyfiles.configure_settings_py import compile_dir_list, list_filter
from pyfiles.colors import *
try:
	from .colors import *
except ImportError:
	from colors import *

home_dir = os.path.join(os.path.expanduser("~"), '.xbin')  # Expands "~" to "/home/your-username"
bumpAppJsonVersionScript = os.path.join(home_dir, "pyfiles")  # location to bumpAppJsonVersion
bumpCCVersion = os.path.join(home_dir, "pyfiles")  # location to bumpCCVersion

# now = datetime.now()
formatted_date_time = datetime.now().strftime("%H:%M:%S on %a %b %Y")

def exit2(leave: bool = False):
	if leave == True:
		sys.exit(0)

root_repo = True
try:
	# print('starting ... ####################')
	current_dir_var = os.getcwd()
	# print(f'current_dir_var: {current_dir_var}')
	root_repo = backward_search()
	# print(f'root_repo: {root_repo}')

	pycache, venv = compile_dir_list(root_repo, venv=True)
	# print(f'pycache: {pycache}')
	delimiter = root_repo + os.sep
	# print(f'delimiter: {delimiter}')
	# print('..........................')
	# print('returned: #################')
	# for d in pycache:
	# 	print(':::::', f'{os.sep}'.join(d.split(os.sep)[6:]))
	# print('..........................')
	# # sys.exit(0)

	py = any(True for _ in pycache if '__pycache__' in _)
	nodeModules = any(True for _ in pycache if 'node_modules' in _)
	# print('nodeModules:', nodeModules)
	if py or nodeModules:
		py = '__pycache__' if py else 'node_modules'
		# py = '__pycache__' if py else 'src'

	pycache = [i for i in pycache if not os.path.isfile(i) and i.split(os.sep).pop() == py]
	if py == 'node_modules':
		# py = 'node_modules'
	# if py == 'src':
	# 	py = 'node_modules'
		pycache = [
			(f'{os.sep}'.join(i.split(os.sep)[:-1] + ['node_modules'])).split(delimiter).pop()
			for i in pycache
			if (os.path.exists(i) and os.path.isdir(i))]
		# print('pycache4:', pycache)

	gitignore_content = write_to_file([], '', read=True)
	pycache = [file for file in pycache if file.split(delimiter).pop() not in gitignore_content]
	venv = [dir for dir in venv if dir.split(delimiter)[-1] not in gitignore_content]
except:
	print('...')
	exit2(leave=root_repo)

def gitignore():
	"""Initiates the gitignore operation
	"""
	# print('Setting up .gitignore file ...')
	# print(f'py: {py}')
	auto_set_pycache1 = setup_gitignore(py=py)
	# print(f'auto_set_pycache1: {auto_set_pycache1}')
	ret = gitignore_resp(auto_set_pycache1, pycache)
	# print(f'ret: {ret}')
	if py != 'node_modules':
		auto_set_pycache2 = setup_gitignore(pycache=venv, envFile=True)
		ret = gitignore_resp(auto_set_pycache2, venv)
	if ret == 'n':
		browse_files()
	print()
	print_norm('Successful.')
	print_norm('Check the root of your repository for the newly created/updated .gitignore file')


def setup_gitignore(pycache: list=pycache, envFile: bool=False, py: str=None):
	"""display the list of files/directories paths to append to the .gitignore file.

	Args:
		pycache (list, optional): list of __pycache__ in the project. Defaults to pycache.
		envFile (bool, optional): list of venv directories in the project. Defaults to False.

	Returns:
		str: user's selection
	"""
	delimiter = backward_search() + f'{os.sep}'
	# print('delimiter: %s' % delimiter)
	# print('envFile: %s' % envFile)
	var = py
	if envFile:
		var = 'venv'
	# print(f'var: {var}')
	# print(f'pycache: {pycache}')
	if pycache == []:
		print()
		print_norm(f'==> .gitignore file is upto date with "{var}" directories')
		time.sleep(.5)
		input('Press Enter to continue...')
		return 'n'
	mainVar = 'Setting up and/or Updating .gitignore file (For'
	print()
	print_norm(f'{mainVar} {var})')
	print(''.rjust(len(mainVar)+len(var)+8, '.'))
	for index, filepath in enumerate(pycache):
		filepath = filepath.split(delimiter)[-1]
		print_norm(f'{index+1}. {filepath}')
	print('\n')
	print_norm('[y] - To add this list to .gitignore file')
	print_norm('Press any other key to browse through this directory')
	print_norm('[q] - To quit')
	print()
	auto_set_pycache = prompt_1ch('Make a choice >>> ')
	print()
	return auto_set_pycache

def gitignore_resp(auto_set_pycache: str, pycache: list):
	"""operates on the user response

	Args:
		auto_set_pycache (str): user's response
		pycache (list): list of __pycache__ directories in the project

	Returns: str
	"""
	delimiter = backward_search() + f'{os.sep}'
	# print('delimiter: %s' % delimiter)
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
	# print(f'root_list: {root_list}')
	search_repo(root_list, delimiter=delimiter)

def print_set_commit(var: str):
	"""This function prints information regarding the state of "Update README.md" setting.

	Args:
		var (str): string
	"""

	print("........................................................................................")
	if var.lower() == "unset":
		print_norm('"Update README.md" is no longer your default commit message to all README.md files')
	elif var.lower() == "set":
		print_norm('"Update README.md" is now your default commit message for all README.md files.')
	print_norm('##### NOTE: CHANGES WILL TAKE EFFECT THE NEXT TIME YOU RUN THE "pushfile" command. #####')
	print("........................................................................................")


# def pull():
# 	"""This function pulls and merges updates from the remote to the local branch
# 	"""

# 	print()
# 	print_norm("#### pulling ...################################################")
# 	pull = subprocess.run(["git", "pull"], capture_output=True, text=True)
# 	if pull.returncode == 0:
# 		print_stdout(pull.stdout)
# 	elif "You have divergent branches and need to specify how to reconcile them" in pull.stderr\
# 			and "Need to specify how to reconcile divergent branches" in pull.stderr:
# 		rebase = subprocess.run(["git", "config", "pull.rebase", "true"])
# 		pull = subprocess.run(["git", "pull"], capture_output=True, text=True)
# 		if pull.returncode == 0:
# 			print_stdout(pull.stdout)
# 		elif pull.stdout:
# 			print_stdout(pull.stdout)
# 		elif pull.stderr:
# 			print_stdout(pull.stderr)
# 	elif pull.returncode > 0:
# 		print_stdout(pull.stderr)
# 	else:
# 		print_norm("Oops! I got {}".format(pull.stderr))
# 		sys.exit()
# 	print_norm("Pull successful...")
# 	print()

def print_stashes(arg=''):
	"""This function prints the list of stashes in the repository
	"""
	stashList = subprocess.run(["git", "stash", "list"], capture_output=True, text=True)
	if stashList.stdout:
		print_norm(f'$$$$$ stdout: {stashList.stdout.strip()} fxn {arg}')
	elif stashList.stderr:
		print_norm(f'$$$$$ stderr: {stashList.stderr.strip()} fxn {arg}')
	else:
		print_norm(f"$$$$$ No stashes found. fxn {arg}")
	return ''


def run_subprocess(cmd, capture=True):
	return subprocess.run(cmd, capture_output=capture, text=True)

def getUserInput(promptText='Select a choice', allowedEntryArray=None, invalidText='Invalid choice.'):
	while True:
		choice = prompt_1ch(promptText).strip().lower()
		if choice == 'q':
			quit()
		elif allowedEntryArray:
			if choice in allowedEntryArray:
				return choice
		else:
			if choice:
				return choice
		print_norm(invalidText)

def get_conflicted_files():
	result = run_subprocess(['git', 'diff', '--name-only', '--diff-filter=U'])
	return result.stdout.strip().splitlines()

def is_binary(file_path):
	result = run_subprocess(["git", "check-attr", "binary", file_path])
	return "binary: set" in result.stdout

def show_conflict_lines(file_path):
	conflict_start = '<<<<<<<'
	conflict_middle = '======='
	conflict_end = '>>>>>>>'

	try:
		with open(file_path, 'r', errors='ignore') as f:
			lines = f.readlines()

		filename = f"{('/').join(file_path.split('/')[:-1])}/{BOLD}{MAGENTA}{file_path.split('/')[-1]}{RESET}" if '/' in file_path else f'{BOLD}{MAGENTA}{file_path}{RESET}'
		print(f"\nConflicts in: {filename}")

		in_conflict = False
		for i, line in enumerate(lines):
			stripped_line = line.strip()

			if stripped_line.startswith(conflict_start):
				in_conflict = "remote"
				print(f"line: {i+1} {stripped_line}	{BOLD}{YELLOW} - changes from {UNDERLINE}{in_conflict.upper()}{RESET}{BOLD}{YELLOW} starts here{RESET}")
			elif stripped_line.startswith(conflict_middle):
				in_conflict = "local"
				print(f"line: {i+1} {stripped_line}			{BOLD}{GREEN} - your {UNDERLINE}{in_conflict.upper()}{RESET}{BOLD}{GREEN} changes starts here{RESET}")
			elif stripped_line.startswith(conflict_end):
				print(f"line: {i+1} {stripped_line}	{BOLD}{WHITE} - end of conflict{RESET}\n")
				in_conflict = False
			elif in_conflict:
				print(f"line: {i+1} {stripped_line}")
	except FileNotFoundError:
		print(f"File not found: {file_path}")

def pop_stash(stash_resp=None):
	# if not stash_resp:
	# 	stash_pop = run_subprocess(['git', 'stash', 'pop'])
	# else:
	
	if stash_resp:
		stash_pop = stash_resp
		# print_norm(f"EEEEE{stash_pop.stdout}EEEEE")
		# print_norm(f"FFFFF{stash_pop.stderr}FFFFF")
		# print(f'{print_stashes(77777)}')
		
			# print('2222222222')
		# print_norm(f"CCCCC{stash_pop.stdout}CCCCC")
		# if stash_pop.stderr:
		# 	print_norm(f"DDDDD{stash_pop.stderr}DDDDD")
		print_stdout(f"{stash_pop.stdout.strip() or stash_pop.stderr.strip()}")
	# print(f'{print_stashes(88888)}')
	# Clean up stash if it still exists after popping
	cleanup = run_subprocess(['git', 'stash', 'list'])
	if cleanup.stdout.strip():
		print_norm("Cleaning up...")
		run_subprocess(['git', 'stash', 'drop'])  # drops top stash (stas

def is_rebase_in_progress():
	result = run_subprocess(['git', 'rev-parse', '--git-dir'])
	git_dir = result.stdout.strip()
	# print(f'git_dir: {git_dir}')
	response = os.path.exists(os.path.join(git_dir, 'rebase-merge')) or os.path.exists(os.path.join(git_dir, 'rebase-apply'))
	# print(f'is_rebase_in_progress: {response}')
	return response

def resolve_conflict(file_path, keep='local', rebase_in_progress=None):
	# print(f"keep arg received: {keep}")
	# print(f"file_path: {file_path}")

	# if rebase_in_progress is None:
	rebase_in_progress = is_rebase_in_progress()
	# print(f'rebase_in_progress: {rebase_in_progress} ##########')
	# if rebase_in_progress:
	# 	# During rebase: --ours = remote (upstream), --theirs = local
	# 	oursOrTheirs = '--ours' if keep == 'remote' else '--theirs'
	# else:
	# 	# During merge: --ours = local, --theirs = remote
	# 	oursOrTheirs = '--theirs' if keep == 'remote' else '--ours'

	oursOrTheirs = '--ours' if keep == 'remote' else '--theirs'
	# print(f'Using git checkout {oursOrTheirs} for {file_path}')
	run_subprocess(['git', 'checkout', oursOrTheirs, file_path])
	# if resoleve_conflict_result.returncode != 0:
	# 	print(f'failed to resolve conflict for {file_path}')
	run_subprocess(['git', 'add', file_path])
	# else:
	# 	run_subprocess(['git', 'checkout', '--theirs', file_path])
	# run_subprocess(['git', 'add', file_path])
	check_result = run_subprocess(['git', 'diff', '--check'])
	# print(f'return code from git diff check: {check_result.returncode}')
	# if check_result.returncode != 0:
	# 	print(f"Warning: Conflict markers might still exist in the file: {file_path}")
	# 	print(f"Please check the file manually to ensure all conflicts are resolved.")

def check_for_conflicts(rebase_in_progress=is_rebase_in_progress()):
	# if 'CONFLICT' in conflictText or 'you have unmerged files' in conflictText:
	print()
	print_norm("Oopsi! Merge conflicts detected...")
	# print_norm(f"Pull unsuccessful. YYYYY{conflictText}YYYYY")

	# print(f'{print_stashes(33333)}')
	conflicted_files = get_conflicted_files()

	number_of_conflicted_files = len(conflicted_files)
	append_s = 's' if number_of_conflicted_files > 1 else ''
	print_norm(f"Found {number_of_conflicted_files} conflicted file{append_s}.")
	# print()
	for file in conflicted_files:
		# if file.endswith('.png') or file.endswith('.jpg') or file.endswith('.jpeg') or file.endswith('.pdf') or file.endswith('.docx'):
		# 	# binary file — prompt user
		# 	choice = input(f"Binary conflict in {file}. Keep (l)ocal or (r)emote? ").strip().lower()
		# 	resolve_conflict(file, 'local' if choice == 'l' else 'remote')
		filename = f"{('/').join(file.split('/')[:-1])}/{BOLD}{BLUE}{file.split('/')[-1]}{RESET}" if '/' in file else f'{BOLD}{BLUE}{file}{RESET}'
		promptText = f"Conflict in {filename}. Keep (l)ocal or (r)emote? [l/r and q - quit] >>> "
		invalidText = "Invalid choice. Please enter 'l' for local or 'r' for remote or q to quit."
		if not is_binary(file):
			show_conflict_lines(file)
		choice = getUserInput(promptText, allowedEntryArray=['l', 'r'], invalidText=invalidText)
		# print(f"choice: X{choice}X #####")
		# print(f'file: {file}')
		# print(f'choice: {choice}')
		resolve_conflict(file, keep='local' if choice == 'l' else 'remote', rebase_in_progress=rebase_in_progress)
		# resolve_conflict(file, keep='local' if choice == 'l' else 'remote')
		# else:
			
		# 	choice = getUserInput(promptText, allowedEntryArray=['l', 'r'], invalidText=invalidText)
		# 	resolve_conflict(file, keep='local' if choice == 'l' else 'remote')

	print()
	conflictSuccess = 'Successful! conflicts resolved.'
	# print(f'rebase_in_progress: {rebase_in_progress} #####XXXXX#####')
	# if rebase_in_progress:
	# Continue rebase after resolving
	# print(f'{print_stashes(44444)}')
	cont = run_subprocess(['git', 'rebase', '--continue'])
	# print_norm(f"cont stdout: {cont.stdout}")
	# print_norm(f"cont returncode: {cont.returncode}")
	if cont.returncode != 0 and 'No rebase in progress' not in cont.stderr.strip():
		print_norm("Rebase continue failed. You may need to fix manually.")
		print_norm(f"Rebase unsuccessful. {cont.stderr}")
		quit()
	print_norm(f"{conflictSuccess} {cont.stdout}")
	# else:
	# 	# print(f'{print_stashes(55555)}')
	# 	print_norm(f"{conflictSuccess}")
	# return rebase_in_progress

def pull():
	"""This function pulls and merges updates from the remote to the local branch
	"""

	print()
	print_norm("#### pulling ...################################################")

	# print(f'{print_stashes(11111)}')

	# Stash everything
	# print_norm("Stashing changes...")
	# stash_result = run_subprocess(['git', 'stash', '--include-untracked'])
	# resolved = False
	is_stashed = None
	status = run_subprocess(['git', 'status', '--porcelain'])
	if status.stdout.strip():
		run_subprocess(['git', 'stash', '--include-untracked'])
		is_stashed = True
		# print_norm("Stashed local changes...")
	else: # consider removing
		# _ = ''
		print_norm("No local changes found.")

	# print_norm("Stashed local changes...")
	# print_stdout(stash_result.stdout)
	# print(f'{print_stashes(22222)}')

	# Pull with rebase
	pull = run_subprocess(["git", "pull", "--rebase"])
	# print_norm(f"stdout: {pull.stdout}")
	# print_norm(f"stderr: {pull.stderr}")
	is_stashed and print_norm("adding local changes ontop of remote...")
	if pull.returncode == 0:
		print_stdout(pull.stdout)
	else:
		# stderr_content = map(lambda x: x, pull.stderr)
		# print('type of stderr:', type(pull.stderr))
		# print(pull.stderr.replace('\n', ' '))
		unmerged_text = pull.stderr.replace('\n', ' ')
		# print_norm(f"HHHHH{unmerged_text}HHHHHH")
		if 'you have unmerged files' in unmerged_text:
			# print_norm("&&&&&&&&&&&&&&&&&&&")
			check_for_conflicts()
			pop_stash()
			is_stashed = False
		else:
			print_norm("Oops! I got {}".format(pull.stderr))
			quit()

	if is_stashed:
		stash_pop = run_subprocess(['git', 'stash', 'pop'])
		stderr_clean = stash_pop.stderr.replace('\n', ' ')
		stdout_clean = stash_pop.stdout.replace('\n', ' ')
		unmerged_pop_text = f"{stderr_clean} {stdout_clean}"
		# print_norm(f"GGGGG{unmerged_pop_text}GGGGG")
		
		if 'CONFLICT' in unmerged_pop_text:
			# print_norm("|||||||||||||||||||||")
			# print('111111111')
			check_for_conflicts(rebase_in_progress=False)
			pop_stash(stash_resp=stash_pop)
		# else: # consider removing
		# 	_ = ''
	# Apply stash back
	# print_norm("Applying stash back...")
	# print(f'{print_stashes(66666)}')
	# print_norm(f"AAAAA{pull.stdout}AAAAA")
	# print_norm(f"BBBBB{pull.stderr}BBBBB")
	# print(f'{print_stashes(99999)}')
	print()
	print_norm("Pull successful...")
	print()

def push(file_list: list=None):
	"""This function takes a list as argument and Updates the
		remote with the changes on the local machine.

	Args:
		file_list (list): list of files in the current working directory
	"""
	if 'custom_commands' in os.getcwd():
		subprocess.run(["bash", "bumpCCVersion"], check=True, cwd=bumpCCVersion, stdout=None, stderr=None)
	print_norm("#### pushing ...################################################")
	push = subprocess.run(["git", "push"])
	if push.returncode == 0:
		print()
		print_norm('Handshake with remote successful.')
		# print("The file(s)/folder(s): {} are in the working tree.".format([xfile for xfile in file_list]))
	elif push.stdout:
		print_stdout(push.stdout)
	elif push.stderr:
		print_stdout(push.stderr)
	else:
		print_norm("Oops! I got {}".format(push.stderr))
		sys.exit()

def checkPushAccess():
	"""This function checks if the user has push access to the remote repository.
	"""
	with open(f'{root_repo}/.git/config', 'r') as f:
		config_content = f.readlines()
	for line in config_content:
		if 'url =' in line:
			url = line.split('=')[1].strip()
			if 'ghp_' in url:
				token = url.split('//')[1].split('@')[0]
				return True
			else:
				print_norm("You don't have push access to this repository, only pull.")
				print_norm("Please provide a valid Github token with push access.")
				return False

def add_commit_all(type: str="current", commit_message: str=""):
	"""This function stages and commits all changes made on the working tree
		with just a message.

	Args:
		type (str, optional): Defaults to "current".
		commit_message (str, optional): Defaults to "".
	"""
	checkEditAccess = checkPushAccess()
	if not checkEditAccess:
		sys.exit()
	while True:
		if len(sys.argv) > 1:
			commit_message = (sys.argv)[1]
			break
		# if commit_message:
		# 	pass
		# else:
		# 	commit_message = input("Provide a commit message. [q] to quit >>> ")
		if not commit_message:
			commit_message = input("Provide a commit message. [q] to quit >>> ")
		quit(commit_message)
		if commit_message != "":
			break
		print_norm("You have to provide a commit message.")
	print_norm("#### staging and committing ...################################")
	if type == "current":
		# stage changes in current directories ####
		subprocess.run(["git", "add", "."])
	elif type == "all":
		# stage changes in all directories ########
		subprocess.run(["git", "add", "-A"])
	############################################################################################################
	############################################################################################################
	############################################################################################################
	# print(f'current location (git_codes): {os.getcwd()}')
	if '/home/dafetite/alx/altaviz/altaviz_mobile/altaviz_mobile' in os.getcwd():
		subprocess.run(["bash", "bumpAppJsonVersion"], check=True, cwd=bumpAppJsonVersionScript, stdout=None, stderr=None)
	# print(f'current location (git_codes): {os.getcwd()}')
	############################################################################################################
	############################################################################################################
	############################################################################################################
	commit = subprocess.run(["git", "commit", "-m", commit_message], capture_output=True, text=True)
	if commit.returncode == 0:
		print_stdout(commit.stdout)
		print_norm('"{}" successfully committed to files.'.format(commit_message))
	elif commit.stdout:
		print_stdout(commit.stdout)
	elif commit.stderr:
		print_stdout(commit.stderr)


def quit(val='q'):
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
		print_norm("Revert successful...")
		print_norm("Recent changes on this branch cleaned.")
		print_norm("Most recent state of the remote has been restored to the working tree of this branch.")
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
				print_norm("Working tree is the same as last commit. No changes to save.")
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
			print_norm(F"{RED}NOTE: IF YOU QUIT. YOUR STASH WILL NOT BE APPLIED TO THIS BRANCH.{RESET}")
			item = prompt_1ch('Select the stash you wish to apply. [q] to quit >>> ')
			quit(item)
		if item.isdecimal() and int(item) > 0 and int(item) <= num:
			item = int(item)
			break
		print()
		if string == "branch_list":
			print_norm("You should enter the number corresponding to the branch name.")
		elif string == "stash":
			print_norm("You should enter the number corresponding to the stash you want to apply.")
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
				# if line.startswith("*"):
				# 	main = (line.strip("*")).strip()
				# else:
				# 	main = line.strip()
				main = (line.strip("*")).strip() if line.startswith("*") else line.strip()
		return main
	elif new_branch:
		for line in (branch_list.stdout).split("\n"):
			if line.strip() == new_branch.strip():
				print_norm(f"The branch {new_branch} already exist.")
				quit("q")
			if line.startswith("*"):
				if (line.strip("*").strip()) == new_branch.strip():
					print_norm(f"You are currently on this branch({new_branch}).")
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
		# if create.stdout:
		# 	print_stdout(create.stdout)
		# elif create.stderr:
		# 	print_stdout(create.stderr)
		print_stdout(f"{create.stdout if create.stdout else create.stderr}")
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
	# if switch_branch.stderr:
	# 	print_stdout(switch_branch.stderr)
	# else:
	# 	print_stdout(switch_branch.stdout)
	print_stdout(f"{switch_branch.stderr if switch_branch.stderr else switch_branch.stdout}")

def auto_apply_stash():
	"""This function automatically apply the most recent stash to the current
		branch
	"""
	# auto apply stashed updates
	auto_stash = subprocess.run(["git", "stash", "apply"], capture_output=True, text=True)
	# if auto_stash.stdout:
	# 	print_stdout(auto_stash.stdout)
	# elif auto_stash.stderr:
	# 	print_stdout(auto_stash.stderr)
	print_stdout(f"{auto_stash.stdout if auto_stash.stdout else auto_stash.stderr}")


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
				print_norm(f"How do you want to handle changes in {current_branch_name}?")
				print_norm("[v] to see file(s) with changes - [d] to see content of change(s) - [q] to quit ")
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
		print_norm(f"You are in {current_branch_name} branch.")
		print_norm(f"Switch to the desired branch you want to merge to {current_branch_name}.")
		quit("q")
	while True:
		print()
		check = prompt_1ch("Are you sure that you want to merge this branch to main/master? [y/N] >>> ")
		if check.lower() == "y":
			break
		elif check.lower() == "n":
			quit("q")
		print()
		print_norm("You must decide.")
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
		print_norm("Nothing to show.")
		print_norm("Your working directory is in the same state as your last commit.")
	elif diff_res.returncode > 0:
		print_norm("Oops! I got:")
		print_norm("{}".format(print_stdout(diff_res.stderr)))


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
	try:
		dir = (os.sep).join((repo_dir[0]).split(os.sep)[:-1])
	except:
		pass
	if repeat and dir_path:
		dir = (os.sep).join(dir_path.split(os.sep)[:-1])
	if child_dir:
		dir = repo_dir[0]
		repo_dir = os.listdir(repo_dir[0])
	gitignore_content = write_to_file([], '', read=True)
	gitignore_content = [file.split(delimiter)[-1] for file in gitignore_content]
	repo_dir = [dir+f'{os.sep}'+file.split(delimiter)[-1] for file in repo_dir]
	repo_dir = [file for file in repo_dir if file.split(delimiter)[-1] not in gitignore_content]
	print('Browse through your file/dirs...')
	print()
	print_norm(f'You are in: {os.path.basename(dir)}')
	print(''.rjust(len(os.path.basename(dir)) + 18, '.'))
	ignore_list = []
	count = 0
	dir_list = []
	for fileOrDir in repo_dir:
		fileOrDir = fileOrDir.split(os.sep).pop()
		if fileOrDir == '.git':
			continue
		print_norm(f'{count + 1}. {fileOrDir}')
		dir_list.append(fileOrDir)
		count += 1
	print()
	selection = input('Make a selecion [Enter to submit], [q to quit] >>> ')
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
	# print(f'You selected: {cur_dir}')
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


def repo_details():
	"""pints the username of the current repository
	"""
	root = backward_search()
	path = f'{root}{os.sep}.git{os.sep}config'
	config = subprocess.run(['cat', path], capture_output=True, text=True)
	github_url = [(url.split(os.sep)) for url in (config.stdout).split("\n") if "url =" in url]
	user_name = github_url[0][-2]
	repo_name = github_url[0][-1].split(".")[0]
	print()
	print_norm(f'Github Username: {user_name}')
	print_norm(f'Repository: {repo_name}')


def Update_github_token(token: str, my_token: str):
	abort_op = f'\nOperation Aborted.'
	done = f"{BOLD}{'Done.'}{RESET}"
	if len(token) != 36 and (len(token) != 40 or not token.startswith('ghp_')):
		print_norm("\nInvalid token. Please enter a valid Github token.")
		sys.exit(1)
	if len(token) == 36:
		token = f'ghp_{token}'
	root = backward_search()
	# path = f'{root}{os.sep}.git{os.sep}config_test'
	path = f'{root}{os.sep}.git{os.sep}config'
	config = subprocess.run(['cat', path], capture_output=True, text=True)
	github_url = [(url.split(os.sep)) for url in (config.stdout).split("\n") if "url =" in url]
	# print(github_url)
	append_github = '@github.com'
	search_word = append_github[1:]
	print()
	user_name = github_url[0][-2]
	repo_name = github_url[0][-1].split(".")[0]
	print('Found the following:')
	print_norm(f'Github Username: {user_name}')
	print_norm(f'Repository: {BRIGHT_GREEN}{repo_name}{RESET}')
	if len(github_url[0][2]) == 51:
		old_token = f'{github_url[0][2][:40]}'
		print_norm(f'Old token: {BRIGHT_BLUE}{old_token[:8]}...{old_token[32:]}{RESET}')
		print_norm(f'New token: {BRIGHT_MAGENTA}{token[:8]}...{token[32:]}{RESET}')
		replace = prompt_1ch(f"\nReplace old token with the new token in the repo {BRIGHT_GREEN}{repo_name}{RESET} ? [y/N] >>> ")
		search_word = f'{old_token+append_github}'
		if replace.lower() != 'y' and replace == '':
			print(abort_op)
			sys.exit(0)
	elif len(github_url[0][2]) == 10:
		print(f'New token: {BRIGHT_MAGENTA}{token[:8]}...{token[32:]}{RESET}')
		adding = prompt_1ch(f"\nAdd it to your local credentials ? [y/N] >>> ")
		if adding.lower() != 'y' and adding == '':
			print(abort_op)
			sys.exit(0)
	replacement = f'{token+append_github}'
	# print('search_word:', search_word)
	# print('replacement:', replacement)
	copy_of_config = f'{(os.sep).join(path.split(os.sep)[:-1] + ["config_copy"])}'
	if not os.path.exists(copy_of_config):
		make_copy = subprocess.run(['cp', path, copy_of_config], capture_output=True, text=True)
	add_token = subprocess.run(['sed', '-i', f's|{search_word}|{replacement}|g', path ], capture_output=True, text=True)
	True and print(add_token.stderr, done)

	if token != my_token:
		save = prompt_1ch(f'\nSave "{BRIGHT_MAGENTA}{token[:8]}...{token[32:]}{RESET}" for future use? [y/N] >>> ')
		if save.lower() == 'y' or save == '':
			command_path = f"{os.path.join(os.path.expanduser('~'), '.xbin', 'pyfiles', 'git_codes.py')}"
			save_token = subprocess.run(['sed', '-i', f's|{my_token}|{token}|g', command_path ], capture_output=True, text=True)
			True and print(save_token.stderr, done)
		else:
			print('Token not saved.')

def incorrect_args():
	if len(sys.argv) != 2:
		token = input('Enter Github token to Add/Update to your Credentials [q] - quit >>> ')
		if token.lower() == 'q':
			print('\nCheers!')
			sys.exit(0)
		return token

def update_token_command():
	token = ''
	my_token = 'MY_TOKEN_UPDATED'
	if len(sys.argv) == 2:
		token = sys.argv[1]
	elif my_token.startswith('ghp_'):
		use_token = prompt_1ch(f'Use the token: {BRIGHT_MAGENTA}{my_token[:8]}...{my_token[32:]}{RESET}? [y/N] >>> ')
		if use_token.lower() == 'y' or use_token == '':
			token = my_token
		else:
			token = incorrect_args()
	else:
		token = incorrect_args()

	Update_github_token(token, my_token)


# def print_stashes():
# 	"""This function prints the list of stashes in the repository
# 	"""
# 	stashList = subprocess.run(["git", "stash", "list"], capture_output=True, text=True)
# 	if stashList.stdout:
# 		print_stdout(f'$$$$$ {stashList.stdout} fxn')
# 	elif stashList.stderr:
# 		print_stdout(f'$$$$$ {stashList.stderr} fxn')
# 	else:
# 		print_norm(f"$$$$$ No stashes found. fxn")




# entry point for pull_from_main_or_master command
def pull_from_main_or_master():
	"""pulls changes from the main/master branch into the current branch
	"""
	stashCreated = False
	main = view_branch(new_branch="main", action=-2)

	print_norm(f'current branch: {current_branch_name}')
	if current_branch_name in ["main", "master"]:
		print_norm(f"You are on {main} branch.")
		print_norm(f"Switch to the desired branch you want to pull {main} into.")
		quit("q")

	# stash changes, if any
	stashChanges = subprocess.run(["git", "stash"], capture_output=True, text=True)
	stashedOutput = stashChanges.stdout.strip()
	if "No local changes" not in stashedOutput:
		print_norm(stashedOutput)
		stashCreated = True
	else:
		print_norm("No local changes to stash. Proceeding with rebase...")

	# fetch changes from origin
	fetchChangesFromOrigin = subprocess.run(["git", "fetch", "origin"], capture_output=True, text=True)
	if fetchChangesFromOrigin.stderr:
		print_norm(fetchChangesFromOrigin.stderr)
		quit("q")

	# rebase from main/master branch
	rebaseFromMain = subprocess.run(["git", "rebase", f"origin/{main}"], capture_output=True, text=True)
	if rebaseFromMain.stdout:
		print_norm(rebaseFromMain.stdout)
	elif rebaseFromMain.stderr:
		print_norm('Rebase failed.')
		print_norm(rebaseFromMain.stderr)
		quit("q")

	# pop stash if one was created
	if stashCreated:
		popStash = subprocess.run(["git", "stash", "pop"], capture_output=True, text=True)
		if popStash.stdout:
			print_norm(popStash.stdout)
		elif popStash.stderr:
			print_norm(popStash.stderr)
			quit("q")

def getCurrentAccessToken():
	"""This function fetches the users access token from the repository.
	"""
	with open(f'{root_repo}/.git/config', 'r') as f:
		config_content = f.readlines()
	for line in config_content:
		if 'url =' in line:
			url = line.split('=')[1].strip()
			if 'ghp_' in url:
				token = url.split('//')[1].split('@')[0]
				print(f'Found token: {token}')
			else:
				print_norm("No token found for this repository.")


# if current_dir_var:
os.chdir(current_dir_var) if current_dir_var else None
