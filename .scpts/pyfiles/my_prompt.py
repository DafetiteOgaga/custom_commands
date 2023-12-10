#!/usr/bin/env python3

import sys
import os

def get_char():
    try:
        # Windows
        if os.name == 'nt':
            import msvcrt
            return msvcrt.getch().decode('utf-8')
        # Unix-like
        else:
            import tty
            import termios
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(fd)
                return sys.stdin.read(1)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    except Exception as e:
        print(f"Error reading character: {e}")
        return None

def main(prompt_disp: str):
    print(prompt_disp, end='', flush=True)
    option = get_char()
    print(option)
    # print()
    # if option is not None:
    #     print(f"\nYou pressed: {option}")
    return option

if __name__ == "__main__":
    main("Press any key (except Enter) to continue >>> ")
