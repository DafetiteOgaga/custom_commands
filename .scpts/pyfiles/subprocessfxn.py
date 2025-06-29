#!/usr/bin/env python3

import subprocess

def run_subprocess(cmd, capture=True, env=None):
	return subprocess.run(cmd, capture_output=capture, text=True, env=env)

def run_subprocess_cmd_alone(cmd):
	return subprocess.run(cmd)
