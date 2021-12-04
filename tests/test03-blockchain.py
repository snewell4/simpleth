#! python3
# Unit test of Blockchain class

from simpleth import Blockchain, Convert, SimplEthError
b = Blockchain()
c = Convert()

# Test properties
print(f'Accounts = {b.accounts}')
print('')

print(f'API Version = {b.api_version}')
print('')

print(f'Block number = {b.block_number}')
print('')

print(f'Client Version = {b.client_version}')
print('')

print(f'Eth object = {b.eth}')
print('')

print(f'Web3 object = {b.web3}')
print('')

# Test methods
# Get account address for user 0
i = 0
addr = b.get_address(i)
print(f'get_address({i}) = {addr}.')
print('')

# Get account address for bogus user 
i = len(b.accounts) + 1
try:
    addr = b.get_address(i)
except SimplEthError as e:
    print(f'PASS: Unable to get address for bogus index of {i}.')
else:
    print(f'FAIL: Able to get address for bogus index:\n')
    print(f'get_address({i}) = {addr}')
print('')

# Get ether balance for user 0
addr = b.get_address(0)
try:
    bal = b.get_balance(addr)
except SimplEthError as e:
    print(f'FAIL: Unable to get ether get_balance for get_balance({addr}).')
else:
    print(f'get_balance({addr}) = {bal}.')
print('')

# Attempt to get ether balance using wrong data type for account_address
addr = 2
try:
    bal = b.get_balance(addr)
except SimplEthError as e:
    print(f'PASS: Unable to get ether balance using bogus arg type.')
    print(f'MESSAGE: {e}')
else:
    print(f'FAIL: Able to get ether balance using bogus address:\n')
    print(f'get_balance({addr}) = {bal}.\n')

# Get transaction count for user 0
addr = b.get_address(0)
count = b.get_trx_count(addr)
print(f'get_trx_count({addr}) = {count}.')
print('')

# Get transaction count for bogus user
addr = 2
try:
    count = b.get_trx_count(addr)
except SimplEthError as e:
    print(f'PASS: Unable to get transaction count using bogus arg type.')
    print(f'MESSAGE: {e}')
else:
    print(f'FAIL: Able to get transaction count using bogus arg type:\n')
    print(f'get_trx_count({addr}) = {count}.\n')

# Setup two accounts for test cases
acct0 = b.get_address(0)
acct1 = b.get_address(1)

# Check that valid address is True
if b.is_valid_address(acct0):
    print(f'PASS: {acct0} is a valid address.\n')
else:
    print(f'FAIL: {acct0} is incorrectly deemed an invalid address.\n')

# Check that invalid address is False
bad_addr = '0xDDDDDDDDDDDDDDDDD'
if not b.is_valid_address(bad_addr):
    print(f'PASS: {bad_addr} is an invalid address.\n')
else:
    print(f'FAIL: {bad_addr} is incorrectly deemed an invalid address.\n')

# Test sending ether from one account to another
bal0 = c.from_wei(b.get_balance(acct0), 'ether')
bal1 = c.from_wei(b.get_balance(acct1), 'ether')
print(f'Balance of acct0 is = {bal0} ether')
print(f'Balance of acct1 is = {bal1} ether')
amount_ether = 1
amount_wei = c.to_wei(amount_ether, 'ether')
print(f'Transfer {amount_ether} ether from acct1 to acct0')
success = b.transfer_ether(acct1, acct0, amount_wei)
bal0 = c.from_wei(b.get_balance(acct0), 'ether')
bal1 = c.from_wei(b.get_balance(acct1), 'ether')
print(f'Transfer success = {success}')
print(f'Balance of acct0 is = {bal0} ether')
print(f'Balance of acct1 is = {bal1} ether')
