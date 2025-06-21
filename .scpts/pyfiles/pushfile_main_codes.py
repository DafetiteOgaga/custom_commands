#!/usr/bin/env python3

import subprocess, sys, os, time, shutil
from .my_prompt import main as prompt_1ch
from .git_codes import print_set_commit, print_norm, print_stdout, quit, clear_staged_and_commit, pull, push, checkPushAccess
from pyfiles.subprocessfxn import run_subprocess

home_dir = os.path.join(os.path.expanduser("~"), '.xbin')  # Expands "~" to "/home/your-username"
bumpAppJsonVersionScript = os.path.join(home_dir, "pyfiles")  # location to bumpAppJsonVersion
bumpCCVersion = os.path.join(home_dir, "pyfiles")  # location to bumpCCVersion

def add_commit(file, arg="arg"):
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

	# strip trailing slashes
	re_file = (file.split(file[-1]))[0] if "\\" == file[-1] or "/" == file[-1] else file
	file = re_file
	if arg == "arg" and file not in os.listdir():
		print()
		print("::::: {} does not exist in the current directory".format(file))
		print()
		print("...................................................")
		return 1
	
	displayed_filename = file.split("/")[-1] if "/" in file else file
	set_default = success_mode = ""
	if file == "README.md":
#		time.sleep(.05) # xnorm
#		while True:  # xnorm
#			commit_message = prompt_1ch('Would you prefer to use "Update README.md" as commit message for {}? [y/N] >>> '.format(displayed_filename))  # xnorm
#			if commit_message.lower() == "y" or commit_message.lower() == "n":  # xnorm
#				break  # xnorm
#			print("Invalid response.") # xnorm
#			print()  # xnorm
#		time.sleep(.05) # xnorm
#		if commit_message.lower() == "y":  # xnorm
#			print()  # xnorm
#			print('"Update README.md" has been set to {}'.format(displayed_filename))  # xnorm
#			print()  # xnorm
#			time.sleep(.05) # xnorm
#			while True:  # xnorm
#				print('Would you love to keep using "Update README.md" as commit message for all your {} displayed_filename?'.format(displayed_filename))  # xnorm
#				print("Note: you can change this setting anytime.")  # xnorm
#				set_default = prompt_1ch('[y/N] >>> ')  # xnorm
#				if set_default.lower() == "y":  # xnorm
#					success_mode = set_default_commit_msg(set_default)  # xnorm
#					break  # xnorm
#				elif set_default.lower() == "n":  # xnorm
#					print() # xnorm
#					print('"Update README.md" is not set as your default commit message for all {} files.'.format(displayed_filename)) # xnorm
#					print()  # xnorm
#					break  # xnorm
#				print("Invalid response.") # xnorm
#				print()  # xnorm
#			commit_message = "Update README.md"  # xnorm
#		elif commit_message.lower() == "n":  # xnorm
#			pass  # xnorm
		commit_message = "Updated README.md" # xmodification
		set_default = "auto" # xmodification
	file_status = run_subprocess(["git", "status"])
	# print_stdout(file_status.stdout)
	if arg == "arg" and file not in file_status.stdout:
		time.sleep(.04)
		print("::#:: {} has previously been staged and committed or ignored".format(displayed_filename))
		return 3
	else:
		print()
	# displayed_filename = file.split("/")[-1] if "/" in file else file
	if not set_default:		
		commit_message = input("Enter a commit message for {} [q] to abort >>> ".format(displayed_filename))
		if commit_message.lower() == "pass":
			print()
			print(":###: You skipped {} #####".format(displayed_filename))
			print()
			return 3
		if commit_message.lower() == "unset commit" and file != "README.md": # xmodification
			success_mode = set_default_commit_msg("n") # xmodification
			print_set_commit("unset") # xmodification
			commit_message = input("Enter a commit message for {} [q] to abort >>> ".format(displayed_filename)) # xmodification
		elif commit_message.lower() == "unset commit" and file == "README.md": # xmodification
			success_mode = set_default_commit_msg("n") # xmodification
			print_set_commit("unset") # xmodification
	quit(commit_message)
	if commit_message == "":
		print("You must provide a commit message for {}. Try again".format(displayed_filename))
		return 2
		
	add = run_subprocess(["git", "add", file])
	if add.returncode != 0:
		print("Oops! I got {}. When trying to stage {}".format(add.stderr, displayed_filename))
		sys.exit()
	else:
		print_stdout(add.stdout)
		print("{} successfully staged.".format(displayed_filename))
	###########################################################################################################
	############################################################################################################
	############################################################################################################
	# print(f'current location (pushfile_main_codes): {os.getcwd()}')
	if '/home/dafetite/alx/altaviz/altaviz_mobile/altaviz_mobile' in os.getcwd():
		subprocess.run(["bash", "bumpAppJsonVersion"], check=True, cwd=bumpAppJsonVersionScript, stdout=None, stderr=None)
	# if 'custom_commands' in os.getcwd():
	# 	subprocess.run(["bash", "bumpCCVersion"], check=True, cwd=bumpCCVersion, stdout=None, stderr=None)
	# print(f'current location (pushfile_main_codes): {os.getcwd()}')
	############################################################################################################
	############################################################################################################
	############################################################################################################
	commit = run_subprocess(["git", "commit", "-m", commit_message])
	if commit.returncode == 0:
		print_stdout(commit.stdout)
		print('"{}" successfully committed to {} in the repository.'.format(commit_message, displayed_filename))
	elif commit.returncode == 1:
		if "nothing to commit, working tree clean" in commit.stdout.split("\n"): # and commit.stderr == None:
			print("##### You have previously committed a message to {} in the repository ...##########".format(displayed_filename))
		elif "Your branch is up to date with 'origin/main'." in commit.stdout.split("\n"): # and commit.stderr == None:
			print("##### {} already exists in the repository. ...##########".format(displayed_filename))
		print("nothing to commit, working tree clean")
	else:
		print("Oops! I got: {}When trying to commit {} to {} in the repository.".format(commit.stderr,commit_message, displayed_filename))
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
	shell_return = run_subprocess(["wc", source_file_name]) # for bar
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

