#!
"""Unit test for Contract() class using Ganache with a mining delay

Tests only run_trx() and submit_trx() with arg values for polling and timeout.

Set the delay in Ganache by creating a new workspace and adjusting
Server->Automining to OFF and Sever->Mining Block Time to match
`MINING_DELAY`.

"""

import argparse
import time
from simpleth import Blockchain, Contract, SimplEthError
import s_time as stime
import s_constant as constant
import s_print as p

# Ganache mining delay, in seconds
MINING_DELAY = 10

# Test contract params
cname = 'TestTrx'  # contract name
ename = 'TestTrxConstructed'  # event name for contract constructor
init_num = 123  # constructor arg

# Counters
pass_count = 0
fail_count = 0

parser = argparse.ArgumentParser(
    description = ('Unit test for Contract() class with mining delay')
    )
parser.add_argument(
    '-v',
    help='print details of successful test cases',
    dest='verbose',
    action='store_true'
    )
args = parser.parse_args()

# Remind user about assumptions
if args.verbose:
    print(
        f'These test cases assume use of a Ganache workspace '
        f'with AUTOMINE=OFF and MINING BLOCK TIME={MINING_DELAY}.\n'
        )

# Set up objects and the user account for test cases.
# Will exit if unable to instantiate objects since Ganache is
# probably not running.
try:
    b = Blockchain()
    user = b.accounts[0]
except SimplEthError as e:
    print(f'Unable to setup blockchain and user.')
    print(f'MESSAGE:  {e}')
    print('')
    exit()

# Instantiate Contract() object
try:
    c = Contract(cname)
except SimplEthError as e:
    print(f'Unable to instantiate contract "{cname}".')
    print(f'MESSAGE:  {e}')
    print('')
    exit()

# Deploy contract
try:
    c.deploy(user, init_num)
except SimplEthError as e:
    print(f'FAIL:  Unable to deploy contract "{cname}".')
    print(f'MESSAGE:  {e}')
    print('')
    exit()
else:
    if args.verbose:
        print(
            f'Contract "{cname}" deployed. Had to wait for transaction '
            f'to be mined due to MINING_DELAY of {MINING_DELAY} seconds.'
            )
        print('')

# Run transaction with defaults for timing and show time taken
try:
    trx_name = 'storeNums'
    start_time = stime.get_epoch()
    tresults = c.run_trx(user, trx_name, 10, 20, 30)
    end_time = stime.get_epoch()
    trx_time = round(end_time - start_time, 2)
except SimplEthError as e:
    fail_count += 1
    print(f'FAIL:  Unable to run transaction "{trx_name}" with defaults.')
    print(f'MESSAGE:  {e}')
else:
    pass_count += 1
    if args.verbose:
        print(f'PASS:  Ran transaction "{trx_name}" with timing defaults.')
        p.print_trx_results(tresults)
if args.verbose:
    print(
        f'TIMING VALUES:\n'
        f'    mining_delay  = {MINING_DELAY}\n'
        f'    timeout       = {constant.TIMEOUT} sec.\n'
        f'    poll_latency  = {constant.POLL_LATENCY} sec.\n'
        f'    trx time      = {trx_time} sec.'
        )
    print('')

# Attempt to run transaction with a timeout expiring before mining
try:
    trx_name = 'storeNums'
    bogus_timeout = MINING_DELAY - 2
    start_time = stime.get_epoch()
    tresults = c.run_trx(user, trx_name, 10, 20, 30, timeout=bogus_timeout)
    end_time = stime.get_epoch()
    trx_time = round(end_time - start_time, 2)
except SimplEthError as e:
    pass_count += 1
    if args.verbose:
        print(
            f'PASS:  Unable to run transaction "{trx_name}" using '
            f'a timeout that expires before mining.'
            )
        print(f'MESSAGE:  {e}')
        print('')
else:
    fail_count += 1
    print(
        f'FAIL:  Able to run transaction "{trx_name}" using '
        f'a timeout that expires before mining.'
        )
    p.print_trx_results(tresults)
if args.verbose:
    print(
        f'TIMING VALUES:\n'
        f'    mining_delay  = {MINING_DELAY}\n'
        f'    timeout       = {bogus_timeout} sec.\n'
        f'    poll_latency  = {constant.POLL_LATENCY} sec.\n'
        f'    trx time      = {trx_time} sec.'
        )
    print('')

