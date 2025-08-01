#!/usr/bin/env python3

import subprocess, sys, os, time, shlex
from datetime import datetime
from pyfiles.verify_repo_new import entry_point
from pyfiles.my_prompt import main as prompt_1ch
from pyfiles.print import print_stdout, write_to_file, backward_search, print_norm, quit_program
from pyfiles.configure_settings_py import compile_dir_list, list_filter, check_for_venv_or_node_modules
from pyfiles.colors import *
from pyfiles.subprocessfxn import run_subprocess, run_subprocess_cmd_alone, run_interactive_subprocess, subprocess_for_pull_command, run_subprocess_live
from pyfiles.keyboardInterruption import auto_wrap_interrupt_guard
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
formatted_stash_time = int(datetime.now().timestamp())

def exit2(leave: bool = False):
	if leave == True:
		quit_program("q")

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
		quit_program('q')
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
			quit_program('q')
		# elif len(choice) == 0:
		if allowedEntryArray:
			if choice in allowedEntryArray:
				return choice
		else:
			if choice:
				return choice
		print_norm(invalidText)
		print()

############################################################################
def get_conflicted_files():
	code, out, _ = subprocess_for_pull_command("git diff --name-only --diff-filter=U")
	return out.splitlines() if out else []

def get_file_content_as_list(filepath):
	with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
		lines = f.readlines()
	return lines

def resolve_conflict(filepath):
	conflict_start = '<<<<<<<'
	conflict_middle = '======='
	conflict_end = '>>>>>>>'
	conflict_number = 0

	lines = get_file_content_as_list(filepath)

	a_line = get_conflict_label(lines, conflict_start).strip()
	b_line = get_conflict_label(lines, conflict_end).strip()
	resolved = []
	i = 0
	while i < len(lines):
		if lines[i].startswith(conflict_start):
			version_a = []
			version_b = []
			i += 1
			while i < len(lines) and not lines[i].startswith(conflict_middle):
				version_a.append(lines[i])
				i += 1
			i += 1  # Skip the =======
			while i < len(lines) and not lines[i].startswith(conflict_end):
				version_b.append(lines[i])
				i += 1
			i += 1  # Skip the >>>>>>>
			# print("\nConflict detected in file:", filepath)
			conflict_number += 1
			print_norm(f"{BOLD}{BLUE}{UNDERLINE}for conflict: {conflict_number}{RESET}")
			print_norm(f"(A){a_line} or (B){b_line}?")
			# print(f"B ({b_line}) version:")
			promptText = "::::: Choose version to keep (A/B) >>> "
			choice_options = ['a', 'b']
			invalidText = "Invalid choice. Please enter 'A' or 'B', [q to quit]."
			choice = getUserInput(promptText=promptText, allowedEntryArray=choice_options, invalidText=invalidText)
			print()
			if choice == 'b':
				resolved.extend(version_b)
			else:
				resolved.extend(version_a)
		else:
			resolved.append(lines[i])
			i += 1

	with open(filepath, 'w', encoding='utf-8') as f:
		f.writelines(resolved)
	run_subprocess(['git', 'add', filepath])

def show_conflict_blocks(filepath):
	conflict_start = '<<<<<<<'
	conflict_middle = '======='
	conflict_end = '>>>>>>>'
	conflict_number = 0

	try:
		mid_index = -1
		strt_index = -1
		lines = get_file_content_as_list(filepath)

		first = get_conflict_label(lines, conflict_start) + ' '
		second = get_conflict_label(lines, conflict_end) + ' '
		# last = ''

		# print(f'filepath: {filepath}')
		filename = f"{('/').join(filepath.split('/')[:-1])}/{BOLD}{MAGENTA}{filepath.split('/')[-1]}{RESET}" if '/' in filepath else f'{BOLD}{MAGENTA}{filepath.split(".")[-1] if filepath.startswith(".") else filepath}{RESET}'
		print_norm(f"\nDetails of conflict in {filename}:")

		in_conflict = False
		for i, line in enumerate(lines):
			stripped_line = line.strip()

			if i == strt_index:
				print_norm(f"line: {i+1} {stripped_line}	{BOLD}{YELLOW} <- {UNDERLINE}{first}starts here{RESET}")
			elif i == mid_index:
				print_norm(f"line: {i+1} {stripped_line}	{BOLD}{GREEN} <- {UNDERLINE}{second}starts here{RESET}")
			elif stripped_line.startswith(conflict_start):
				in_conflict = "A"
				# first = line.split(conflict_start)[-1].strip()
				strt_index = i + 1
				conflict_number += 1
				print_norm(f"line: {i+1} {stripped_line}	{BOLD}{BLUE} <= {UNDERLINE}conflict: {conflict_number}{RESET}")
			elif stripped_line.startswith(conflict_middle):
				in_conflict = "B"
				mid_index = i + 1
				print_norm(f"line: {i+1} {stripped_line}")
			elif stripped_line.startswith(conflict_end):
				# second = line.split(conflict_end)[-1].strip()
				print_norm(f"line: {i+1} {stripped_line}	{BOLD}{ITALIC}{BRIGHT_CYAN} <- {UNDERLINE}end of conflict{RESET}\n")
				print("\n")
				in_conflict = False
			elif in_conflict:
				print_norm(f"line: {i+1} {stripped_line}")
		# print(f"mid_index: {mid_index}")
		# return first, second
	except FileNotFoundError:
		print_norm(f"File not found: {filepath}")

