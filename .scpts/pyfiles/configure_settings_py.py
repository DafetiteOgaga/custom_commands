#!/usr/bin/env python3

import os, sys, subprocess

def skip_venv_dir():
	"""Checks if the current working directory is a venv directory
        and returns True if it is, otherwise false.

	Returns:
		bool: boolean
	"""
	current_dir_files = os.listdir()
	venv = ['pyvenv.cfg', 'include', 'lib']
	resp = []
	resp_dict = {}
	for dir in venv:
		if dir in current_dir_files:
			resp_dict[dir] = True
			resp.append(True)
	if len(resp_dict) == 3:
		if resp_dict['pyvenv.cfg'] and resp_dict['include'] and resp_dict['lib']:
			if resp_dict['pyvenv.cfg'] == resp_dict['include'] == resp_dict['lib'] == True:
				# print('resp_dict: %s' % resp_dict)
				# filter_resp = set(resp)
				return True
	return False

def dir_checker(venv: bool=False):
	"""Generates a list of subdirectories that ascertain the current working
        directory is a virtual environment

	Args:
		venv (bool, optional): indicates that the function is expected
        to return a list of subdirectories with their complete paths. 
        Defaults to False.

	Returns:
		list: list of venv subdirectories
	"""
	final_list = []
	venv_check = skip_venv_dir()
	if venv_check:
		final_list.append(os.getcwd())
	for item in os.listdir():
		if not os.path.isfile(item):
			current_dir = os.getcwd()
			os.chdir(os.path.join(current_dir, item))
			venv_check2 = skip_venv_dir()
			if venv_check2:
				final_list.append(os.getcwd())
			else:
				if venv:
					final_list.extend(dir_checker(venv=True))
				else:
					final_list.extend(dir_checker())
			os.chdir(current_dir)
	
	# make this return the venv dir instead of its subdirs
	if venv:
		return final_list
	else:
		final_list = [i.split('/')[-1] for i in final_list] + ['.git']
		return list(set(final_list))


# FILE_COUNT_THRESHOLD = 1000  # Adjust this threshold as needed
def should_skip_directory(dir_path):
	"""Ascertain if the given directory path is a virtual environment.

	Args:
		dir_path (str): the directory to check

	Returns:
		bool: boolean
	"""
	# if len(os.listdir(dir_path)) > FILE_COUNT_THRESHOLD:
	#     return True
	if dir_path.split('/')[-1] in dir_checker():
		return True
	return False


def compile_dir_list(directory, venv: bool=False):
	"""Generates a list of subdirectories in the current working
		directory and returns a list with complete paths of just
        the directories names, depending on the the boolean value
        of venv

	Args:
		directory (str): parent directory
		venv (bool, optional): indicates that the function is expected
        to return a list of subdirectories with their complete paths. 
        Defaults to False.

	Returns:
		list: list of subdirectories
	"""
	final_list = []
	for item in os.listdir(directory):
		item_path = os.path.join(directory, item)
		final_list.append(item_path)
		if os.path.isdir(item_path):
			if not should_skip_directory(item_path):
				final_list.extend(compile_dir_list(item_path))
	if venv:
		return final_list, list(set(dir_checker(venv=True)))
	else:
		return final_list


def find_settings_py():
	"""Generates a paths to settings.py and views.py files

	Returns:
		list: list of settings.py and views.py files
	"""
	settings = compile_dir_list(os.getcwd())
	settings = [file for file in settings if file.endswith('settings.py') or file.endswith('views.py')]
	ret = set(settings)
	return list(ret)

try:
	# lines = '................................'
	settings_path = find_settings_py()
	# print(lines)
	# for d, s in enumerate(settings_path):
	# 	print(f'{d+1}. {s}')
	# print(lines)
	file_path = [k for k in settings_path if k.endswith('settings.py')][0]
	# print('file_path global: {}'.format(file_path))
except IndexError:
    print('...')


