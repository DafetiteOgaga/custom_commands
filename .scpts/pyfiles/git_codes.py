#!/usr/bin/env python3

import subprocess, sys, os, time, shlex
from datetime import datetime
from pyfiles.verify_repo_new import entry_point
from pyfiles.my_prompt import main as prompt_1ch
from pyfiles.print import print_stdout, write_to_file, backward_search
from pyfiles.print import print_norm
from pyfiles.configure_settings_py import compile_dir_list, list_filter, check_for_venv_or_node_modules
from pyfiles.colors import *
from pyfiles.subprocessfxn import run_subprocess, run_subprocess_cmd_alone, run_interactive_subprocess, subprocess_for_pull_command
try:
	from .colors import *
except ImportError:
	from colors import *
env = os.environ.copy()
# env["GIT_COMMITTER_NAME"] = "Automatic Committer"
# env["GIT_COMMITTER_EMAIL"] = "auto@example.com"

home_dir = os.path.join(os.path.expanduser("~"), '.xbin')  # Expands "~" to "/home/your-username"
bumpAppJsonVersionScript = os.path.join(home_dir, "pyfiles")  # location to bumpAppJsonVersion
bumpCCVersion = os.path.join(home_dir, "pyfiles")  # location to bumpCCVersion

# now = datetime.now()
formatted_date_time = datetime.now().strftime("%H:%M:%S on %a %b %Y")
formatted_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
formatted_stash_time = int(datetime.datetime.now().timestamp())

def exit2(leave: bool = False):
	if leave == True:
		sys.exit(0)

root_repo = True
delimiter = ''
try:
	# print(f'try block')
	# print('starting ... ####################')
	current_dir_var = os.getcwd()
	# print(f'current_dir_var: {current_dir_var}')
	root_repo = backward_search()
	delimiter = root_repo + os.sep if isinstance(root_repo, str) else os.sep
except:
	print('.....')
	# print(f'except block')
	# py = None
	exit2(leave=root_repo)

if root_repo == True:
	exit2(leave=True)
print('...')
def gitignore():
	"""Initiates the gitignore operation
	"""
	pycache, venv = compile_dir_list(root_repo, venv=True)
	# print(f'type of pycache: {type(pycache)}')
	# print(f'type of venv: {type(venv)}')
	for file_or_dir in pycache:
		# print(f'in - {file_or_dir.split(os.sep).pop()}')
		if os.path.isdir(file_or_dir):
			boolVal, listVal, venv_dir = check_for_venv_or_node_modules(file_or_dir)
			if boolVal:
				venv.append(venv_dir)
	
	# watches for __pycache__ directories
	py = any(True for _ in pycache if '__pycache__' in _ and 'node_modules' not in _)
	# watches for node_modules directories
	nodeModules = any(True for _ in pycache if 'node_modules' in _)
	# print(f'py: {py} 63')
	# print(f'nodeModules: {nodeModules} 64')
	if py or nodeModules:
		py = '__pycache__' if py else 'node_modules'
		# py = '__pycache__' if py else 'src'
	# print(f'py: {py} 74')
	# gets the absolute paths of the directories (__pycache__ or node_modules)
	pycache = [i for i in pycache if not os.path.isfile(i) and i.split(os.sep).pop() == py]
	# print(f'pycache 1st: {pycache}')
	if py == 'node_modules':
		# print('py == node_modules')
		# py = 'node_modules'
	# if py == 'src':
	# 	py = 'node_modules'
		# reduces the absolute path of the node_modules directories to that of the root repo
		pycache = [
			(f'{os.sep}'.join(i.split(os.sep)[:-1] + ['node_modules'])).split(delimiter).pop()
			for i in pycache
			if (os.path.exists(i) and os.path.isdir(i)) and i.split(delimiter).pop().count('node_modules') == 1]
		# print('pycache for node_module:', pycache)

	gitignore_content = write_to_file([], delimiter, read=True)
	# print(f'gitignore_content: {gitignore_content}')
	venv = list(set([dir for dir in venv if dir.split(delimiter)[-1] not in gitignore_content and
				not any(dir.startswith(v) for v in gitignore_content)]))
	# print(f'venv after gitignore_content: {venv}')
	pycache = [file for file in pycache
			if file.split(delimiter).pop() not in gitignore_content and
			not any(file.startswith(v) for v in venv) and
			not any(file.startswith(f'{delimiter}{v}') for v in gitignore_content)]
	# print(f'pycache after gitignore_content: {pycache[:3]}')


	# print('Setting up .gitignore file ...')
	# print(f'py: {py}')
	auto_set_pycache1 = setup_gitignore(pycache=pycache, py=py)
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


def setup_gitignore(pycache, envFile: bool=False, py: str=None):
	"""display the list of files/directories paths to append to the .gitignore file.

	Args:
		pycache (list, optional): list of __pycache__ in the project. Defaults to pycache.
		envFile (bool, optional): list of venv directories in the project. Defaults to False.

	Returns:
		str: user's selection
	"""
	# delimiter = root_repo + f'{os.sep}'
	# print('delimiter: %s' % delimiter)
	# print('envFile: %s' % envFile)
	var = py
	if envFile:
		var = 'venv'
	# print(f'var: {var}')
	# print(f'pycache: {pycache}')
	if pycache == []:
		# print()
		# print_norm(f'==> .gitignore file is upto date with "{var}" directories')
		# time.sleep(.5)
		# input('Press Enter to continue...')
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
	# delimiter = root_repo + f'{os.sep}'
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
	# delimiter = root_repo + f'{os.sep}'
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
# 	pull = run_subprocess(["git", "pull"])
# 	if pull.returncode == 0:
# 		print_stdout(pull.stdout)
# 	elif "You have divergent branches and need to specify how to reconcile them" in pull.stderr\
# 			and "Need to specify how to reconcile divergent branches" in pull.stderr:
# 		rebase = run_subprocess_cmd_alone(["git", "config", "pull.rebase", "true"])
# 		pull = run_subprocess(["git", "pull"])
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
	stashList = run_subprocess(["git", "stash", "list"])
	if stashList.stdout:
		print_norm(f'$$$$$ stdout: {stashList.stdout.strip()} fxn {arg}')
	elif stashList.stderr:
		print_norm(f'$$$$$ stderr: {stashList.stderr.strip()} fxn {arg}')
	else:
		print_norm(f"$$$$$ No stashes found. fxn {arg}")
	return ''


