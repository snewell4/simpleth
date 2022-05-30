@echo off
REM
REM Run all test cases for simpleth and contracts
REM
cd C:\Users\snewe\OneDrive\Desktop\simpleth\tests
pytest
REM
REM Run doctest to check simpleth's docstring examples
REM
cd C:\Users\snewe\OneDrive\Desktop\simpleth\src\simpleth
python simpleth.py
REM
REM Run linter to find problems with style, types, suspicious code
REM
cd C:\Users\snewe\OneDrive\Desktop\simpleth\src\utils
pylint compile.py
cd C:\Users\snewe\OneDrive\Desktop\simpleth\dev\src\tools
pylint nat2rst.py
cd C:\Users\snewe\OneDrive\Desktop\simpleth\src\simpleth
pylint simpleth.py
REM
REM Do static type checking
REM
cd C:\Users\snewe\OneDrive\Desktop\simpleth\src\utils
mypy compile.py
cd C:\Users\snewe\OneDrive\Desktop\simpleth\dev\src\tools
mypy nat2rst.py
cd C:\Users\snewe\OneDrive\Desktop\simpleth\src\simpleth
mypy simpleth.py
