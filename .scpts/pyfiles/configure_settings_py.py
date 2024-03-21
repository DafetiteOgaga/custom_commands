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


def install_entity(entity: str, file_path: str):
	with open(file_path) as f:
		data = f.readlines()
	for index, line in enumerate(data):
		if "'django.contrib.staticfiles'," in line:
			line = "    " + "'" + entity + "'"  + "," + "\n"
			data.insert(index + 1, line)
			break
	with open(file_path, 'w') as g:
		g.writelines(data)

entity = input()
settings_path = configure_settings_py()
if len(settings_path) > 1:
	print('You have multiple settings.py files')
	print('Setting settings:', settings_path)
install_entity(entity, settings_path[0])