def check_and_resolve_conflicts(incoming_branch=None, current_branch=None, is_from_stash=False, stash_msg=None):
	conflicted_files = get_conflicted_files()
	if not conflicted_files:
		print_norm("No merge conflicts detected.")
		return
	length_of_conflicted_files = len(conflicted_files)
	add_s = 's' if length_of_conflicted_files > 1 else ''
	print_norm(f"\nFound {length_of_conflicted_files} conflicted file{add_s}:")
	for f in conflicted_files:
		if is_binary(f):
			print_norm(f"Skipping binary file: {f} (cannot resolve textually)")
			continue

		# print(f" - {f}")
		show_conflict_blocks(f)

	# for f in conflicted_files:
		resolve_conflict(f)

	print_norm("\nAll conflicts resolved.")
	if not is_from_stash:
		return is_from_stash
	result = run_subprocess(['git', 'rev-parse', '--git-dir'])
	git_dir = result.stdout.strip()
	merge_head = os.path.exists(os.path.join(git_dir, 'MERGE_HEAD'))
	rebase_apply = os.path.exists(os.path.join(git_dir, 'rebase-merge')) or os.path.exists(os.path.join(git_dir, 'rebase-apply'))
	if merge_head or rebase_apply:
		unmerged_files = subprocess.check_output(["git", "diff", "--name-only", "--diff-filter=U"]).decode().strip()
		if unmerged_files:
			print("❗ Unresolved merge conflicts remain:\n" + unmerged_files)
			print("❌ Resolve all conflicts and run again.")
			quit_program('q', 1)
	if merge_head:
		commit_changes(stash_msg=stash_msg, operation_type="merge", incoming_branch=incoming_branch, current_branch=current_branch)
	elif rebase_apply:
		commit_changes(stash_msg=stash_msg, operation_type="rebase", incoming_branch=incoming_branch, current_branch=current_branch)

def restore_stash(is_stashed, message, branch, current_branch):
	if is_stashed:
		print_norm("Restoring stashed changes...")
		_, stash_list_out, _ = subprocess_for_pull_command('git stash list')
		stash_id = None
		for line in stash_list_out.splitlines():
			if message in line:
				stash_id = line.split(':')[0]
				break
		if stash_id:
			try:
				result = run_subprocess(['git', 'stash', 'pop', stash_id])
				if result.returncode == 0:
					print_norm("Restore successful!")
				else:
					print_norm(f"Restore failed due to conflicts. Your changes are still in: {stash_id}")
					print_norm("Attempting to help resolve stash conflicts interactively...")
					check_and_resolve_conflicts(incoming_branch=branch, current_branch=current_branch, is_from_stash=True)
					print_norm("Conflict resolution complete for stashed changes.")
			except Exception:
				print_norm("Restore failed. Please recover manually in stashes.")
		else:
			print_norm("Expected stash not found. You may need to restore it manually.")

