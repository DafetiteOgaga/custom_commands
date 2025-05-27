#!/usr/bin/env python3

import subprocess, sys, os, time, shutil
from .my_prompt import main as prompt_1ch
from .git_codes import *

home_dir = os.path.expanduser("~")  # Expands "~" to "/home/your-username"
bumpAppJsonVersionScript = os.path.join(home_dir, ".xbin", "pyfiles")  # location to bumpAppJsonVersion

def add_commit(file):
	"""This function will:
	1. Check if the input is a directory and dress it for processing
	2. Check if the file/directory exists in the current working directory
	3. Check and skip files/directories that have been staged and committed
	4. Loop through the files as provided via the command line. 
		Then, add and commit to each files separately

	Args:
		file (str): filename to be processed

	Returns:
		int:
	"""

	# if "\\" == file[-1] or "/" == file[-1]:
	# 	re_file = (file.split(file[-1]))[0]
	# else:
	# 	re_file = file
	re_file = (file.split(file[-1]))[0] if "\\" == file[-1] or "/" == file[-1] else file
	file = re_file
	if file not in os.listdir():
		print()
		print("::::: {} does not exist in the current directory".format(file))
		print()
		print("...................................................")
		return 1
	
	set_default = success_mode = ""
	if file == "README.md":
#		time.sleep(.05) # xnorm
#		while True:  # xnorm
#			commit_message = prompt_1ch('Would you prefer to use "Update README.md" as commit message for {}? [y/N] >>> '.format(file))  # xnorm
#			if commit_message.lower() == "y" or commit_message.lower() == "n":  # xnorm
#				break  # xnorm
#			print("Invalid response.") # xnorm
#			print()  # xnorm
#		time.sleep(.05) # xnorm
#		if commit_message.lower() == "y":  # xnorm
#			print()  # xnorm
#			print('"Update README.md" has been set to {}'.format(file))  # xnorm
#			print()  # xnorm
#			time.sleep(.05) # xnorm
#			while True:  # xnorm
#				print('Would you love to keep using "Update README.md" as commit message for all your {} files?'.format(file))  # xnorm
#				print("Note: you can change this setting anytime.")  # xnorm
#				set_default = prompt_1ch('[y/N] >>> ')  # xnorm
#				if set_default.lower() == "y":  # xnorm
#					success_mode = set_default_commit_msg(set_default)  # xnorm
#					break  # xnorm
#				elif set_default.lower() == "n":  # xnorm
#					print() # xnorm
#					print('"Update README.md" is not set as your default commit message for all {} files.'.format(file)) # xnorm
#					print()  # xnorm
#					break  # xnorm
#				print("Invalid response.") # xnorm
#				print()  # xnorm
#			commit_message = "Update README.md"  # xnorm
#		elif commit_message.lower() == "n":  # xnorm
#			pass  # xnorm
		commit_message = "Update README.md" # xmodification
		set_default = "auto" # xmodification
	file_status = subprocess.run(["git", "status"], capture_output=True, text=True)
	# print_stdout(file_status.stdout)
	if file not in file_status.stdout:
		time.sleep(.04)
		print("::#:: {} has previously been staged and committed".format(file))
		return 3
	else:
		print()
	if not set_default:		
		commit_message = input("Enter a commit message for {} [q] to abort >>> ".format(file))
		if commit_message.lower() == "pass":
			print()
			print(":###: You skipped {} #####".format(file))
			print()
			return 3
		if commit_message.lower() == "unset commit" and file != "README.md": # xmodification
			success_mode = set_default_commit_msg("n") # xmodification
			print_set_commit("unset") # xmodification
			commit_message = input("Enter a commit message for {} [q] to abort >>> ".format(file)) # xmodification
		elif commit_message.lower() == "unset commit" and file == "README.md": # xmodification
			success_mode = set_default_commit_msg("n") # xmodification
			print_set_commit("unset") # xmodification
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
	############################################################################################################
	############################################################################################################
	############################################################################################################
	# print(f'current location (pushfile_main_codes): {os.getcwd()}')
	if '/home/dafetite/alx/altaviz/altaviz_mobile/altaviz_mobile' in os.getcwd():
		subprocess.run(["bash", "bumpAppJsonVersion"], check=True, cwd=bumpAppJsonVersionScript, stdout=None, stderr=None)
	# print(f'current location (pushfile_main_codes): {os.getcwd()}')
	############################################################################################################
	############################################################################################################
	############################################################################################################
	commit = subprocess.run(["git", "commit", "-m", commit_message], capture_output=True, text=True)
	if commit.returncode == 0:
		print_stdout(commit.stdout)
		print('"{}" successfully committed to {} in the repository.'.format(commit_message, file))
	elif commit.returncode == 1:
		if "nothing to commit, working tree clean" in commit.stdout.split("\n"): # and commit.stderr == None:
			print("##### You have previously committed a message to {} in the repository ...##########".format(file))
		elif "Your branch is up to date with 'origin/main'." in commit.stdout.split("\n"): # and commit.stderr == None:
			print("##### {} already exists in the repository. ...##########".format(file))
		print("nothing to commit, working tree clean")
	else:
		print("Oops! I got: {}When trying to commit {} to {} in the repository.".format(commit.stderr,commit_message, file))
		sys.exit()
	return success_mode


