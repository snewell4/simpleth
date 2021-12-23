"""Test Blockchain() properties"""
from simpleth import Blockchain


def test_accounts():
    """Ganache should return 10 valid addresses"""
    # Default Ganache settings provides 10 accounts. This number
    # can be altered with a setting. If altered, this test will fail.
    accounts = Blockchain().accounts
    default_num_accounts = 10
    assert(all([Blockchain().is_valid_address(a) for a in accounts]) and
           len(accounts) == default_num_accounts)


def test_api_version():
    """api_version should return a string"""
    assert(isinstance(Blockchain().api_version, str))


def test_block_number():
    """block_number should return an integer"""
    assert(isinstance(Blockchain().block_number, int))


def test_client_version():
    """client_version should return a string"""
    assert(isinstance(Blockchain().client_version, str))


def test_eth():
    """web3.eth object should be valid if its block number matches
    Blockchain()'s"""
    assert(Blockchain().eth.block_number == Blockchain().block_number)


def test_web3():
    """web3 object should be valid if its client version matches
    Blockchain()'s"""
    assert(Blockchain().web3.clientVersion == Blockchain().client_version)
