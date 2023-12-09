#!/usr/bin/env python3

import subprocess, sys, os, time, shutil


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
			commit_message = input('Would you prefer to use "Update README.md" as commit message for {}? [y/N] >>> '.format(file))  # xnorm
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
				set_default = input('[y/N] >>> ')  # xnorm
				if set_default.lower() == "y":  # xnorm
					success_mode = set_default_commit_msg(set_default)  # xnorm
					break  # xnorm
				elif set_default.lower() == "n":  # xnorm
					print() # xnorm
					print('"Update README.md" is not set as your default commit message for all {} files.'.format(file)) # xnorm
					print()  # xnorm
					break  # xnorm
			commit_message = "Update README.md"  # xnorm
		elif commit_message.lower() == "n":  # xnorm
			pass  # xnorm
#		commit_message = "Update README.md" # xmodification
#		set_default = "auto" # xmodification
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
	for i in add.stdout.split("\n"):
		print(f"::::: {i}")
		time.sleep(.03)
	if add.returncode != 0:
		print("Oops! I got {}. When trying to stage {}".format(add.stderr, file))
		sys.exit()
	else:
		print("{} successfully staged.".format(file))
		
	commit = subprocess.run(["git", "commit", "-m", commit_message], capture_output=True, text=True)
	for i in commit.stdout.split("\n"):
		print(f"::::: {i}")
		time.sleep(.03)
	if commit.returncode == 0:
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
	file_path = os.path.join(os.path.expanduser("~"), ".xbin")
	temp_file = os.path.join(file_path, "mod_git_codes.py")
	source_file = os.path.join(file_path, "git_codes.py")
	# test_file = os.path.sep(file_path, "git_codes.py")
	# print("set_default_commit_msg: start *************************************")
	print()

	res_list = ["xmodification", "xnorm"]
	if par.lower() == "y":
		set_def1, set_def2 = res_list
		print('Setting up "Update README.md" to all README.md files ...')
	elif par.lower() == "n":
		set_def2, set_def1 = res_list
		print('Removing "Update README.md" as the default commit message to all README.md files ...')
	
	print("Please wait ... ")
	with open(source_file, "r") as main_code, open(temp_file, "w") as def_commit:
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
	pull = subprocess.run(["git", "pull"])
	if pull.returncode == 0:
		print("\nPull successful...")
		print()
	else:
		print("Oops! I got {}".format(pull.stderr))
		sys.exit()

def push(file_list: list):
	"""This function takes a list as argument and Updates the
		remote with the changes on the local machine
	"""

	print("#### pushing ...################################################")
	push = subprocess.run(["git", "push"])
	if push.returncode == 0:
		print("\nThe file(s): {} are in the remote.".format([xfile for xfile in file_list]))
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
	subprocess.run(["git", "commit", "-m", commit_message])


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
	sure = input("""You will lose all the recent changes on your local machine
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
	print("...................................................")
	if arg_len > 0:
		if arg_len > 1:
			all_files = []
#			print("Enter \"unset commit\" to unset default README.md commit message.") # xmodification
			while count != (arg_len - 1):
				file = (sys.argv)[count + 1]
				res_add_commit = add_commit(file)
				if res_add_commit == 1:
					count += 1
					continue
				elif res_add_commit == 2:
					continue
				if res_add_commit == "mod":
					print_set_commit("set")
				all_files.append(file)
				count += 1
				print("...................................................")
		
		if arg_len == 1:
			all_files = []
#			print("Enter \"unset commit\" to unset default README.md commit message.") # xmodification
			while True:
				file = input("Enter file(s). Enter [q] after last file >>> ")
				quit(file)
				if file.lower() == "s":
					print()
					break
				
				if file:
					res_add_commit = add_commit(file)
					if res_add_commit == 1:
						count += 1
						continue
					elif res_add_commit == 2:
						continue
					if res_add_commit == "mod":
						print_set_commit("set")
					all_files.append(file)
				print("...................................................")


		while True:
			print('[y] or "Enter" to push these changes to remote')
			print('[q] to abort')
#			print('[unset commit] to unset auto commit message for README.md files') # xmodification
			print('[r] to clear your staging area and commits')
			ready = input('Select one >>> ')
			
			quit(ready)
			if ready.lower() == "r":
				clear_staged_and_commit()
#			if ready.lower() == "unset commit": # xmodification
#				set_default_commit_msg("n") # xmodification
			if ready == "" or ready.lower() == "y":
				pull()
				push(all_files)
				break
	else:
		print("No command found.")
		sys.exit()
	print("Done.")
	print()


if __name__ == "__main__":
	main_enrty()
