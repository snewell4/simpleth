@echo off
REM
REM Compile all smart contracts
REM
cd %SIMPLETH_PATH%/src/contracts
compile.py HelloWorld1.sol
compile.py HelloWorld2.sol
compile.py HelloWorld3.sol
compile.py HelloWorld4.sol
compile.py Test.sol
compile.py TestNeverDeployed.sol