def getUserInput(promptText='Select a choice', allowedEntryArray=None, invalidText='Invalid choice.'):
	while True:
		# choice = prompt_1ch(promptText).strip().lower()
		first = prompt_1ch(promptText).strip()

		# Start of escape sequence (e.g., arrow key)
		if first == '\x1b':
			second = prompt_1ch('')  # expected to be '['
			third = prompt_1ch('')   # expected to be 'A', 'B', 'C', or 'D'
			print_norm(invalidText)
			continue  # Skip the rest of the loop and reprompt

		choice = first.lower()
		# print(f'length of choice: {len(choice)}')
		# print(f'choice: {choice}')
		if choice == 'q':
			quit()
		# elif len(choice) == 0:
		if allowedEntryArray:
			if choice in allowedEntryArray:
				return choice
		else:
			if choice:
				return choice
		print_norm(invalidText)

def check_for_marker_in_file(file_path):
	"""Check if conflict markers are present in the file."""
	try:
		with open(file_path, 'r') as f:
			content = f.read()
		if any(marker in content for marker in ['<<<<<<<', '=======', '>>>>>>>']):
			return True
		return False
	except Exception as e:
		print(f"Error reading file {file_path}: {e}")
		return False
############################################################################
def get_conflicted_files():
	code, out, _ = subprocess_for_pull_command("git diff --name-only --diff-filter=U")
	return out.splitlines() if out else []

	# result = run_subprocess(['git', 'diff', '--name-only', '--diff-filter=U'])
	# # print(f'result.stdout: {result.stdout.strip()} xxxxxxxxx')
	# list_of_conflicted_files = result.stdout.strip().splitlines()
	# cleaned_list_of_conflicted_files = []
	# for check_file in list_of_conflicted_files:
	# 	checkForMarker = check_for_marker_in_file(check_file)
	# 	# print(f"check for Marker in {check_file}. is marker: {checkForMarker}")
	# 	if not checkForMarker:
	# 		run_subprocess(['git', 'add', check_file])
	# 		merge_operation()
	# 		continue
	# 	cleaned_list_of_conflicted_files.append(check_file)
	# return cleaned_list_of_conflicted_files

def resolve_conflict(filepath):
	with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
		lines = f.readlines()

	resolved = []
	i = 0
	while i < len(lines):
		if lines[i].startswith("<<<<<<<"):
			version_a = []
			version_b = []
			i += 1
			while i < len(lines) and not lines[i].startswith("======="):
				version_a.append(lines[i])
				i += 1
			i += 1  # Skip the =======
			while i < len(lines) and not lines[i].startswith(">>>>>>>"):
				version_b.append(lines[i])
				i += 1
			i += 1  # Skip the >>>>>>>
			print("\nConflict detected in file:", filepath)
			print("A) Your version:\n", "".join(version_a))
			print("B) Incoming version:\n", "".join(version_b))
			choice = input("Choose version to keep (A/B): ").strip().lower()
			if choice == 'b':
				resolved.extend(version_b)
			else:
				resolved.extend(version_a)
		else:
			resolved.append(lines[i])
			i += 1

	with open(filepath, 'w', encoding='utf-8') as f:
		f.writelines(resolved)
	subprocess.run(['git', 'add', filepath])


# def resolve_conflict(file_path, keep='a'):
	# marker = check_for_marker_in_file(file_path)
	# # print(f"marker: {marker}")
	# if marker:
	# 	# print("❗ Conflict markers in file — cleaning.")
	# 	success = clean_conflict_markers(file_path, keep=keep)
	# 	if success:
	# 		# checkBranch()
	# 		# print("staging file after cleaning conflict markers...")
	# 		add_result = run_subprocess(['git', 'add', file_path])
	# 		if add_result.returncode != 0:
	# 			print(f'Failed to add {file_path} to staging area')
	# 			print(f'Error: {add_result.stderr}')
	# 			return False
	# 		else:
	# 			pass
	# 			# checkBranch()
	# 			# print(f'Added {file_path} to staging area.')
	# 	else:
	# 		return False
	# # checkBranch()
	# return True


def show_conflict_blocks(filepath):
	print(f"\n📝 Conflict in {filepath}:")
	with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
		lines = f.readlines()

	i = 0
	while i < len(lines):
		if lines[i].startswith("<<<<<<<"):
			print("======= BEGIN CONFLICT =======")
			while i < len(lines) and not lines[i].startswith("======="):
				print(lines[i].rstrip())
				i += 1
			print("======= VS =======")
			while i < len(lines) and not lines[i].startswith(">>>>>>>"):
				print(lines[i].rstrip())
				i += 1
			print("======== END CONFLICT ========")
		i += 1

def check_and_resolve_conflicts():
	conflicted_files = get_conflicted_files()
	if not conflicted_files:
		print("✅ No merge conflicts detected.")
		return

	print("\n⚠️ Merge conflicts found in the following files:")
	for f in conflicted_files:
		print(f" - {f}")
		show_conflict_blocks(f)

	for f in conflicted_files:
		resolve_conflict(f)

	print("\n✅ All conflicts resolved and staged.")
	if os.path.exists(".git/MERGE_HEAD"):
		subprocess.run(["git", "commit"], check=True)
		print("✅ Merge commit completed.")
	elif os.path.exists(".git/rebase-merge") or os.path.exists(".git/rebase-apply"):
		subprocess.run(["git", "rebase", "--continue"], check=True)
		print("✅ Rebase continued.")

############################################################################

def is_binary(file_path):
	result = run_subprocess(["git", "check-attr", "binary", file_path])
	return "binary: set" in result.stdout

def get_conflict_label(lines, marker):
	conflict_label = ''
	for index, line in enumerate(lines):
		if line.startswith(marker):
			# first_conflict_line = line
			conflict_label = line[len(marker):].strip()  # gets text after marker
			break
	return conflict_label

