#!/usr/bin/env python3

def check_mysqldb():
	try:
		import MySQLdb
		print('installed')
		return 'installed'
	except ModuleNotFoundError:
		print('not installed')
		return 'not installed'

if __name__ == '__main__':
    check_mysqldb()