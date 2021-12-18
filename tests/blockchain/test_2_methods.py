"""Test Blockchain() methods"""
import pytest
from simpleth import Blockchain, SimplEthError


def test_address():
    """address() returns a valid address for an account number"""
    # check this first. It is used in subsequent tests.
    addr4 = Blockchain().address(4)
    assert(Blockchain().is_valid_address(addr4))


def test_address_raises_b_020_010():
    """address() with bad account_num raises SimplEthError"""
    bad_acct_num = 10
    with pytest.raises(SimplEthError) as excp:
        Blockchain().address(bad_acct_num)
    assert excp.value.code == 'B-020-010'


def test_account_num():
    """account_num() returns the correct account number for an address"""
    addr7 = Blockchain().address(7)
    assert(Blockchain().account_num(addr7) == 7)


def test_account_num_invalid_addr():
    """account_num() returns None for invalid account_address"""
    invalid_addr = '0xF0E9C98500f34BE7C7c4a99700e4c56C0D9d6e6'
    assert(Blockchain().account_num(invalid_addr) is None)


def test_account_num_invalid_type():
    """account_num() returns None for bad account_address type"""
    bad_type = 200
    assert(Blockchain().account_num(bad_type) is None)


def test_balance():
    """balance() returns an integer for an address"""
    addr3 = Blockchain().address(3)
    assert(isinstance(Blockchain().balance(addr3), int))


def test_balance_raises_b_030_010():
    """balance() with bad address type raises SimplEthError"""
    bad_addr_type = 200
    with pytest.raises(SimplEthError) as excp:
        Blockchain().balance(bad_addr_type)
    assert excp.value.code == 'B-030-010'


def test_balance_raises_b_030_020():
    """balance() with invalid address raises SimplEthError"""
    invalid_addr = '0xF0E9C98500f34BE7C7c4a99700e4c56C0D9d6e6'
    with pytest.raises(SimplEthError) as excp:
        Blockchain().balance(invalid_addr)
    assert excp.value.code == 'B-030-020'