def show_conflict_lines(file_path):
	conflict_start = '<<<<<<<'
	conflict_middle = '======='
	conflict_end = '>>>>>>>'

	try:
		mid_index = -1
		strt_index = -1
		with open(file_path, 'r', errors='ignore') as f:
			lines = f.readlines()

		first = get_conflict_label(lines, conflict_start) + ' '
		second = get_conflict_label(lines, conflict_end) + ' '
		# last = ''

		filename = f"{('/').join(file_path.split('/')[:-1])}/{BOLD}{MAGENTA}{file_path.split('/')[-1]}{RESET}" if '/' in file_path else f'{BOLD}{MAGENTA}{file_path.split(".")[-1]}{RESET}'
		print(f"\nDetails of conflict in {filename}:")

		in_conflict = False
		for i, line in enumerate(lines):
			stripped_line = line.strip()

			if i == strt_index:
				print(f"line: {i+1} {stripped_line}	{BOLD}{YELLOW} <- {UNDERLINE}{in_conflict.upper()} {first}starts here{RESET}")
			elif i == mid_index:
				print(f"line: {i+1} {stripped_line}	{BOLD}{GREEN} <- {UNDERLINE}{in_conflict.upper()} {second}starts here{RESET}")
			elif stripped_line.startswith(conflict_start):
				in_conflict = "A"
				# first = line.split(conflict_start)[-1].strip()
				strt_index = i + 1
				print(f"line: {i+1} {stripped_line}")
			elif stripped_line.startswith(conflict_middle):
				in_conflict = "B"
				mid_index = i + 1
				print(f"line: {i+1} {stripped_line}")
			elif stripped_line.startswith(conflict_end):
				# second = line.split(conflict_end)[-1].strip()
				print(f"line: {i+1} {stripped_line}	{BOLD}{WHITE} <- end of conflict{RESET}\n")
				in_conflict = False
			elif in_conflict:
				print(f"line: {i+1} {stripped_line}")
		# print(f"mid_index: {mid_index}")
		return first, second
	except FileNotFoundError:
		print(f"File not found: {file_path}")

def pop_stash(stash_resp=None, stash_status=False):
	if stash_status:
		pop_top_stash = run_subprocess(['git', 'stash', 'pop'])
		stashList = run_subprocess(['git', 'stash', 'list'])

def is_rebase_in_progress():
	result = run_subprocess(['git', 'rev-parse', '--git-dir'])
	git_dir = result.stdout.strip()
	# print(f'git_dir: {git_dir}')
	response = os.path.exists(os.path.join(git_dir, 'rebase-merge')) or os.path.exists(os.path.join(git_dir, 'rebase-apply'))
	# print(f'is_rebase_in_progress: {response}')
	return response

def is_merge_in_progress():
	result = run_subprocess(['git', 'rev-parse', '--git-dir'])
	git_dir = result.stdout.strip()
	response = os.path.exists(os.path.join(git_dir, 'MERGE_HEAD'))
	return response

def set_editor():
	"""Sets the editor for Git commit messages."""
	# List of common editors
	editors = [
			'nano',           # Simple editor
			'vim',            # Vi improved
			'vi',             # Original vi
			'code --wait',    # VS Code
			'emacs',          # Emacs
			'subl --wait',    # Sublime Text
			'atom --wait',    # Atom (if still installed)
			'gedit',          # GNOME text editor (Linux GUI)
			'kate',           # KDE text editor (Linux GUI)
			'micro',          # Modern terminal editor
			'joe',            # Joe's Own Editor
			'pico',           # Pico editor
			'mcedit',         # Midnight Commander editor
			'notepad',        # Windows Notepad (Windows only)
			'notepad++',      # Notepad++ (Windows, if in PATH)
		]

	# Editor commands to attempt setting, in preferred order
	preferred_commands = [
		'code --wait',
		'nano',
		'vi',
		'emacs',
		'vim',
		'micro'
	]

	# Check if Git already has an editor
	editor_check = run_subprocess(['git', 'config', '--get', 'core.editor'])
	editor_output = editor_check.stdout.strip()
	print(f"Current git editor: {editor_output!r}")

	if editor_output:
		parts = shlex.split(editor_output)
		base_editor = os.path.basename(parts[0]).lower()
		if base_editor in editors:
			print(f"Editor '{base_editor}' is already configured and recognized.")
			return editor_output  # use the configured one

	# Otherwise, find a usable editor from preferred list
	for cmd in preferred_commands:
		parts = shlex.split(cmd)
		base_cmd = parts[0]
		which_check = run_subprocess(['which', base_cmd])
		if which_check.returncode == 0:
			print(f"Using temporary editor: {cmd}")
			return cmd

	print("No known editor found.")
	return None
		# available_editors = []
		# for index, editor in enumerate(editors):
		# 	cmd = editor.split()[0]  # Get just the command part
		# 	check = run_subprocess(['which', cmd])
		# 	if check.returncode == 0:
		# 		available_editors.append(editor)
		# 		print(f"{index+1}. {cmd} is installed")
		# selected =


def merge_operation():
	mergePromptText = "(a)uto commit the merges or open your (d)efault editor\nWhat do you want to do? [a/d] >>> "
	mergeInvalidText = "Invalid choice. Please enter 'a' or 'd' [q to quit]."
	auto_commit_merge = getUserInput(mergePromptText, allowedEntryArray=['a', 'd'], invalidText=mergeInvalidText)
	if auto_commit_merge == 'a':
		print_norm("Auto committing the merges...")
		commit_merges = run_subprocess(['git', 'commit', '-m', f"Merge resolved on {formatted_now}"])
		if commit_merges.returncode != 0:
			print(f'Failed to auto commit changes.')
			print("Commit the changes manually.")
			print(f'Error: {commit_merges.stderr}')
		else:
			# checkBranch()
			print(f'Auto commit successful.')
	else:
		# env["GIT_EDITOR"] = "true"
		# print(f'env editor: {env["GIT_EDITOR"]}')
		print_norm("Opening default editor for merge commit...")
		editor = set_editor()
		if editor:
			print(f"Using editor: {editor}")
			env['GIT_EDITOR'] = editor
			run_interactive_subprocess(['git', 'commit'], env=env)
		# if manual_commit.returncode != 0:
		# 	print(f'Failed to open default editor for merge commit.')
		# 	print("Commit the changes manually.")
		# 	print(f'Error: {manual_commit.stderr}')
		else:
			# checkBranch()
			print(f'Manual commit successful.')

def merge_or_rebase_in_progress():
	if is_rebase_in_progress():
		run_subprocess(['git', 'rebase', '--continue'])
	elif is_merge_in_progress():
		merge_operation()
	else:
		pass
		# print_norm("No rebase or merge in progress.")
		# return True

