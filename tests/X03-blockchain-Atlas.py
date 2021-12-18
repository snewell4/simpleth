#!
# Unit test of Blockchain class

from simpleth import Blockchain, SimplEthError
import s_ethconv as ethconv

b = Blockchain()

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
print(f'PASS: get_address({i}) = {addr}.')
print('')

# Get account number from an address
acct_num = 2
acct_addr = b.get_address(acct_num)
acct_num_returned = b.to_account_num(acct_addr)
if acct_num == acct_num_returned:
    print(f'PASS: to_account_num({acct_addr}) = {acct_num_returned}')
else:
    print(
        f'FAIL: to_account_num(acct_addr) = {acct_num_returned}' 
        f'      Should have returned: {acct_num}'
        )
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
    print(f'PASS: get_balance({addr}) = {bal}.')
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
print(f'PASS: get_trx_count({addr}) = {count}.')
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
amount_ether = 1
init_bal0 = ethconv.convert(b.get_balance(acct0), 'wei', 'ether')
init_bal1 = ethconv.convert(b.get_balance(acct1), 'wei', 'ether')
amount_wei = int(ethconv.convert(amount_ether, 'ether', 'wei'))
try:
    b.send_ether(acct1, acct0, amount_wei)
except SimplEthError as e:
    print(
        f'FAIL: Unable to transfer {amount_ether} from '
        f'acct {acct0} to acct {acct1}.\n'
        f'MESSAGE: {e}\n'
        )
else:
    bal0 = ethconv.convert(b.get_balance(acct0), 'wei', 'ether')
    bal1 = ethconv.convert(b.get_balance(acct1), 'wei', 'ether')
    print(f'PASS: Transfer {amount_ether} ether from acct1 to acct0')
    print(f'Balance of acct0 went from {init_bal0} to {bal0} ether')
    print(f'Balance of acct1 went from {init_bal1} to {bal1} ether')
