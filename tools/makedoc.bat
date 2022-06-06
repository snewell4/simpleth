echo off
REM Make new ReadTheDoc documentation

cd %SIMPLETH_PATH%/docs

REM
REM If TOC or indexing changed, clean out old HTML first
REM Unable to run this command in the script. Script ends after
REM that command. Leaving here for now.
REM
REM make clean

REM
REM Get current version of Test.sol in the docs\source dir in
REM order for TestContract.rst to include. Forces overwrite.
REM
copy /Y ..\src\contracts\Test.sol source

REM
REM Create smart contract reference reST documents from docstrings.
REM
REM Do you need to do a compile.py of any contracts first to get
REM any new Natspec comments included?
REM
cd %SIMPLETH_PATH%/src/contracts
nat2rst.py HelloWorld1.sol HelloWorld2.sol HelloWorld3.sol HelloWorld4.sol Test.sol

REM
REM Use Sphinx to build the ReadTheDocs HTML pages from reST files.
REM
cd %SIMPLETH_PATH%/docs
make html
