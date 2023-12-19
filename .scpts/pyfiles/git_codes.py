#!/usr/bin/env python3

import subprocess, sys, os, time, shutil
from .my_prompt import main as prompt_1ch


def add_commit(file):
	"""This function will:
	1. the input is a directory and dress it for processing
	2. Check if the input file/directory exists in the 
		current working directory
	3. Loop through the files as provided via the command line. 
		Then, add and commit to each files separately
	"""

	if "\\" == file[-1] or "/" == file[-1]:
		re_file = (file.split(file[-1]))[0]
	else:
		re_file = file
	file = re_file
	if file not in os.listdir():
		print()
		print("::::: {} does not exist".format(file))
		print()
		print("...................................................")
		return 1
	
	set_default = success_mode = ""
	if file == "README.md":
		time.sleep(.05) # xnorm
		while True:  # xnorm
			commit_message = prompt_1ch('Would you prefer to use "Update README.md" as commit message for {}? [y/N] >>> '.format(file))  # xnorm
			if commit_message.lower() == "y" or commit_message.lower() == "n":  # xnorm
				break  # xnorm
			print("Invalid response.") # xnorm
			print()  # xnorm
		time.sleep(.05) # xnorm
		if commit_message.lower() == "y":  # xnorm
			print()  # xnorm
			print('"Update README.md" has been set to {}'.format(file))  # xnorm
			print()  # xnorm
			time.sleep(.05) # xnorm
			while True:  # xnorm
				print('Would you love to keep using "Update README.md" as commit message for all your {} files?'.format(file))  # xnorm
				print("Note: you can change this setting anytime.")  # xnorm
				set_default = prompt_1ch('[y/N] >>> ')  # xnorm
				if set_default.lower() == "y":  # xnorm
					success_mode = set_default_commit_msg(set_default)  # xnorm
					break  # xnorm
				elif set_default.lower() == "n":  # xnorm
					print() # xnorm
					print('"Update README.md" is not set as your default commit message for all {} files.'.format(file)) # xnorm
					print()  # xnorm
					break  # xnorm
				print("Invalid response.") # xnorm
				print()  # xnorm
			commit_message = "Update README.md"  # xnorm
		elif commit_message.lower() == "n":  # xnorm
			pass  # xnorm
#		commit_message = "Update README.md" # xmodification
#		set_default = "auto" # xmodification
	file_status = subprocess.run(["git", "status"], capture_output=True, text=True)
	if file not in file_status.stdout:
		time.sleep(.04)
		print("::#:: {} has previously been staged and committed".format(file))
		return 3
	else:
		print()
	if not set_default:		
		commit_message = input("Enter a commit message for {} [q] to abort >>> ".format(file))
#		if commit_message.lower() == "unset commit" and file != "README.md": # xmodification
#			success_mode = set_default_commit_msg("n") # xmodification
#			print_set_commit("unset") # xmodification
#			commit_message = input("Enter a commit message for {} [q] to abort >>> ".format(file)) # xmodification
#		elif commit_message.lower() == "unset commit" and file == "README.md": # xmodification
#			success_mode = set_default_commit_msg("n") # xmodification
#			print_set_commit("unset") # xmodification
	quit(commit_message)
	if commit_message == "":
		print("You must provide a commit message for {}. Try again".format(file))
		return 2
		
	add = subprocess.run(["git", "add", file], capture_output=True, text=True)
	if add.returncode != 0:
		print("Oops! I got {}. When trying to stage {}".format(add.stderr, file))
		sys.exit()
	else:
		print_stdout(add.stdout)
		print("{} successfully staged.".format(file))
		
	commit = subprocess.run(["git", "commit", "-m", commit_message], capture_output=True, text=True)
	if commit.returncode == 0:
		print_stdout(commit.stdout)
		print('"{}" successfully committed to {}.'.format(commit_message, file))
	elif commit.returncode == 1:
		if "nothing to commit, working tree clean" in commit.stdout.split("\n"): # and commit.stderr == None:
			print("##### You have previously committed a message to {} ...##########".format(file))
		elif "Your branch is up to date with 'origin/main'." in commit.stdout.split("\n"): # and commit.stderr == None:
			print("##### {} already exists in the remote ...##########".format(file))
		print("nothing to commit, working tree clean")
	else:
		print("Oops! I got: {}When trying to commit {} to {}".format(commit.stderr,commit_message, file))
		sys.exit()
	return success_mode


