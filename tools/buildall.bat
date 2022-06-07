@echo off
REM
REM Create a new distribution and wheel.
REM
cd %SIMPLETH_PATH%
echo "******** Create a new distribution ********"
py -m build --sdist
echo "******** Create a new wheel        ********"
py -m build --wheel