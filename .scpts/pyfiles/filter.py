#!/usr/bin/env python3

import os, sys

input_str = input()

def filterFunc(list_in: str):
	# print(f'list_in: {list_in}')
	list_in = list_in.split()
	list_in = [filename.split(os.sep)[-1] for filename in list_in]
	# print(f'list_in: {list_in}')
	files = ['App.js', 'index.js', 'package.json', 'index.html']
	result = all(file in list_in for file in files)
	print(result)
	return result

def getAppName(list_in: str):
    list_in = list_in.split()
    # print('list_in-start: %s' % list_in)
    list_in = [file for file in list_in if file if file.endswith('package.json')]
    with open(list_in[0]) as f:
        next(f)
        filename = f.readline().strip().split('"')[3]
    print(filename)

if __name__ == '__main__':
    # print('sys.argv: %s' % sys.argv)
    func = sys.argv[1]
    if func == 'filterFunc':
        filterFunc(input_str)
    elif func == 'getAppName':
        getAppName(input_str)
        