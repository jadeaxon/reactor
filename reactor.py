# PRE: Running from Windows.

from sys import stdout
from sys import stderr
from sys import argv
import time
import os
import re


#==============================================================================
# Globals
#==============================================================================

S = argv[0]
S = os.path.basename(S)

# Check the environment.
user = os.environ['USERNAME']
home = os.environ['USERPROFILE']
desktop = f'{home}\\Desktop'


# When apps are installed for all users, shared links will be created here.
publicDesktop = 'C:\\Users\\Public\\Desktop'
publicDesktopAccessible = True

# TO DO: Read reactions from JSON file.
# TO DO: Reread config if it has changed.
# TO DO: Tray icon that allows disable/enable.

# All the reactions to potentially trigger each iteration.
reactions = []


#==============================================================================
# Functions
#==============================================================================

# Add a reaction.
def reaction(r, a1=None, a2=None):
    global reactions
    r = (r, a1, a2)
    reactions.append(r)

# Moves a file from the desktop to a subfolder of the desktop.
# Creates directory if necessary.  Clobbers existing files.
def move(fromFile, toDir):
    global publicDesktopAccessible
    fromPath = f'{desktop}\\{fromFile}'
    fromPublicPath = f'{publicDesktop}\\{fromFile}'
    toDirPath = f'{desktop}\\{toDir}'
    toPath = f'{toDirPath}\\{fromFile}'

    if os.path.exists(fromPath):
        print(f'{S}: {fromPath} -> {toPath}.')
        if not os.path.exists(toDirPath):
            os.mkdir(toDirPath)
        if os.path.exists(toPath):
            os.remove(toPath)

        os.rename(fromPath, toPath)
    elif os.path.exists(fromPublicPath):
        if publicDesktopAccessible:
            print(f'{S}: {fromPublicPath} -> {toPath}.')
            if not os.path.exists(toDirPath):
                os.mkdir(toDirPath)
            if os.path.exists(toPath):
                os.remove(toPath)

            try:
                os.rename(fromPublicPath, toPath)
            except PermissionError as e:
                # On work machines, access is denied to this folder.
                print(f'{S}: WARNING: Public desktop is not accessible.');
                publicDesktopAccessible = False

    return


# Moves a file from the desktop to a subfolder if it matches given regex.
# Creates directory if necessary.  Clobbers existing files.
def moveRegex(fromPattern, toDir):
    global desktop
    pattern = re.compile(fromPattern)
    nodes = os.listdir(desktop)
    paths = [f'{desktop}\\{n}' for n in nodes if pattern.match(n)]

    public_nodes = os.listdir(publicDesktop)
    public_paths = [f'{publicDesktop}\\{n}' for n in public_nodes if pattern.match(n)]

    paths += public_paths
    files = [path for path in paths if os.path.isfile(path)]
    files = [os.path.basename(f) for f in files]
    for f in files:
        move(f, toDir)
    return

# Renames shortcuts in the Desktop directory.
def renameShortcuts():
    pattern = re.compile('^.* (- Shortcut).lnk')
    nodes = os.listdir(desktop)

    paths = [f'{desktop}\\{n}' for n in nodes if pattern.match(n)]
    files = [path for path in paths if os.path.isfile(path)]
    files = [os.path.basename(f) for f in files]
    for f in files:
        # Windows has the annoying habit of appending - Shortcut to all shortcuts.
        # You can disable this in the registery, but Windows reenables it after each ugrade.
        # Yes, I could just rig something to reapply that registry change all the time, but I didn't.
        f2 = re.sub(' [-] Shortcut', '', f)
        print(f'{S}: {f} -> {f2}.')
        os.rename(f'{desktop}\\{f}', f'{desktop}\\{f2}')


#==============================================================================
# Tests
#==============================================================================


#==============================================================================
# Main
#==============================================================================

reaction('rename_shortcuts')

reaction('move', 'Microsoft Teams.lnk', 'Comm')
reaction('move', 'Google Chrome.lnk', 'Comm')
reaction('move', 'Slack.lnk', 'Comm')
reaction('move', 'Skype.lnk', 'Comm')
reaction('move', 'Microsoft Edge.lnk', 'Comm')
reaction('move', 'Discord.lnk', 'Comm')
reaction('move', 'FileZilla Client.lnk', 'Comm')

reaction('move', 'iTunes.lnk', 'Media')
reaction('move', 'Kindle.lnk', 'Media')
reaction('move', 'VLC media player.lnk', 'Media')

reaction('move', 'Steam.lnk', 'Games')
reaction('move', 'GeForce Experience.lnk', 'Games')
reaction('move', 'Goat Simulator.url', 'Games')

reaction('move', 'WinDirStat.lnk', 'System\\Diagnostics')
reaction('move', 'Speccy.lnk', 'System\\Diagnostics')

reaction('move', 'Launchy.lnk', 'System\\Productivity')

reaction('move', 'Canon Quick Menu.lnk', 'System\\Peripherals\\Scanner')

reaction('move', 'VeraCrypt.lnk', 'System\\Security')
reaction('move', 'KeePass (Portable).lnk', 'System\\Security')

reaction('move_regex', '^gVim.*[.]lnk$', 'Editors')

reaction('move_regex', '^Universal-USB-Installer-.*[.]exe', 'Utilities')

reaction('move', 'Excel.lnk', 'Office')
reaction('move', 'Work.lnk', 'Office')
reaction('move', 'PowerPoint.lnk', 'Office')
reaction('move', 'Outlook.lnk', 'Office')
reaction('move_regex', '^Excel .*[.]lnk$', 'Office')
reaction('move_regex', '^Word .*[.]lnk$', 'Office')
reaction('move_regex', '^PowerPoint .*[.]lnk$', 'Office')
reaction('move_regex', '^Outlook .*[.]lnk$', 'Office')

print(f'{S}: Started.')
while True:
    stdout.flush()
    stderr.flush()

    if os.path.exists('stop'):
        print(f'{S}: Stopped by signal file.')
        exit(0)

    for r in reactions:
        # TO DO: Dynamically call right function.
        if r[0] == 'move':
            move(r[1], r[2])
        elif r[0] == 'move_regex':
            moveRegex(r[1], r[2])
        elif r[0] == 'rename_shortcuts':
            renameShortcuts()
    time.sleep(5)



