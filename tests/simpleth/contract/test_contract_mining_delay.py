"""Test Contract() with a mining delay class"""
import pytest
import time

import testconstants as constants

# Set True to skip this module. Otherwise, set False to run all.
SKIP_MINING_DELAY_TESTS = True
pytestmark = pytest.mark.skipif(
    SKIP_MINING_DELAY_TESTS,
    reason='tests require a mining block delay in ganache'
    )

# Uses ganache with automining set to 'off' and a mining delay of
# MINING_DELAY seconds specified in the ganache settings.
# These test cases only cover passes and fails due to calling the
# combination of submit_trx() and get_trx_receipt() / get_trx_receipt_wait().
# The methods are called only with valid parameters. These cases only
# check that the timing of calling get_trx_receipt() and the use
# of timeout in get_trx_receipt_wait() work as expected when there is
# a delay between submitting the trx and getting the receipt.
# The test cases for all other parameters are found in test_contract.py
#
# I have not found a way to use ganache cli or other to dynamically
# set a mining delay. These tests must be run with a ganache blockchain
# that has the proper blocktime of MINING_DELAY set. For that reason,
# these tests are typically skipped.
#
# To run these tests, switch ganache to a chain using MINING_DELAY
# and run only this file. When you want to run any other tests, you
# need to switch back to a ganache chain that uses AUTOMINING.
#
# BEWARE - sometimes the 'bad' timing test cases work. Ganache does not
# seem to always adhere to the MINING_DELAY. I've seen mining finish in
# one or two seconds before the delay should expire. Test case timings have
# been tweaked to work (hopefully) reliably.


# Seconds for block to be mined. Must match the setting in ganache.
# Value must be at least 3. Used in all test cases.
MINING_DELAY = 5


@pytest.mark.usefixtures(
    'deploy_test_contract',
    'connect_to_test_contract'
    )
class TestContractRunTrxGoodTiming:
    """Test cases for Contract().run_trx() that waits long enough."""
    def test_run_trx_with_good_timeout(
            self,
            connect_to_test_contract
            ):
        """Test run_trx() with the typical set of args fails."""
        c = connect_to_test_contract
        receipt = c.run_trx(
            constants.TRX_SENDER,
            constants.TRX_NAME,
            constants.TRX_ARG0,
            constants.TRX_ARG1,
            constants.TRX_ARG2,
            timeout=MINING_DELAY + 1
            )
        assert receipt is not None


@pytest.mark.usefixtures('connect_to_test_contract')
class TestContractRunTrxBadTiming:
    """Test cases for Contract().run_trx() that does not wait enough."""
    def test_run_trx_with_good_timeout(
            self,
            connect_to_test_contract
            ):
        """Test run_trx() with the typical set of args fails."""
        c = connect_to_test_contract
        receipt = c.run_trx(
            constants.TRX_SENDER,
            constants.TRX_NAME,
            constants.TRX_ARG0,
            constants.TRX_ARG1,
            constants.TRX_ARG2,
            timeout=MINING_DELAY - 2
            )
        assert receipt is None


@pytest.mark.usefixtures('connect_to_test_contract')
class TestContractSubmitTrxAndGetTrxReceiptGoodTiming:
    """Test cases for get_trx_receipt() that waits long enough."""
    def test_submit_trx_and_get_trx_receipt_with_good_delay(
            self,
            connect_to_test_contract
            ):
        """Test sleep long enough before getting the receipt"""
        c = connect_to_test_contract
        trx_hash = c.submit_trx(
            constants.TRX_SENDER,
            constants.TRX_NAME,
            constants.TRX_ARG0,
            constants.TRX_ARG1,
            constants.TRX_ARG2
            )
        time.sleep(MINING_DELAY+2)
        receipt = c.get_trx_receipt(trx_hash)
        assert receipt is not None

    def test_submit_trx_and_get_trx_receipts_with_good_delay(
            self,
            connect_to_test_contract
            ):
        """Test first get fails and second get works"""
        c = connect_to_test_contract
        trx_hash = c.submit_trx(
            constants.TRX_SENDER,
            constants.TRX_NAME,
            constants.TRX_ARG0,
            constants.TRX_ARG1,
            constants.TRX_ARG2
            )
        receipt1 = c.get_trx_receipt(trx_hash)
        time.sleep(MINING_DELAY+1)
        receipt2 = c.get_trx_receipt(trx_hash)
        assert receipt1 is None and receipt2 is not None


