#!/usr/bin/python3

# This is called from daily.bat which is called from a task in Windows Task Scheduler.
# The log is in ~/projects/reactor/log/daily.<host>.log.

import os
from datetime import date


#==============================================================================
# Functions
#==============================================================================

def writeProgressHeader():
    host = os.getenv("COMPUTERNAME")
    home = os.getenv("USERPROFILE")
    path = home + r"\Dropbox\Organization\Progress\Home\Progress (Home).txt"
    # print(home)
    # print(path)
    # print(host)

    print("daily.py: Running.")

    today = date.today()
    formatted = today.strftime("%Y-%m-%d")
    day = today.strftime("%a")
    # 2022-07-10: Sun, for example.
    line = formatted + ": " + day + "\n\n"
    print(line)

    # The newline arg forces it to write Linux line endings.
    # If you don't do this, you'll see ^M in Vim due to Windows line endings being written.
    # Even though your string has \n above, when file is open in text mode, it translates it
    # to OS line ending.  You could also open the file in binary mode to avoid this.
    f = open(path, "r+", newline="\n", encoding="utf-8")
    content = f.read()

    lines = content.split("\n")
    if (lines[0].strip() == line.strip()):
        # print("Already ran today.")
        return

    f.seek(0, 0)
    f.write(line)
    f.write(content)
    f.flush()
    f.close()
    return


#==============================================================================
# Main
#==============================================================================

writeProgressHeader()
exit(0)


