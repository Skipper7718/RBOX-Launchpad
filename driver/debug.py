"""
This module is only for the print statements. In production mode stdout printing is disabled.
File logging can be enabled by creating a file that named 'debug.txt'.
"""

import os

debug = True
log_file = False

#toggle logging if debug.txt is found in workdir
if(os.path.isfile("debug.txt")):
    log_file = True


if(log_file):
    with open("debug_log.txt", "w") as d:
        d.write("")

#debug print
def printd(s):

    if(debug):
        print(s)

    if(log_file):
        with open("debug_log.txt", "a") as d:
            d.write(f"{s}\n")