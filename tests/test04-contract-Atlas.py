#!
"""Unit test for Contract() class"""

import argparse
from simpleth import Blockchain, Contract, SimplEthError
import s_ethconv as ethconv
import s_constant as constant
import s_print as p


# Test contract 
cname = 'TestTrx'  # contract name
ename = 'TestTrxConstructed'  # event name for contract constructor

# Counters
pass_count = 0
fail_count = 0

parser = argparse.ArgumentParser(
    description = ('Unit test for Contract() class')
    )
parser.add_argument(
    '-v',
    help='print details of successful test cases',
    dest='verbose',
    action='store_true'
    )
args = parser.parse_args()


# Test setting up Blockchain() object and the user account for test cases
# Will exit if unable to instantiate Blockchain() object since Ganache is
# probably not running.
try:
    b = Blockchain()
    user = b.accounts[0]
except SimplEthError as e:
    fail_count += 1
    print(f'FAIL:  Unable to instantiate Blockchain() object.')
    print(f'MESSAGE:  {e}')
    print('')
    exit()
else:
    pass_count += 1
    if args.verbose:
        print(f'PASS:  Blockchain() object instantiated.')
        print('')

# Instantiate Contract() object
try:
    c = Contract(cname)
except SimplEthError as e:
    fail_count += 1
    print(f'FAIL:  Unable to instantiate contract object for "{cname}"')
    print(f'MESSAGE: {e}')
    print('Must exit. Test cases depend on a valid contract object.')
    exit()
else:
    pass_count += 1
    if args.verbose:
        print(f'PASS:  Contract "{cname}" object instantiated.')
        print('')

# Attempt to deploy contract with bad contract name
try:
    bogus_cname = 'bogus_contract'
    bogus_c = Contract(bogus_cname)
    tresults = bogus_c.deploy(user, ename)
except SimplEthError as e:
    pass_count += 1
    if args.verbose:
        print(f'PASS:  Unable to deploy contract "{bogus_cname}".')
        print(f'MESSAGE:  {e}')
        print('')
else:
    fail_count += 1
    print(f'FAIL:  Contract "{bogus_cname}" unexpectedly deployed.')
    print('')

# Attempt to deploy contract with missing constructor param
try:
    tresults = c.deploy(user, constructor_event_name=ename)
except SimplEthError as e:
    pass_count += 1
    if args.verbose:
        print(
            f'PASS:  Unable to deploy contract "{bogus_cname}" without '
            f'its constructor arg.'
            )
        print(f'MESSAGE:  {e}')
        print('')
else:
    fail_count += 1
    print(
        f'FAIL:  Contract "{bogus_cname}" unexpectedly deployed. It'
        f'should have failed since the constructor arg was not given.'
        )
    print('')

# Deploy contract
try:
    init_num = 1
    tresults = c.deploy(user, init_num, constructor_event_name=ename)
except SimplEthError as e:
    fail_count += 1
    print(f'FAIL:  Unable to deploy contract "{cname}".')
    print(f'MESSAGE:  {e}')
    print('')
else:
    pass_count += 1
    if args.verbose:
        print(f'PASS:  Deployed contract "{cname}".')
        p.print_trx_results(tresults)
        print('')

# Test constructor arg was used to set its variable
try:
    var_name = 'initNum'
    num = c.get_var(var_name)
except SimplEthError as e:
    fail_count += 1
    print(f'FAIL:  Unable to get a value for constructor var "{var_name}".')
    print(f'MESSAGE:  {e}')
    print('')
else:
    pass_count += 1
    if args.verbose:
        if init_num == num:
            print(
                f'PASS:  Able to get correct value of {init_num} for '
                f'constructor variable "{var_name}".'
                )
        else:
            print(
                f'FAIL:  Value for constructor variable "{var_name}" '
                f'should have been {init_num}. Got {num}.'
                )
        print('')

# Test address property
try:
    address = c.address
except SimplEthError as e:
    fail_count += 1
    print(f'FAIL:  Unable to get address for "{cname}".')
    print(f'MESSAGE:  {e}')
    print('')
else:
    pass_count += 1
    if args.verbose:
        print(f'PASS:  Blockchain address for "{cname}" = {address}.')
        print('')

# Test abi property
try:
    abi = c.abi
except SimplEthError as e:
    fail_count += 1
    print(f'FAIL:  Unable to get abi for "{cname}".')
    print(f'MESSAGE:  {e}')
    print('')
else:
    pass_count += 1
    if args.verbose:
        print(f'PASS:  ABI for "{cname}" = {abi}.')
        print('')

# Test bytecode property
try:
    bytecode = c.bytecode
