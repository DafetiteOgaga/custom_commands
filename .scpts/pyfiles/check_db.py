#!/usr/bin/env python3

# CheckDatabase.py
def check_database(py: bool=False):

	import os, sys
	try:
		from pyfiles.configure_settings_py import find_settings_py as settings
	except ModuleNotFoundError:
		from configure_settings_py import find_settings_py as settings

	cur_dir = os.getcwd()
	settings_path = settings()
	setting_dir = "/".join(settings_path[0].split('/')[:-1])
	os.chdir(setting_dir)
	with open(f'{setting_dir}/settings.py') as f:
		data = f.readlines()
	os.chdir(cur_dir)
	# data = " ".join(data)

	try:
		sqlite = '.sqlite'
		postgresql = '.postgresql'
		mysql = '.mysql'
		found1 = found2 = found3 = False
		unknown_db = "Unknown database detected:"
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
					print(unknown_db)
				ret = unknown_db
			elif found1 == found2 == True:
				if not py:
					print(unknown_db)
				ret = unknown_db
			elif found1 == found3 == True:
				if not py:
					print(unknown_db)
				ret = unknown_db
			elif found2 == found3 == True:
				if not py:
					print(unknown_db)
				ret = unknown_db
			# else:
			# 	ret = unknown_db
		return ret
	except Exception as e:
		print("Error:", e)

	
if __name__ == "__main__":
	check_database()