@pytest.mark.usefixtures('connect_to_test_contract')
class TestContractSubmitTrxAndGetTrxReceiptBadTiming:
    """Test cases for get_trx_receipt() that do not wait enough."""
    def test_submit_trx_and_get_trx_receipt_with_bad_delay(
            self,
            connect_to_test_contract
            ):
        """Test not sleeping long enough and then looking for the receipt"""
        # Note: this is also tested above as part of
        # test_submit_trx_and_get_trx_receipts_with_good_delay()
        c = connect_to_test_contract
        trx_hash = c.submit_trx(
            constants.TRX_SENDER,
            constants.TRX_NAME,
            constants.TRX_ARG0,
            constants.TRX_ARG1,
            constants.TRX_ARG2
            )
        time.sleep(MINING_DELAY-2)
        receipt = c.get_trx_receipt(trx_hash)
        assert receipt is None


@pytest.mark.usefixtures('connect_to_test_contract')
class TestContractSubmitTrxAndGetTrxReceiptWaitGood:
    """Test cases for get_trx_receipt_wait() that wait long enough."""
    def test_submit_trx_and_get_trx_receipt_wait_with_one_good_poll(
            self,
            connect_to_test_contract
            ):
        """Test using one get_trx... using a poll frequency greater than
        mining delay"""
        c = connect_to_test_contract
        trx_hash = c.submit_trx(
            constants.TRX_SENDER,
            constants.TRX_NAME,
            constants.TRX_ARG0,
            constants.TRX_ARG1,
            constants.TRX_ARG2
            )
        receipt = c.get_trx_receipt_wait(
            trx_hash,
            timeout=MINING_DELAY+4,
            poll_latency=MINING_DELAY+3
            )
        assert receipt is not None

    def test_submit_trx_and_get_trx_receipt_wait_with_two_good_polls(
            self,
            connect_to_test_contract
            ):
        """Test using two get_trx... using a poll frequency less than
        mining delay"""
        c = connect_to_test_contract
        trx_hash = c.submit_trx(
            constants.TRX_SENDER,
            constants.TRX_NAME,
            constants.TRX_ARG0,
            constants.TRX_ARG1,
            constants.TRX_ARG2
            )
        receipt = c.get_trx_receipt_wait(
            trx_hash,
            timeout=MINING_DELAY*2,
            poll_latency=MINING_DELAY-3
            )
        assert receipt is not None


@pytest.mark.usefixtures('connect_to_test_contract')
class TestContractSubmitTrxAndGetTrxReceiptWaitBad:
    """Test cases for get_trx_receipt_wait() that do not wait properly"""
    def test_submit_trx_and_get_trx_receipt_wait_with_short_timeout(
            self,
            connect_to_test_contract
            ):
        """Test using a timeout less than mining delay with one poll."""
        c = connect_to_test_contract
        trx_hash = c.submit_trx(
            constants.TRX_SENDER,
            constants.TRX_NAME,
            constants.TRX_ARG0,
            constants.TRX_ARG1,
            constants.TRX_ARG2
            )
        receipt = c.get_trx_receipt_wait(
            trx_hash,
            timeout=MINING_DELAY-3,  # Using 1 or 2 sometimes gets mined in time
            poll_latency=1
            )
        assert receipt is None

    def test_submit_trx_and_get_trx_receipt_wait_with_one_short_poll(
            self,
            connect_to_test_contract
            ):
        """Test using a timeout more than mining delay but poll less than delay."""
        c = connect_to_test_contract
        trx_hash = c.submit_trx(
            constants.TRX_SENDER,
            constants.TRX_NAME,
            constants.TRX_ARG0,
            constants.TRX_ARG1,
            constants.TRX_ARG2
            )
        receipt = c.get_trx_receipt_wait(
            trx_hash,
            timeout=MINING_DELAY+1,
            poll_latency=MINING_DELAY-1.5  # MINING_DELAY-1 sometimes works
            )
        assert receipt is None

    def test_submit_trx_and_get_trx_receipt_wait_timeout_shorter_than_poll(
            self,
            connect_to_test_contract
            ):
        """Test using a timeout that expires before first poll."""
        c = connect_to_test_contract
        trx_hash = c.submit_trx(
            constants.TRX_SENDER,
            constants.TRX_NAME,
            constants.TRX_ARG0,
            constants.TRX_ARG1,
            constants.TRX_ARG2
            )
        receipt = c.get_trx_receipt_wait(
            trx_hash,
            timeout=MINING_DELAY-2,
            poll_latency=MINING_DELAY
            )
        assert receipt is None