def set_default_commit_msg(par: str):
	"""
	This function recreates the git_codes.py script to account for the
	default use of "Update README.md" as commit message for README.md files.
	Also, provides the means to revert the modification.
	"""
	source_file_name = "git_codes.py" # for bar or not
	file_path = os.path.join(os.path.expanduser("~"), ".xbin", "pyfiles")
	temp_file = os.path.join(file_path, "mod_git_codes.py")
	source_file = os.path.join(file_path, source_file_name)
	# test_file = os.path.join(file_path, "Test_git_codes.py")
	# print("set_default_commit_msg: start *************************************")
	print()

	res_list = ["xmodification", "xnorm"]
	if par.lower() == "y":
		set_def1, set_def2 = res_list
		my_str = "Updating" # for bar
		print('Setting up "Update README.md" to all README.md files ...')
	elif par.lower() == "n":
		set_def2, set_def1 = res_list
		my_str = "Reverting" # for bar
		print('Removing "Update README.md" as the default commit message to all README.md files ...')

	cur_dir = os.getcwd() # for bar
	os.chdir(file_path) # for bar
	shell_return = subprocess.run(["wc", source_file_name], capture_output=True, text=True) # for bar
	total_iterations = int((shell_return.stdout.strip().split())[0]) # for bar
	os.chdir(cur_dir) # for bar

	with open(source_file, "r") as main_code, open(temp_file, "w") as def_commit:
		count = 1 # for bar
		for line in main_code:
			time.sleep(.05)
			if line.strip().endswith(set_def1):
				line = line.lstrip("#")
				def_commit.write(line)
				# print('::::**:::: {}'.format(line.strip()))
			elif line.strip().endswith(set_def2):
				line = "#" + line
				def_commit.write(line)
				# print('::::##:::: {}'.format(line.strip()))
			else:
				def_commit.write(line)
				# print(':::::::::: {}'.format(line.strip()))

			progress = count / total_iterations # for bar
			print("\r{}. please wait... : %-40s %d%% done.".format(my_str) % ('>' * int(40 * progress), int(100 * progress)), end='') # for bar
			count += 1 # for bar
		print("") # for bar
	shutil.copy(temp_file, source_file)
	os.remove(temp_file)
	print()
	print("Done.")
	if par.lower() == "y":
		mode = "mod"
	elif par.lower() == "n":
		mode = "norm"
	print()
	# print("set_default_commit_msg: finished *************************************")
	return mode


def print_set_commit(var: str):
	print("........................................................................................")
	if var.lower() == "unset":
		print('"Update README.md" is no longer your default commit message to all README.md files')
	elif var.lower() == "set":
		print('"Update README.md" is now your default commit message for all README.md files.')
	print('##### NOTE: CHANGES WILL TAKE EFFECT THE NEXT TIME YOU RUN THE "pushfile" command. #####')
	print("........................................................................................")


def pull():
	"""This function pulls updates from the remote
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
	else:
		print("Oops! I got {}".format(pull.stderr))
		sys.exit()
	print("Pull successful...")
	print()


def push(file_list: list):
	"""This function takes a list as argument and Updates the
		remote with the changes on the local machine
	"""

	print("#### pushing ...################################################")
	push = subprocess.run(["git", "push"])
	if push.returncode == 0:
		print("\nThe file(s)/folder(s): {} are in the remote.".format([xfile for xfile in file_list]))
	else:
		print("Oops! I got {}".format(push.stderr))
		sys.exit()


def add_commit_all():
	"""This function stages and commit a single message to all the
		changes in the current working directory intended to be
		updated to the remote
	"""

	while True:
		if len(sys.argv) > 1:
			commit_message = (sys.argv)[1]
			break
		commit_message = input("Provide a commit message. [q] to quit >>> ")
		quit(commit_message)
		if commit_message != "":
			break
		print("You have to provide a commit message.")
	print("#### staging and committing ...################################")
	subprocess.run(["git", "add", "."])
	commit = subprocess.run(["git", "commit", "-m", commit_message], capture_output=True, text=True)
	if commit.returncode == 0:
		print_stdout(commit.stdout)
		print('"{}" successfully committed to files.'.format(commit_message))


def print_stdout(stdout: str):
	for i in stdout.split("\n"):
		time.sleep(.03)
		print(f"::::: {i}")

def quit(val):
	"""
	This function stops and exit the execution process
	"""

	if val.lower() == "q":
		print()
		print("Cheers.")
		sys.exit()


def clear_staged_and_commit():
	"""This function unstage and clears the recent changes on the
		local machine and revert the machine to the same state as
		the most recent on the remote
	"""

	print()
	sure = prompt_1ch("""You will lose all the recent changes on your local machine
