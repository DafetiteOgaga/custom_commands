#!/usr/bin/env python3

import sys, json

# Read all lines from stdin
lines = sys.stdin.read().strip()

# Print the processed output
# print(f'echoValue:\n{lines}')
newVar = lines.split("———")
# print(f'New Variable 0: {newVar[0]}')
# print('\n\n\n')
# print(f'New Variable 1: {newVar[1]}')
# print('\n\n\n')
# print(f'New Variable 1: {newVar[2]}')
build_dict = {}
# print(f'newVar: {newVar}, length: {len(newVar)}')
for index, info in enumerate(newVar):
	build_dict[index] = {}
	for item in info.split('\n'):
		if (item.strip().startswith('Builds') and '@' in item) or item.strip() == '':
			continue
		key, value = item.split("  ", 1)
		build_dict[index][key.strip()] = value.strip()

# print(f'echoValue:\n{json.dumps(build_dict, indent=4)}')
# print(f'Artifact: {build_dict[0]["Artifact"]}')
print(build_dict[0]['Version'], build_dict[0]["Artifact"])