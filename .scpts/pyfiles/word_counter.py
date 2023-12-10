#!/usr/bin/env python3

import subprocess, time, os, sys

def check_arg(files):
	length = len(files)
	if length == 1:
		print("No argument(s) provided.")
		sys.exit(1)
	return length
	

def counter(files):
	length = check_arg(files)
	print()
	for file in range(1, length):
		check = os.path.join((files[0].split(os.path.sep))[0], files[file])
		if os.path.isdir(check):
			continue
		time.sleep(.8)
		shell_return = subprocess.run(["wc", files[file]], capture_output=True)
		lines, words, chars, name = shell_return.stdout.decode().strip().split()
		print("============= {} =============".format(name))
		print("lines: {}, words: {}, characters: {}".format(lines, words, chars))
		print()


def lines_words_chars_file(files):
	length = check_arg(files)
	for file in range(1, length):
		check = os.path.join((files[0].split(os.path.sep))[0], files[file])
		if os.path.isdir(check):
			continue
		shell_return = subprocess.run(["wc", files[file]], capture_output=True, text=True)
		lines, words, chars, name = shell_return.stdout.strip().split()
		print("lines: {}, words: {}, characters: {}".format(lines, words, chars))
	
	return lines, words, chars, name
