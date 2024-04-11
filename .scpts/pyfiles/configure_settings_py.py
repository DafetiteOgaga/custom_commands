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

def append_variable(file_path: str, variable: str, no_append: bool=False, index: int=-1):
	if variable:
		line = '............................................................'
		filename = file_path.split(os.sep).pop()
		print(line)
		line_no = ''
		if index > -1:
			line_no = f' on line: {index}'
		print(f'Added to {filename}{line_no} :::::')
		print(f'{".".rjust(len(filename) + len(line_no) + 15, ".")}')
		print(f'{variable}')
		if not no_append:
			with open(file_path, 'a') as k:
				k.writelines([variable])
		print()

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
	file_path = ''
	print('...')

def install_entity(entity: str, file_path: str=file_path, djoser: bool=False,):# variable: str=None):
	"""Configures the settings.py and project's urls.py files for django apps,
		DRF, DRF auth token, djoser, jwt, django toolbar, xml renderer and static files

	Args:
		entity (str): the string that will be installed under
		INSTALLED_APPS in settings.py
		file_path (strl): path to settings.py file
		djoser (bool, optional): indicates that the function is called
		with a djoser command. Defaults to False.
	"""
	command = None
	variable = ''
	rm_FW = False
	try:
		entity, filename = entity.split()
		command = filename.split(os.sep).pop()
	except:
		entity = entity
		pass

	description = "\t\t" + "# <- added " + entity
	line_content = "    " + "'" + entity + "'"  + "," + description + " here" + "\n"

	if command:
		app = entity
	else:
		app = ([k for k in settings_path if k.endswith('views.py')][0]).split('/')[-2]

	check, frameW = check_existence(entity=entity)
	djoser_variable = \
			"\n" + f"# Added {entity} variable to the here" + \
			"\n" + "# Configure Djoser and also to use JWT tokens" + \
			"\n" + "DJOSER = {" + \
			"\n" + "    'USER_ID_FIELD': 'username'," + \
			"\n" + "    'LOGIN_FIELD': 'email'," + \
			"\n" + "#    'SERIALIZERS': {" +  \
			"\n" + f"#        'user_create': '{app}.serializers.UserCreateSerializer'," + \
			"\n" + "#    }," + \
			"\n" + "#    'AUTH_TOKEN_CLASSES': (" + \
			"\n" + "#        'djoser.auth.tokens.JWTToken',  # Use JWT for authentication tokens" + \
			"\n" + "#    )," + \
			"\n" + "#    'JWT_AUTH_COOKIE': 'your_cookie_name',  # Customize the cookie name if needed" + \
			"\n" + "#    'JWT_EXPIRATION_DELTA': timedelta(days=1),  # Customize token expiration if needed" + \
			"\n" + "#    # Add any other Djoser configurations as needed" + \
			"\n" + "}" + "\n"

	if frameW:
		add_jwt_line = \
						"\n" + "    'DEFAULT_AUTHENTICATION_CLASSES': (" + "# <- TokenAuthentication configuration here" + \
						"\n" + "        'rest_framework.authentication.TokenAuthentication'," +  "# <- TokenAuthentication configuration here" + \
						"\n" + "        'rest_framework.authentication.SessionAuthentication'," +  "# <- TokenAuthentication configuration here" + \
						"\n" + "        'rest_framework_simplejwt.authentication.JWTAuthentication'," + "\t" + "# <- rest_framework_simplejwt.authentication configuration here" + \
						"\n" + "    ),"
		rm_FW = True
	else:
		add_jwt_line = ''
		
	restframework_variable = \
			"\n" + f"# Added {entity} variable to here" + \
			"\n" + "REST_FRAMEWORK = {" + \
			f"{add_jwt_line}" + \
			"\n" + "    'DEFAULT_RENDERER_CLASSES': [" + \
			"\n" + "        'rest_framework.renderers.JSONRenderer'," + \
			"\n" + "        'rest_framework.renderers.BrowsableAPIRenderer'," + \
			"\n" + "    ]," + \
			"\n" + "    'DEFAULT_FILTER_BACKENDS': [" + \
			"\n" + "        'rest_framework.filters.OrderingFilter'," + \
			"\n" + "        'rest_framework.filters.SearchFilter'," + \
			"\n" + "    ]," + \
			"\n" + "    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination'," + \
			"\n" + "    'PAGE_SIZE': 5," + \
			"\n" + "}" + "\n"

	jwt_variable = \
			"\n" + "# Configure Django REST Framework to use Simple JWT authentication" + \
			"\n" + "SIMPLE_JWT = {" + \
			"\n" + "    'AUTH_HEADER_TYPES': ('Bearer',)," + \
			"\n" + "}" + "\n"

	django_toolbar_variable = \
			"\n" + f"# Added {entity} config here" + \
			"\n" + "INTERNAL_IPS = [" + \
			"\n" + "    '127.0.0.1'" + \
			"\n" + "]" + "\n"

	urls_datails = \
			"from django.urls import path" + \
			"\n" + "from . import views" + \
			"\n\n" "urlpatterns = [" + \
			"\n\t" + "# Create your urlpatterns here." + \
			"\n" + "]" + "\n"

	if not check:
		mod_data = insert_lines(entity=entity, line_content=line_content, djoser=djoser, file_path=file_path, rm_FW=rm_FW)
		if command == 'startapp':
			temp = entity
			entity = command
		match entity:
			case "djoser":
				urls_data = insert_lines(entity=entity, line_content=line_content, urls=True, djoser=True, file_path=file_path)
				variable = djoser_variable
			case "debug_toolbar":
				line_content = "    'debug_toolbar.middleware.DebugToolbarMiddleware'," + "\t" + "# <- added debug_toolbar here" + "\n"
				urls_data1 = insert_lines(entity=entity, line_content=line_content, djoser=True, djangotoolbar=True, file_path=file_path)
				line_content = ''
				urls_data2 = insert_lines(entity=entity, line_content=line_content, urls=True, djoser=True, djangotoolbar=True, file_path=file_path)
				variable = django_toolbar_variable
			case "startapp":
				entity = temp
				urls_path = os.path.join((os.sep.join(file_path.split(os.sep)[:-2])), entity)
				os.makedirs(urls_path, exist_ok=True)
				append_variable(file_path=urls_path + os.sep + 'urls.py', variable=urls_datails)
				# with open(urls_path + os.sep + 'urls.py', 'w') as script:
				# 	script.write(urls_datails)
				urls_data = insert_lines(entity=entity, line_content=entity, urls=True, d_app=True, file_path=file_path)
			case "rest_framework":
				variable = restframework_variable
			case "rest_framework.authtoken":
				urls_data = insert_lines(entity=entity, line_content=line_content, urls=True, drf_auth=True, file_path=file_path)
				urls_data = insert_lines(entity=entity, line_content=line_content, drf_auth=True, sett=True, file_path=file_path)
			case "rest_framework_simplejwt":
				variable = jwt_variable
				line_content = "'rest_framework_simplejwt.authentication.JWTAuthentication'"
				urls_data = insert_lines(entity='SECOND CALL', line_content=line_content, just_auth=True, drf_jwt=True, file_path=file_path)
				urls_data = insert_lines(entity='THIRD CALL', line_content="", urls=True, drf_jwt=True, file_path=file_path)
			case "static":
				project_dir = file_path.split('/')[-2]
				base_dir_path = os.path.join(os.getcwd(), 'static', project_dir)
				project_dir_path = os.path.join(os.getcwd(), project_dir, 'static', project_dir)
				os.makedirs(base_dir_path, exist_ok=True)
				os.makedirs(project_dir_path, exist_ok=True)

				variable = \
					"\n" + f"# Added {entity} variable to the here" + \
					"\n" + "STATICFILES_DIRS = [" + \
					"\n" + "    BASE_DIR / 'static'," + description + " to BASE_DIR" + \
					"\n" + f"    BASE_DIR / 'static/{project_dir}'," + description + " to project dir" + \
					"\n" + "]" + "\n"
			# case _:
			# 	variable = ''
		append_variable(file_path=file_path, variable=variable)

