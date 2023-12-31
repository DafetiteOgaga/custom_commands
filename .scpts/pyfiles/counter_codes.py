#!/usr/bin/env python3

import time, subprocess, os, sys
from .colors import *

def check_arg(files):
	"""This function checks that atleast a file(argument) is
		passed from the CL
	"""

	length = len(files)
	if length == 1:
		print("No argument(s) provided.")
		sys.exit(1)
	return length
	

def counter(files):
	"""This function loops through the files(arguments) passed from
		the CL and prints their
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
	"""

	length = check_arg(files)
	for file in range(1, length):
		check = os.path.join((files[0].split(os.path.sep))[0], files[file])
		if os.path.isdir(check):
			continue
		shell_return = subprocess.run(["wc", files[file]], capture_output=True,
				text=True)
		lines, words, chars, name = shell_return.stdout.strip().split()
		print("lines: {}, words: {}, characters: {}".format(lines, words, chars))
	
	return lines, words, chars, name
