REM This runs the command to add new rst files. Run for new docs.
REM Run from the project dir: Desktop\simpleth
REM Delete .rst file from source if a file is renamed or deleted.
cd %simplethpath%\docs
set PYTHONPATH=%simplethpath%\src
sphinx-apidoc -f -o source %PYTHONPATH%
