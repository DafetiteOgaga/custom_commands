#!/usr/bin/env python3

import os, sys, subprocess
from pyfiles.my_prompt import main as prompt
from pyfiles.check_db import check_database
from pyfiles.check_MySQLdb import check_mysqldb
from pyfiles import check_MySQLdb
from pyfiles.configure_settings_py import find_settings_py as settings
from pyfiles.print import print_norm as print_stdout, quit_program, is_git_bash_sh
from pyfiles.subprocessfxn import run_subprocess, run_subprocess_cmd_alone

def locator(disp_list: list, manage_py_list: list, migration_list: list):
	"""Forward seraches the current directory and its sub-directory(ies)

	Args:
		disp_list (list): []
		manage_py_list (list): []
		migration_list (list): []

	Returns:
		tuple: tuple of all the list parameters passed as arguments
	"""
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
			locator(disp_list, manage_py_list, migration_list)
			os.chdir(cur_dir)
	return disp_list, manage_py_list, migration_list


def main(runserver: str=None, migrate: str=None, show: str=None):
	"""parse the lists and return the option selected by the user

	Args:
		runserver (str, optional):  Defaults to None.
		migrate (str, optional):  Defaults to None.
		show (str, optional):  Defaults to None.

	Returns:
		tuple: the option selected by the user
	"""
	_, manage, migration = locator([], [], [])
	# cur_path = os.getcwd()
	if runserver:
		if len(manage) == 0:
			print_stdout('No django project found in this directory or its sub-directories.')
			print_stdout('Change to a directory that has a django project or has it in its sub-directory(ies).')
			quit_program("q", 1)
		elif len(manage) == 1:
			return manage[0]
		else:
			str_name = 'List of projects in the current directory.'
			print_stdout(str_name)
			print(''.rjust(len(str_name) + 5, '.'))
			for index, i in enumerate(manage):
				a, b , c = (i.split(os.sep))[-3], (i.split(os.sep))[-2], (i.split(os.sep))[-1]
				print_stdout(f'{index + 1}. {(os.sep).join([a, b, c])}')
			print()
			try:
				option = input("Select the project you wish to spin up. [q] - exit >>> ")
			except KeyboardInterrupt:
				quit_program("q", 1)
			quit_program(option)
			option = int(option) - 1
			print_stdout(f'Spinning server for project: {manage[option].split(os.sep)[-1]}')
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
			if len(app_list) == 0:
				print()
				print_stdout('No migration found')
				print_stdout('Use "makemigrations", "migrate" or "mkandmigrate"')
				quit_program("q", 1)
			for index, i in enumerate(app_list):
				print(f'{index + 1}. {i}')
			print()
			try:
				selection = input('Make a selection. [q] - exit >>> ')
			except KeyboardInterrupt:
				quit_program("q")
			quit_program(selection)
			selection = int(selection) - 1
		else:
			if len(app_name_list) == 0:
				print()
				print_stdout('No app/history found')
				print_stdout('Use "makemigrations", "migrate" or "mkandmigrate"')
				quit_program("q", 1)
			for index, i in enumerate(app_name_list):
				print_stdout(f'{index + 1}. {i}')
			print()
			try:
				selection = input('Select an option. [q] - exit >>> ')
			except KeyboardInterrupt:
				quit_program("q")
			quit_program(selection)
			selection = int(selection) - 1
		return dict_app_name, app_list[selection]
	
	
def output_func():
	"""displays the output of the process to the user

	Returns:
		str: the django command and args to be executed by the shell
	"""
	# manage_obj = open(os.path.join(os.environ['HOME'], '.xbin', 'pymanage'))
	manage_obj = "python3 manage.py "
	# content = manage_obj.readlines()[0]
	content = manage_obj
	migrate = content + 'migrate'
	showmigrations = content + 'showmigrations'
	sqlmigrate = content + 'sqlmigrate'
	runserver = content + 'runserver'
	manage_text = migrate
	number_of_args = len(sys.argv)

	if number_of_args == 2 and (sys.argv[1] == 'migration' or sys.argv[1] == 'show') or '/sqlmigrate' in sys.argv[0]:
		if sys.argv[1] == 'show':
			app_name, selection = main(migrate='yes', show='yes')
			if '/showmigrations' in sys.argv[0]:
				manage_text = showmigrations
				ret = f'{manage_text} {app_name}'
			else:
				manage_text = sqlmigrate
				ret = f'{manage_text} {app_name} {selection}'
		else:
			app_name, selection = main(migrate='yes')
			ret = f'{manage_text} {app_name} {selection}'
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
		quit_program("q", 1)
	return ret


def error_check():
	"""Uses the django version command to determine whether there is
	error in the input and process the result accordingly.

	Returns:
		str: integers and strings in the order of errors encountered
	"""

	django = ['python3', '-m', 'django', '--version'] if not is_git_bash_sh else ['python', '-m', 'django', '--version']
	check1 = run_subprocess(django)
	ls = ['ls']
	check2 = run_subprocess(ls)
	if 'No module named django' in check1.stderr:
		return check1.returncode, 'django_not_installed'
	# if "manage.py" not in check2.stdout and "runserver" not in sys.argv[0]:
	# 	return 1, 'wrong_dir'
	# else:
	# 	return 0, 'all good'
	return (1, 'wrong_dir') if ("manage.py" not in check2.stdout and "runserver" not in sys.argv[0]) else (0, 'all good')
	

def error_response(code, response):
	"""present the error response

	Args:
		code (int): int
		response (str): str

	Returns:
		int: 1 for error response
	"""
	if code:
		if response == 'django_not_installed':
			print()
			print_stdout("You don't have django installed or check your virtual environment")
			print_stdout("pip install django")
			print()
		elif response =='wrong_dir':
			print()
			print_stdout("change to the directory containing \"manage.py\"")
			print()
		return 1
	return 0
		
