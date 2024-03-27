#!/usr/bin/env python3

def check_mysqldb(py: bool=False):
	try:
		import MySQLdb
		if not py:
			print('installed')
		return 'installed'
	except ModuleNotFoundError:
		if not py:
			print('not installed')
		return 'not installed'

if __name__ == '__main__':
    check_mysqldb()