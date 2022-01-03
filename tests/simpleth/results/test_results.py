"""Test Results() class properties"""
# I'm not testing the constructor. Not sure if/where to have those test cases.
import pytest
import re

import simpleth
import testconstants as constants


@pytest.mark.usefixtures('results_from_test_trx')
class TestResultsProperties:
    """Test properties in the Results object returned from running the test trx"""

    def test_block_number(self, results_from_test_trx):
        """Test result block_number is an integer"""
        assert isinstance(results_from_test_trx.block_number, int)

    def test_time_epoch(self, results_from_test_trx):
        """Test result block_time_epoch is an integer"""
        assert isinstance(results_from_test_trx.block_time_epoch, int)

    def test_contract(self, results_from_test_trx):
        """Test result contract_address is a string"""
        assert isinstance(
            results_from_test_trx.contract,
            simpleth.Contract
            )

    def test_contract_address(self, results_from_test_trx):
        """Test result contract_address is a string"""
        assert isinstance(results_from_test_trx.contract_address, str)

    def test_contract_name(self, results_from_test_trx):
        """Test result contract_name is CONTRACT_NAME"""
        assert results_from_test_trx.contract_name == constants.CONTRACT_NAME

    def test_event_args(self, results_from_test_trx):
        """Test result event_args has one of the expected args"""
        assert results_from_test_trx.event_args[0][constants.EVENT_ARG_KEY1] == \
               constants.TRX_ARG0

    def test_event_log(self, results_from_test_trx):
        """Test result event_log first event has the expected event name"""
        assert results_from_test_trx.event_logs[0]['event'] == \
               constants.EVENT_NAME

    def test_event_name(self, results_from_test_trx):
        """Test result event_name is the expected event name"""
        assert results_from_test_trx.event_names[0] == constants.EVENT_NAME

    def test_gas_price_wei(self, results_from_test_trx):
        """Test result gas_price_wei is an integer"""
        assert isinstance(results_from_test_trx.gas_price_wei, int)

    def test_gas_used(self, results_from_test_trx):
        """Test result gas_used is an integer"""
        assert isinstance(results_from_test_trx.gas_used, int)

    def test_trx_hash(self, results_from_test_trx):
        """Test result trx_hash has expected number of chars"""
        assert len(results_from_test_trx.trx_hash) == constants.HASH_SZ

    def test_trx_args(self, results_from_test_trx):
        """Test result trx_args has the expected arg0 """
        assert results_from_test_trx.trx_args[constants.TRX_ARG_KEY1] == \
               constants.TRX_ARG0

    def test_trx_name(self, results_from_test_trx):
        """Test result trx_name is TRX_NAME"""
        assert results_from_test_trx.trx_name == constants.TRX_NAME

    def test_trx_sender(self, results_from_test_trx):
        """Test result trx_sender is TRX_NAME"""
        assert results_from_test_trx.trx_sender == constants.TRX_SENDER

    def test_trx_value_wei(self, results_from_test_trx):
        """Test result trx_value_wei is TRX_VALUE"""
        assert results_from_test_trx.trx_value_wei == constants.TRX_VALUE

    def test_transaction(self, results_from_test_trx):
        """Test result transaction has hash of the correct length"""
        assert(len(results_from_test_trx.transaction['hash']) == constants.HASH_SZ)


