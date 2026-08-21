Set fso = CreateObject("Scripting.FileSystemObject")
scriptsDir = fso.GetParentFolderName(WScript.ScriptFullName)
rootDir = fso.GetParentFolderName(scriptsDir)
Set WshShell = CreateObject("WScript.Shell")
WshShell.CurrentDirectory = rootDir
WshShell.Run "pythonw.exe """ & rootDir & "\main.py""", 0, False
