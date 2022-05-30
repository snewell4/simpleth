echo off
REM Make new ReadTheDoc documentation

REM
REM If TOC or indexing changed, clean out old HTML first
REM Unable to run this command in the script. Script ends after
REM that command. Leaving here for now.
REM
REM cd %SIMPLETH_PATH%/docs
REM make clean

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
