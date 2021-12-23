"""Constants used for simpleth test cases"""
from simpleth import Blockchain


# Contract used for testing (must match a Solidity file name)
CONTRACT_NAME = 'Test'

# Parameters for CONTRACT_NAME's constructor
CONSTRUCTOR_SENDER = Blockchain().address(0)
CONSTRUCTOR_ARG = 10  # Test constructor expects a uint
CONSTRUCTOR_EVENT_NAME = 'TestConstructed'

# Parameters for a test transaction in CONTRACT_NAME
TRX_SENDER = Blockchain().address(0)
TRX_NAME = 'storeNums'
TRX_ARG0 = 50
TRX_ARG1 = 60
TRX_ARG2 = 70
TRX_VALUE = 0       # amount of wei sent with trx. storeNums sends 0
TRX_ARG_KEY1 = '_num0'
EVENT_NAME = 'NumsStored'
EVENT_ARG_KEY1 = 'num0'
EVENT_ARG_VALUE1 = 10

# General constants used for test cases.
HASH_SZ = 66  # number chars in a blockchain hash

# Test.sol contract constants
INIT_NUM0 = 0      # nums[0] is initialized to 0
INIT_NUM1 = 1
INIT_NUM2 = 2