def print_committted_files(files, additional_list=None, mode=None, prompt1=None, prompt2=None):
	"""This function prints the files that have been committed to the
		repository. But not pushed to the remote repository.

	Args:
		files (list): list of files that have been committed
	"""
	if not files and not additional_list:
		print("No files were committed.")
	else:
		if not mode:
			if files:
				print(prompt1)
				for index, file in enumerate(files):
					displayed_filename = file.split("/")[-1] if "/" in file else file
					print_norm(f'{index+1}. {displayed_filename}')
			else:
				print("No files were staged and committed.")
			if additional_list:
				new_additionals = [addition for addition in additional_list if addition not in files]
				# print(f'new_additionals: {new_additionals}')
				if new_additionals:
					print()
					print(prompt2)
					for index, file in enumerate(new_additionals):
						displayed_additional_filename = file.split("/")[-1] if "/" in file else file
						print_norm(f'{index+1}. {displayed_additional_filename}')
		elif mode == "delete":
			if files:
				print(prompt1)
				for index, file in enumerate(files):
					displayed_filename = file.split("/")[-1] if "/" in file else file
					print_norm(f'{index+1}. {displayed_filename}')
				print()
				delete_response = prompt_1ch(prompt2)
				return "y" if delete_response.lower() == "y" else "n"

def commit_deleted_files(files, mode=0):
	prompt1 = f"You{' also' if mode==1 else ', however'} have untracked/unstaged deleted files:"
	prompt2 = "Do you want to commit them? [y/N] >>> "
	print()
	commit_deleted_files_response = print_committted_files(files, mode="delete", prompt1=prompt1, prompt2=prompt2)
	if commit_deleted_files_response.lower() == "y":
		print()
		for file in files:
			deleted_filename = file.split("/")[-1] if "/" in file else file
			# print(f"Processing deleted file: {deleted_filename}")
			add_deleted_file = run_subprocess(["git", "add", file])
			if add_deleted_file.returncode != 0:
				print(f"Error adding {file} to staging area: {add_deleted_file.stderr}")
				continue
			deleted_file_commit_message = f"Deleted {file.split('/')[-1].strip() if '/' in file else file.strip()}"
			# print(f"Committed {deleted_filename} with message: {deleted_file_commit_message}")
			
			commit_deleted_file = run_subprocess(["git", "commit", "-m", deleted_file_commit_message])
			if commit_deleted_file.returncode != 0:
				print(f"Error committing {file}: {commit_deleted_file.stderr}")
				continue
			print(f"Committed {deleted_filename}")
		print()
	else:
		print("Deleted files not staged and committed. Hence, not pushed to remote.")
	return "y" if commit_deleted_files_response.lower() == "y" else "n"

def get_file_recursively(directory):
	"""This function gets all files in a directory recursively.

	Args:
		directory (str): the directory to search for files

	Returns:
		list: list of file paths
	"""
	file_paths = []
	for root, dirs, files in os.walk(directory):
		for file in files:
			file_paths.append(os.path.join(root, file))
	return file_paths

