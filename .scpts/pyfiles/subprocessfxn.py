#!/usr/bin/env python3

import subprocess

def run_subprocess(cmd, capture=True):
	return subprocess.run(cmd, capture_output=capture, text=True)