@pytest.mark.usefixtures('results_from_test_trx')
class TestResultsPrint:
    """Test printed output of results from running the test trx."""
    
    def test_block_number_print(self, results_from_test_trx, capsys):
        """Test block_number is printed with correct title and value"""
        results = results_from_test_trx
        print(results)
        printed_results = capsys.readouterr()
        expected_substring = f'Block number.*=.*{results.block_number}'
        expected_pattern = re.compile(expected_substring)
        assert(
            re.search(
                expected_pattern,
                printed_results.out
                )
            )
        
    def test_time_epoch_print(self, results_from_test_trx, capsys):
        """Test block_time_epoch is printed with correct title and value"""
        results = results_from_test_trx
        print(results)
        printed_results = capsys.readouterr()
        expected_substring = f'Block time epoch.*=.*{results.block_time_epoch}'
        expected_pattern = re.compile(expected_substring)
        assert(
            re.search(
                expected_pattern,
                printed_results.out
                )
            )

    def test_contract_address_print(self, results_from_test_trx, capsys):
        """Test contract_address is printed with correct title and value"""
        results = results_from_test_trx
        print(results)
        printed_results = capsys.readouterr()
        expected_substring = f'Contract address.*=.*{results.contract_address}'
        expected_pattern = re.compile(expected_substring)
        assert(
            re.search(
                expected_pattern,
                printed_results.out
                )
            )

    def test_contract_name_print(self, results_from_test_trx, capsys):
        """Test contract_name is printed with correct title and value"""
        results = results_from_test_trx
        print(results)
        printed_results = capsys.readouterr()
        expected_substring = f'Contract name.*=.*{results.contract_name}'
        expected_pattern = re.compile(expected_substring)
        assert(
            re.search(
                expected_pattern,
                printed_results.out
                )
            )

    def test_event_args_print(self, results_from_test_trx, capsys):
        """Test one event_arg is printed with correct title and value.
        Note, 'timestamp' key is hard-coded here."""
        results = results_from_test_trx
        print(results)
        printed_results = capsys.readouterr()
        expected_substring = f'Event args.*=.*{results.event_args[0]["timestamp"]}'
        expected_pattern = re.compile(expected_substring)
        assert(
            re.search(
                expected_pattern,
                printed_results.out
                )
            )

    def test_event_name_print(self, results_from_test_trx, capsys):
        """Test event_name is printed with correct title and value"""
        results = results_from_test_trx
        print(results)
        printed_results = capsys.readouterr()
        expected_substring = f'Event name.*=.*{results.event_names[0]}'
        expected_pattern = re.compile(expected_substring)
        assert(
            re.search(
                expected_pattern,
                printed_results.out
                )
            )

    def test_gas_price_wei_print(self, results_from_test_trx, capsys):
        """Test gas_price_wei is printed with correct title and value"""
        results = results_from_test_trx
        print(results)
        printed_results = capsys.readouterr()
        expected_substring = f'Gas price wei.*=.*{results.gas_price_wei}'
        expected_pattern = re.compile(expected_substring)
        assert(
            re.search(
                expected_pattern,
                printed_results.out
                )
            )

    def test_gas_used_print(self, results_from_test_trx, capsys):
        """Test gas_used is printed with correct title and value"""
        results = results_from_test_trx
        print(results)
        printed_results = capsys.readouterr()
        expected_substring = f'Gas used.*=.*{results.gas_used}'
        expected_pattern = re.compile(expected_substring)
        assert(
            re.search(
                expected_pattern,
                printed_results.out
                )
            )

    def test_trx_hash_print(self, results_from_test_trx, capsys):
        """Test trx_hash is printed with correct title and value"""
        results = results_from_test_trx
        print(results)
        printed_results = capsys.readouterr()
        expected_substring = f'Trx hash.*=.*{results.trx_hash}'
        expected_pattern = re.compile(expected_substring)
        assert(
            re.search(
                expected_pattern,
                printed_results.out
                )
            )

    def test_trx_args_print(self, results_from_test_trx, capsys):
        """Test one trx_arg is printed with correct title and value.
        Note: arg0 name is hard-coded here."""
        results = results_from_test_trx
        print(results)
        printed_results = capsys.readouterr()
        expected_substring = f'Trx args.*=.*{results.trx_args["_num0"]}'
        expected_pattern = re.compile(expected_substring)
        assert(
            re.search(
                expected_pattern,
                printed_results.out
                )
            )

    def test_trx_name_print(self, results_from_test_trx, capsys):
        """Test trx_name is printed with correct title and value"""
        results = results_from_test_trx
        print(results)
        printed_results = capsys.readouterr()
        expected_substring = f'Trx name.*=.*{results.trx_name}'
        expected_pattern = re.compile(expected_substring)
        assert(
            re.search(
                expected_pattern,
                printed_results.out
                )
            )

    def test_trx_sender_print(self, results_from_test_trx, capsys):
        """Test trx_sender is printed with correct title and value"""
        results = results_from_test_trx
        print(results)
        printed_results = capsys.readouterr()
        expected_substring = f'Trx sender.*=.*{results.trx_sender}'
        expected_pattern = re.compile(expected_substring)
        assert(
            re.search(
                expected_pattern,
                printed_results.out
                )
            )

    def test_trx_value_wei_print(self, results_from_test_trx, capsys):
        """Test result trx_value_wei is TRX_VALUE"""
        """Test trx_value_wei is printed with correct title and value"""
        results = results_from_test_trx
        print(results)
        printed_results = capsys.readouterr()
        expected_substring = f'Trx value wei.*=.*{results.trx_value_wei}'
        expected_pattern = re.compile(expected_substring)
        assert(
            re.search(
                expected_pattern,
                printed_results.out
                )
            )

    def test_transaction_print(self, results_from_test_trx, capsys):
        """Test result transaction has hash of the correct length"""
        """Test trx_hash is printed with correct title and value"""
        results = results_from_test_trx
        print(results)
        printed_results = capsys.readouterr()
        expected_substring = f'Trx hash.*=.*{results.trx_hash}'
        expected_pattern = re.compile(expected_substring)
        assert(
            re.search(
                expected_pattern,
                printed_results.out
                )
            )


@pytest.mark.usefixtures('results_from_test_trx')
class TestResultsWeb3Attributes:
    """Test `web3` attributes are included in results after running the test trx."""

    def test_web3_contract_object(self, results_from_test_trx):
        """Test web3_contract_object is a class"""
        assert isinstance(results_from_test_trx.web3_contract_object, object)

    def test_web3_contract_event_logs(self, results_from_test_trx):
        """Test web3_contract_event_logs exists"""
        assert results_from_test_trx.web3_event_logs

    def test_web3_function_object(self, results_from_test_trx):
        """Test web3_function_object is a class"""
        assert isinstance(results_from_test_trx.web3_function_object, object)

    def test_web3_receipt(self, results_from_test_trx):
        """Test web3_receipt exists"""
        assert results_from_test_trx.web3_receipt

    def test_web3_transaction(self, results_from_test_trx):
        """Test web3_transaction exists"""
        assert results_from_test_trx.web3_transaction
