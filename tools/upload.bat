@echo off
REM
REM Create a new distribution and wheel. Upload to pyPI
REM
REM 1) Update version number in setup.py
REM 2) Delete the old version numbered files from dist/*
REM
REM I've had to wait a minute or two for the PyPI caches get refreshed.
REM Until then, it downloads the previous version.
cd %SIMPLETH_PATH%
echo "******** Create a new distribution ********"
py -m build --sdist
echo "******** Create a new wheel        ********"
py -m build --wheel
echo "******** Upload to PyPI            ********"
twine upload dist/*