def clean_conflict_markers(file_path, keep='a'):
	"""
	Removes Git conflict markers and keeps either 'a' or 'b' changes.
	"""
	# print(f"Cleaning conflict markers in {file_path}, keeping: {keep}")
	try:
		with open(file_path, 'r') as f:
			lines = f.readlines()

		new_lines = []
		inside_conflict = False
		keep_local = (keep == 'a')
		buffer = {'a': [], 'b': []}
		current = None

		for line in lines:
			if line.startswith('<<<<<<<'):
				inside_conflict = True
				current = 'a'
				buffer = {'a': [], 'b': []}
			elif line.startswith('=======') and inside_conflict:
				current = 'b'
			elif line.startswith('>>>>>>>') and inside_conflict:
				inside_conflict = False
				part_to_keep = buffer['a'] if keep_local else buffer['b']
				# print(f'part_to_keep: {part_to_keep}')
				new_lines.extend(part_to_keep)
				current = None
			elif inside_conflict and current:
				buffer[current].append(line)
			else:
				new_lines.append(line)

		with open(file_path, 'w') as f:
			f.writelines(new_lines)

		# print(f"✅ Conflict markers removed and '{keep}' version kept.")
		return True
	except Exception as e:
		print(f"❌ Failed to clean conflict markers: {e}")
		return False

def checkBranch():
	"""This function checks if the current branch is main or master.
		It returns True if it is, otherwise False.
	"""
	current_branch = run_subprocess(["git", "branch", "--show-current"])
	print(f"you are currently in {current_branch.stdout or current_branch.stderr} branch")

def check_for_conflicts():
	conflicted_files = get_conflicted_files()
	# print(f'conflicted_files: {conflicted_files}')
	if conflicted_files:
		print()
		print_norm("Oopsi! Merge conflicts detected...")
		# print_norm(f"Pull unsuccessful. YYYYY{conflictText}YYYYY")

		# print(f'{print_stashes(33333)}')
		# checkBranch()

		number_of_conflicted_files = len(conflicted_files)
		append_s = 's' if number_of_conflicted_files > 1 else ''
		print_norm(f"Found {number_of_conflicted_files} conflicted file{append_s}.")
		# print()
		comfile = None
		is_conflicts_resolved = []
		for file in conflicted_files:
			comfile = file
			# if file.endswith('.png') or file.endswith('.jpg') or file.endswith('.jpeg') or file.endswith('.pdf') or file.endswith('.docx'):
			# 	# binary file — prompt user
			# 	choice = input(f"Binary conflict in {file}. Keep (l)ocal or (r)emote? ").strip().lower()
			# 	resolve_conflict(file, 'local' if choice == 'l' else 'remote')
			# print(f'file: {file}')
			filename = f"{('/').join(file.split('/')[:-1])}/{BOLD}{BLUE}{file.split('/')[-1]}{RESET}" if '/' in file else f'{BOLD}{BLUE}{file.split(".")[-1]}{RESET}'
			# print(f'filename: {filename}')
			if not is_binary(file):
				first, second = show_conflict_lines(file)
			promptText = f"How do you want to resolve the conflict:\nKeep A-({first}) or B-({second}) [q - quit]\nHow do you wish to proceed [a/b]? >>> "
			invalidText = "Invalid choice. Please enter 'a' or 'b' [q to quit]."
			choice = getUserInput(promptText, allowedEntryArray=['a', 'b'], invalidText=invalidText)
			# print(f"choice: X{choice}X #####")
			# print(f'file: {file}')
			# checkBranch()
			# print(f'choice: {choice}')
			# print(f'is_rebase_in_progress2: {is_rebase_in_progress()}')
			is_conflict_resolved = resolve_conflict(file, keep='a' if choice == 'a' else 'b')
			
			# print(f'is_conflict_resolved: {is_conflict_resolved}')
			print(f"Resolved conflict in {filename} by keeping {'local' if choice == 'l' else 'remote'} changes.")
			# resolve_conflict(file, keep='local' if choice == 'l' else 'remote')
			# else:
			# checkBranch()
			is_conflicts_resolved.append(is_conflict_resolved)
			# 	choice = getUserInput(promptText, allowedEntryArray=['l', 'r'], invalidText=invalidText)
			# 	resolve_conflict(file, keep='local' if choice == 'l' else 'remote')
		# print("out of the loop...")
		if all(is_conflicts_resolved) == True:
			print_norm("All conflicts resolved.")
			# print_norm("continuing with the rebase or merge process.")
			merge_or_rebase_in_progress()

		else:
			print_norm("Some conflicts were not resolved successfully. Please check the files manually.")
			print_norm("You can try running 'git status' to see the current state of your repository.")
			print_norm("Exiting...")
			quit("q")
		# print("exiting..."); sys.exit()
		print()
		conflictSuccess = 'Successful! conflicts resolved.'
		print_norm(f"{conflictSuccess}")
	else:
		print_norm("Conflicts resolved. Continuing with the process...")

#######################################################################
def check_unstaged_or_untracked():
	# Check for unstaged changes
	unstaged = run_subprocess(['git', 'diff-index', '--quiet', 'HEAD', '--'])
	# Check for staged changes
	staged = run_subprocess(['git', 'diff-index', '--quiet', '--cached', 'HEAD', '--'])
	# Check for untracked files
	untracked_code, untracked_out, _ = subprocess_for_pull_command('git ls-files --others --exclude-standard')
	has_untracked = bool(untracked_out.strip())
	return unstaged.returncode != 0 or staged.returncode != 0 or has_untracked

