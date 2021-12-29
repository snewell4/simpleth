"""Test Result() class properties"""
# I'm not testing the constructor. Not sure if/where to have those test cases.
import pytest

import simpleth
import testconstants as constants


@pytest.mark.usefixtures('result_from_test_trx')
class TestResultProperties:
    """Test properties in the Result object returned from running the test trx"""

    def test_block_number(self, result_from_test_trx):
        """Test result block_number is an integer"""
        assert isinstance(result_from_test_trx.block_number, int)

    def test_time_epoch(self, result_from_test_trx):
        """Test result block_time_epoch is an integer"""
        assert isinstance(result_from_test_trx.block_time_epoch, int)

    def test_contract(self, result_from_test_trx):
        """Test result contract_address is a string"""
        assert isinstance(
            result_from_test_trx.contract,
            simpleth.Contract
            )

    def test_contract_address(self, result_from_test_trx):
        """Test result contract_address is a string"""
        assert isinstance(result_from_test_trx.contract_address, str)

    def test_contract_name(self, result_from_test_trx):
        """Test result contract_name is CONTRACT_NAME"""
        assert result_from_test_trx.contract_name == constants.CONTRACT_NAME

    def test_event_args(self, result_from_test_trx):
        """Test result event_args has one of the expected args"""
        assert result_from_test_trx.event_args[0][constants.EVENT_ARG_KEY1] == \
            constants.TRX_ARG0

    def test_event_log(self, result_from_test_trx):
        """Test result event_log first event has the expected event name"""
        assert result_from_test_trx.event_logs[0]['event'] == \
            constants.EVENT_NAME

    def test_event_name(self, result_from_test_trx):
        """Test result event_name is the expected event name"""
        assert result_from_test_trx.event_names[0] == constants.EVENT_NAME

    def test_gas_price_wei(self, result_from_test_trx):
        """Test result gas_price_wei is an integer"""
        assert isinstance(result_from_test_trx.gas_price_wei, int)

    def test_gas_used(self, result_from_test_trx):
        """Test result gas_used is an integer"""
        assert isinstance(result_from_test_trx.gas_used, int)

    def test_trx_hash(self, result_from_test_trx):
        """Test result trx_hash has expected number of chars"""
        assert len(result_from_test_trx.trx_hash) == constants.HASH_SZ

    def test_trx_args(self, result_from_test_trx):
        """Test result trx_args has the expected arg0 """
        assert result_from_test_trx.trx_args[constants.TRX_ARG_KEY1] == \
            constants.TRX_ARG0

    def test_trx_name(self, result_from_test_trx):
        """Test result trx_name is TRX_NAME"""
        assert result_from_test_trx.trx_name == constants.TRX_NAME

    def test_trx_sender(self, result_from_test_trx):
        """Test result trx_sender is TRX_NAME"""
        assert result_from_test_trx.trx_sender == constants.TRX_SENDER

    def test_trx_value_wei(self, result_from_test_trx):
        """Test result trx_value_wei is TRX_VALUE"""
        assert result_from_test_trx.trx_value_wei == constants.TRX_VALUE

    def test_transaction(self, result_from_test_trx):
        """Test result transaction has hash of the correct length"""
        assert(len(result_from_test_trx.transaction['hash']) == constants.HASH_SZ)
