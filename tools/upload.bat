@echo off
REM
REM Upload all distributions
REM
cd %SIMPLETH_PATH%
echo "******** Upload to PyPI            ********"
twine upload dist/*