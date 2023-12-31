#!/usr/bin/env python3

import subprocess, os, time, sys
from .colors import *

def create_gitignore(list_dict: dict, current_directory, action: str=None):
	if action:
		file_dir = ".gitignore"
	else:
		file_dir = "__pycache__"
	print()
	for i, dir in enumerate(list_dict.keys()):
		print(f"Checking for {BRIGHT_BLACK}{file_dir}{RESET} in {BRIGHT_BLACK}{os.path.basename(dir)}{RESET} ...")
		if f"{file_dir}" in os.listdir(dir):
			print(f"Found one!")
			if not os.path.isfile(".gitignore"):
				open(".gitignore", "w").close()
				# print(f"Creating .gitignore file.")
			
			with open(".gitignore") as f:
				lines = f.readlines()
				# print(f"lines {lines}")
			if action:
					return lines
			else:
				if f"{(list_dict[dir]).strip()}" not in [i.strip() for i in lines]:
					with open(".gitignore", "a") as f:
						f.write(list_dict[dir])
						print(f"Wrote {(list_dict[dir]).strip()} to .gitgnore.")
				else:
					print("But nothing to write.")
					print(f"{(list_dict[dir]).strip()} already in .gitignore")
		else:
			print(f"No {file_dir} in {dir}")
			if i == len(list_dict) - 1:
				break
		print()

	os.chdir(current_directory)


def ignore__pycache(dir_list: list):
	repo_dir = [ len(i) for i in dir_list ]
	separator = ((dir_list[-1]).split(os.sep))[-1]
	# print(f"separator: {separator}")
	repo_root = f"{dir_list[-1]}"
	# print(f"repo_root: {repo_root}")
	# print("navigating to root repository.")
	os.chdir(repo_root)
	list_dict = {}
	for pathz in dir_list:
		new_path = pathz.split(separator)[1]
		new_path = f"{new_path}{os.sep}__pycache__"
		# print(f"new_path: {new_path}")
		list_dict[pathz] = new_path[1:] + " " + "\n"
	return list_dict


def scan_dir(dir, num_items: int, repo, verify_repo: int=0):
	time.sleep(.03)
	git = False
	for num in range(num_items):
		if dir[num] != repo:
			continue
		else:
			git = True
			path_c = f"{repo}/config"
			cat_content = subprocess.run(["cat", path_c], capture_output=True, text=True)
			time.sleep(.5)
			print()
			print("verfying ...")
			if os.path.basename(os.getcwd()) in cat_content.stdout:
				if verify_repo:
					time.sleep(1)
					print("Repository verified!")
					# time.sleep(1)
					print(f"Root repo is {os.getcwd()}")
					print()
					sys.exit(0)
				break
	return num, git

def entry_point(action: str=None, verify_repo: int=0):
	"""verify repo"""
	current_directory = os.getcwd()
	repository = ".git"
	directory = os.listdir()
	num_of_items_in_dir = len(directory)
	res = False
	print()
	time.sleep(.05)

	print("Scanning directory(ies) ...")

	current_dir_list = []
	count=0
	while res is False:
		time.sleep(.05)
		print(f"Checking: {BLACK}{os.getcwd()}{RESET}")
		current_dir_list.append(os.getcwd())
		num, res = scan_dir(directory, num_of_items_in_dir, repository, verify_repo)
		directory = os.chdir("..")
		directory = os.listdir()
		num_of_items_in_dir = len(directory)
		if count == 10:
			# time.sleep(1)
			print("Not a git repository.")
			print()
			sys.exit(1)
		count += 1
	returned_dict = ignore__pycache(current_dir_list)
	if action:
		paths_list = create_gitignore(returned_dict, current_directory, action=action)
		# print("the list: ", [ i.strip() for i in paths_list ])
		return [ i.strip() for i in paths_list ]
	else:
		create_gitignore(returned_dict, current_directory)
		# print(f"create_gitignore else clause")
		return 1

if __name__ == "__main__":
	entry_point()
	# entry_point(action="extraction")
