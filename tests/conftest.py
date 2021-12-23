"""conftest.py for simpleth class test cases"""
import pytest

from simpleth import Contract
import testconstants as constants


@pytest.fixture(scope='class')
def construct_test_contract():
    """Set up a simpleth contract object. Return contract object ready for either
    connect() or deploy()"""
    return Contract(constants.CONTRACT_NAME)


@pytest.fixture(scope='class')
def deploy_test_contract(construct_test_contract):
    """Deploy the test contract. Return contract_obj ready to be used for
    transactions."""
    contract_obj = construct_test_contract
    contract_obj.deploy(
        constants.CONSTRUCTOR_SENDER,
        constants.CONSTRUCTOR_ARG,
        constructor_event_name=constants.CONSTRUCTOR_EVENT_NAME
        )
    return contract_obj


@pytest.fixture(scope='class')
def connect_to_test_contract(construct_test_contract):
    """Connect to previously deployed contract. Return contract_obj ready to
    be used for transactions."""
    contract_obj = construct_test_contract
    contract_obj.connect()
    return contract_obj


@pytest.fixture(scope='class')
def result_from_test_trx(connect_to_test_contract):
    """Return simpleth Result object with outcomes from running store_nums()"""
    contract_obj = connect_to_test_contract
    return contract_obj.run_trx(
        constants.TRX_SENDER,
        constants.TRX_NAME,
        constants.TRX_ARG0,
        constants.TRX_ARG1,
        constants.TRX_ARG2,
        event_name=constants.EVENT_NAME
        )
