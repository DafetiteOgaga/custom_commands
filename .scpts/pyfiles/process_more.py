#!/usr/bin/env python3

import sys

def add_line(data: str):
	line = sys.argv[2]
	formatted_line = ''
	# print(f'line::::: {line}')
	for char in line:
		if char == '£':
			# print('adding 4 tabs')
			formatted_line += '\t' * 4
		elif char == '&':
			# print('adding newline')
			formatted_line += '\n'
		elif char == '*':
			# print('adding a tab')
			formatted_line += '\t'
		else:
			# print('adding nothing')
			formatted_line += char
	file_path = sys.argv[3]
	# print(f'file_path::::: {file_path}')
	is_index_js = file_path.split("/")[-1]=="index.js"
	# print(f'is_index_js::::: {is_index_js}')
	with open(file_path) as original:
		file_data = original.readlines()
	for index, fileline in enumerate(file_data):
		has_strictmodestr = "</React.StrictMode>" in fileline.strip()
		import_for_index_js = "import './index.css';" in fileline.strip()
		# print(f'has_strictmodestr::::: {has_strictmodestr}')
		if "</a>" in fileline.strip():
			file_data.insert(index+1, formatted_line)
			print('ok')
			break
		if is_index_js:
			if import_for_index_js:
				# print('import for index.js')
				file_data.insert(index+1, line.split("+++")[0].strip()+'\n')
				# print('ok')
				# break
				# continue
			if has_strictmodestr:
				# print('sw for index.js')
				# file_data.insert(index+2, '\n\n')
				# file_data.insert(index+2, '\n\n'+line.split("+++")[1].strip()+'\n\n')
				c = line.split("+++")[1].strip()
				# split into lines + clean each line
				lines = [l.strip() for l in c.splitlines() if l.strip()]
				# file_data.insert(index + 2, '\n')
				# insert each line separately (preserve order)
				for i, l in enumerate(lines):
					file_data.insert(index + 2 + i, l + '\n')
				print('ok')
				# break
				# continue
	with open(file_path, 'w') as modified:
		# print(f'modified::::: {modified}')
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
