#!/usr/bin/env python3

import sys

def add_line(data: str):
	line = sys.argv[2]
	formatted_line = ''
	for char in line:
		if char == '£':
			formatted_line += '\t' * 4
		elif char == '&':
			formatted_line += '\n'
		elif char == '*':
			formatted_line += '\t'
		else:
			formatted_line += char
	file_path = sys.argv[3]
	with open(file_path) as original:
		file_data = original.readlines()
	for index, fileline in enumerate(file_data):
		if "</a>" in fileline.strip():
			file_data.insert(index+1, formatted_line)
			print('ok')
			break
	with open(file_path, 'w') as modified:
		modified.writelines(file_data)
		print('ok')

def get_module_error(data: str):
	# print('##### data from fxn:', data, '#####')
	data = data.split('\n')
	for line in data:
		if 'ModuleNotFoundError' in line:
			module = line.split().pop()
			# print('##### module from fxn:', module, '#####')
			# print('GOT HERE')
			print(module)
			return module

def entry_point():
	# print('HEREEEEEEEEEEEEEEEEEEE')
	# arg = sys.argv
	# for i, v in enumerate(arg):
	# 	print(f'{i}. {v}')
	arg1 = sys.argv[1]
	# print(f'argument 1: {arg1}')
	commands = ['django', 'react',]
	fxn_list = [get_module_error, add_line]
	commands = {x : {'fxn': fxn, 'length': len(x)} for x, fxn in zip(commands, fxn_list)}
	input_data = sys.stdin.read()
	# print('raw input:', input_data)
	for command, item in commands.items():
		# print(f'Command: {command}, arg: {arg1}')
		# print(f'Command: {command}, item: {item}')
		if arg1 == command:
			# print('FOUND!!!')
			# print(input_data)
			item['fxn'](input_data)
			break
	else:
		print('NOT FOUND!!!')
		print("Command not found in the function list.")

entry_point() if __name__ == "__main__" else None