except SimplEthError as e:
    fail_count += 1
    print(f'FAIL:  Unable to get bytecode for "{cname}".')
    print(f'MESSAGE:  {e}')
    print('')
else:
    pass_count += 1
    if args.verbose:
        print(f'PASS:  Bytecode for "{cname}" = {bytecode}.')
        print('')

# Test deployed_code property
try:
    deployed_code = c.deployed_code
except SimplEthError as e:
    fail_count += 1
    print(f'FAIL:  Unable to get deployed code for "{cname}".')
    print(f'MESSAGE:  {e}')
    print('')
else:
    pass_count += 1
    if args.verbose:
        print(f'PASS:  Deployed code for "{cname}" = {deployed_code}.')
        print('')

# Test events property
try:
    events = c.events
except SimplEthError as e:
    fail_count += 1
    print(f'FAIL:  Unable to get events for "{cname}".')
    print(f'MESSAGE:  {e}')
    print('')
else:
    pass_count += 1
    if args.verbose:
        print(f'PASS:  Events for "{cname}" = {events}.')
        print('')

# Test functions property
try:
    functions = c.functions
except SimplEthError as e:
    fail_count += 1
    print(f'FAIL:  Unable to get functions for "{cname}".')
    print(f'MESSAGE:  {e}')
    print('')
else:
    pass_count += 1
    if args.verbose:
        print(f'PASS:  Transactions for "{cname}" = {functions}.')
        print('')

# Test address property
try:
    addr = c.address
except SimplEthError as e:
    fail_count += 1
    print(f'FAIL:  Unable to get artifact address for "{cname}".')
    print(f'MESSAGE:  {e}')
    print('')
else:
    pass_count += 1
    if args.verbose:
        print(f'PASS:  Artifact address for "{cname}" = {addr}.')
        print('')

# Test connect
try:
    c.connect()
except SimplEthError as e:
    fail_count += 1
    print(f'FAIL:  Unable to connect to contract "{cname}".')
    print(f'MESSAGE:  {e}')
    print('')
else:
    pass_count += 1
    if args.verbose:
        print(f'PASS:  Connected to contract "{cname}".')
        print('')

# Attempt to run transaction with bogus name
# Includes printing details of an exception
try:
    trx_name = 'bogusTransaction'
    tresults = c.run_trx(user, trx_name, 10, 20, 30, event_name='NumsStored')
except SimplEthError as e:
    pass_count += 1
    if args.verbose:
        print(f'PASS:  Unable to run bogus transaction "{trx_name}".')
        print(f'MESSAGE:  {e}')
        print(f'*****  Print Exception Instance Variables  *****')
        print(f'code                = {e.code}')
        print(f'message             = {e.message}')
        print(f'exc_info type       = {e.exc_info[0]}')
        print(f'exc_info value      = {e.exc_info[1]}')
        print(f'exc_info traceback  = {e.exc_info[2]}')
        print(f'************************************************')
        print('')
else:    
    fail_count += 1
    print(f'FAIL:  Ran the bogus transaction "{trx_name}".')
    p.print_trx_results(tresults)
    print('')

# Attempt to run transaction with bogus sender address
try:
    trx_name = 'storeNums'
    bogus_user = '0x0000000000000000000000000000000000000000'
    tresults = c.run_trx(
        bogus_user,
        trx_name,
        10,
        20,
        30,
        event_name='NumsStored'
        )
except SimplEthError as e:
    pass_count += 1
    if args.verbose:
        print(f'PASS:  Unable to run transaction with bogus sender address.')
        print(f'MESSAGE:  {e}')
        print('')
else:    
    fail_count += 1
    print(f'FAIL:  Ran trx "{trx_name}" with bogus sender "{bogus_user}".')
    p.print_trx_results(tresults)
    print('')

# Attempt to run transaction with bogus event name
try:
    trx_name = 'storeNums'
    tresults = c.run_trx(user, trx_name, 10, 20, 30, event_name='BogusEvent')
except SimplEthError as e:
    pass_count += 1
    if args.verbose:
        print(f'PASS:  Unable to run transaction with bogus event name.')
        print(f'MESSAGE:  {e}')
        print('')
else:    
    fail_count += 1
    print(f'FAIL:  Ran transaction "{trx_name}" with bogus event name.')
    p.print_trx_results(tresults)
    print('')

# Attempt to run transaction with too few transaction args
try:
    trx_name = 'storeNums'
    tresults = c.run_trx(user, trx_name, 10, 20, event_name='NumsStored')
