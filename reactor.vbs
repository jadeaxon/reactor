Set oShell = CreateObject ("Wscript.Shell") 
Dim strArgs
strArgs = "cmd /c reactor.bat"
oShell.Run strArgs, 0, false

