#!/usr/bin/env python3

import os, sys
from print import is_git_bash_sh

input_str = input()

def filterFunc(list_in: str, type: str):
	# print(f'list_in: {list_in}')
	list_in = list_in.split()
	# print(f'type: {type}')
	# print(f'list_in: {list_in}')
	isgitBash = is_git_bash_sh()
	# print(f'isgitBash: {isgitBash}')
	list_in = [filename.split('/' if isgitBash else os.sep)[-1] for filename in list_in]
	# print(f'os sep: {os.sep}')
	# print(f'list_in: {list_in}')
	files = []
	type, _ = type.split('-')
	if type == 'react':
		files = ['App.js', 'index.js', 'package.json', 'index.html']
	elif type == 'reactNative':
		files = ['app.json', 'package.json', 'index.tsx']
	# [print(f'{file}') in list_in for file in files]
	result = all(file in list_in for file in files)
	print(result)
	return result

def reactNative(list_in: str):
	list_in = list_in.split()
	# for i in list_in:
	# 	print(i)
	appjson = [file for file in list_in if file.endswith('app.json')]
	indextsxjs = [file for file in list_in if file if file.endswith('index.tsx') or file.endswith('index.js')]
	# print(f'appjson: {appjson} indextsxjs: {indextsxjs}')
	if appjson and indextsxjs:
		list_in = [file for file in list_in if file if file.endswith('package.json')]
		with open(list_in[0]) as f:
			next(f)
			filename = f.readline().strip().split('"')[3]
		print(filename)

def react(list_in: str):
	list_in = list_in.split()
	# for i in list_in:
	# 	print(i)
	appjs = [file for file in list_in if file if file.endswith('App.js')]
	appcss = [file for file in list_in if file if file.endswith('App.css')]
	# print(f'appjs: {appjs} appcss: {appcss}')
	if appjs and appcss:
		list_in = [file for file in list_in if file if file.endswith('package.json')]
		with open(list_in[0]) as f:
			next(f)
			filename = f.readline().strip().split('"')[3]
		print(filename)


if __name__ == '__main__':
	# print('sys.argv: %s' % sys.argv)
	func = sys.argv[1]
	if func == 'reactNative-Check' or func == 'react-Check':
		filterFunc(input_str, type=func)
	elif func == 'reactNative':
		reactNative(input_str)
		pass
	elif func == 'react':
		react(input_str)
		pass
