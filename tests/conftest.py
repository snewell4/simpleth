"""conftest.py for simpleth class test cases"""
import pytest

from simpleth import Blockchain, Contract


@pytest.fixture(scope='class')
def test_contract():
    """Return simpleth contract object for Test.sol freshly deployed by account[0]"""
    user0 = Blockchain().address(0)
    test_contract_obj = Contract('Test')
    test_contract_obj.deploy(user0, 10, constructor_event_name='TestConstructed')
    return test_contract_obj
