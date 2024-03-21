#!/usr/bin/env python3

import os, sys, subprocess

def configure_settings_py():
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
	line_content = "    " + "'" + entity + "'"  + "," + "\t\t" + "# <- added " + entity + " here" + "\n"
	djoser_variable = "\n" + "# Add a new section in the settings.py file" + "\n" + "DJOSER = {" + "\n" +"    'USER_ID_FIELD': 'username'  # <-- Add this line" + "\n" + "}" + "\n"
	restframework_variable = "\n" + "REST_FRAMEWORK = {" + "\n" + "    'DEFAULT_AUTHENTICATION_CLASSES': [" + "\n" + "        'rest_framework.authentication.TokenAuthentication'," + "\n" + "        'rest_framework.authentication.SessionAuthentication'," + "\n" +  "    ]," + "\n" + "}" + "\n"
	installed_apps = False
	check = check_existence(entity=entity, data=data)
	if not check:
		for index, line in enumerate(data):
			if "'django.contrib.staticfiles'," in line:
				if djoser:
					installed_apps = True
					continue
				data.insert(index + 1, line_content)
				break
			if installed_apps and "]" in line:
				data.insert(index, line_content)
				break
		with open(file_path, 'w') as g:
			g.writelines(data)
		if djoser:
			with open(file_path, 'a') as k:
				k.writelines(djoser_variable)
		if entity == "rest_framework.authtoken":
			with open(file_path, 'a') as h:
				h.writelines(restframework_variable)


def check_existence(entity: str, data: list):
    for i in data:
        if f"'{entity}'," in i or f'"{entity}",' in i:
            return True


entity = input()
djoser = False
settings_path = configure_settings_py()
if len(settings_path) > 1:
	print('You have multiple settings.py files')
	print('Setting settings:', settings_path)
	sys.exit(0)
if entity == "djoser":
	djoser = True
install_entity(entity, settings_path[0], djoser=djoser)

