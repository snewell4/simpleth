:Description: Check all Python code and smart contracts for problems.

:Purpose:  Run after any code or docstring changes

:Usage: ``checkall``

:Notes:  Runs:

* all simpleth test cases
* doctest to check simpleth docstring examples
* linters (pylint and mypy) on Python code
* Made new environment variable, MYPYPATH, and added
  the simpleth directory.
