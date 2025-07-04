#!/usr/bin/env python3

import subprocess, shlex, sys

def run_subprocess(cmd, capture=True, env=None, check=False):
	return subprocess.run(cmd, capture_output=capture, text=True, env=env, check=check)

def run_subprocess_cmd_alone(cmd):
	return subprocess.run(cmd)

def run_interactive_subprocess(cmd, env=None):
	return subprocess.run(cmd, env=env)

def subprocess_for_pull_command(cmd, **kwargs):
    """Run a shell command and return (returncode, stdout, stderr)"""
    result = subprocess.run(shlex.split(cmd), capture_output=True, text=True, **kwargs)
    return result.returncode, result.stdout.strip(), result.stderr.strip()

def run_subprocess_live(cmd):
	return subprocess.run(cmd, stdout=sys.stdout, stderr=sys.stderr)


# Run a command and return the output as a string