def commit_changes(stash_msg=None, operation_type="merge", incoming_branch=None, current_branch=None, msg=False):
	if not incoming_branch and not current_branch:
		print_norm("No branches specified for commit message.")
		print_norm("Kind provide the branch names to use in the commit message.")
		quit_program('q')
	print()
	commit_message = input(
		f"Enter a commit message for the {operation_type}.\n"
		f"- Press Enter to use a default message\n"
		# f"- Type (q) to exit without doing anything\n"
		f"- Type (a) to abort the {operation_type} operation\n"
		"::::: >>> "
		).strip()
	# if commit_message.lower() == 'q':
	# 	print_norm(f"Restoring working directory...")
	# 	run_subprocess_live(["git", operation_type, "--abort"])
	# 	restore_stash(is_stashed=True, message=stash_msg, branch=incoming_branch, current_branch=current_branch)
	# 	print_norm(f"{operation_type.title()} operation stopped.")
	# 	quit(commit_message.lower()) # if q is pressed, exit the operation
	if commit_message.lower() == 'a':
		print()
		print_norm(f"Aborting {operation_type} operation...")
		run_subprocess_live(["git", operation_type, "--abort"])
		print_norm("Restoring working directory...")
		restore_stash(is_stashed=True, message=stash_msg, branch=incoming_branch, current_branch=current_branch)
		print_norm(f"{operation_type.title()} operation aborted.")
		quit_program('q')
	if not commit_message and incoming_branch and current_branch:
		commit_message = f"{operation_type.title()} remote-tracking branch 'origin/{incoming_branch}' into {current_branch} resolved on {formatted_now}"
	print()
	print_norm(f"Using commit message:\n  {commit_message}")
	print()
	if msg:
		return commit_message
	if operation_type == "merge":
		run_subprocess_live(["git", "commit", "-m", commit_message])
		print_norm(f"{operation_type.title()} commit completed.")
	else:
		run_subprocess_live(["git", operation_type, "--continue"])
		print_norm("Rebase continued.")

def is_fast_forward(branch_name=None):
	fetch_for_base = run_subprocess(["git", "fetch", "origin"])
	print(f'fetch_for_base output: {fetch_for_base.stdout}')
	print(f'fetch_for_base stderr: {fetch_for_base.stderr}')
	print(f'fetch_for_base returncode: {fetch_for_base.returncode}')
	result = run_subprocess(["git", "merge-base", "--is-ancestor", "HEAD", f"origin/{branch_name}"])
	print(f"merge-base output: {result.stdout.strip()}")
	print(f"merge-base returncode: {result.returncode}")
	print(f"merge-base stderr: {result.stderr.strip()}")
	if result.returncode == 0:
		return True  # Fast-forward possible
	return False     # Not fast-forward (diverged or up-to-date or behind)

def check_merge_type(branch_name):
	# Compare local and remote branch history
	result = run_subprocess(["git", "rev-list", "--left-right", "--count", f"HEAD...origin/{branch_name}"])
	output = result.stdout.strip()
	# print(f"rev-list output: {output}")

	merge_type = "unknown"

	if not output:
		return merge_type, None, None

	local_ahead, remote_ahead = map(int, output.split())

	if local_ahead == 0 and remote_ahead > 0:
		merge_type = "fast-forward"
		return merge_type, local_ahead, remote_ahead
	elif local_ahead > 0 and remote_ahead > 0:
		merge_type = "diverged"
		# if is_fast_forward(branch_name):
		# 	merge_type = "fast-forward"
		# 	return merge_type
		return merge_type, local_ahead, remote_ahead
	elif local_ahead == 0 and remote_ahead == 0:
		merge_type = "up-to-date"
		return merge_type, local_ahead, remote_ahead
	else:
		return merge_type, None, None