except SimplEthError as e:
    pass_count += 1
    if args.verbose:
        print(f'PASS:  Unable to run transaction with too few args.')
        print(f'MESSAGE:  {e}')
        print('')
else:    
    fail_count += 1
    print(f'FAIL:  Ran transaction "{trx_name}" with too few args.')
    p.print_trx_results(tresults)
    print('')

# Attempt to run transaction with too many transaction args
try:
    trx_name = 'storeNums'
    tresults = c.run_trx(user, trx_name, 10, 20, 30, 40, event_name='NumsStored')
except SimplEthError as e:
    pass_count += 1
    if args.verbose:
        print(f'PASS:  Unable to run transaction with too many args.')
        print(f'MESSAGE:  {e}')
        print('')
else:    
    fail_count += 1
    print(f'FAIL:  Ran transaction "{trx_name}" with too many args.')
    p.print_trx_results(tresults)
    print('')

# Attempt to run transaction with bad arg type
try:
    trx_name = 'storeNums'
    bogus_arg = 'bogus'
    tresults = c.run_trx(user, trx_name, bogus_arg, 20, 30, event_name='NumsStored')
except SimplEthError as e:
    pass_count += 1
    if args.verbose:
        print(f'PASS:  Unable to run transaction with bad arg type.')
        print(f'MESSAGE:  {e}')
        print('')
else:    
    fail_count += 1
    print(f'FAIL:  Ran "{trx_name}" with bogus arg "{bogus_arg}".')
    p.print_trx_results(tresults)
    print('')

# Attempt to run transaction with missing sender arg
try:
    trx_name = 'storeNums'
    tresults = c.run_trx(trx_name, 10, 20, 30, event_name='NumsStored')
except SimplEthError as e:
    pass_count += 1
    if args.verbose:
        print(f'PASS:  Unable to run transaction with missing sender arg.')
        print(f'MESSAGE:  {e}')
        print('')
else:    
    fail_count += 1
    print(f'FAIL:  Ran "{trx_name}" with sender arg missing.')
    p.print_trx_results(tresults)
    print('')

# Attempt to run transaction with missing transaction name arg
try:
    trx_name = 'storeNums'
    tresults = c.run_trx(user, 10, 20, 30, event_name='NumsStored')
except SimplEthError as e:
    pass_count += 1
    if args.verbose:
        print(f'PASS:  Unable to run transaction with missing trx_name arg.')
        print(f'MESSAGE:  {e}')
        print('')
else:    
    fail_count += 1
    print(f'FAIL:  Ran "{trx_name}" with trx_name arg missing.')
    p.print_trx_results(tresults)
    print('')

# Attempt to run transaction with insufficient gas limit
try:
    trx_name = 'storeNums'
    bogus_gas = 1000
    tresults = c.run_trx(
        user,
        trx_name,
        10,
        20,
        30,
        event_name='NumsStored',
        gas_limit=bogus_gas
        )
except SimplEthError as e:
    pass_count += 1
    if args.verbose:
        print(
            f'PASS:  Unable to run "{trx_name}" with gas limit = {bogus_gas}.'
            )
        print(f'MESSAGE:  {e}')
        print('')
else:    
    fail_count += 1
    print(
        f'FAIL:  Ran "{trx_name}" with {bogus_gas} gas. This amount '
        f'of gas should have been too small and the trx should revert.'
        )
    p.print_trx_results(tresults)
    print('')

# Attempt to run transaction with gas limit beyond the max for Ganache
try:
    trx_name = 'storeNums'
    bogus_gas = 7_000_000
    tresults = c.run_trx(
        user,
        trx_name,
        10,
        20,
        30,
        event_name='NumsStored',
        gas_limit=bogus_gas
        )
except SimplEthError as e:
    pass_count += 1
    if args.verbose:
        print(
            f'PASS:  Unable to run "{trx_name}" with gas limit = {bogus_gas}.'
            )
        print(f'MESSAGE:  {e}')
        print('')
else:    
    fail_count += 1
    print(
        f'FAIL:  Ran "{trx_name}" with {bogus_gas} gas. This amount '
        f'of gas should have been greater than Ganache max gas limit '
        f'amount.'
        )
    p.print_trx_results(tresults)
    print('')

# Run transaction and get the fee
try:
    trx_name = 'storeNums'
    initial_balance = b.get_balance(user)
    tresults = c.run_trx(user, trx_name, 10, 20, 30, event_name='NumsStored')
    end_balance = b.get_balance(user)
except SimplEthError as e:
    fail_count += 1
    print(f'FAIL:  Unable to run transaction "{trx_name}".')
    print(f'MESSAGE:  {e}')
    print('')