def pull(is_main_branch=False):
	# Ensure script exits on unhandled error
	try:
		current_branch_name = view_branch(action=100)
		# set back the main branch from fake_main_branch when test is completed
		main = 'fake_main_branch' # view_branch(new_branch="main", action=-2)
		use_branch = main if is_main_branch else current_branch_name
		stashed = False
		stash_msg = ""

		# Fetch from origin
		run_subprocess(['git', 'fetch', 'origin', use_branch], check=True)

		# Determine if we need to stash
		if check_unstaged_or_untracked():
			print("🔒 Changes detected. Stashing before merge...")
			stash_msg = f"temp-stash-before-merge-{formatted_stash_time}"
			run_subprocess(['git', 'stash', 'push', '-u', '-m', stash_msg], check=True)
			stashed = True
		else:
			pass
			# stashed = False
			# stash_msg = ""

		# Merge (do not raise exception on failure)
		print("🔁 Merging with origin/main...")
		merge_result = run_subprocess(['git', 'merge', f'origin/{use_branch}'])
		merge_success = merge_result.returncode == 0

		if merge_success:
			print("✅ Merge successful!")
		else:
			print("❌ Merge conflict occurred. Attempting to resolve interactively...")
			check_and_resolve_conflicts()
			merge_success = True  # After successful resolution

		# Restore stash only if merge was successful
		if stashed and merge_success:
			print("🔓 Restoring stashed changes...")
			_, stash_list_out, _ = subprocess_for_pull_command('git stash list')
			stash_id = None
			for line in stash_list_out.splitlines():
				if stash_msg in line:
					stash_id = line.split(':')[0]
					break
			if stash_id:
				try:
					result = run_subprocess(['git', 'stash', 'pop', stash_id])
					if result.returncode == 0:
						print("✅ Stash restored successfully!")
					else:
						print("⚠️ Stash pop failed due to conflicts. Your changes are still in:")
						print(f"    {stash_id}")
						print("Attempting to help you resolve stash conflicts interactively...")
						check_and_resolve_conflicts()
						print("✅ Conflict resolution complete for stashed changes.")
				except Exception:
					print("⚠️ Stash pop failed. Please recover manually.")
			else:
				print("⚠️ Expected stash not found. You may need to restore it manually.")

		# Inform user about stash if merge failed
		if stashed and not merge_success:
			print("⚠️ Merge failed. Your changes were stashed as:")
			print(f"    {stash_msg}")
			print("You can recover them with:")
			print("    git stash list")
			print("    git stash pop <stash@{{N}}>")
	except KeyboardInterrupt:
		print("\n🚫 Interrupted by user")
		sys.exit(1)
	except subprocess.CalledProcessError as e:
		print(f"❌ Command failed: {e.cmd}")
		sys.exit(e.returncode)

#######################################################################

# def pull(is_main_branch=False):
# 	"""This function pulls and merges updates from the remote (corresponding current/main/master branch)
# 		to the local branch
# 	Args:
# 		is_main_branch (bool, optional): Defaults to False.
# 	"""
# 	print()
# 	print_norm("#### pulling ...################################################")

# 	# Stash everything
# 	is_stashed = None
# 	# print(f'is_main_branch: {is_main_branch}')
# 	status = run_subprocess(['git', 'status', '--porcelain'])
# 	if status.stdout.strip():
# 		run_subprocess(['git', 'stash', '--include-untracked'])
# 		is_stashed = True
# 		# print_norm("Stashed local changes...")
# 	else: # consider removing
# 		# _ = ''
# 		print_norm("No local changes found.")

# 	# print_norm("Stashed local changes...")
# 	# print_stdout(stash_result.stdout)
# 	# print(f'{print_stashes(22222)}')

# 	# Pull with rebase
# 	# pull = run_subprocess(["git", "pull", "--rebase"])
# 	# pulls from corresponding remote branch but if is_main_branch is true, it pulls from that main/master branch
# 	main = view_branch(new_branch="main", action=-2)
# 	current_branch_name = view_branch(action=100)
# 	print(f'current_branch_name: {current_branch_name}')
# 	if is_main_branch:
# 		# print_norm(f'current branch: {current_branch_name}')
# 		if current_branch_name in ["main", "master"]:
# 			print_norm(f"You are on {main} branch.")
# 			print_norm(f"Switch to the desired branch you want to pull {main} into.")
# 			quit("q")

# 	pull = run_subprocess(["git", "pull"] if not is_main_branch else ["git", "pull", "origin", main])
# 	# pull = run_subprocess(["git", "pull"] if not is_main_branch else ["git", "pull", "origin", "fake_main_branch"],)


# 	# print_norm(f"stdout: {pull.stdout}")
# 	# print_norm(f"stderr: {pull.stderr}")

# 	conflict_str = "CONFLICT (content)".lower()
# 	unmerged_files = "you have unmerged files".lower()
# 	resolve_manually = "Resolve all conflicts manually".lower()

# 	is_stashed and print_norm("adding local changes ontop of update...")
# 	# checkBranch()
# 	if pull.returncode == 0:
# 		print_stdout(pull.stdout)
# 	else:
# 		# stderr_content = map(lambda x: x, pull.stderr)
# 		# print('type of stderr:', type(pull.stderr))
# 		# print(pull.stderr.replace('\n', ' '))
# 		unmerged_text = "{} {}".format(pull.stderr.replace('\n', ' '), pull.stdout.replace('\n', ' '))
# 		# print(f"".rjust(40, 'P'))
# 		if any(any_str in unmerged_text.lower() for any_str in [conflict_str, unmerged_files, resolve_manually]):
# 			print_norm(f'{pull.stdout}\n:pull.stdout')
# 			print_norm(f'{pull.stderr}\n:pull.stderr')
# 			# print(f'is_rebase_in_progress1: {is_rebase_in_progress()}')
# 			# print_norm(pull.stderr)
# 			# checkBranch()
# 			check_for_conflicts()
# 			# checkBranch()
# 			# print(f'is_rebase_in_progress5: {is_rebase_in_progress()}')
# 			# print_norm("Unmerged files found. Please resolve conflicts before proceeding.")
# 			# print(f'is_stashed pull: {is_stashed}')
# 			pop_stash(stash_status=is_stashed)
# 			is_stashed = False
# 			# checkBranch()
# 		else:
# 			print_norm("Oops! I got {}".format(pull.stderr))
# 			quit()

# 	if is_stashed:
# 		# checkBranch()
# 		stash_pop = run_subprocess(['git', 'stash', 'pop'])
# 		stderr_clean = stash_pop.stderr.replace('\n', ' ')
# 		stdout_clean = stash_pop.stdout.replace('\n', ' ')
# 		unmerged_pop_text = f"{stderr_clean} {stdout_clean}"
# 		# print_norm(f"GGGGG{unmerged_pop_text}GGGGG")

# 		if any(any_str in unmerged_pop_text.lower() for any_str in [conflict_str, unmerged_files, resolve_manually]):
# 		# if 'CONFLICT' in unmerged_pop_text:
# 			# checkBranch()
# 			print_norm(f'{stash_pop.stdout}\n:stash_pop.stdout')
# 			print_norm(f'{stash_pop.stderr}\n:stash_pop.stderr')
# 			# print_norm(stash_pop.stderr)
# 			# print(f'is_rebase_in_progress6: {is_rebase_in_progress()}')
# 			# print(f"".rjust(40, 'S'))
# 			check_for_conflicts()
# 			# print(f'is_rebase_in_progress7: {is_rebase_in_progress()}')
# 			# print(f'is_stashed stash: {is_stashed}')
# 			# checkBranch()
# 			pop_stash(stash_status=is_stashed)
# 			is_stashed = False
# 	# print(f'is_stashed final: {is_stashed}')
# 	# checkBranch()