def check_for_merge_conflict(branch_name=None):
	"""Check for merge conflicts when merging a branch into the current branch."""
	if not branch_name:
		print_norm("No branch name provided. Cannot check for merge conflicts.")
		quit_program('q')
	merge_type, merge_type_tag, local_ahead, remote_ahead = None, None, None, None
	merge_type, local_ahead, remote_ahead = check_merge_type(branch_name)
	# print(f'merge_type: {merge_type}')

	# if merge_type == "up-to-date":
	# 	merge_type_tag = 'no commit'

	# merge_command = ["git", "merge", "--no-commit", "--no-ff", f"origin/{branch_name}"]
	check_for_merge_conflicts = None
	# Check/perform a merge operation/is already in progress
	if merge_type == "fast-forward":
		run_subprocess_live(["git", "merge", "--no-commit", f"origin/{branch_name}"])
	else:
		check_for_merge_conflicts = run_subprocess(["git", "merge", "--no-commit", "--no-ff", f"origin/{branch_name}"])

	if check_for_merge_conflicts:
		stdout = check_for_merge_conflicts.stdout.lower()
		stderr = check_for_merge_conflicts.stderr.lower()
		returncode = check_for_merge_conflicts.returncode

		# print(f'check_for_merge_conflicts.stdout: {check_for_merge_conflicts.stdout}')
		# print(f'check_for_merge_conflicts.stderr: {check_for_merge_conflicts.stderr}')
		# print(f'check_for_merge_conflicts.returncode: {returncode}')

		# Look for known conflict indicators
		conflict_keywords = [
			"automatic merge failed".lower(),
			"conflict (content)".lower(),
			"merge conflict".lower()
		]

		# Combine outputs
		combined_output = f"{stdout} {stderr}"

		if any(word in combined_output for word in conflict_keywords) or returncode != 0:
			# print_norm("Merge conflict detected. sending signal for interactive resolution...")
			# print_norm("Merge conflict detected. Aborting merge to restore original state...")
			# restore_init_state = run_subprocess(["git", "merge", "--abort"])
			# print(f'restore_init_state.stdout: {restore_init_state.stdout}')
			# print(f'restore_init_state.stderr: {restore_init_state.stderr}')
			# print(f'restore_init_state.returncode: {restore_init_state.returncode}')
			merge_type_tag = None
			return True, merge_type, merge_type_tag, local_ahead, remote_ahead
		if returncode == 0 and "Already up to date".lower() in combined_output.replace('\n', ' ').lower() or merge_type == "up-to-date":
			# print_norm("No merge conflict detected.")
			# print(f'returncode: {returncode}')
			merge_type_tag = 'no commit'
			return False, merge_type, merge_type_tag, local_ahead, remote_ahead

	# print_norm("No merge conflict detected.")
	return False, merge_type, merge_type_tag, local_ahead, remote_ahead

def get_conflict_label(lines, marker):
	conflict_label = ''
	for index, line in enumerate(lines):
		if line.startswith(marker):
			# first_conflict_line = line
			conflict_label = line[len(marker):].strip()  # gets text after marker
			break
	return conflict_label

# def count_conflicts(filepath):
# 	conflict_start = '<<<<<<<'
# 	conflict_middle = '======='
# 	conflict_end = '>>>>>>>'
# 	lines = get_file_content_as_list(filepath)
# 	count = 0
# 	# start_line_with_conflicts = []
# 	i = 0
# 	while i < len(lines):
# 		if lines[i].startswith(conflict_start):
# 			has_middle = False
# 			has_end = False
# 			# if i < len(lines):
# 			# 	found_line = lines[i].strip()
# 			# else:
# 			# 	found_line = "<empty>"
# 			i += 1
# 			while i < len(lines):
# 				if lines[i].startswith(conflict_middle):
# 					has_middle = True
# 				elif lines[i].startswith(conflict_end):
# 					has_end = True
# 					break
# 				i += 1
# 			if has_middle and has_end:
# 				count += 1
# 				# if found_line != "<empty>":
# 				# 	start_line_with_conflicts.append(f"{count}øŋ{found_line}")
# 		else:
# 			i += 1
# 	return count

def is_binary(file_path):
	result = run_subprocess(["git", "check-attr", "binary", file_path])
	return "binary: set" in result.stdout
############################################################################

def is_rebase_in_progress():
	result = run_subprocess(['git', 'rev-parse', '--git-dir'])
	git_dir = result.stdout.strip()
	# print(f'git_dir: {git_dir}')
	response = os.path.exists(os.path.join(git_dir, 'rebase-merge')) or os.path.exists(os.path.join(git_dir, 'rebase-apply'))
	# print(f'is_rebase_in_progress: {response}')
	return response

def is_merge_in_progress(check_remote_branch=None):
	fatal1 = "(MERGE_HEAD exists)".lower()
	fatal2 = "commit your changes before you merge".lower()
	check_merge = run_subprocess(["git", "merge", "--no-commit", "--no-ff", f"origin/{check_remote_branch}"])
	response = "{} {}".format(check_merge.stdout.replace('\n', ' '), check_merge.stderr.replace('\n', ' ')).lower()
	if fatal1 in response or fatal2 in response:
		print_norm("Merge in progress. Please resolve conflicts before proceeding.")
		return True
	return False
	# result = run_subprocess(['git', 'rev-parse', '--git-dir'])
	# git_dir = result.stdout.strip()
	# response = os.path.exists(os.path.join(git_dir, 'MERGE_HEAD'))
	# return response

