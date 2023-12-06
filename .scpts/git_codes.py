#!/usr/bin/env python3

import subprocess, sys, os, time


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
	if re_file not in os.listdir():
		print()
		print("::::: {} does not exist".format(re_file))
		print()
		print("...................................................")
		return 1
		
	commit_message = input("Enter a commit message for {}. [q] to abort >>> ".format(file))
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
		print("{} successfully committed to {}.".format(commit_message, file))
	
	elif commit.returncode == 1:
		if "nothing to commit, working tree clean" in commit.stdout.split("\n"): # and commit.stderr == None:
			print("##### You have previously committed a message to {} ...##########".format(file))
		elif "Your branch is up to date with 'origin/main'." in commit.stdout.split("\n"): # and commit.stderr == None:
			print("##### {} already exists in the remote ...##########".format(file))
		print("nothing to commit, working tree clean")

	else:
		print("Oops! I got: {}When trying to commit {} to {}".format(commit.stderr,commit_message, file))
		sys.exit()


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
			while count != (arg_len - 1):
				file = (sys.argv)[count + 1]

				res_add_commit = add_commit(file)
				if res_add_commit == 1:
					count += 1
					continue
				elif res_add_commit == 2:
					continue

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
					if res_add_commit == 1:
						count += 1
						continue
					elif res_add_commit == 2:
						continue

					all_files.append(file)
				print("...................................................")


		while True:
			ready = input('''...............................................
[y] or "Enter" to push these changes to remote
[q] to abort
[r] to clear your staging area and commits
Select one >>> ''')
			quit(ready)
			if ready.lower() == "r":
				clear_staged_and_commit()
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

# .................................................................................................. #

# refactore the code
## commit message will be class variable
## filename(s) will be instance variable
# merge
# branches
# status
# git add -A, general staging
# rebase
# 12
# .................................................................................................. #