else:
    pass_count += 1
    if args.verbose:
        trx_fee = initial_balance - end_balance
        print(f'PASS:  Ran transaction "{trx_name}" and calculated the fee.')
        p.print_trx_results(tresults)
        print(f'Fee to run trx = {ethconv.convert(trx_fee, "wei", "gwei")} gwei.')
        print('')

# Run transaction again and specify enough gas to run successfully.
try:
    trx_name = 'storeNums'
    enough_gas = tresults['gas_used'] + 200
    tresults = c.run_trx(
        user,
        trx_name,
        10,
        20,
        30,
        event_name='NumsStored',
        gas_limit=enough_gas
        )
except SimplEthError as e:
    fail_count += 1
    print(
        f'FAIL:  Unable to run transaction "{trx_name}" when specifying '
        f'{enough_gas} gas, which should have worked.'
        )
    print(f'MESSAGE:  {e}')
    print('')
else:
    pass_count += 1
    if args.verbose:
        print(
            f'PASS:  Ran transaction "{trx_name}" and specified '
            f'{enough_gas} gas.'
            )
        p.print_trx_results(tresults)
        print('')

# Run transaction again and specify half the default fees.
# Calculate trx fee paid.
try:
    trx_name = 'storeNums'
    max_priority_fee_wei=int(constant.MAX_PRIORITY_FEE_GWEI / 2)
    max_fee_wei=int(constant.MAX_FEE_GWEI / 2)
    max_priority_fee_gwei = int(
        ethconv.convert(
            max_priority_fee_wei,
            'wei',
            'gwei'
            )
        )
    max_fee_gwei = int(
        ethconv.convert(
            max_fee_wei,
            'wei',
            'gwei'
            )
        )
    initial_balance = b.get_balance(user)
    tresults = c.run_trx(
        user,
        trx_name,
        10,
        20,
        30,
        event_name='NumsStored',
        max_priority_fee_gwei=max_priority_fee_gwei,
        max_fee_gwei=max_fee_gwei
        )
    end_balance = b.get_balance(user)
except SimplEthError as e:
    fail_count += 1
    print(
        f'FAIL:  Unable to run transaction "{trx_name}" when specifying '
        f'Max Priority Fee of {max_priority_fee_gwei} '
        f'and Max Fee {max_fee_gwei}.'
        )
    print(f'MESSAGE:  {e}')
    print('')
else:
    pass_count += 1
    if args.verbose:
        trx_fee = initial_balance - end_balance
        print(
            f'PASS:  Ran transaction "{trx_name}" and specified '
            f'Max Priority Fee of {max_priority_fee_gwei} '
            f'and Max Fee {max_fee_gwei}.'
            )
        p.print_trx_results(tresults)
        print(f'Fee to run trx = {ethconv.convert(trx_fee, "wei", "gwei")} gwei.')
        print('')

# Run estimate gas method for the same transaction
try:
    gas_estimate = c.get_gas_estimate(user, trx_name, 10, 20, 30)
except SimplEthError as e:
    fail_count += 1
    print(f'FAIL:  Unable to estimate gas for "{trx_name}".')
    print(f'MESSAGE:  {e}')
    print('')
else:
    pass_count += 1
    if args.verbose:
        print(f'PASS:  Able to get gas estimate for "{trx_name}".')
        print(f'Gas required (estimate) = {gas_estimate}.')
        print('')

# Run transaction without the event name arg
try:
    trx_name = 'storeNums'
    tresults = c.run_trx(user, trx_name, 10, 20, 30)
except SimplEthError as e:
    fail_count += 1
    print(f'FAIL:  Unable to run trx "{trx_name}" with no event_name arg.')
    print(f'MESSAGE:  {e}')
    print('')
else:
    pass_count += 1
    if args.verbose:
        print(f'PASS:  Ran trx "{trx_name}" without specifying event_name.')
        p.print_trx_results(tresults)
        print('')

# Run a transaction with different types of args
try:
    trx_name = 'storeTypes'
    tresults = c.run_trx(
        user,
        trx_name,
        1,
        -2,
        user,
        'test',
        event_name='TypesStored'
        )
    trx_hash = tresults["trx_hash"]
except SimplEthError as e:
    fail_count += 1
    print(f'FAIL:  Unable to run transaction "{trx_name}".')
    print(f'MESSAGE:  {e}')
    print('')
else:
    pass_count += 1
    if args.verbose:
        print(f'PASS:  Ran transaction "{trx_name}".')
        p.print_trx_results(tresults)
        print('')