# Attempt to run transaction with a polling frequency longer than timeout
try:
    trx_name = 'storeNums'
    timeout = MINING_DELAY + 2
    too_long_latency = timeout + 2
    start_time = stime.get_epoch()
    tresults = c.run_trx(user, trx_name, 10, 20, 30, timeout=timeout, poll_latency=too_long_latency)
    end_time = stime.get_epoch()
    trx_time = round(end_time - start_time, 2)
except SimplEthError as e:
    pass_count += 1
    if args.verbose:
        print(
            f'PASS:  Unable to run transaction "{trx_name}" using '
            f'a polling frequency that is greater than the timeout.\n'
            f'This never looks for the transaction completion. The first '
            f'poll never took place. It timed out before ever checking.'
            )
        print(f'MESSAGE:  {e}')
else:
    fail_count += 1
    print(
        f'FAIL:  Able to run transaction "{trx_name}" using '
        f'a timeout that expires before mining.'
        )
    p.print_trx_results(tresults)
if args.verbose:
    print(
        f'TIMING VALUES:\n'
        f'    mining_delay  = {MINING_DELAY}\n'
        f'    timeout       = {timeout} sec.\n'
        f'    poll_latency  = {too_long_latency} sec.\n'
        f'    trx time      = {trx_time} sec.'
        )
    print('')

# Send a transaction
try:
    trx_name = 'storeTypes'
    event_name = 'TypesStored'
    send_time = stime.get_epoch()
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
        print(f'trx_hash = {trx_hash.hex()}')
        print('')

# Attempt to immediately get trx_results. Should fail since mining is delayed.
immediate_get_trx_time = stime.get_epoch()
try:
    tresults = c.get_trx_results(trx_hash, trx_name, event_name='TypesStored')
except SimplEthError as e:
    fail_count += 1
    print(
        f'FAIL:  Error in get_trx_results({trx_name}).\n'
        f'       Unable to run test case to immediately get trx_results.\n'
        f'MESSAGE:  {e}'
        )
else:    
    send_to_get_time = round(immediate_get_trx_time - send_time,2)
    if not tresults:
        pass_count += 1
        if args.verbose:
            print(
                f'PASS:  Unable to get trx_results immediately after sending the '
                f'transaction. Must wait for mining.'
                )
    else:
        fail_count += 1
        print(
            f'FAIL:  Able to get trx_results before the mining delay. '
            f'Should not have been able to get results yet.'
            )
        p.print_trx_results(tresults)
    if args.verbose:
        print(
            f'TIMING VALUES:\n'
            f'    mining_delay       = {MINING_DELAY}\n'
            f'    send-to-get time   = {send_to_get_time} sec.'
            )
        print('')

# Sleep for the MINING_DELAY and try again to get the trx_results. Should work.
time.sleep(MINING_DELAY)
delayed_get_trx_time = stime.get_epoch()
try:
    tresults = c.get_trx_results(trx_hash, trx_name, event_name='TypesStored')
except SimplEthError as e:
    fail_count += 1
    print(
        f'FAIL:  Error in get_trx_results({trx_name}).\n'
        f'       Unable to run test case to sleep and then get trx_results.\n'
        f'MESSAGE:  {e}'
        )
else:
    send_to_get_time = round(delayed_get_trx_time - send_time,2)
    if tresults:
        pass_count += 1
        if args.verbose:
            print(
                f'PASS:  Able to get trx_results after sleeping for the mining delay.'
                )
            p.print_trx_results(tresults)
    else:
        fail_count += 1
        print(
            f'FAIL:  Unable to get trx_results after sleeping for the mining '
            f'delay. Should have been able to get the results.'
            )
    if args.verbose:
        print(
            f'TIMING VALUES:\n'
            f'    mining_delay       = {MINING_DELAY}\n'
            f'    send-to-get time   = {send_to_get_time} sec.'
            )
        print('')

# Send the transaction again
try:
    send_time = stime.get_epoch()
    trx_hash = c.submit_trx(user, trx_name, 1, -2, user, 'test')
except SimplEthError as e:
    fail_count += 1
    print(f'FAIL:  Unable to send transaction "{trx_name}" again.')
    print(f'MESSAGE:  {e}')
    print('')
else:
    pass_count += 1
    if args.verbose:
        print(f'PASS:  Sent transaction again "{trx_name}" again.')
        print(f'trx_hash = {trx_hash.hex()}')
        print('')

