#!/usr/bin/env python3

import time, subprocess, os, sys
from .colors import *
from pyfiles.subprocessfxn import run_subprocess
from pyfiles.print import quit_program, print_norm

def check_arg(files):
	"""checks that atleast a file(argument) is
		passed from the CL

	Args:
		files (str): arguments

	Returns:
		int: length of arguments
	"""
	length = len(files)
	if length == 1:
		print_norm("No argument(s) provided.")
		quit_program("q", 1)
	return length
	

def counter(files):
	"""This function loops through the files(arguments) passed from
		the CL and prints their
	1. number of lines
	2. number of words
	3. number of characters
	4. filenames

	Args:
		files (str): arguments
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
			print("::::: ============= {}{}{} =============".format(BRIGHT_GREEN, name, RESET))
			print("::::: {}lines: {}{}, {}words: {}{}, {}characters: {}{}".format(GREEN, RESET, lines, BLUE, RESET, words, MAGENTA, RESET, chars))
		except ValueError:
			print('::::: Error: "{}{}{}" is not a valid filename.'.format(RED, files[file], RESET))
		except Exception as e:
			print(f"::::: An unexpected error occurred: {RED}{e}{RESET}")
		print()
		# {RED}{line}{RESET}


def lines_words_chars_file(files):
	"""This function loops through the files(arguments) passed from the
		CL and returns their
	1. number of lines
	2. number of words
	3. number of characters
	4. filenames

	Args:
		files (str): arguments

	Returns:
		str: lines, words, chars, name of the file
	"""
	length = check_arg(files)
	for file in range(1, length):
		check = os.path.join((files[0].split(os.path.sep))[0], files[file])
		if os.path.isdir(check):
			continue
		shell_return = run_subprocess(["wc", files[file]])
		lines, words, chars, name = shell_return.stdout.strip().split()
		print("lines: {}, words: {}, characters: {}".format(lines, words, chars))
	
	return lines, words, chars, name