# Get same transaction results using hash from above with get_trx_results()
tresults = c.get_trx_results(trx_hash, trx_name, event_name='TypesStored')
if not tresults:
    fail_count += 1
    print(f'FAIL:  Unable to get tresults for "{trx_name}".')
    print('')
else:
    pass_count += 1
    if args.verbose:
        print(f'PASS:  Get tresults using hash = "{trx_hash.hex()}".')
        p.print_trx_results(tresults)
        print('')

# And get same transaction results again using hash from above with
# get_trx_results_wait()
tresults = c.get_trx_results_wait(trx_hash, trx_name, event_name='TypesStored')
if not tresults:
    fail_count += 1
    print(f'FAIL:  Unable to get trx results with wait for "{trx_name}".')
    print('')
else:
    pass_count += 1
    if args.verbose:
        print(f'PASS:  Get tresults with wait using hash = "{trx_hash.hex()}".')
        p.print_trx_results(tresults)
        print('')

# Attempt to get_trx_results() with a bogus hash
trx_hash = 0
tresults = c.get_trx_results(trx_hash, trx_name, event_name='TypesStored')
if not tresults:
    pass_count += 1
    if args.verbose:
        print(f'PASS:  Unable to get_trx_results() with hash of 0.')
        print('')
else:
    fail_count += 1
    print(f'FAIL:  get_trx_results() with hash of 0 unexpectedly worked.')
    p.print_trx_results(tresults)
    print('')

# Attempt to get_trx_results_wait() with a bogus hasn
# Set it to fail after waiting one second to speed up the test.
trx_hash = 0
tresults = c.get_trx_results_wait(
    trx_hash,
    trx_name,
    event_name='TypesStored',
    timeout=1,
    poll_latency=1
    )
if not tresults:
    pass_count += 1
    if args.verbose:
        print(f'PASS:  Unable get_trx_results_wait() with hash 0.')
        print('')
else:
    fail_count += 1
    print(f'FAIL:  get_trx_results_wait() with hash of 0 unexpectedly worked.')
    p.print_trx_results(tresults)
    print('')

# Send a transaction
try:
    trx_name = 'storeTypes'
    trx_hash = c.submit_trx(user, trx_name, 1, -2, user, 'test')
except SimplEthError as e:
    fail_count += 1
    print(f'FAIL:  Unable to send transaction "{trx_name}".')
    print(f'MESSAGE:  {e}')
    print('')
else:
    pass_count += 1
    if args.verbose:
        print(f'PASS:  Sent transaction "{trx_name}".')
        print(f'trx_hash = {trx_hash}')
        print(f'trx_hash converted to hex = {trx_hash.hex()}')
        print('')

# Get transaction results using hash from above with get_trx_results()
tresults = c.get_trx_results(trx_hash, trx_name, event_name='TypesStored')
if not tresults:
    fail_count += 1
    print(f'FAIL:  Unable to get tresults for "{trx_name}".')
    print('')
else:
    pass_count += 1
    if args.verbose:
        print(f'PASS:  Get tresults using hash = "{trx_hash.hex()}".')
        p.print_trx_results(tresults)
        print('')

# And get same transaction results again using hash from above with
# get_trx_results_wait()
tresults = c.get_trx_results_wait(trx_hash, trx_name, event_name='TypesStored')
if not tresults:
    fail_count += 1
    print(f'FAIL:  Unable to get trx results with wait for "{trx_name}".')
    print('')
else:
    pass_count += 1
    if args.verbose:
        print(f'PASS:  Get tresults with wait using hash = "{trx_hash.hex()}".')
        p.print_trx_results(tresults)
        print('')

# Get events from previous transactions
try:
    num_blocks = 10
    event_name = 'TypesStored'
    elist = c.get_past_events(event_name, num_blocks)
except SimplEthError as e:
    fail_count += 1
    print(f'FAIL:  Unable to get past events for "{event_name}".')
    print(f'MESSAGE:  {e}')
    print('')
else:
    pass_count += 1
    if args.verbose:
        print(
            f'PASS:  Found {len(elist)} events for "{event_name}" in '
            f'the most recent {num_blocks} blocks.'
            )
        p.print_event_list(elist, indent=4)
        print('')

# Attempt to get events using bogus event name
try:
    num_blocks = 10
    event_name = 'bogus'
    elist = c.get_past_events(event_name, num_blocks)
except SimplEthError as e:
    pass_count += 1
    if args.verbose:
        print(
            f'PASS:  Unable to get past events for '
            f'"{event_name}" event name.'
            )
        print(f'MESSAGE:  {e}')
        print('')
else:
    fail_count += 1
    print(
        f'FAIL:  Found {len(elist)} events for event: "{event_name}" in '
        f'the most recent {num_blocks} blocks. Should not happen.'
        )
    p.print_event_list(elist, indent=4)
    print('')

