#! python3
# Unit test for PPrint() class

from simpleth import Blockchain, Contract, PPrint, SimplEthError

# Test parameters
contract_name = 'TestTrx'  
trx_name = 'storeNums'
event_name ='NumsStored'
num_blocks = 5

# Test instantiating Blockchain and PPrint objects
try:
    b = Blockchain()
    p = PPrint()
    user = b.get_address(0)
except SimplEthError as e:
    print(f'FAIL:  Unable to instantiate objects.')
    print(f'MESSAGE:  {e}')
    print(f'')
    exit()
else:
    print(f'PASS:  Objects instantiated.')
print(f'')

# Run a transaction to have something to print.
# Assume test03 has been run and all Contract() methods are working.
try:
    c = Contract(contract_name)
    c.connect()
    trx_results = c.run_trx(user, trx_name, 10, 20, 30, event_name=event_name)
except SimplEthError as e:
    print(f'FAIL:  Unable to run transaction "{trx_name}".')
    print(f'MESSAGE:  {e}')
else:
    print(f'PASS:  Ran transaction "{trx_name}".')
print(f'')

# Print results
print(f'=== Results from transaction "{trx_name}" ===')
p.print_trx_results(trx_results)
print(f'')

# Print trx receipt
print(f'=== Receipt from transaction "{trx_name}" ===')
p.print_trx_receipt(trx_results['trx_receipt'])
print(f'')

# Print trx receipt logs
print(f'=== Receipt logs from transaction "{trx_name}" ===')
p.print_trx_receipt_logs(trx_results['trx_receipt'])
print(f'')

# Get an event and print
event_list = c.get_past_events(event_name, num_blocks)
print(f'=== Event list from event "{event_name}" ===')
p.print_event_list(event_list, indent=4)