def set_default_commit_msg(par: str):
	"""
	This function recreates the git_codes.py script to account for the
	default use of "Update README.md" as commit message for README.md files.
	Also, provides the means to revert the modification.

	Args:
		par (str): user response

	Returns:
		str: mode of configuration
	"""
	source_file_name = "pushfile_main_codes.py" # for bar or not
	file_path = os.path.join(os.path.expanduser("~"), ".xbin", "pyfiles")

	# file_path = "pyfiles" # remove

	temp_file = os.path.join(file_path, "mod_pushfile_main_codes.py")
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

	new_file = []
	with open(source_file, "r") as main_code:
		count = 1 # for bar
		content = main_code.readlines()
		for line in content:
			time.sleep(.005)
			if line.rstrip().endswith(set_def1):
				line = line.lstrip("#")
			elif line.rstrip().endswith(set_def2):
				line = "#" + line
			new_file.append(line)
			# print('::::##:::: {}'.format(line.strip()))

			progress = count / total_iterations # for bar
			print("\r{}. please wait... : %-40s %d%% done.".format(my_str) % ('>' * int(40 * progress), int(100 * progress)), end='') # for bar
			count += 1 # for bar

		print("") # for bar
		# print(new_file)

	with open(temp_file, "w") as def_commit:
		def_commit.writelines(new_file)
			
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


def main_enrty():
	"""The main execution of the program
	"""

	arg_len = len(sys.argv)
	count = 0
	print("...............................................................")
	print("Enter \"unset commit\" to undo the default README.md commit message.") # xmodification
	print("Enter \"pass\" to skip the current file.")
	print("...............................................................")
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
				if file.lower() == "unset commit" and file != "README.md": # xmodification
					success_mode = set_default_commit_msg("n") # xmodification
					print_set_commit("unset") # xmodification
					file = input("Enter file(s). Enter [q] after last file >>> ") # xmodification
				elif file.lower() == "unset commit" and file == "README.md": # xmodification
					success_mode = set_default_commit_msg("n") # xmodification
					print_set_commit("unset") # xmodification
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
			print('\n')
			# print('[y] or "Enter" to push these changes to remote')
			print('[y] (push) update your remote repository with these changes')
			print('[q] to abort')
			print('[u] to unset auto commit message for README.md files') # xmodification
			print('[r] to clear your staging area and commits')
			print()
			ready = prompt_1ch('Select one >>> ')
			
			quit(ready)
			if ready.lower() == "r":
				clear_staged_and_commit()
			elif ready.lower() == "u": # xmodification
				set_default_commit_msg("n") # xmodification
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


# if __name__ == "__main__":
main_enrty() if __name__ == "__main__" else None
