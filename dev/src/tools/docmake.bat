REM Use "make clean" to clear out old files to fix problems
REM Recompile contracts first to catch Natspec comment updates.
cd %simplethpath%\dev\src\contracts
nat2rtd.py TestNatspec.sol
cd %simplethpath%\src\contracts
nat2rtd.py club.sol HelloWorld1.sol HelloWorld2.sol HelloWorld3.sol HelloWorld4.sol
cd %simplethpath%\tests\src\contracts
nat2rtd.py Test.sol TestNeverDeployed.sol
cd %simplethpath%\docs
make html