# Attempt to get events using zero number of blocks
try:
    num_blocks = 0
    event_name = 'TypesStored'
    elist = c.get_past_events(event_name, num_blocks)
except SimplEthError as e:
    pass_count += 1
    if args.verbose:
        print(
            f'PASS:  Unable to get past events using '
            f'num_blocks that is too low = {num_blocks}'
            )
        print(f'MESSAGE:  {e}')
        print('')
else:
    fail_count += 1
    print(
        f'FAIL:  Found {len(elist)} events in '
        f'the most recent {num_blocks} blocks. Should not happen.'
        )
    p.print_event_list(elist, indent=4)
    print('')

# Attempt to get events using too many number of blocks
try:
    num_blocks = b.block_number + 1
    event_name = 'TypesStored'
    elist = c.get_past_events(event_name, num_blocks)
except SimplEthError as e:
    pass_count += 1
    if args.verbose:
        print(
            f'PASS:  Unable to get past events using '
            f'num_blocks that is too high = {num_blocks}'
            )
        print(f'MESSAGE:  {e}')
        print('')
else:
    fail_count += 1
    print(
        f'FAIL:  Found {len(elist)} events in '
        f'the most recent {num_blocks} blocks. Should not happen.'
        )
    p.print_event_list(elist, indent=4)
    print('')

# Attempt to get events using wrong type for event_name
try:
    num_blocks = 10
    event_name = 0
    elist = c.get_past_events(event_name, num_blocks)
except SimplEthError as e:
    pass_count += 1
    if args.verbose:
        print(
            f'PASS:  Unable to get past events using '
            f'event_name = {ename} (wrong type).'
            )
        print(f'MESSAGE:  {e}')
        print('')
else:
    fail_count += 1
    print(
        f'FAIL:  Found {len(elist)} events in the most recent {num_blocks} '
        f'blocks while using wrong type for event_name: {ename}. '
        f'Should not happen.'
        )
    p.print_event_list(elist, indent=4)
    print('')

# Attempt to send a transaction with insufficient gas limit
try:
    trx_name = 'storeTypes'
    bogus_gas = 1000
    trx_hash = c.submit_trx(
        user,
        trx_name,
        1,
        -2,
        user,
        'test',
        gas_limit=bogus_gas
        )
except SimplEthError as e:
    pass_count += 1
    if args.verbose:
        print(
            f'PASS:  Unable to send "{trx_name}" with gas limit = {bogus_gas}.'
            )
        print(f'MESSAGE:  {e}')
        print('')
else:
    pass_count += 1
    if args.verbose:
        print(
            f'FAIL:  Sent transaction "{trx_name}" with {bogus_gas} gas.\n'
            f'       This amount of gas should have been too low and should'
            f'       have failed. Instead, it returned a valid trx_hash of '
            f'       {trx_hash}'
            )
        print('')

# Send the transaction again and specify enough gas to run successfully.
try:
    trx_name = 'storeTypes'
    enough_gas = tresults['gas_used'] + 200
    trx_hash = c.submit_trx(
        user,
        trx_name,
        1,
        -2,
        user,
        'test',
        gas_limit=enough_gas
        )
except SimplEthError as e:
    fail_count += 1
    print(
        f'FAIL:  Unable to send transaction "{trx_name}" when specifying.'
        f'{enough_gas} gas, which should have worked.'
        )
    print(f'MESSAGE:  {e}')
    print('')
else:
    pass_count += 1
    if args.verbose:
        print(
            f'PASS:  Sent transaction "{trx_name}" and specified '
            f'{enough_gas} gas.\n'
            f'trx_hash converted to hex = {trx_hash.hex()}'
            )
        print('')

# Send the transaction again and specify half the default fees.
# Calculate trx fee paid.
try:
    trx_name = 'storeTypes'
    max_priority_fee_wei=int(constant.MAX_PRIORITY_FEE_GWEI / 2)
    max_fee_wei=int(constant.MAX_FEE_GWEI / 2)
    max_priority_fee_gwei = int(
        ethconv.convert(
            max_priority_fee_wei,
            'wei',
            'gwei'
            )
        )
    max_fee_gwei = int(
        ethconv.convert(
            max_fee_wei,
            'wei',
            'gwei'
            )
        )
    initial_balance = b.get_balance(user)
    trx_hash = c.submit_trx(
        user,
        trx_name,
        1,
        -2,
        user,
        'test',
        max_priority_fee_gwei=max_priority_fee_gwei,
        max_fee_gwei=max_fee_gwei
        )
    end_balance = b.get_balance(user)
