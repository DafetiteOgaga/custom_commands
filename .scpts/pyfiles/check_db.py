#!/usr/bin/env python3

# CheckDatabase.py
def check_database(py: bool=False):
	"""Checks, print and return the type of database installed
        in django's settings.py

	Args:
		py (bool, optional): indicates that the function was called
		from a .py script. Defaults to False.

	Returns:
		str: database type detected
	"""

	import os, sys
	try:
		from pyfiles.configure_settings_py import find_settings_py as settings
	except ModuleNotFoundError:
		from configure_settings_py import find_settings_py as settings

	cur_dir = os.getcwd()
	settings_path = settings()
	settings_path = [setting for setting in settings_path if setting.endswith('settings.py')]
	# print("Settings path: %s" % settings_path)
	setting_dir = "/".join(settings_path[0].split('/')[:-1])
	os.chdir(setting_dir)
	with open(f'{setting_dir}/settings.py') as f:
		data = f.readlines()
	os.chdir(cur_dir)

	try:
		sqlite = '.sqlite'
		postgresql = '.postgresql'
		mysql = '.mysql'
		found1 = found2 = found3 = False
		unknown_db = "Unknown database detected:"
		multiple_dbs = "Multiple databases detected:"
		for line in data:
			if postgresql in line:
				if not py:
					print("PostgreSQL database detected.")
				found1 = True
				ret = 'PostgreSQL database detected.'
			if sqlite in line:
				if not py:
					print("SQLite database detected.")
				found2 = True
				ret = 'SQLite database detected.'
			if mysql in line:
				if not py:
					print("MySQL database detected.")
				found3 = True
				ret = 'MySQL database detected.'
			if found1 == found2 == found3 == True:
				if not py:
					print(multiple_dbs)
				ret = multiple_dbs
			elif found1 == found2 == True:
				if not py:
					print(multiple_dbs)
				ret = multiple_dbs
			elif found1 == found3 == True:
				if not py:
					print(multiple_dbs)
				ret = multiple_dbs
			elif found2 == found3 == True:
				if not py:
					print(multiple_dbs)
				ret = multiple_dbs
			else:
				if not py:
					print(unknown_db)
				ret = unknown_db
		return ret
	except Exception as e:
		print("Error:", e)

	
if __name__ == "__main__":
	check_database()

