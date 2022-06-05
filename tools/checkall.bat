@echo off
REM
REM Run all test cases for simpleth and contracts
REM
cd %SIMPLETH_PATH%/tests
pytest
REM
REM Run doctest to check simpleth's docstring examples
REM
cd %SIMPLETH_PATH%/src/simpleth
python simpleth.py
REM
REM Run linter to find problems with style, types, suspicious code
REM
cd %SIMPLETH_PATH%/tools
pylint compile.py
pylint nat2rst.py
cd %SIMPLETH_PATH%/src/simpleth
pylint simpleth.py
REM
REM Do static type checking
REM
cd %SIMPLETH_PATH%/tools
mypy compile.py
mypy nat2rst.py
cd %SIMPLETH_PATH%/src/simpleth
REM Check as a package. Also avoids mypy error:
REM 'Source file found twice under different module names: "simpleth.simpleth" and "simpleth"'
REM since MYPYPATH finds it along with being in current working directory.
mypy -p simpleth