# safeexit.py
import sys
import types
from functools import wraps

def interrupt_guard(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except KeyboardInterrupt:
            print("\nInterrupted by user (Ctrl+C)")
            sys.exit(1)
    return wrapper

def auto_wrap_interrupt_guard(module_globals):
    for name, obj in module_globals.items():
        if isinstance(obj, types.FunctionType) and not name.startswith("__"):
            module_globals[name] = interrupt_guard(obj)
