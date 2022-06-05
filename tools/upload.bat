@echo off
REM
REM Create a new distribution and wheel. Upload to pyPI
REM
REM 1) Update version number in setup.py
REM 2) Delete the old version numbered files from dist/*
echo "******** Create a new distribution ********"
py -m build --sdist
echo "******** Create a new wheel        ********"
py -m build --wheel
echo "******** Upload to PyPI            ********"
twine upload dist/*