Are you sure that you want to proceed? [y/N] >>> """)
	print()
	if sure.lower() == "y":
		current_branch = subprocess.run(["git", "branch", "--show-current"], capture_output=True, text=True)
		fetch = subprocess.run(["git", "fetch", "origin", current_branch.stdout.strip()], capture_output=True, text=True)
		clear = subprocess.run(["git", "reset", "--hard", f"origin/{current_branch.stdout.strip()}"])
		print("Revert successful...")
		print("Recent changes on local machine cleaned.")
	else:
		print("Operation aborted.")
	print()
	sys.exit()


def main_enrty():
	"""The main execution of the program
	"""

	arg_len = len(sys.argv)
	count = 0
	print("...............................................................")
#	print("Enter \"unset commit\" to unset default README.md commit message.") # xmodification
#	print("...............................................................")	# xmodification
	if arg_len > 0:
		if arg_len > 1:
			all_files = []
			while count != (arg_len - 1):
				file = (sys.argv)[count + 1]
				res_add_commit = add_commit(file)
				# moves to the next file
				if res_add_commit in [1, 3]:
					count += 1
					continue
				# stays on the current file
				elif res_add_commit == 2:
					continue
				if res_add_commit == "mod":
					print_set_commit("set")
				all_files.append(file)
				count += 1
				print("...................................................")
		
		if arg_len == 1:
			all_files = []
			while True:
				file = input("Enter file(s). Enter [q] after last file >>> ")
				quit(file)
				if file.lower() == "s":
					print()
					break
				
				if file:
					res_add_commit = add_commit(file)
					# moves to the next file
					if res_add_commit in [1, 3]:
						count += 1
						continue
					# stays on the current file
					elif res_add_commit == 2:
						continue
					if res_add_commit == "mod":
						print_set_commit("set")
					all_files.append(file)
				print("...................................................")


		while True:
			# print('[y] or "Enter" to push these changes to remote')
			print('[y] to push these changes to remote')
			print('[q] to abort')
#			print('[u] to unset auto commit message for README.md files') # xmodification
			print('[r] to clear your staging area and commits')
			print()
			ready = prompt_1ch('Select one >>> ')
			
			quit(ready)
			if ready.lower() == "r":
				clear_staged_and_commit()
#			elif ready.lower() == "u": # xmodification
#				set_default_commit_msg("n") # xmodification
			elif ready == "" or ready.lower() == "y":
				pull()
				push(all_files)
				break
			else:
				print("Invalid response.")
				print()
				print("...............................................")
	else:
		print("No command found.")
		sys.exit()
	print("Done.")
	print()


def check_arg(files):
	"""This function checks that atleast a file(argument) is passed from the CL
	"""

	length = len(files)
	if length == 1:
		print("No argument(s) provided.")
		sys.exit(1)
	return length
	

def counter(files):
	"""This function loops through the files(arguments) passed from the CL and prints their
	1. number of lines
	2. number of words
	3. number of characters
	4. filenames
	"""

	length = check_arg(files)
	print()
	for file in range(1, length):
		try:
			check = os.path.join((files[0].split(os.path.sep))[0], files[file])
			if os.path.isdir(check):
				continue
			time.sleep(.8)
			shell_return = subprocess.run(["wc", files[file]], capture_output=True)
			lines, words, chars, name = shell_return.stdout.decode().strip().split()
			print("============= {} =============".format(name))
			print("lines: {}, words: {}, characters: {}".format(lines, words, chars))
		except ValueError:
			print('Error: "{}" is not a valid filename.'.format(files[file]))
		except Exception as e:
			print(f"An unexpected error occurred: {e}")
		print()


def lines_words_chars_file(files):
	"""This function loops through the files(arguments) passed from the CL and returns their
	1. number of lines
	2. number of words
	3. number of characters
	4. filenames
	"""

	length = check_arg(files)
	for file in range(1, length):
		check = os.path.join((files[0].split(os.path.sep))[0], files[file])
		if os.path.isdir(check):
			continue
		shell_return = subprocess.run(["wc", files[file]], capture_output=True, text=True)
		lines, words, chars, name = shell_return.stdout.strip().split()
		print("lines: {}, words: {}, characters: {}".format(lines, words, chars))
	
	return lines, words, chars, name



if __name__ == "__main__":
	main_enrty()
