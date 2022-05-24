cd %simplethpath%\dev\src\contracts
REM add -u *"^-_
nat2rst.py TestNatspec.sol
cd %simplethpath%\src\contracts
nat2rst.py club.sol HelloWorld1.sol HelloWorld2.sol HelloWorld3.sol HelloWorld4.sol
cd %simplethpath%\tests\src\contracts
nat2rst.py Test.sol TestNeverDeployed.sol
cd %simplethpath%\docs
make html
