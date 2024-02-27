#!/usr/bin/env python3

import os, sys, subprocess

def exit(option: str):
	if option == 'q'.lower():
		print()
		print('Cheers.')
		sys.exit()

def locator1(disp_list: list, manage_py_list: list, migration_list: list):
	migration_dict = {}
	cur_dir = os.getcwd()
	for i in os.listdir():
		if i == 'manage.py':
			manage_py_list.append(cur_dir)
		if os.path.isdir(i):
			new_path = os.path.join(cur_dir, i)
			if i == 'migrations':
				for j in os.listdir(new_path):
					if os.path.isfile(os.path.join(new_path, j)) and j != '__init__.py':
						app_name = new_path.split(os.sep)[-2]
						migration_name = (j.split('.py'))[0]
						name_list = migration_dict.setdefault(app_name, [])
						name_list.append(migration_name)
						if migration_dict not in migration_list:
							migration_list.append(migration_dict)
			disp_list.append(new_path)
			os.chdir(new_path)
			locator1(disp_list, manage_py_list, migration_list)
			os.chdir(cur_dir)
	return disp_list, manage_py_list, migration_list


def main(runserver: str=None, migrate: str=None, show: str=None):
	dirs, manage, migration = locator1([], [], [])
	cur_path = os.getcwd()
	if runserver:
		if len(manage) == 0:
			print('No django project found in this directory or its subdirectories.')
			print('Change to a directory that has a django project or has it in its subdirectory(ies).')
			print()
			sys.exit(1)
		elif len(manage) == 1:
			return manage[0]
		else:
			print('List of projects in the current directory.')
			print('..........................................')
			for index, i in enumerate(manage):
				a, b , c= (i.split(os.sep))[-3], (i.split(os.sep))[-2], (i.split(os.sep))[-1]
				print(f'{index + 1}. {(os.sep).join([a, b, c])}')
			print()
			try:
				option = input("Select the project you wish to spin up. [q] - exit >>> ")
			except KeyboardInterrupt:
				print()
				sys.exit()
			exit(option)
			option = int(option) - 1
			print(f'Spinning server for project: {manage[option].split(os.sep)[-1]}')
			print()
		return manage[option]
	elif migrate:
		cur_dir = os.getcwd()
		app_name = cur_dir.split(os.sep)[-1]
		app_list = []
		app_name_list = []
		for i in migration:
			dict_app_name = (list(i.keys()))[0]
			app_name_list.append(dict_app_name)
			if dict_app_name in os.listdir(cur_dir):
				app_list += i[dict_app_name]
		if not show or 'sqlmigrate' in sys.argv[0]:
			for index, i in enumerate(app_list):
				print(f'{index + 1}. {i}')
			print()
			try:
				selection = input('Select the file you want to use. [q] - exit >>> ')
			except KeyboardInterrupt:
				print()
				sys.exit()
			exit(selection)
			selection = int(selection) - 1
			return f'{dict_app_name} {app_list[selection]}', dict_app_name
		else:
			for index, i in enumerate(app_name_list):
				print(f'{index + 1}. {i}')
			print()
			try:
				selection = input('Select the file you want to use. [q] - exit >>> ')
			except KeyboardInterrupt:
				print()
				sys.exit()
			exit(selection)
			selection = int(selection) - 1
			return f'{dict_app_name} {app_name_list[selection]}', dict_app_name
	
	

def output_func(text_path: str=None):
	manage_obj = open(os.path.join(os.environ['HOME'], '.xbin', 'pymanage'))
	content = manage_obj.readlines()[0]
	migrate = content + 'migrate'
	showmigrations = content + 'showmigrations'
	sqlmigrate = content + 'sqlmigrate'
	runserver = content + 'runserver'
	manage_text = migrate
	number_of_args = len(sys.argv)

	if number_of_args == 2 and (sys.argv[1] == 'migration' or sys.argv[1] == 'show') or '/sqlmigrate' in sys.argv[0]:
		if sys.argv[1] == 'show':
			output, app_name = main(migrate='yes', show='yes')
			if '/showmigrations' in sys.argv[0]:
				manage_text = showmigrations
				ret = f'{manage_text} {app_name}'
			else:
				manage_text = sqlmigrate
				ret = f'{manage_text} {output}'
		else:
			output, app_name = main(migrate='yes')
			ret = f'{manage_text} {output}'
	elif '/migrate' in sys.argv[0]:
		ret = f'{migrate}'
	elif '/showmigrations' in sys.argv[0]:
		ret = f'{showmigrations}'
	elif '/runserver' in sys.argv[0]:
		if number_of_args == 1:
			ret = f'{runserver}'
		elif number_of_args == 2:
			ret = f'{runserver} {sys.argv[1]}'
	else:
		print()
		print('Invalid entry!')
		sys.exit(1)
	return ret


def error_check():
	django = ['python3', '-m', 'django', '--version']
	check1 = subprocess.run(django, capture_output=True,text=True)
	ls = ['ls']
	check2 = subprocess.run(ls, capture_output=True, text=True)
	if check1.stderr == '/usr/bin/python3: No module named django\n':
		return check1.returncode, 'django_not_installed'
	if "manage.py" not in check2.stdout and "runserver" not in sys.argv[0]:
		return 1, 'wrong_dir'
	else:
		return 0, 'all good'
	

def error_response(code, response):
	if code:
		if response == 'django_not_installed':
			print()
			print("You don't have django installed or check your virtual environment")
			print("pip install django")
			print()
		elif response =='wrong_dir':
			print()
			print("change to the directory containing \"manage.py\"")
			print()
		return 1
	return 0
		