def get_git_state():
	git_dir = subprocess.check_output(['git', 'rev-parse', '--git-dir']).decode().strip()
	return {
		"merge": os.path.exists(os.path.join(git_dir, "MERGE_HEAD")),
		"rebase": os.path.exists(os.path.join(git_dir, "rebase-merge")) or os.path.exists(os.path.join(git_dir, "rebase-apply"))
	}

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
	# elif is_merge_in_progress():
	# 	merge_operation()
	else:
		pass
		# print_norm("No rebase or merge in progress.")
		# return True

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
	# print()
	print_norm("#### pulling ...################################################")
	# try:
	current_branch_name = view_branch(action=100)
	main = view_branch(new_branch="main", action=-2)
	use_branch = main if is_main_branch else current_branch_name
	stashed = False
	stash_msg = ""

	print_norm(f"Pulling updates from origin/{use_branch}\n")

	# Fetch from origin
	fetch_from_origin = run_subprocess(['git', 'fetch', 'origin'])
	# print(f'fetch_from_origin.stdout: {fetch_from_origin.stdout}')
	# print(f'fetch_from_origin.stderr: {fetch_from_origin.stderr}')
	# print(f'fetch_from_origin.returncode: {fetch_from_origin.returncode}')

	# Determine if we need to stash
	if check_unstaged_or_untracked():
		print_norm("Local changes detected. Stashing...")
		# print()
		stash_msg = f"temp-stash-before-merge-{formatted_stash_time}"
		git_stash = run_subprocess(['git', 'stash', 'push', '-u', '-m', stash_msg])
		# print(f"git_stash.stdout: {git_stash.stdout}")
		# print(f"git_stash.stderr: {git_stash.stderr}")
		stashed = True
	# else:
	# 	pass
		# stashed = False
		# stash_msg = ""

	# Merge (do not raise exception on failure)
	# print(f"Synchronising origin/{use_branch}...")
	print()
	# print("start of merge operation...")
	state = get_git_state()
	if state["merge"]:
		print(f"Merge in progress on branch {current_branch_name}")
		commit_changes(stash_msg=stash_msg, operation_type="merge", incoming_branch=use_branch, current_branch=current_branch_name)
	elif state["rebase"]:
		print(f"Rebase in progress on branch {current_branch_name}")
		commit_changes(stash_msg=stash_msg, operation_type="rebase", incoming_branch=use_branch, current_branch=current_branch_name)
	is_merge_conflict, merge_type, merge_tag, local_ahead, remote_ahead = check_for_merge_conflict(branch_name=use_branch)
	# print(f'\nis_merge_conflict: {is_merge_conflict}')
	# print(f'merge_type: {merge_type}')
	# print(f'merge_tag: {merge_tag}')
	# print(f'local_ahead: {local_ahead}')
	# print(f'remote_ahead: {remote_ahead}\n')
	if is_merge_conflict:
		print_norm("Merge conflict occurred. Attempting to resolve interactively...")
		proceed_to_pop_stash = check_and_resolve_conflicts(incoming_branch=use_branch, current_branch=current_branch_name, stash_msg=stash_msg)
		merge_success = proceed_to_pop_stash  # After successful resolution
		# merge_command = ['git', 'merge', f'origin/{use_branch}']
	else:
		if merge_tag == "no commit":
			print_norm("Already up to date.")
			merge_success = True
		elif merge_type == "fast-forward":
			merge_success = True
		elif merge_type == "up-to-date":
			merge_success = True
		elif merge_type == "diverged":
			local_is_ahead = {'first': f'{current_branch_name}', 'fhead': local_ahead, 'second': f'origin/{use_branch}', 'rhead': remote_ahead} if local_ahead > remote_ahead else {'first': f'origin/{use_branch}', 'fhead': remote_ahead, 'second': f'{current_branch_name}','rhead': local_ahead}
			print_norm("Your branches have diverged. you need to merge them with a commit...")
			print_norm(f"{local_is_ahead['first']} branch has diverged by {local_is_ahead['fhead']} commit{'s' if local_ahead > 1 else ''} and {local_is_ahead['second']} branch has diverged by {local_is_ahead['rhead']} commit{'s' if remote_ahead > 1 else ''}.")
			print_norm(f"Merging updates from origin/{use_branch} into {current_branch_name} branch...")
			merge_commit_msg = commit_changes(stash_msg=stash_msg, operation_type="merge", incoming_branch=use_branch, current_branch=current_branch_name, msg=True)
			merge_result = run_subprocess(['git', 'commit', '-m', merge_commit_msg])
			# print(f'merge_result.stdout: {merge_result.stdout}')
			# print(f'merge_result.stderr: {merge_result.stderr}')
			# print(f'merge_result.returncode: {merge_result.returncode}')
			merge_success = merge_result.returncode == 0
 
 
 
	# # print("exiting..."); quit_program('q')
	# merge_result = run_subprocess_live(['git', 'merge', f'origin/{use_branch}'])
	# # merge_result = run_subprocess(['git', 'merge', f'origin/{use_branch}'])
	# # print(f"merge_result.stdout: {merge_result.stdout}")
	# # print(f"merge_result.stderr: {merge_result.stderr}")
	# # merge_result_message = "\n".join([
	# # 	line for line in f"{merge_result.stdout}{merge_result.stderr}".splitlines()
	# # 	if "Merge made by the 'ort' strategy" not in line.strip()
	# # ])
	# # # print(f'merge_result_message: {merge_result_message}')
	# # print_stdout(merge_result_message.strip())
	# # print('middle')
	# # print_norm(merge_result_message)
	# print("end of merge operation...")
	# merge_success = merge_result.returncode == 0

	# print(f'merge_result: {merge_result}')
	# print(f"merge_tag!=no commit or merge_type!=fast-forward: {merge_tag!='no commit' or merge_type!='fast-forward'}")
	(merge_tag!="no commit" and merge_type!="fast-forward") and print()
	if merge_success:
		merge_tag != "no commit" and print_norm("Pull successful!")
	else:
		print_norm("Pull failed. Manual intervention might be required.")

	print()

	# Restore stash only if merge was successful
	if stashed and merge_success:
		restore_stash(is_stashed=stashed, message=stash_msg, branch=use_branch, current_branch=current_branch_name)
	# Inform user about stash if merge failed
	if stashed and not merge_success:
		print_norm(f"Operation failed. Your changes were stashed as: {stash_msg}")
		print_norm("You can recover them with:")
		print_norm("    git stash list")
		print_norm("    git stash pop <stash@{{N}}>")

