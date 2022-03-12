"""Test Results() class properties"""
# I'm not testing the constructor. Not sure if/where to have those test cases.
import pytest
import re

import simpleth
import testconstants as constants


@pytest.mark.usefixtures('run_test_trx_to_store_nums')
class TestResultsProperties:
    """Test properties in the Results object returned from running the test trx"""

    def test_block_number(self, run_test_trx_to_store_nums):
        """Test result block_number is an integer"""
        assert isinstance(run_test_trx_to_store_nums.block_number, int)

    def test_time_epoch(self, run_test_trx_to_store_nums):
        """Test result block_time_epoch is an integer"""
        assert isinstance(run_test_trx_to_store_nums.block_time_epoch, int)

    def test_contract(self, run_test_trx_to_store_nums):
        """Test result contract_address is a string"""
        assert isinstance(
            run_test_trx_to_store_nums.contract,
            simpleth.Contract
            )

    def test_contract_address(self, run_test_trx_to_store_nums):
        """Test result contract_address is a string"""
        assert isinstance(run_test_trx_to_store_nums.contract_address, str)

    def test_contract_name(self, run_test_trx_to_store_nums):
        """Test result contract_name is CONTRACT_NAME"""
        assert run_test_trx_to_store_nums.contract_name == constants.CONTRACT_NAME

    def test_event_args(self, run_test_trx_to_store_nums):
        """Test result event_args has one of the expected args"""
        assert run_test_trx_to_store_nums.event_args[0][constants.EVENT_ARG_KEY1] == \
               constants.TRX_ARG0

    def test_event_log(self, run_test_trx_to_store_nums):
        """Test result event_log first event has the expected event name"""
        assert run_test_trx_to_store_nums.event_logs[0]['event'] == \
               constants.EVENT_NAME

    def test_event_name(self, run_test_trx_to_store_nums):
        """Test result event_name is the expected event name"""
        assert run_test_trx_to_store_nums.event_names[0] == constants.EVENT_NAME

    def test_gas_price_wei(self, run_test_trx_to_store_nums):
        """Test result gas_price_wei is an integer"""
        assert isinstance(run_test_trx_to_store_nums.gas_price_wei, int)

    def test_gas_used(self, run_test_trx_to_store_nums):
        """Test result gas_used is an integer"""
        assert isinstance(run_test_trx_to_store_nums.gas_used, int)

    def test_trx_hash(self, run_test_trx_to_store_nums):
        """Test result trx_hash has expected number of chars"""
        assert len(run_test_trx_to_store_nums.trx_hash) == constants.HASH_SZ

    def test_trx_args(self, run_test_trx_to_store_nums):
        """Test result trx_args has the expected arg0 """
        assert run_test_trx_to_store_nums.trx_args[constants.TRX_ARG_KEY1] == \
               constants.TRX_ARG0

    def test_trx_name(self, run_test_trx_to_store_nums):
        """Test result trx_name is TRX_NAME"""
        assert run_test_trx_to_store_nums.trx_name == constants.TRX_NAME

    def test_trx_sender(self, run_test_trx_to_store_nums):
        """Test result trx_sender is TRX_NAME"""
        assert run_test_trx_to_store_nums.trx_sender == constants.TRX_SENDER

    def test_trx_value_wei(self, run_test_trx_to_store_nums):
        """Test result trx_value_wei is TRX_VALUE"""
        assert run_test_trx_to_store_nums.trx_value_wei == constants.TRX_VALUE

    def test_transaction(self, run_test_trx_to_store_nums):
        """Test result transaction has hash of the correct length"""
        assert(len(run_test_trx_to_store_nums.transaction['hash']) == constants.HASH_SZ)


@pytest.mark.usefixtures('run_test_trx_to_store_nums')
class TestResultsPrint:
    """Test printed output of results from running the test trx."""
    
    def test_block_number_print(self, run_test_trx_to_store_nums, capsys):
        """Test block_number is printed with correct title and value"""
        results = run_test_trx_to_store_nums
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
        
    def test_time_epoch_print(self, run_test_trx_to_store_nums, capsys):
        """Test block_time_epoch is printed with correct title and value"""
        results = run_test_trx_to_store_nums
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

    def test_contract_address_print(self, run_test_trx_to_store_nums, capsys):
        """Test contract_address is printed with correct title and value"""
        results = run_test_trx_to_store_nums
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

    def test_contract_name_print(self, run_test_trx_to_store_nums, capsys):
        """Test contract_name is printed with correct title and value"""
        results = run_test_trx_to_store_nums
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

    def test_event_args_print(self, run_test_trx_to_store_nums, capsys):
        """Test one event_arg is printed with correct title and value.
        Note, 'timestamp' key is hard-coded here."""
        results = run_test_trx_to_store_nums
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

    def test_event_name_print(self, run_test_trx_to_store_nums, capsys):
        """Test event_name is printed with correct title and value"""
        results = run_test_trx_to_store_nums
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

    def test_gas_price_wei_print(self, run_test_trx_to_store_nums, capsys):
        """Test gas_price_wei is printed with correct title and value"""
        results = run_test_trx_to_store_nums
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

    def test_gas_used_print(self, run_test_trx_to_store_nums, capsys):
        """Test gas_used is printed with correct title and value"""
        results = run_test_trx_to_store_nums
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

    def test_trx_hash_print(self, run_test_trx_to_store_nums, capsys):
        """Test trx_hash is printed with correct title and value"""
        results = run_test_trx_to_store_nums
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

    def test_trx_args_print(self, run_test_trx_to_store_nums, capsys):
        """Test one trx_arg is printed with correct title and value.
        Note: arg0 name is hard-coded here."""
        results = run_test_trx_to_store_nums
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

    def test_trx_name_print(self, run_test_trx_to_store_nums, capsys):
        """Test trx_name is printed with correct title and value"""
        results = run_test_trx_to_store_nums
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

    def test_trx_sender_print(self, run_test_trx_to_store_nums, capsys):
        """Test trx_sender is printed with correct title and value"""
        results = run_test_trx_to_store_nums
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

    def test_trx_value_wei_print(self, run_test_trx_to_store_nums, capsys):
        """Test result trx_value_wei is TRX_VALUE"""
        """Test trx_value_wei is printed with correct title and value"""
        results = run_test_trx_to_store_nums
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

    def test_transaction_print(self, run_test_trx_to_store_nums, capsys):
        """Test result transaction has hash of the correct length"""
        """Test trx_hash is printed with correct title and value"""
        results = run_test_trx_to_store_nums
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


@pytest.mark.usefixtures('run_test_trx_to_store_nums')
class TestResultsWeb3Attributes:
    """Test `web3` attributes are included in results after running the test trx."""

    def test_web3_contract_object(self, run_test_trx_to_store_nums):
        """Test web3_contract_object is a class"""
        assert isinstance(run_test_trx_to_store_nums.web3_contract_object, object)

    def test_web3_contract_event_logs(self, run_test_trx_to_store_nums):
        """Test web3_contract_event_logs exists"""
        assert run_test_trx_to_store_nums.web3_event_logs

    def test_web3_function_object(self, run_test_trx_to_store_nums):
        """Test web3_function_object is a class"""
        assert isinstance(run_test_trx_to_store_nums.web3_function_object, object)

    def test_web3_receipt(self, run_test_trx_to_store_nums):
        """Test web3_receipt exists"""
        assert run_test_trx_to_store_nums.web3_receipt

    def test_web3_transaction(self, run_test_trx_to_store_nums):
        """Test web3_transaction exists"""
        assert run_test_trx_to_store_nums.web3_transaction
