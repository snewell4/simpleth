"""Test Result() properties"""
# I'm not testing the constructor. Not sure if/where to have those test cases.
import pytest

from simpleth import Blockchain

#
# Test case constants.
# Used to confirm expected values for various properties.
# Must match contract and transaction values setup with fixtures.
#
CONTRACT_NAME = 'Test'
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
HASH_SZ = 66  # number chars in a blockchain hash


@pytest.fixture(scope='class')
def result_from_store_nums(test_contract):
    """Return simpleth Result object with outcomes from running store_nums()"""
    return test_contract.run_trx(
        TRX_SENDER,
        TRX_NAME,
        TRX_ARG0,
        TRX_ARG1,
        TRX_ARG2,
        event_name=EVENT_NAME
        )


@pytest.mark.usefixtures('result_from_store_nums')
class TestResultProperties:
    """Test properties in the Result object returned from running a
    storeNums() transaction in Test contract"""

    def test_block_number(self, result_from_store_nums):
        """Test result block_number is an integer"""
        assert isinstance(result_from_store_nums.block_number, int)

    def test_time_epoch(self, result_from_store_nums):
        """Test result block_time_epoch is an integer"""
        assert isinstance(result_from_store_nums.block_time_epoch, int)

    def test_contract_address(self, result_from_store_nums):
        """Test result contract_address is a string"""
        assert isinstance(result_from_store_nums.contract_address, str)

    def test_contract_name(self, result_from_store_nums):
        """Test result contract_name is CONTRACT_NAME"""
        assert result_from_store_nums.contract_name == CONTRACT_NAME

    def test_event_args(self, result_from_store_nums):
        """Test result event_args has one of the expected args"""
        assert result_from_store_nums.event_args[EVENT_ARG_KEY1] == \
            TRX_ARG0

    def test_event_log(self, result_from_store_nums):
        """Test result event_log first event has the expected event name"""
        assert result_from_store_nums.event_log[0]['event'] == \
            EVENT_NAME

    def test_event_name(self, result_from_store_nums):
        """Test result event_name is the expected event name"""
        assert result_from_store_nums.event_name == EVENT_NAME

    def test_gas_price_wei(self, result_from_store_nums):
        """Test result gas_price_wei is an integer"""
        assert isinstance(result_from_store_nums.gas_price_wei, int)

    def test_gas_used(self, result_from_store_nums):
        """Test result gas_used is an integer"""
        assert isinstance(result_from_store_nums.gas_used, int)

    def test_trx_hash(self, result_from_store_nums):
        """Test result trx_hash has expected number of chars"""
        assert len(result_from_store_nums.trx_hash) == HASH_SZ

    def test_trx_args(self, result_from_store_nums):
        """Test result trx_args has the expected arg0 """
        assert result_from_store_nums.trx_args[TRX_ARG_KEY1] == \
            TRX_ARG0

    def test_trx_name(self, result_from_store_nums):
        """Test result trx_name is TRX_NAME"""
        assert result_from_store_nums.trx_name == TRX_NAME

    def test_trx_sender(self, result_from_store_nums):
        """Test result trx_sender is TRX_NAME"""
        assert result_from_store_nums.trx_sender == TRX_SENDER

    def test_trx_value_wei(self, result_from_store_nums):
        """Test result trx_value_wei is TRX_VALUE"""
        assert result_from_store_nums.trx_value_wei == TRX_VALUE

    def test_transaction(self, result_from_store_nums):
        """Test result transaction has hash of the correct length"""
        assert(len(result_from_store_nums.transaction['hash']) == HASH_SZ)
