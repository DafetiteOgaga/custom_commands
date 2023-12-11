#!/usr/bin/env python3

import time

def progress_bar(duration: int, resp: str):
    total_iterations = 100
    per_loop = duration/100
    if resp.lower() == "y":
        my_str = "Updating"
    else:
        my_str = "Reverting"
    for i in range(total_iterations+1):
        time.sleep(per_loop)
        progress = i / total_iterations
        print("\r{}: %-40s done %d%%".format(my_str) % ('#' * int(40 * progress), int(100 * progress)), end='')
    print("")
