@ REM Start reactor in the background and log output.

@ set python=%USERPROFILE%\AppData\Local\Programs\Python\Python310\python.exe
@ IF %COMPUTERNAME%==L17006 (
	@ set python=%USERPROFILE%\AppData\Local\Programs\Python\Python311\python.exe
)
@ cd %USERPROFILE%\projects\reactor
@ start /B %python% .\daily.py 1> .\log\daily.%COMPUTERNAME%.log 2>&1