def requirement_txt(found: bool=False):
	"""presents the options to what operation to peform(if applicable)
	the sends the command and args as a return value

	Args:
		found (bool, optional): Defaults to False.

	Returns:
		str: first part of the command
	"""
	if found:
		options = """
a. Update the requirements.txt file
b. Install the dependencies in the requirements.txt
"""
		print(options)
		response = prompt(f'Make a choice. [q] - quit >>> ')
		quit_program(response)
	else:
		print_stdout('Creating requirements.txt file ...')
		response = 'a'

	if response.lower() == 'a':
		return "pip freeze"
	elif response.lower() == 'b':
		return "pip install -r"
	else:
		print()
		print('Invalid entry!')
		quit_program("q", 1)


def check_database_type(drf: bool=False):
	"""Checks the database type installed or if DRF is installed.

	Args:
		drf (bool, optional): indicates if the process is checking for
		DRF or database. Defaults to False.
	"""
	db_check = check_database(py=True)
	print(db_check)
	if drf:
		print()
		print_stdout("You don't have django rest framework installed properly.")
		print_stdout("Run: drf command")
		quit_program("q", 1)
	if 'MySQL' in db_check:
		mysqlclient = check_mysqldb(py=True)
		if mysqlclient == 'not installed':
			print()
			print_stdout("You don't have mysqlclient(django connector) installed.")
			print_stdout("pip install mysqlclient")
			print_stdout("if any issue:")
			print_stdout("    sudo apt-get install pkg-config")
			print_stdout("    sudo apt-get install libmysqlclient-dev")
			print_stdout("    pip install mysqlclient")
			quit_program("q", 1)

def moduleNotFound_in_settings(err_output):
	"""Handles the ModuleNotFoundError.

	Args:
		err_output (str): the error content
	"""
	# print('output.stderr:s', err_output)
	if "ModuleNotFoundError: No module named" in err_output:
		check_database_type()
		_, module1 = err_output.split("ModuleNotFoundError: No module named")
		module1 = module1.strip()
		module1 = module1.strip("'")
		cur_dir = os.getcwd()
		settings_path = settings()
		setting_dir = "/".join(settings_path[0].split('/')[:-1])
		os.chdir(setting_dir)
		with open(f'{setting_dir}/settings.py') as f:
			data = f.readlines()
		os.chdir(cur_dir)
		data = " ".join(data)
		if f'"{module1}"' in data or f"'{module1}'" in data:
			print_stdout(f"Error: ModuleNotFoundError: No module named '{module1}'")
			print_stdout(f"If you installed '{module1}' and later deleted the app:")
			print_stdout(f"	either Remove '{module1}' from the list of INSTALLED_APPS in settings.py")
			print_stdout(f"	and/or Re-install '{module1}'")
		else:
			print_stdout('output.stderr:', err_output)


def django_migrate():
	"""Initiates the migrate operation
	"""
	code, response = error_check()
	stop = error_response(code, response)
	if stop:
		quit_program("q", stop)

	if len(sys.argv) > 2:
		args = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
		sys.argv = args
	if len(sys.argv) == 2:
		sys.argv[1] = 'migration'
	command = output_func()
	print()
	# check_database_type()
	output = run_subprocess(command.split())
	if output.stderr:
		moduleNotFound_in_settings(output.stderr)
	if output.stdout:
		print('output.stdout:', output.stdout)
	# if "import MySQLdb as Database" and "No module named 'MySQLdb'" in output.stderr:


def runserver_func():
	"""Initiates the runserver operation
	"""
	code, response = error_check()
	stop = error_response(code, response)
	if stop:
		quit_program("q", stop)

	if len(sys.argv) == 2 and type(sys.argv[1]) != int and len(sys.argv[1]) != 4:
		print()
		print_stdout('port number must be an integer of 4 numbers')
		quit_program("q", 1)

	text_path = os.getcwd()
	print()
	command1 = main(runserver='yes')

	os.chdir(command1)

	command2 = output_func()
	drf = check_MySQLdb.check_drf(py=True)
	# if drf == "DRF not installed":
	# 	check_database_type(drf=True)
	check_database_type()
	try:
		ctrl_c = run_subprocess_cmd_alone(command2.split())
	except KeyboardInterrupt:
		print()
		print_stdout('Development Server exited.')
		print()
		

def sqlmigrate_func():
	"""Initiates the sqlmigrate operation
	"""
	error_check()
	code, response = error_check()
	stop = error_response(code, response)
	if stop:
		quit_program("q", stop)

	if len(sys.argv) > 1:
		args = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
		sys.argv = args
	sys.argv = sys.argv + ['show']
	command = output_func()
	print()
	check_database_type()
	output = run_subprocess(command.split())
	if output.stderr:
		moduleNotFound_in_settings(output.stderr)
	if output.stdout:
		print('output.stdout:', output.stdout)


def requirements_func():
	"""Initiates the requirement_txt operation
	"""
	code, response = error_check()
	stop = error_response(code, response)
	if stop:
		quit_program("q", stop)

	if len(sys.argv) > 1:
		args = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
		sys.argv = args
		output_func()

	requirement = 'requirements.txt'
	check_req = run_subprocess(['ls'])
	found = False
	for i in check_req.stdout.split():
		if i == requirement:
			found = True
			
	command = requirement_txt(found=found)
	print()
	command = command.split()

	if len(command) == 2:
		with open(requirement, 'w') as requirements_file:
			create = subprocess.run(command, stdout=requirements_file)
		if create.returncode == 0:
			print_stdout('Success.')
	else:
		command = command + [requirement]
		run_subprocess_cmd_alone(command)