except SimplEthError as e:
    fail_count += 1
    print(
        f'FAIL:  Unable to send transaction "{trx_name}" when specifying '
        f'Max Priority Fee of {max_priority_fee_gwei} '
        f'and Max Fee {max_fee_gwei}.'
        )
    print(f'MESSAGE:  {e}')
    print('')
else:
    pass_count += 1
    if args.verbose:
        trx_fee = initial_balance - end_balance
        print(
            f'PASS:  Able to send transaction "{trx_name}" with '
            f'Max Priority Fee of {max_priority_fee_gwei} '
            f'and Max Fee {max_fee_gwei}.'
            )
        p.print_trx_results(tresults)
        print(
            f'Fee to send trx = '
            f'{ethconv.convert(trx_fee, "wei", "gwei")} gwei.'
            )
        print('')

# Get transaction results using hash from above with get_trx_results()
tresults = c.get_trx_results(trx_hash, trx_name, event_name='TypesStored')
if not tresults:
    fail_count += 1
    print(f'FAIL:  Unable to get tresults for "{trx_name}".')
    print('')
else:
    pass_count += 1
    if args.verbose:
        print(f'PASS:  Get tresults using hash = "{trx_hash.hex()}".')
        p.print_trx_results(tresults)
        print('')

# Create event filter
try:
    event_name = 'NumsStored'
    efilter = c.create_event_filter(event_name)
except SimplEthError as e:
    fail_count += 1
    print(f'FAIL:  Unable to create event filter for "{event_name}".')
    print(f'MESSAGE:  {e}')
    print('')
else:
    pass_count += 1
    if args.verbose:
        print(f'PASS:  Created event filter for "{event_name}".')
        print('')

# Check for a new event. Should fail since this is the first time we look.
try:
    elist = c.get_new_events(efilter)
    num_events = len(elist)
except SimplEthError as e:
    fail_count += 1
    print(f'FAIL:  Unable to get new "{event_name}" events.\n')
    print(f'MESSAGE:  {e}')
    print('')
else:
    if num_events == 0:
        pass_count += 1
        if args.verbose:
            print(
                f'PASS:  No new "{event_name}" events were found.\n'
                f'       This is expected since this is the first time '
                f'we looked.\n'
                )
            print('')
    else:    
        fail_count += 1
        if args.verbose:
            print(
                f'FAIL:  {num_events} new "{event_name}" events were found.\n'
                f'       This is unexpected. Since this is the first time '
                f'we looked and should have found 0. Here are the '
                f'events found:\n'
                )
            p.print_event_list(elist)
            print('')

# Run transaction
try:
    trx_name = 'storeNums'
    tresults = c.run_trx(user, trx_name, 10, 20, 30, event_name='NumsStored')
except SimplEthError as e:
    fail_count += 1
    print(f'FAIL:  Unable to run transaction "{trx_name}".')
    print(f'MESSAGE:  {e}')
    print('')
else:
    pass_count += 1
    if args.verbose:
        print(f'PASS:  Ran transaction "{trx_name}".')
        p.print_trx_results(tresults)
        print('')

# Check for a new event. Should succeed since a transaction just completed.
try:
    elist = c.get_new_events(efilter)
    num_events = len(elist)
except SimplEthError as e:
    fail_count += 1
    print(f'FAIL:  Unable to get new "{event_name}" events.\n')
    print(f'MESSAGE:  {e}')
    print('')
else:
    if num_events == 0:
        fail_count += 1
        print(f'FAIL:  Found {num_events} new events. Should have found 1.\n')
        print('')
    else:    
        pass_count += 1
        if args.verbose:
            print(f'PASS:  {num_events} new "{event_name}" events were found.\n')
            p.print_event_list(elist)
            print('')

# Attempt to create event filter with bogus event name
try:
    event_name = 'bogus'
    efilter = c.create_event_filter(event_name)
except SimplEthError as e:
    pass_count += 1
    if args.verbose:
        print(f'PASS:  Unable to create event filter using "{event_name}".')
        print(f'MESSAGE:  {e}')
        print('')
else:    
    fail_count += 1
    print(f'FAIL:  Able to get create event filter using "{event_name}" event.')
    print('')

# Use public getter for a public state variable
try:
    var_name = 'specialNum'
    var_value = c.get_var(var_name)
except SimplEthError as e:
    fail_count += 1
    print(f'FAIL:  Unable to get variable "{var_name}".')
    print(f'MESSAGE:  {e}')
    print('')