# 	print()
# 	print_norm("Done...")
# 	print()

def push(file_list: list=None):
	"""This function takes a list as argument and Updates the
		remote with the changes on the local machine.

	Args:
		file_list (list): list of files in the current working directory
	"""
	if 'custom_commands' in os.getcwd():
		subprocess.run(["bash", "bumpCCVersion"], check=True, cwd=bumpCCVersion, stdout=None, stderr=None)
	print_norm("#### pushing ...################################################")
	push = run_subprocess_cmd_alone(["git", "push"])
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
		run_subprocess_cmd_alone(["git", "add", "."])
	elif type == "all":
		# stage changes in all directories ########
		run_subprocess_cmd_alone(["git", "add", "-A"])
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
	commit = run_subprocess(["git", "commit", "-m", commit_message])
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
		current_branch = run_subprocess(["git", "branch", "--show-current"])
		fetch = run_subprocess(["git", "fetch", "origin", current_branch.stdout.strip()])
		clear = run_subprocess_cmd_alone(["git", "reset", "--hard", f"origin/{current_branch.stdout.strip()}"])
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
	status = run_subprocess(["git", "status"])
	if status.stdout:
		if action == 0:
			print_stdout(status.stdout)
		else:
			if "working tree clean" in status.stdout:
				print_norm("Working tree is the same as last commit. No changes to save.")
				return 1
			else:
				return 0
	elif "not a git repository" not in status.stderr.strip():
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
		elif string == "delete_branch":
			item = prompt_1ch('Select the branch to delete. [q] to quit >>> ')
			quit(item)
		elif string == "stash":
			print_norm(F"{RED}NOTE: IF YOU QUIT. YOUR STASH WILL NOT BE APPLIED TO THIS BRANCH.{RESET}")
			item = prompt_1ch('Select the stash you wish to apply. [q] to quit >>> ')
			quit(item)
		if item.isdecimal() and int(item) > 0 and int(item) <= num:
			item = int(item)
			break
		print()
		if string == "branch_list" or string == "delete_branch":
			print_norm("You should enter the number corresponding to the branch name.")
		elif string == "stash":
			print_norm("You should enter the number corresponding to the stash you want to apply.")
	return item


def view_branch(action: int=0, new_branch="", remove_current_and_main_and_master_branch: bool=False):
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
	branch_list = run_subprocess(["git", "branch"])
	selection = ""
	if action == 0:
		input_str_type = "branch_list"
		# list branches for selection and return the selected branch
		branch_listlist = branch_list.stdout
		# print(f"branch_list.stdout (initial):\n{branch_listlist}")
		if remove_current_and_main_and_master_branch:
			# remove current, main, master branch from the list
			input_str_type = "delete_branch"
			branch_listlist = "\n".join(line for line in branch_listlist.split("\n")
											if not line.startswith("*") and
											("main" not in line) and
											("master" not in line))
			# print(f"branch_list.stdout (after removing current branch):\n{branch_listlist}")
		# print(f"branch_list.stdout (updated):\ns#{branch_listlist}#f")
		if not branch_listlist.strip():
			getCurrentBranchName = view_branch(action=100)
			getMainBranch = view_branch(new_branch="main", action=3)
			# print(f'getCurrentBranchName: {getCurrentBranchName}')
			# print(f'getMainBranch: {getMainBranch}')
			unifiedBranch = f"'{getMainBranch}' branch" if getMainBranch == getCurrentBranchName else f"your current '{getCurrentBranchName}' branch and '{getMainBranch}' branch"
			# final_string = f"There are no branches to delete except your {unifiedBranch if }) and/or {getMainBranch} branch."
			print_norm(f"There are no branches to delete except {unifiedBranch}.")
			quit("q")
		num, returned_list = print_stdout(branch_listlist, serial_numbered=1)
		item = collect_input(num, input_str_type)
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
		# check if the branch already exists or if you are already on this branch
		for line in (branch_list.stdout).split("\n"):
			if line.strip() == new_branch.strip():
				print_norm(f"The branch {new_branch} already exist.")
				quit("q")
			if line.startswith("*"):
				if (line.strip("*").strip()) == new_branch.strip():
					print_norm(f"You are currently on this branch({new_branch}).")
					quit("q")
	elif action == 100:
		# get current branch name
		for line in (branch_list.stdout).split("\n"):
			if line.startswith("*"):
				current_branch = (line.strip("*")).strip()
				return  current_branch
	elif action > 0:
		# check if you are not on the main or master branch before proceeding to stash your changes
		for line in (branch_list.stdout).split("\n"):
			if line.startswith("*") and (("master" not in line) or ("main" not in line)):
				stash(action)
				break


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
		create = run_subprocess(["git", "branch", new_branch_name])
		# if create.stdout:
		# 	print_stdout(create.stdout)
		# elif create.stderr:
		# 	print_stdout(create.stderr)
		print_stdout(f"{create.stdout if create.stdout else create.stderr}")
		setup_branch = run_subprocess(["git", "push", "-u", "origin", new_branch_name])
		print_stdout(setup_branch.stdout)
		print_stdout(setup_branch.stderr)
		branch_name = new_branch_name
	# commit the recent changes
	
	# print(f"commit before switching from {CYAN}{current_branch_name}{RESET} to {BRIGHT_MAGENTA}{branch_name}{RESET} at {formatted_date_time}")
	# commit_message = f"committed before switching from {current_branch_name} to {branch_name} at {formatted_date_time}"
	# print()
	# add_commit_all(type="all", commit_message=commit_message)
	
	# switch to next/new branch
	switch_branch = run_subprocess(["git", "checkout", branch_name])
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
	auto_stash = run_subprocess(["git", "stash", "apply"])
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
	current_branch_name = view_branch(action=100)
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
			to_stash = run_subprocess(["git", "stash", "save", message])
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
	stash = run_subprocess(["git", "stash", "list"])
	if stash.stdout:
		num, returned_list = print_stdout(stash.stdout, serial_numbered=1)
		item = collect_input(num, "stash")
		item = item - 1
		selection = (((returned_list[item]).split(":"))[0]).strip()
		paths_list = entry_point(action="extraction")
		for item in paths_list:
			untrack = run_subprocess(["git", "rm", "-rf", item])
			print_stdout(untrack.stdout)
			print_stdout(untrack.stderr)
		# apply stash
		stashed = run_subprocess(["git", "stash", "apply", selection])
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

