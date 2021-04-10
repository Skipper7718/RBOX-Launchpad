import os

debug = True
log_file = False

if(os.path.isfile("debug.txt")):
    log_file = True

if(log_file):
    with open("debug_log.txt", "w") as d:
        d.write("")

def printd(s):

    if(debug):
        print(s)

    if(log_file):
        with open("debug_log.txt", "a") as d:
            d.write(f"{s}\n")