# Attempt to get_trx_results_wait with a timeout that is too short. 
# It expires before mining takes place (it is less than MINING_DELAY).
too_short_timeout = MINING_DELAY - 4
try:
    tresults = c.get_trx_results_wait(
        trx_hash,
        trx_name,
        event_name=event_name,
        timeout=too_short_timeout
        )
except SimplEthError as e:
    fail_count += 1
    print(
        f'FAIL:  Error in get_trx_results_wait({trx_name}).\n'
        f'       Unable to run test case with a too-short timeout.\n'
        f'MESSAGE:  {e}'
        )
else:
    get_results_time = stime.get_epoch()
    send_to_get_time = round(get_results_time - send_time, 2)
    if not tresults:
        pass_count += 1
        if args.verbose:
            print(
                f'PASS:  Unable to get_trx_results_wait("{trx_name}") using '
                f'a timeout that expires before mining.'
                )
    else:
        fail_count += 1
        print(
            f'FAIL:  Able to get_trx_results_wait("{trx_name}") using '
            f'a timeout that should have expired before mining.'
            )
        p.print_trx_results(tresults)
        print(
            f'TIMING VALUES:\n'
            f'    mining_delay       = {MINING_DELAY}\n'
            f'    timeout            = {too_short_timeout} sec.\n'
            f'    poll_latency       = {constant.POLL_LATENCY} sec.\n'
            f'    send-to-get time   = {send_to_get_time} sec.'
            )
        print('')
    if args.verbose:
        print(
            f'TIMING VALUES:\n'
            f'    mining_delay       = {MINING_DELAY}\n'
            f'    timeout            = {too_short_timeout} sec.\n'
            f'    poll_latency       = {constant.POLL_LATENCY} sec.\n'
            f'    send-to-get time   = {send_to_get_time} sec.'
            )
        print('')

# Send the transaction yet again
try:
    send_time = stime.get_epoch()
    trx_hash = c.submit_trx(user, trx_name, 1, -2, user, 'test')
except SimplEthError as e:
    fail_count += 1
    print(f'FAIL:  Unable to send transaction "{trx_name}" yet again.')
    print(f'MESSAGE:  {e}')
    print('')
else:
    pass_count += 1
    if args.verbose:
        print(f'PASS:  Sent transaction again "{trx_name}" yet again.')
        print(f'trx_hash = {trx_hash.hex()}')
        print('')

# Attempt to run transaction with a polling frequency longer than timeout.
# Should fail since the mining occurs (after MINING_DELAY seconds) and then
# it reaches timeout before the first poll occurs.
timeout = MINING_DELAY + 2
too_long_latency = timeout + 2
try:
    tresults = c.get_trx_results_wait(
        trx_hash,
        trx_name,
        event_name=event_name,
        timeout=timeout,
        poll_latency=too_long_latency
        )
except SimplEthError as e:
    fail_count += 1
    print(
        f'FAIL:  Error in get_trx_results_wait({trx_name}).\n'
        f'       Unable to run test case with polling longer than timeout.\n'
        f'MESSAGE:  {e}'
        )
else:
    get_results_time = stime.get_epoch()
    send_to_get_time = round(get_results_time - send_time, 2)
    if not tresults:
        pass_count += 1
        if args.verbose:
            print(
                f'PASS:  Unable to get_trx_results_wait("{trx_name}") using '
                f'a polling frequency that is greater than the timeout.\n'
                f'This never looks for the transaction completion. The first '
                f'poll never took place. It timed out before ever checking.'
                )
    else:
        fail_count += 1
        print(
            f'FAIL:  Able to get_trx_results_wait("{trx_name}") using '
            f'a polling frequency that is greater than the timeout.\n'
            f'This should have not returned any trx results since the'
            f'get results should have timed out before the first poll.\n'
            )
        p.print_trx_results(tresults)
    if args.verbose:
        print(
            f'TIMING VALUES:\n'
            f'    mining_delay       = {MINING_DELAY}\n'
            f'    timeout            = {timeout} sec.\n'
            f'    poll_latency       = {too_long_latency} sec.\n'
            f'    send-to-get time   = {send_to_get_time} sec.'
            )
        print('')

# Print test results summary
print(f'PASS: {pass_count} test cases.')
print(f'FAIL: {fail_count} test cases.')