def delete_branch():
	"""deletes branches locally and the corresponding remote branch.
	"""
	args = sys.argv
	len_args = len(args)
	# print(f'args: {args}')
	# print(f'len_args: {len_args}')
	if len_args > 1:
		print_norm("This command takes no argument.")
		print_norm("Try again.")
		quit("q")
	# if len_args == 1:
	selection = view_branch(remove_current_and_main_and_master_branch=True)
	print()
	print(f'selection: {selection}')
	currentBranch = run_subprocess(["git", "branch", "--show-current"])
	print(f'currentBranch.stdout: {currentBranch.stdout.strip()}')
	print(f'currentBranch.stderr: {currentBranch.stderr.strip()}')
	print_norm(f"This process will delete the branch locally and remotely.")
	print_norm(f"{BOLD}{RED}NOTE: It's not REVERSIBLE.{RESET}")
	print()
	deleteBrnch = prompt_1ch(f'Are you sure you want to delete the branch {BOLD}{RED}{selection}{RESET}? [y/N] [q] to quit >>> ')
	quit(deleteBrnch)
	if deleteBrnch.lower() == "y":
		# delete local branch
		delete_local = run_subprocess(["git", "branch", "-D", selection])
		if delete_local.stdout:
			print_stdout(delete_local.stdout)
		elif delete_local.stderr:
			print_stdout(delete_local.stderr)
		# delete remote branch
		delete_remote = run_subprocess(["git", "push", "origin", "--delete", selection])
		if delete_remote.stdout:
			print_stdout(delete_remote.stdout)
		elif delete_remote.stderr:
			print_stdout(delete_remote.stderr)
		print()
	else:
		print()
		print_norm("Branch deletion aborted.")
		quit("q")


# entry point for merge command
def merge_to_main_master():
	"""merge the current branch to the main/master branch
	"""
	current_branch_name = view_branch(action=100)
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
	rebase = run_subprocess(["git", "rebase", main])
	if rebase.stdout:
		print_stdout(rebase.stdout)
	elif rebase.stderr:
		print_stdout(rebase.stderr)
	create_or_switch_branch(main)
	merge = run_subprocess(["git", "merge", current_branch_name])
	if merge.stdout:
		print_stdout(merge.stdout)
	elif merge.stderr:
		print_stdout(merge.stderr)
	push(file_list=[])
	# print(f"switching back to other branch")
	# create_or_switch_branch(current_branch_name)


def diff(is_main_branch=False):
	"""display detailed changes on the current/main/master branch compared to
		its corresponding on the local/remote repository

	Args:
		is_main_branch (bool, optional): Defaults to False.
	"""
	if is_main_branch == 1:
		current_branch_name = view_branch(action=100)
		main = view_branch(new_branch="main", action=-2)
		print_norm(f'current branch: {current_branch_name}')
		print()

		# fetch changes from origin
		fetchChangesFromOrigin = run_subprocess(["git", "fetch", "origin"])
		if fetchChangesFromOrigin.stdout:
			print_norm(f'{fetchChangesFromOrigin.stdout}:stdout')
		elif fetchChangesFromOrigin.stderr:
			print_norm(f'{fetchChangesFromOrigin.stderr}:stderr')

	diff_res = run_subprocess(["git", "diff"] if is_main_branch else ["git", "diff", f"HEAD..origin/{main}"])
	# diff_res = run_subprocess(["git", "diff"] if is_main_branch else ["git", "diff", f"HEAD..origin/fake_main_branch"])
	if diff_res.returncode == 0:
		if diff_res.stdout:
			print_stdout(f'{diff_res.stdout}:stdout', status=1)
		elif diff_res.stderr:
			print_stdout(f'{diff_res.stderr}:stderr', status=1)
		else:
			print()
			print_norm(f"No changes found{'' if is_main_branch else ' on remote main/master branch'}.")
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
	run_subprocess_cmd_alone(['clear'])
	try:
		dir = (os.sep).join((repo_dir[0]).split(os.sep)[:-1])
	except:
		pass
	if repeat and dir_path:
		dir = (os.sep).join(dir_path.split(os.sep)[:-1])
	if child_dir:
		dir = repo_dir[0]
		repo_dir = os.listdir(repo_dir[0])
	gitignore_content = write_to_file([], delimiter, read=True)
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
	root = root_repo
	path = f'{root}{os.sep}.git{os.sep}config'
	config = run_subprocess(['cat', path])
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
	root = root_repo
	# path = f'{root}{os.sep}.git{os.sep}config_test'
	path = f'{root}{os.sep}.git{os.sep}config'
	config = run_subprocess(['cat', path])
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
		make_copy = run_subprocess(['cp', path, copy_of_config])
	add_token = run_subprocess(['sed', '-i', f's|{search_word}|{replacement}|g', path ])
	True and print(add_token.stderr, done)

	# if token != my_token:
	# 	save = prompt_1ch(f'\nSave "{BRIGHT_MAGENTA}{token[:8]}...{token[32:]}{RESET}" for future use? [y/N] >>> ')
	# 	if save.lower() == 'y' or save == '':
	# 		command_path = f"{os.path.join(os.path.expanduser('~'), '.xbin', 'pyfiles', 'git_codes.py')}"
	# 		save_token = run_subprocess(['sed', '-i', f's|{my_token}|{token}|g', command_path ])
	# 		True and print(save_token.stderr, done)
	# 	else:
	# 		print('Token not saved.')

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
# 	stashList = run_subprocess(["git", "stash", "list"])
# 	if stashList.stdout:
# 		print_stdout(f'$$$$$ {stashList.stdout} fxn')
# 	elif stashList.stderr:
# 		print_stdout(f'$$$$$ {stashList.stderr} fxn')
# 	else:
# 		print_norm(f"$$$$$ No stashes found. fxn")




# entry point for pull_from_main_or_master command
# def pull_from_main_or_master():
# 	"""pulls changes from the remote main/master branch into the current branch
# 	"""
# 	# print('in pull_from_main_or_master()')
# 	stashCreated = False
# 	main = view_branch(new_branch="main", action=-2)

# 	current_branch_name = view_branch(action=100)
# 	print_norm(f'current branch: {current_branch_name}')
# 	if current_branch_name in ["main", "master"]:
# 		print_norm(f"You are on {main} branch.")
# 		print_norm(f"Switch to the desired branch you want to pull {main} into.")
# 		quit("q")
# 	# print("Exiting early...");sys.exit()

