# safeexit.py
import sys, types
from pyfiles.print import quit_program
from functools import wraps

def interrupt_guard(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except KeyboardInterrupt:
            print("\nInterrupted by user (Ctrl+C)")
            quit_program("q", 1)
    return wrapper

def auto_wrap_interrupt_guard(module_globals):
    for name, obj in module_globals.items():
        if isinstance(obj, types.FunctionType) and not name.startswith("__"):
            module_globals[name] = interrupt_guard(obj)
