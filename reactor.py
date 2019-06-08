# PRE: Running from Windows.

from sys import stdout
from sys import stderr
from sys import argv
import time
import os


#==============================================================================
# Globals
#==============================================================================

S = argv[0]
S = os.path.basename(S)

# Check the environment.
user = os.environ['USERNAME']
home = os.environ['USERPROFILE']
desktop = f'{home}\\Desktop'


# TO DO: Read reactions from JSON file.
reactions = []
r = ('move', 'Microsoft Teams.lnk', 'Comms')
reactions.append(r)
r = ('move', 'Google Chrome.lnk', 'Comms')
reactions.append(r)
r = ('move', 'Slack.lnk', 'Comms')
reactions.append(r)
r = ('move', 'Skype.lnk', 'Comms')
reactions.append(r)
r = ('move', 'Microsoft Edge.lnk', 'Comms')
reactions.append(r)
r = ('move', 'Discord.lnk', 'Comms')
reactions.append(r)


r = ('move', 'iTunes.lnk', 'Media')
reactions.append(r)
r = ('move', 'Kindle.lnk', 'Media')
reactions.append(r)


#==============================================================================
# Functions
#==============================================================================

# Moves a file from the desktop to a subfolder of the desktop.
# Creates directory if necessary.  Clobbers existing files.
def move(fromFile, toDir):
    fromPath = f'{desktop}\\{fromFile}'
    toDirPath = f'{desktop}\\{toDir}'
    toPath = f'{toDirPath}\\{fromFile}'

    if os.path.exists(fromPath):
        print(f'{S}: {fromPath} -> {toPath}.')
        if not os.path.exists(toDirPath):
            os.mkdir(toDirPath)
        if os.path.exists(toPath):
            os.remove(toPath)

        os.rename(fromPath, toPath)


#==============================================================================
# Tests
#==============================================================================


#==============================================================================
# Main
#==============================================================================


print(f'{S}: Started.')
while True:
    stdout.flush()
    stderr.flush()
    for r in reactions:
        # TO DO: Dynamically call right function.
        if r[0] == 'move':
            move(r[1], r[2])
    time.sleep(5)

