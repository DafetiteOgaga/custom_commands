#!/usr/bin/env python3

import time
from pyfiles.subprocessfxn import run_subprocess
from pathlib import Path
from pyfiles.verify_repo_new import entry_point
try:
	from .colors import *
except ImportError:
	from colors import *

def print_stdout(stdout: str, index: int=0, serial_numbered: int=0, status: int=0):
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

	# if stdout == None:
	# 	std_list = []
	# else:
	# 	std_list = (stdout.split("\n"))[:-1]
	std_list = std_list = [] if stdout == None else (stdout.split("\n"))[:-1]
	i = 0
	for_untrack = 0
	status_line = None
	for i, line in enumerate(std_list):
		time.sleep(.03)
		if status:
			if isinstance(status_line, int):
				if i == status_line + 1:
					line = f"{BOLD}{BRIGHT_YELLOW}{line}"
				elif (i >= status_line + 2) and (line.startswith('+++') or line.startswith('---')):
					line = f"{ITALIC}{BRIGHT_WHITE}{line}"
			if line.startswith('+') and not line.startswith('+++'):
				line = f"{GREEN}{line}"
			elif line.startswith('-') and not line.startswith('---'):
				line = f"{RED}{line}"
			elif line.startswith('diff --git'):
				line = f"{UNDERLINE}{BOLD}{BRIGHT_BLUE}{line}"
				status_line = i
			else:
				line = f"{RESET}{line}"
		else:
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
					# if line.startswith("*"):
					# 	line = f"{i+1}. {BRIGHT_MAGENTA}{line}"
					# else:
					# 	line = f"{i+1}. {line}"
					line = f"{i+1}. {BRIGHT_MAGENTA}{line}" if line.startswith("*") else f"{i+1}. {line}"
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


def print_norm(norm: str):
	"""This function nicely prints out the output stream the
		result of the argument passed to it

	Args:
		norm (str): the string to print

	Returns:
		int, list: index of the line and list of line substrings.
	"""
	output = norm.split('\n')
	for line in output:
		time.sleep(.03)
		print(f"::::: {line}")
	# print(f"::::: {norm}")


def write_to_file(ignore_list, delimiter: str, read: bool=False, empty: bool=False):
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
	# print('filename:', filename)
	# print('ignore_list:', ignore_list)
	ignore_file = 1
	file_list = []
	try:
		with open(filename) as g:
			for line in g:
				file_list.append(line.strip())
		if read:
			# print('Reading...:', file_list)
			return file_list
	except FileNotFoundError:
		if not read: # and not empty:
			open(filename, 'w').close()
		else:
			return file_list
	try:
		if filename.split(delimiter)[-1] not in file_list:
			# print('filename:', filename, 'in file_list:', file_list)
			ignore_file = 0
	except ValueError:
		ignore_file = 0
		if not read: # and not empty:
			open(filename, 'w').close()
		else:
			return file_list
	with open(filename, 'a') as f:
		for k in ignore_list:
			# print('delimiter: %s' % k.split(delimiter))
			try:
				k = k.split(delimiter)[1]
			except IndexError:
				k = k.split(delimiter)[0]
			if k == '.gitignore':
				continue
			if k not in file_list:
				f.write(k + '\n')
		if not ignore_file:
			filename = (filename.split(delimiter)[-1]) if delimiter else filename
			f.write(filename + '\n')

def backward_search(path=None):
	"""
	Recursively searches parent directories for a .git folder,
	indicating the root of a Git repository.

	Args:
		path (str or Path): Starting path. Defaults to current working directory.

	Returns:
		Path or None: Path to the root Git repository or None if not found.
	"""
	path = Path(path or Path.cwd()).resolve()

	for depth, parent in enumerate([path] + list(path.parents)):
		# if depth > 5:
		# 	print_norm(f"You are too deep in the repository: depth: {depth}.")
		# 	return True
		if (parent / '.git').exists():
			# print(f"Found root repository at: {parent}")
			# print(f"Depth to reach root: {depth} folder(s) up")
			print(f'«{depth}')
			# print(f'←{depth}')
			reponame = parent.name
			# print(f"Repository name: {reponame}")
			with open(parent / '.git' / 'config', 'r') as config_file:
				config_content = config_file.readlines()
			configRepoName = [line for line in config_content
                    if 'url' in line and 'https://' in line]
			if not configRepoName:
				print_norm("This repository wasn't cloned using https")
				return True
			configRepoName = configRepoName[0].strip().split('/')[-1].split('.')[0]
			# print(f'configRepoName: {configRepoName}')
			if reponame != configRepoName:
				print(f"Warning: Seems you have a repository inside another repository.")
				print(f"You need to separate them.")
				return True
			return str(parent)

	# Not found
	print()
	print_norm("You don't seem to be in a git repository")
	print_norm('Change into a repository and try again')
	print()
	return True
