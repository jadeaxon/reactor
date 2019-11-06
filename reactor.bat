REM Start reactor in the background and log output.
start /B python .\reactor.py 1> .\log\reactor.%COMPUTERNAME%.log 2>&1