def main_enrty():
	"""The main execution of the program
	"""

	checkEditAccess = checkPushAccess()
	if not checkEditAccess:
		sys.exit()
	# currentDirectory = os.getcwd()
	status_details = run_subprocess(["git", "status"])
	# print(f'status_details.stdout: {status_details.stdout}')
	status_string = status_details.stdout.strip().replace("\n", " ")
	status_line_list = status_details.stdout.split("\n")
	# print(f'status_string: {status_string}')
	# if "nothing to commit, working tree clean" in status_string:
	# 	print("You have nothing to commit. Your working tree is clean.")
		# sys.exit() # uncomment this line to exit the program
	ahead_of_origin = "Your branch is ahead of 'origin/" in status_string
	file_paths = []
	deleted_file_list = []
	continue_keys_list = [
		"both modified",
		"both added",
		"both deleted",
		"deleted by us",
		"deleted by them",
		"added by us",
		"added by them",
	]
	for num, line in enumerate(status_line_list):
		clean_line = line.strip().lower()
		if any(key in clean_line for key in continue_keys_list):
			print(f'skipping line {num+1}: {line.strip()} contains merge conflict or unmerged files')
			continue
		isfile = os.path.isfile(line.split(':')[1].strip()) if ':' in line else os.path.isfile(line.strip())
		isDir = os.path.isdir(line.strip())
		if "renamed:" in line.strip() and "->" in line.strip():
			isfile = os.path.isfile(line.split('->')[1].strip())
		if "deleted:" in line.strip():
			# print(f'isfile: {isfile} at line {num+1}: {full_file}')
			deleted_file_list.append(line.split(':')[1].strip() if ':' in line else line.strip())
		if isfile:
			full_file = line.split(':')[1].strip() if ':' in line else line.strip()
			file_paths.append(full_file)
			# print(f'isfile: {isfile} at line {num+1}: {full_file}')
		if isDir:
			# print('####################')
			# print(f'isDir: {isDir} at line {num+1}: {line.strip()}')
			dir_content = get_file_recursively(line.strip())
			# print(f'dir_content: {dir_content}')
			for dir_file in dir_content:
				# full_dir_file = os.path.join(line.strip(), dir_file)
				isDirfile = os.path.isfile(dir_file)
				if isDirfile:
					# print(f'isDirfile at line {num+1}: {dir_file}')
					file_paths.append(dir_file)
				# print(f'isfile: {isfile} at line {num+1}: {full_file}')
			# print(f'dir_content: {dir_content}')
			# full_file = line.split(':')[1].strip() if ':' in line else line.strip()
			# file_paths.append(full_file)
			# print(f'isfile: {isfile} at line {num+1}: {full_file}')
			# print('####################')
	# print(f'file_paths:')
	# print(f'file_paths: {file_paths}')
	# for xfile in file_paths:
	# 	print(f'- {xfile}')
	# [print(f'-- {xfile}') for xfile in file_paths]
	arg_len = len(sys.argv)
	new_args_len = len(file_paths)
	deleted_file_list_len = len(deleted_file_list)
	count = 0
	
	# if arg_len > 0:
	all_files = None
	# print(f'sys.argv: {sys.argv}')
	# print(f'new_args_len: {new_args_len}')
	# print(f'ahead_of_origin: {ahead_of_origin}')
	# print(f'all_files: {all_files}')
	# print(f'ahead_of_origin: {ahead_of_origin}')
	# print(f'deleted_file_list: {deleted_file_list}')
	if new_args_len > 0 or ahead_of_origin or arg_len > 1 or deleted_file_list_len > 0:
		if new_args_len > 0 or ahead_of_origin or arg_len > 1:
			print("...............................................................")
			print("Enter \"unset commit\" to undo the default README.md commit message.") # xmodification
			print("Enter \"pass\" to skip the current file.")
			print("...............................................................")
		# print("Current working directory: {}".format(currentDirectory))
		# print(f'arg_len: {arg_len-1}')
		# print(f'sys.argv: {sys.argv}')
		# if arg_len > 1:
		if arg_len == 1 and new_args_len > 0:
			# print('1111111111')
			# print(f'(sys.arg)[count + 1]: {(sys.argv)[count + 1]}')
			all_files = []
			# while count != (arg_len - 1):
			while count != (new_args_len):
				# print(f'init count: {count}')
				# file = (sys.argv)[count + 1]
				file = file_paths[count]
				# print(f'for file: {file}')
				res_add_commit = add_commit(file, arg='no arg')
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
			# print(f'end count: {count}')
				print("...................................................")

		if arg_len > 1:
			# print('2222222222')
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

		# if arg_len == 2:
		# 	print('3333333333')
		# 	all_files = []
		# 	while True:
		# 		file = input("Enter file(s). Enter [q] after last file >>> ")
		# 		if file.lower() == "unset commit" and file != "README.md": # xmodification
		# 			success_mode = set_default_commit_msg("n") # xmodification
		# 			print_set_commit("unset") # xmodification
		# 			file = input("Enter file(s). Enter [q] after last file >>> ") # xmodification
		# 		elif file.lower() == "unset commit" and file == "README.md": # xmodification
		# 			success_mode = set_default_commit_msg("n") # xmodification
		# 			print_set_commit("unset") # xmodification
		# 		quit(file)
		# 		if file.lower() == "s":
		# 			print()
		# 			break
				
		# 		if file:
		# 			res_add_commit = add_commit(file)
		# 			# moves to the next file
		# 			if res_add_commit in [1, 3]:
		# 				count += 1
		# 				continue
		# 			# stays on the current file
		# 			elif res_add_commit == 2:
		# 				continue
		# 			if res_add_commit == "mod":
		# 				print_set_commit("set")
		# 			all_files.append(file)
		# 		print("...................................................")

		print()
		# print(f'all_files: {all_files}')
		# print(f'ahead_of_origin: {ahead_of_origin}')
		# print(f'deleted_file_list: {deleted_file_list}')
		use_pushall = False
		committed_files = run_subprocess(["git", "diff", "--name-only", "@{u}..HEAD"])
		prompt1 = "You have successfully staged and committed the following files:"
		prompt2 = "Also you previously committed the following files:"
		# handles when there are no recent files staged and committed
		if not all_files:
			# handles when no files are committed recently
			if not ahead_of_origin:
				# handles when there are previously deleted and uncommitted files
				print()
				print("You are yet to stage and commit any file. Try again.")
				
				if deleted_file_list:
					commite_deleted_files_response_from_fxn = commit_deleted_files(deleted_file_list)
					if commite_deleted_files_response_from_fxn.lower() == "y":
						pull()
						push()
				# else:
					# handles when there are no files staged and committed, including deleted files
					# print("You are yet to stage and commit any file. Try again.")
				sys.exit()
			else:
				# handles previuosly committed that are not pushed
				all_files = committed_files.stdout.splitlines()
				# print(f'committed_files.stdout: {committed_files.stdout}')
				# print(f'committed_files.stderr: {committed_files.stderr}')
				
				print_committted_files([], additional_list=all_files, prompt1=prompt1, prompt2=prompt2)
		else:
			# handles recently committed that are not pushed
			all_files = all_files
			additional_list = committed_files.stdout.splitlines()
			# print(f'all_files (222333444): {all_files}')
			# print(f'additional_list (222333444): {additional_list}')
			# print(F'all_files (when all_files is not empty): {all_files}')
			print_committted_files(all_files, additional_list=additional_list, prompt1=prompt1, prompt2=prompt2)

		# check if the files are not in the current dir and are not directories
		use_pushall = any(map(lambda x: "/" in x and x[-1] != "/", all_files))
		# print(f'use_pushall: {use_pushall}')
		while True:
			print('\n')
			# print('[y] or "Enter" to push these changes to remote')
			print(f'[y] ({"push" if not use_pushall else "pushall"}) update your remote repository with {"these changes" if not use_pushall else "all changes in this repository"}')
			print('[q] to abort')
			print('[u] to unset auto commit message for README.md files') # xmodification
			# print('[r] to clear your staging area and commits')
			print()
			ready = prompt_1ch('Select one >>> ')
			
			quit(ready)
			if ready.lower() == "r":
				clear_staged_and_commit()
			elif ready.lower() == "u": # xmodification
				set_default_commit_msg("n") # xmodification
			elif ready == "" or ready.lower() == "y":
				if deleted_file_list:
					commit_deleted_files(deleted_file_list, mode=1)
				pull()
				push(all_files if not use_pushall else ["*ALL CHANGES*"])
				break
			else:
				print("Invalid response.")
				print()
				print("...............................................")
	else:
		print()
		print_norm("nothing to commit, working tree clean.")
		sys.exit()
	print("Done.")
	print()


# if __name__ == "__main__":
main_enrty() if __name__ == "__main__" else None
