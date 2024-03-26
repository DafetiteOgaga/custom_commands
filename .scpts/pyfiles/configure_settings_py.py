#!/usr/bin/env python3

import os, sys, subprocess

def find_settings_py():
	settings_py_list = []
	def search_for_settings():
		settings_location = None
		for name in os.listdir():
			if os.path.isfile(name):
				if name == 'settings.py':
					settings_location = os.getcwd()
					settings_location = os.path.join(settings_location, name)
					settings_py_list.append(settings_location)
			else:
				initial_path = os.getcwd()
				os.chdir(name)
				settings_py_list.extend(search_for_settings())
				os.chdir(initial_path)
		return settings_py_list
	ret = set(search_for_settings())
	return list(ret)


def install_entity(entity: str, file_path: str, djoser: bool=False):
	with open(file_path) as f:
		data = f.readlines()
	description = "\t\t" + "# <- added " + entity
	line_content = "    " + "'" + entity + "'"  + "," + description + " here" + "\n"
	djoser_variable = "\n" + "# Add a new section in the settings.py file" + "\n" + "DJOSER = {" + "\n" +"    'USER_ID_FIELD': 'username'  # <-- Add this line" + "\n" + "}" + "\n"
	restframework_variable = "\n" + "REST_FRAMEWORK = {" + "\n" + "    'DEFAULT_AUTHENTICATION_CLASSES': [" + "\n" + "        'rest_framework.authentication.TokenAuthentication'," + "\n" + "        'rest_framework.authentication.SessionAuthentication'," + "\n" +  "    ]," + "\n" + "}" + "\n"
	installed_apps = False
	check = check_existence(entity=entity, data=data)
	if not check:
		for index, line in enumerate(data):
			if entity != "static":
				if "'django.contrib.staticfiles'," in line:
					if djoser:
						entity = "djoser"
						installed_apps = True
						continue
					else:
						data.insert(index + 1, line_content)
						break
				if installed_apps and "]" in line:
					data.insert(index, line_content)
					break
		with open(file_path, 'w') as g:
			g.writelines(data)
		variable = False
		match entity:
			case "djoser":
				variable = djoser_variable
			case "rest_framework.authtoken":
				variable = restframework_variable
			case "static":
				# base_dir = file_path.split('/')[-3]
				project_dir = file_path.split('/')[-2]
				base_dir_path = os.path.join(os.getcwd(), 'static')
				project_dir_path = os.path.join(os.getcwd(), project_dir, 'static')
				if not os.path.exists(base_dir_path):
					os.mkdir(base_dir_path)
				if not os.path.exists(project_dir_path):
					os.mkdir(project_dir_path)
				variable = "\n" + "STATICFILES_DIRS = [" + "\n" + "    BASE_DIR / 'static'," + description + " BASE_DIR" + "\n" + f"    BASE_DIR / 'static/{file_path.split('/')[-2]}'," + description + " project dir" + "\n" + "]" + "\n"
		if variable:
			with open(file_path, 'a') as k:
				k.writelines(variable)


def check_existence(entity: str, data: list):
    for i in data:
        if f"'{entity}'," in i or f'"{entity}",' in i:
            return True

def entry_point():
	entity = input()
	djoser = False
	settings_path = find_settings_py()
	# print('settings_path:', settings_path)
	if len(settings_path) > 1:
		print('You have multiple settings.py files')
		print('Setting settings:', settings_path)
		sys.exit(0)
	# print('entity:', entity)
	if entity == "djoser":
		djoser = True
	install_entity(entity, settings_path[0], djoser=djoser)


if __name__ == "__main__":
    entry_point()