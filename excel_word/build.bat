@echo off

echo ### Prepare resource file ...
call compile.bat

echo ### Packaging GUI ...
pyinstaller -w -F SwitchTerminal.py
