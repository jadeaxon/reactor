#!/usr/bin/python3

import os
from datetime import date

host = os.getenv("COMPUTERNAME")
home = os.getenv("USERPROFILE")
path = home + r"\Dropbox\Organization\Progress\Home\Progress (Home).txt"
# print(home)
# print(path)
# print(host)

# host = "Inspiron-VM"

# This is only supposed to run on Inspiron-VM from a Windows scheduled task.
if host != "Inspiron-VM":
    print("daily.py: ERROR: Wrong host.  Inspiron-VM expected.")
    exit(1)
else:
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
    f = open(path, "r+", newline="\n")
    content = f.read()
    f.seek(0, 0)
    f.write(line)
    f.write(content)
    f.flush()
    f.close()

exit(0)

