rem FAIL: This did not work for me on Windows 10 with Python 3.
rem Copy this to your Python directory.
rem This lets you run a Python process as a specific name in Task Manager.
rem python-by-name myname myscript.py

set PYTHON_HOME=%~dp0
set PYTHON_NAME=%1.exe
copy "%PYTHON_HOME%python.exe" "%PYTHON_HOME%%PYTHON_NAME%"
set args=%*
set args=%args:* =%
"%PYTHON_HOME%%PYTHON_NAME%" %args%