# 	# stash changes, if any
# 	stashChanges = run_subprocess(['git', 'status', '--porcelain'])
# 	if stashChanges.stdout.strip():
# 		run_subprocess(['git', 'stash', '--include-untracked'])
# 		stashCreated = True
# 		# print_norm("Stashed local changes...")
# 	else: # consider removing
# 		print_norm("No local changes to stash. Proceeding with rebase...")

# 	# fetch changes from origin
# 	fetchChangesFromOrigin = run_subprocess(["git", "fetch", "origin"])
# 	# print("for: fetchChangesFromOrigin")
# 	# print(f">>>> stdout-start:\n{fetchChangesFromOrigin.stdout}\n<<<<")
# 	# print(f"♧♧♧♧ stderr-start:\n{fetchChangesFromOrigin.stderr}\n♧♧♧♧")
# 	if fetchChangesFromOrigin.stdout:
# 		print_norm(f'{fetchChangesFromOrigin.stdout}:fetch_stdout')
# 	elif fetchChangesFromOrigin.stderr:
# 		print_norm(f'{fetchChangesFromOrigin.stderr}:fetch_stderr')
# 		# quit("q")

# 	# rebase from main/master branch
# 	rebaseFromMain = run_subprocess(["git", "merge", f"origin/{main}"])
# 	# print("for: rebaseFromMain")
# 	# print(f">>>> stdout-start:\n{rebaseFromMain.stdout}\n<<<<")
# 	# print(f"♧♧♧♧ stderr-start:\n{rebaseFromMain.stderr}\n♧♧♧♧")
# 	if rebaseFromMain.stdout:
# 		print_norm(f'{rebaseFromMain.stdout}:rbaseM_stdout')
# 	elif rebaseFromMain.stderr:
# 		print_norm(f'{rebaseFromMain.stderr}:rbaseM_stderr')

# 	# addition from phone starts 1 here
# 	rOut = rebaseFromMain.stdout.replace('\n', ' ')
# 	rErr = rebaseFromMain.stderr.replace('\n', ' ')
# 	chechForMergeConflicts = f"{rOut} {rErr}"
# 	stashCreated and print_norm("adding local changes ontop of update...")
# 	if 'you have unmerged files'.lower() in chechForMergeConflicts.lower() or 'CONFLICT' in chechForMergeConflicts or 'Resolve all conflicts manually'.lower() in chechForMergeConflicts.lower():
# 	# if 'you have unmerged files'.lower() in chechForMergeConflicts.lower() or 'Resolve all conflicts manually'.lower() in chechForMergeConflicts.lower():
# 	# if 'you have unmerged files' in chechForMergeConflicts:
# 		print_norm(f'{rebaseFromMain.stdout}\n:rebFrmMain.stdout')
# 		print_norm(f'{rebaseFromMain.stderr}\n:rebFrmMain.stderr')
# 		# print_norm(rebaseFromMain.stderr)
# 		check_for_conflicts()
# 		pop_stash(stash_status=stashCreated)
# 		stashCreated = False
# 		# addition from phone ends 1 here

# 	# pop stash if one was created
# 	if stashCreated:
# 		# addition from phone starts 2 here
# 		popStash = run_subprocess(["git", "stash", "pop"])
# 		# print(f'popStash: {popStash}')
# 		pOut = popStash.stdout.replace('\n', ' ')
# 		pErr = popStash.stderr.replace('\n', ' ')
# 		pchechForMergeConflicts = f"{pOut} {pErr}"
# 		if 'you have unmerged files'.lower() in pchechForMergeConflicts.lower() or 'CONFLICT' in pchechForMergeConflicts or 'Resolve all conflicts manually'.lower() in pchechForMergeConflicts.lower():
# 		# if 'you have unmerged files'.lower() in pchechForMergeConflicts.lower():
# 		# if 'CONFLICT' in pchechForMergeConflicts:
# 			print_norm(f'{popStash.stdout}\n:popStash.stdout')
# 			print_norm(f'{popStash.stderr}\n:popStash.stderr')
# 			# print('Found=> CONFLICT :::::in stdout and stderr (stash)')
# 			# print_norm(popStash.stderr)
# 			check_for_conflicts(rebase_in_progress=False)
# 			pop_stash(stash_status=stashCreated)
# 			stashCreated = False
# 			# addition from phone ends 2 here

# 		# if popStash.stdout:
# 		# 	print_norm(f'{popStash.stdout}:stdout')
# 		# elif popStash.stderr:
# 		# 	print_norm(f'{popStash.stderr}:stderr')
# 	# cleanup = run_subprocess(['git', 'stash', 'list'])
# 	# print(f"stashes:\n{cleanup.stdout}")
# 	# if cleanup.stdout.strip():
# 	# 	print_norm("Cleaning up...")
# 	# 	run_subprocess(['git', 'stash', 'drop'])  # drops top stash (stas


# entry point for show_diff_from_main_or_master command
# def show_diff_from_main_or_master():
# 	"""shows all the changes on the remote main/master branch compared to the current branch
# 	"""
# 	# current_branch_name = view_branch(action=100)
# 	# main = view_branch(new_branch="main", action=-2)
# 	# print_norm(f'current branch: {current_branch_name}')

# 	# # fetch changes from origin
# 	# fetchChangesFromOrigin = run_subprocess(["git", "fetch", "origin"])
# 	# if fetchChangesFromOrigin.stdout:
# 	# 	print_norm(f'{fetchChangesFromOrigin.stdout}:stdout')
# 	# elif fetchChangesFromOrigin.stderr:
# 	# 	print_norm(f'{fetchChangesFromOrigin.stderr}:stderr')

# 	# diff changes from main/master branch
# 	diffComparedToMain = run_subprocess(["git", "diff", f"HEAD..origin/{main}"])
# 	if diffComparedToMain.returncode == 0:
# 		if diffComparedToMain.stdout:
# 			print_stdout(f'{diffComparedToMain.stdout}:stdout', status=1)
# 		elif diffComparedToMain.stderr:
# 			print_stdout(f'{diffComparedToMain.stderr}:stderr', status=1)
# 		else:
# 			print()
# 			print_norm("No changes found on the remote main/master branch.")
# 			print_norm("Your working directory is in the same state as your last commit.")
# 	elif diffComparedToMain.returncode > 0:
# 		print_norm("Oops! I got:")
# 		print_norm("{}".format(print_stdout(diffComparedToMain.stderr)))

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