#######################################################################

def push(file_list: list=None):
	"""This function takes a list as argument and Updates the
		remote with the changes on the local machine.

	Args:
		file_list (list): list of files in the current working directory
	"""
	if 'custom_commands' in os.getcwd():
		subprocess.run(["bash", "bumpCCVersion"], cwd=bumpCCVersion, stdout=None, stderr=None)
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
		quit_program('q')

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
		quit_program('q')
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
		quit_program(commit_message)
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
		subprocess.run(["bash", "bumpAppJsonVersion"], cwd=bumpAppJsonVersionScript, stdout=None, stderr=None)
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
	quit_program('q')

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
			quit_program(item)
		elif string == "delete_branch":
			item = prompt_1ch('Select the branch to delete. [q] to quit >>> ')
			quit_program(item)
		elif string == "stash":
			print_norm(F"{RED}NOTE: IF YOU QUIT. YOUR STASH WILL NOT BE APPLIED TO THIS BRANCH.{RESET}")
			item = prompt_1ch('Select the stash you wish to apply. [q] to quit >>> ')
			quit_program(item)
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
											(" main" not in line) and
											(" master" not in line))
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
			quit_program("q")
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
				quit_program("q")
			if line.startswith("*"):
				if (line.strip("*").strip()) == new_branch.strip():
					print_norm(f"You are currently on this branch({new_branch}).")
					quit_program("q")
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
				quit_program(resp)
				if resp.lower() == "c":
					response = prompt_1ch("Use default commit message? [y/N] [q] to quit >>> ")
					quit_program(response)
					if response.lower() == "y" or response == "":
						message = default_commit_message
					elif response.lower() == "n":
						message = input("Enter your commit message. [q] to quit >>> ")
						quit_program(message)
					print("Invalid response.")
				elif resp.lower() == "s":
					response = prompt_1ch("Use default stash message? [y/N] [q] to quit >>> ")
					quit_program(response)
					if response.lower() == "y" or response == "":
						message = default_stash_message
					elif response.lower() == "n":
						message = input("Enter your stash message. [q] to quit >>> ")
						quit_program(message)
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
			quit_program(create_branch)
			if create_branch.lower() == "y":
				break
			elif create_branch.lower() == "n":
				quit_program("q")
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
		quit_program("q")
	# if len_args == 1:
	selection = view_branch(remove_current_and_main_and_master_branch=True)
	print()
	# print(f'selection: {selection}')
	currentBranch = run_subprocess(["git", "branch", "--show-current"])
	# print(f'currentBranch.stdout: {currentBranch.stdout.strip()}')
	# print(f'currentBranch.stderr: {currentBranch.stderr.strip()}')
	print_norm(f"This process will delete the branch locally and it's corresponding remote version.")
	print_norm(f"{BOLD}{RED}NOTE: It's not REVERSIBLE.{RESET}")
	print()
	deleteBrnch = prompt_1ch(f'Are you sure you want to delete the branch {BOLD}{RED}{selection}{RESET}? [y/N] [q] to quit >>> ')
	quit_program(deleteBrnch)
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
		quit_program("q")