def install_entity(entity: str, djoser: bool=False):
	"""Configures the settings.py and project's urls.py files for
        DRF, djoser, jwt and static files

	Args:
		entity (str): the string that will be installed under
        INSTALLED_APPS in settings.py
		djoser (bool, optional): indicates that the function is called
        with a djoser command. Defaults to False.
	"""
	description = "\t\t" + "# <- added " + entity
	line_content = "    " + "'" + entity + "'"  + "," + description + " here" + "\n"

	app = ([k for k in settings_path if k.endswith('views.py')][0]).split('/')[-2]
	djoser_variable = \
			"\n" + f"# Added {entity} variable to the settings.py file" + \
			"\n" + "# Configure Djoser to use JWT tokens" + \
			"\n" + "#DJOSER = {" + \
			"\n" + "#    'USER_ID_FIELD': 'username'," + \
			"\n" + "#    'SERIALIZERS': {" +  \
			"\n" + f"#        'user_create': '{app}.serializers.UserCreateSerializer'," + \
			"\n" + "#    }," + \
			"\n" + "#    'AUTH_TOKEN_CLASSES': (" + \
			"\n" + "#        'djoser.auth.tokens.JWTToken',  # Use JWT for authentication tokens" + \
			"\n" + "#    )," + \
			"\n" + "#    'JWT_AUTH_COOKIE': 'your_cookie_name',  # Customize the cookie name if needed" + \
			"\n" + "#    'JWT_EXPIRATION_DELTA': timedelta(days=1),  # Customize token expiration if needed" + \
			"\n" + "#    # Add any other Djoser configurations as needed" + \
			"\n" + "#}" + "\n"

	restframework_variable = \
			"\n" + f"# Added {entity} variable to the settings.py file" + \
			"\n" + "REST_FRAMEWORK = {" + \
			"\n" + "    'DEFAULT_FILTER_BACKENDS': [" + \
			"\n" + "        'rest_framework.filters.OrderingFilter'," + \
			"\n" + "        'rest_framework.filters.SearchFilter'," + \
			"\n" + "    ]," + \
			"\n" + "    'DEFAULT_AUTHENTICATION_CLASSES': (" + \
			"\n" + "        'rest_framework.authentication.TokenAuthentication'," + \
			"\n" + "        'rest_framework.authentication.SessionAuthentication'," + \
			"\n" + "    )," + \
			"\n" + "    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination'," + \
			"\n" + "    'PAGE_SIZE': 2" + \
			"\n" + \
			"\n" + "#    # Configure Django REST Framework to use Simple JWT authentication" + \
			"\n" + "#    'DEFAULT_AUTHENTICATION_CLASSES': (" + \
			"\n" + "#        'rest_framework_simplejwt.authentication.JWTAuthentication'," + \
			"\n" + "#        # Add any other authentication classes as needed" + \
			"\n" + "#    )," + \
			"\n" + "}" + "\n"

	jwt_variable = \
			"\n" + "# Configure Django REST Framework to use Simple JWT authentication" + \
			"\n" + "SIMPLE_JWT = {" + \
			"\n" + "    'AUTH_HEADER_TYPES': ('Bearer',)," + \
			"\n" + "}" + "\n"

	check = check_existence(entity=entity)
	if not check:
		mod_data = insert_lines(entity=entity, line_content=line_content, djoser=djoser)
		variable = False
		match entity:
			case "djoser":
				urls_data = insert_lines(entity=entity, line_content=line_content, urls=True, djoser=True)
				variable = djoser_variable
			case "rest_framework.authtoken":
				variable = restframework_variable
			case "rest_framework_simplejwt":
				variable = jwt_variable
				urls_data = insert_lines(entity=entity, line_content=line_content, urls=True, djoser=False)
			case "static":
				project_dir = file_path.split('/')[-2]
				base_dir_path = os.path.join(os.getcwd(), 'static', project_dir)
				project_dir_path = os.path.join(os.getcwd(), project_dir, 'static', project_dir)
				os.makedirs(base_dir_path, exist_ok=True)
				os.makedirs(project_dir_path, exist_ok=True)

				variable = \
					"\n" + f"# Added {entity} variable to the settings.py file" + \
					"\n" + "STATICFILES_DIRS = [" + \
					"\n" + "    BASE_DIR / 'static'," + description + " to BASE_DIR" + \
					"\n" + f"    BASE_DIR / 'static/{project_dir}'," + description + " to project dir" + \
					"\n" + "]" + "\n"

		if variable:
			with open(file_path, 'a') as k:
				k.writelines(variable)


def insert_lines(entity: str, line_content: str, urls: bool=False, djoser: bool=False):
	"""Afix the necessary configuration lines into settings.py
        and project's urls.py.

	Args:
		entity (str): the string that will be installed under
        INSTALLED_APPS in settings.py
		line_content (str): description to be appended to the
        inserted line.
		urls (bool, optional): indicates that the function is called
        with a djoser command. Defaults to False.
		djoser (bool, optional): indicates that urls.py file is to be
		configured. Defaults to False.

	Returns:
		list: list of file content
	"""
	if urls:
		file_path = f"{os.sep}".join(file_path.split('/')[:-1])
		file_path = os.path.join(file_path, "urls.py")
		entity = 'djoser.urls.authtoken'
		if not djoser:
			entity = 'djoser.urls.jwt'

	with open(file_path) as f:
		data = f.readlines()
	installed_apps = False
	content_insert = ''
	checker = False
	for i in data:
		if "include('djoser.urls'))" in i:
			checker = True
	for index, line in enumerate(data):
		if urls:
			if "urlpatterns =" in line:
				if not checker:
					content_insert += "    path('api/', include('djoser.urls'))," + \
		 							"\n"
				if djoser:
					content_insert += "    path('api/', include('djoser.urls.authtoken'))," + \
								"\n"
				else:
					content_insert += "    path('api/', include('djoser.urls.jwt')),  # For JWT authentication" + \
									"\n"
				continue
			if content_insert and "]" in line:
				data.insert(index, content_insert)
				break
		else:
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
	return data


def check_existence(entity: str):
	"""Checks is the configuration of settings.py and urls.py
    already exists in the project.

	Args:
		entity (str): string to check in the given file

	Returns:
		bool: boolean
	"""
	with open(file_path) as f:
		data = f.readlines()
	for i in data:
		if f"'{entity}'," in i or f'"{entity}",' in i:
			return True

################################


def entry_point():
	"""Point of entry if the script is executed from the command line.
	"""
	# print('AAAAA enter something ...')
	entity = input()
	# entity = 'djoser'
	djoser = False
	print()
	

	# sys.exit(0)
	if len(settings_path) > 2:
		print('You have multiple settings.py files')
		for i, j in enumerate(settings_path):
			print(f'{i+1}. {j}')
		sys.exit(0)

	if entity == "djoser":
		djoser = True
	install_entity(entity, djoser=djoser)


if __name__ == "__main__":
	entry_point()
