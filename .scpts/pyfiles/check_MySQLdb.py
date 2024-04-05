#!/usr/bin/env python3

def check_mysqldb(py: bool=False):
	"""Checks if MySQL is installed

	Args:
		py (bool, optional): indicates that the function was called
							from a .py script. Defaults to False.

	Returns:
		str: if MySQL is installed
	"""
	try:
		import MySQLdb
		if not py:
			print('MySQLdb installed')
		return 'MySQLdb installed'
	except ModuleNotFoundError:
		if not py:
			print('MySQLdb not installed')
		return 'MySQLdb not installed'


def check_drf(py: bool=False):
	"""if DRF is installed

	Args:
		py (bool, optional): indicates that the function was called
							from a .py script. Defaults to False.

	Returns:
		str: if DRF is installed
	"""
	try:
		from rest_framework import serializers
		if not py:
			print('DRF installed')
		return 'DRF installed'
	except ImportError:
		if not py:
			print('DRF not installed')
		return 'DRF not installed'


if __name__ == '__main__':
    check_mysqldb()
    check_drf()