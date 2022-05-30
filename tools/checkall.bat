@echo off
REM
REM Run all test cases for simpleth and contracts
REM
cd %SIMPLE_PATH%/tests
pytest
REM
REM Run doctest to check simpleth's docstring examples
REM
cd %SIMPLE_PATH%/src/simpleth
python simpleth.py
REM
REM Run linter to find problems with style, types, suspicious code
REM
cd %SIMPLE_PATH%/tools
pylint compile.py
pylint nat2rst.py
cd %SIMPLE_PATH%/src/simpleth
pylint simpleth.py
REM
REM Do static type checking
REM
cd %SIMPLE_PATH%/tools
mypy compile.py
mypy nat2rst.py
cd %SIMPLE_PATH%/src/simpleth
mypy simpleth.py