def insert_lines(entity: str, line_content: str, file_path: str=None,
				urls: bool=False, djoser: bool=False, djangotoolbar: bool=False,
				drf_auth: bool=False, drf_jwt: bool=False, d_app: bool=False,
				rm_FW: bool=False, just_auth: bool=False, sett: bool=False):
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
	jwt_auth = False
	xml_renderer = False
	checker =False
	include = False
	auth12 = False
	restFW = False
	debug_tb = False
	get_line_num = False
	app = False
	change_line = False
	JWTAuth = False
	temp_drf_auth = False
	drf_auth_false = False
	content_insert = ''
	count = 0
	for ind, i in enumerate(data):
		if "include('djoser.urls'))" in i:
			checker = True
		if f"include('{line_content}.urls'))" in i:
			app = True
		if "debug_toolbar.urls" in i:
			debug_tb = True
		if "django.urls import path, include" in i:
			include = True
		if "api-token-auth" in i:
			auth12 = True
		if "REST_FRAMEWORK =" in i or count != 0:
			restFW = True
			if count == 15 or "authentication.TokenAuthentication'," in i \
				or "authentication.SessionAuthentication'," in i:
				drf_auth_false = True
				count = 0
				continue
			if "authentication.JWTAuthentication'," not in i:
				count += 1
				continue
			else:
				JWTAuth = True
				count = 0			
		if "'django.contrib.staticfiles'," in i:
			get_line_num = ind
	if drf_jwt:
		temp_drf_auth = drf_auth
		drf_auth = True
	for index, line in enumerate(data):
		if urls:
			if "django.urls import path" in line:
				if not include:
					line = line.strip('\n') + ", include" + "\n"
					append_variable(file_path=file_path, variable=line.strip(), no_append=True, index=index+1)
					data.insert(index, line)
					data.pop(index+1)
				if drf_auth:
					string_to_insert1 = "from rest_framework.authtoken.views import obtain_auth_token" + "\n"
					append_variable(file_path=file_path, variable=string_to_insert1.strip(), no_append=True, index=index+2)
					data.insert(index+1, string_to_insert1)
			if "urlpatterns =" in line:
				if not djangotoolbar:
					if not app and d_app:
						content_insert += f"    path('', include('{line_content}.urls')),     # For {line_content} configuration" + \
										"\n"
						continue
					if not auth12 and not drf_jwt and not djoser:
						content_insert += "    path('api-token-auth/', obtain_auth_token),    # For DRF auth_token" + \
										"\n"
					if not checker:
						content_insert += "    path('api/', include('djoser.urls')),     # For basic djoser authentication" + \
										"\n"
					if djoser:
						content_insert += "    path('api/', include('djoser.urls.authtoken')),     # For more djoser authentication" + \
										"\n"
					if drf_jwt:
						content_insert += "    path('api/', include('djoser.urls.jwt')),  # For JWT authentication" + \
										"\n"
				else:
					if not debug_tb:
						content_insert += "    path('__debug__/', include('debug_toolbar.urls')),      # For debug toolbar authentication" + \
										"\n"
				continue
			if content_insert and "]" in line:
				append_variable(file_path=file_path, variable=content_insert.strip(), no_append=True, index=index+1)
				data.insert(index, content_insert)
				break
		else:
			if drf_auth_false and sett:
				drf_auth = False
				drf_jwt = True
			key_line = '++++++++++++++++'
			if not drf_jwt:
				key_line = "'django.contrib.staticfiles',"
			if rm_FW and restFW and JWTAuth and "XMLRenderer" not in entity:
				change_line = True
				key_line = 'REST_FRAMEWORK ='
			if drf_auth:
				if not temp_drf_auth and sett:
					key_line = 'REST_FRAMEWORK ='
					description1 = "\t" + "# <- Added rest_framework.authtoken configuration here"
					line_content = \
									"    'DEFAULT_AUTHENTICATION_CLASSES': (" + description1 + \
									"\n" + "        'rest_framework.authentication.TokenAuthentication'," + description1 + \
									"\n" + "        'rest_framework.authentication.SessionAuthentication'," + description1 + \
									"\n" + "    )," + "\n"
				if just_auth:
					if not restFW:
						key_line = 'DEFAULT_AUTO_FIELD'
						description2 = "\t" + "# <- rest_framework_simplejwt.authentication configuration here"
						line_content = \
							"\n" + "# Added rest_framework variable to here" + \
							"\n" + "REST_FRAMEWORK = {" + \
							"\n" + "	'DEFAULT_AUTHENTICATION_CLASSES': (" + \
							"\n" + "		'rest_framework_simplejwt.authentication.JWTAuthentication'," + f"{description2}" + \
							"\n" + "	)," + \
							"\n" + "}" + "\n"
					elif "DEFAULT_AUTHENTICATION_CLASSES" in line:
						line_content = "\t\t" + line_content.lstrip() + "\t" + f"# <- {line_content.lstrip()} configuration here" + "\n"
						jwt_auth = True
						key_line = "DEFAULT_AUTHENTICATION_CLASSES"
			if djangotoolbar:
				key_line = "'django.contrib.sessions.middleware.SessionMiddleware',"
			if "XMLRenderer" in entity:
				line_content = "\t\t" + line_content.lstrip()
				xml_renderer = True
				key_line = "DEFAULT_RENDERER_CLASSES"
			if entity != "static":
				if key_line in line:
					if change_line:
						for rm_line in range(6):
							data.pop(index)
						data.pop(index-1)
						index = get_line_num
						# print()
					if djoser or xml_renderer or jwt_auth:
						target = ']'
						if jwt_auth:
							target = ')'
						if djoser:
							entity = "djoser"
						installed_apps = True
						continue
					else:
						append_variable(file_path=file_path, variable=line_content.strip(), no_append=True, index=index+2)
						data.insert(index + 1, line_content)
						break
				if installed_apps and target in line:
					append_variable(file_path=file_path, variable=line_content.strip(), no_append=True, index=index+1)
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
	rm_RF = False
	found_line = False
	with open(file_path) as f:
		data = f.readlines()
	for i in data:
		if 'REST_FRAMEWORK =' in i:
			rm_RF = True
		if f"'{entity}'," in i or f'"{entity}",' in i or \
			f".{entity}'," in i or f'.{entity}",' in i:
			found_line = True
	return found_line, rm_RF

################################


def entry_point():
	"""Point of entry if the script is executed from the command line.
	"""
	# print('AAAAA enter something ...')
	entity = input()
	# entity = 'djoser'
	djoser = False
	# print()
	

	# sys.exit(0)
	settings_path = [file_path]
	if len(settings_path) > 2:
		print('You have multiple files')
		for i, j in enumerate(settings_path):
			print(f'{i+1}. {j}')
		sys.exit(0)

	if entity == "djoser":
		djoser = True
	install_entity(entity, djoser=djoser)


if __name__ == "__main__":
	entry_point()