else:
    pass_count += 1
    if args.verbose:
        print(f'PASS:  Able to get variable.')
        print(f'{var_name} = {var_value}')
        print('')

# Use public getter for a bogus variable name
try:
    bogus_name = 'bogusVar'
    bogus_value = c.get_var(bogus_name)
except SimplEthError as e:
    pass_count += 1
    if args.verbose:
        print(f'PASS:  Unable to get bogus variable "{bogus_name}".')
        print(f'MESSAGE:  {e}')
        print('')
else:    
    fail_count += 1
    print(f'FAIL:  Able to get value for bogus variable "{bogus_name}".')
    print(f'{bogus_name} = {bogus_value}')
    print('')

# Test calling function that has no args
try:
    fname = 'getNum0'
    freturn = c.call_fcn(fname)
except SimplEthError as e:
    fail_count += 1
    print(f'FAIL:  Unable to get call function "{fname}".')
    print(f'MESSAGE:  {e}')
    print('')
else:
    pass_count += 1
    if args.verbose:
        print(f'PASS:  Able to call function that has no args.')
        print(f'{fname}() returned {freturn}')
        print('')
args = parser.parse_args()

# Attempt to call a function without its arg
try:
    fname = 'getNum'
    freturn = c.call_fcn(fname)
except SimplEthError as e:
    pass_count += 1
    if args.verbose:
        print(f'PASS:  Unable to call function without its arg.')
        print(f'MESSAGE:  {e}')
        print('')
else:
    fail_count += 1
    print(f'FAIL:  Able to call "{fname}" without its required arg.')
    print(f'{fname}() = {freturn}')
    print('')

# Attempt to call a function with too many args
try:
    fname = 'getNum'
    farg1 = 1
    farg2 = 2
    freturn = c.call_fcn(fname, farg1, farg2)
except SimplEthError as e:
    pass_count += 1
    if args.verbose:
        print(f'PASS:  Unable to call function with too many args.')
        print(f'MESSAGE:  {e}')
        print('')
else:
    fail_count += 1
    print(f'FAIL:  Able to call "{fname}" with too many args.')
    print(f'{fname}({farg1}, {farg2}) = {freturn}')
    print('')

# Attempt to call a function with out of bounds arg
try:
    fname = 'getNum'
    farg = 10
    freturn = c.call_fcn(fname, farg)
except SimplEthError as e:
    pass_count += 1
    if args.verbose:
        print(f'PASS:  Unable to call function with out of bounds arg.')
        print(f'MESSAGE:  {e}')
        print('')
else:
    fail_count += 1
    print(f'FAIL:  Able to call "{fname}" with out of bounds arg.')
    print(f'{fname}(farg) = {freturn}')
    print('')

# Attempt to call a function with wrong arg type
try:
    fname = 'getNum'
    farg = 'bogus'
    freturn = c.call_fcn(fname, farg)
except SimplEthError as e:
    pass_count += 1
    if args.verbose:
        print(f'PASS:  Unable to call function using wrong arg type.')
        print(f'MESSAGE:  {e}')
        print('')
else:
    fail_count += 1
    print(f'FAIL:  Able to call "{fname}" with wrong arg type.')
    print(f'{fname}(farg) = {freturn}')
    print('')

# Call function that returns an array
try:
    fname = 'getNums'
    freturn = c.call_fcn(fname)
except SimplEthError as e:
    fail_count += 1
    print(f'FAIL:  Unable to call function "{fname}".')
    print(f'MESSAGE:  {e}')
    print('')
else:
    pass_count += 1
    if args.verbose:
        print(f'PASS:  Able to call function with args.')
        print(f'{fname}() returned {freturn}')
        print('')

# Call function to get size of contract
try:
   fname = 'getContractSize'
   size = c.call_fcn(fname, c.address)
except SimplEthError as e:
    fail_count += 1
    print(f'FAIL:  Unable to get contract size with "{fname}".')
    print(f'MESSAGE:  {e}')
    print('')
else:
    pass_count += 1
    if args.verbose:
        print(f'PASS:  Able to get contract size with "{fname}".')
        print(f'Deployed contract size (bytes) = {size}.')
        print('')

# Get size of contract using size attribute. Should match above.
try:
   size = c.size
except SimplEthError as e:
    fail_count += 1
    print(f'FAIL:  Unable to get size attribute.\n')
    print(f'MESSAGE:  {e}')
    print('')
else:
    pass_count += 1
    if args.verbose:
        print(f'PASS:  Able to get contract size with attribute.')
        print(f'Deployed contract size (bytes) = {size}.')
        print('')



print(f'PASS: {pass_count} test cases.')
print(f'FAIL: {fail_count} test cases.')