# entry point for merge command
def merge_to_main_master():
	"""merge the current branch to the main/master branch
	"""
	current_branch_name = view_branch(action=100)
	if current_branch_name == "main" or current_branch_name == "master":
		print_norm(f"You are in {current_branch_name} branch.")
		print_norm(f"Switch to the desired branch you want to merge to {current_branch_name}.")
		quit_program("q")
	while True:
		print()
		check = prompt_1ch("Are you sure that you want to merge this branch to main/master? [y/N] >>> ")
		if check.lower() == "y":
			break
		elif check.lower() == "n":
			quit_program("q")
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


def diff(is_main_branch=False, file: str=None):
	"""display detailed changes on the current/main/master branch compared to
		its corresponding on the local/remote repository

	Args:
		is_main_branch (bool, optional): Defaults to False.
	"""
	current_branch_name = view_branch(action=100)
	main = view_branch(new_branch="main", action=-2)
	use_branch = main if is_main_branch else current_branch_name
	git_command = ["git", "diff", file] if file else (["git", "diff", f"HEAD..origin/{main}"] if is_main_branch else ["git", "diff"])
	if is_main_branch:
		print_norm(f'current branch: {current_branch_name}')
		print()

		# fetch changes from origin
		fetchChangesFromOrigin = run_subprocess(["git", "fetch", "origin", use_branch])
		if fetchChangesFromOrigin.stdout:
			print_norm(f'{fetchChangesFromOrigin.stdout}:stdout')
		elif fetchChangesFromOrigin.stderr:
			print_norm(f'{fetchChangesFromOrigin.stderr}:stderr')

	# print(f'is_main_branch: {is_main_branch}')
	# print(f'git_command: {git_command}')
	
	diff_res = run_subprocess(git_command)
	if diff_res.returncode == 0:
		if diff_res.stdout:
			print_stdout(f'{diff_res.stdout}:stdout', status=1, main=is_main_branch)
		elif diff_res.stderr:
			print_stdout(f'{diff_res.stderr}:stderr', status=1, main=is_main_branch)
		else:
			print()
			print_norm(f"No changes found{f' on remote origin/{main}' if is_main_branch else (f' in {os.path.basename(file)}' if file else '')}.")
			not file and print_norm("Your working tree is squeaky clean .")
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
	quit_program(selection)
	cur_dir = ""
	try:
		selection = int(selection)
		item = dir_list[selection - 1]
	except ValueError:
		print("Invalid selection. Please enter a valid integer.")
		quit_program('q', 1)
	except IndexError:
		print("Selection is out of range. Please enter a valid number.")
		quit_program('q', 1)
	cur_dir = f'{dir}{os.sep}{item}'
	# print(f'You selected: {cur_dir}')
	print()
	if os.path.isdir(cur_dir):
		print('[n] - to add the dir to .gitignore file')
		open_dir = prompt_1ch(f'You want to explore {item}? [y/N] [q] - quit >>> ')
		quit_program(open_dir)
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
			quit_program('q', 1)
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
		quit_program('q', 1)
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
			quit_program('q')
	elif len(github_url[0][2]) == 10:
		print(f'New token: {BRIGHT_MAGENTA}{token[:8]}...{token[32:]}{RESET}')
		adding = prompt_1ch(f"\nAdd it to your local credentials ? [y/N] >>> ")
		if adding.lower() != 'y' and adding == '':
			print(abort_op)
			quit_program('q')
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
			quit_program('q')
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

auto_wrap_interrupt_guard(globals())
