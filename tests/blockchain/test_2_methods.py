"""Test Blockchain() methods"""
import pytest
import re
from simpleth import Blockchain, SimplEthError


def test_address():
    """address() returns a valid address for an account number"""
    # check this first. It is used in subsequent tests.
    addr4 = Blockchain().address(4)
    assert(Blockchain().is_valid_address(addr4))


@pytest.mark.parametrize('bad_acct_num',
                         [-1, len(Blockchain().accounts), 'xxx']
                         )
def test_address_raises_b_020_010(bad_acct_num):
    """address() with bad account_num raises SimplEthError"""
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


def test_block_time_epoch():
    """block_time_epoch() returns an integer for epoch seconds"""
    # Use last block in chain
    block_num = Blockchain().block_number
    assert(isinstance(Blockchain().block_time_epoch(block_num), int))


@pytest.mark.parametrize('bad_block_num',
                         [-1, Blockchain().block_number + 1, 'xxx']
                         )
def test_block_time_epoch_raises_b_040_010(bad_block_num):
    """block_time_epoch() with bad block_num type raises SimplEthError"""
    with pytest.raises(SimplEthError) as excp:
        Blockchain().block_time_epoch(bad_block_num)
    assert excp.value.code == 'B-040-010'


def test_block_time_string_default_format():
    """block_time_string() returns the default formatted time string"""
    # Use last block in chain
    block_num = Blockchain().block_number
    # Assumes default time_format is YYYY-MM-DD HH:MM:SS
    default_time_format = \
        "[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}"
    assert(
        re.match(
            default_time_format,
            Blockchain().block_time_string(block_num)
            )
        )


def test_block_time_string_with_time_format():
    """block_time_string() returns a specified formatted time string"""
    # Use last block in chain
    block_num = Blockchain().block_number
    # Get simple format, HH:MM
    time_format = "[0-9]{2}:[0-9]{2}"
    assert(
        re.match(
            time_format,
            Blockchain().block_time_string(block_num, '%I:%M')
            )
        )


@pytest.mark.parametrize('bad_block_num',
                         [-1, Blockchain().block_number + 1, 'xxx']
                         )
def test_block_time_epoch_raises_b_040_010(bad_block_num):
    """block_time_string() with bad block_num type raises SimplEthError"""
    with pytest.raises(SimplEthError) as excp:
        Blockchain().block_time_string(bad_block_num)
    assert excp.value.code == 'B-040-010'


def test_block_time_string_raises_b_050_010():
    """block_time_string() with bad block_format type raises SimplEthError"""
    # Use last block in chain
    block_num = Blockchain().block_number
    bad_block_format_type = 100
    with pytest.raises(SimplEthError) as excp:
        Blockchain().block_time_string(
            block_num,
            bad_block_format_type
            )
    assert excp.value.code == 'B-050-010'


def fee_history_placeholder():
    """Placeholder for fee_history() test cases"""
    # Ganache has yet to implement the w3.eth_fee_history()
    # method. If and when it is implemented, put in the set of
    # test cases here.  For now, just return a Pass.
    assert True


def test_is_valid_address():
    """is_valid_address() returns true for a valid address"""
    addr3 = Blockchain().address(3)
    assert(isinstance(Blockchain().balance(addr3), int))


@pytest.mark.parametrize('bad_address',
                         ['0xF0E9C98500f34BE7C7c4a99700e4c56C0D9d6e6',
                          'xxx', 123]
                        )
def test_is_valid_address_returns_false(bad_address):
    """address() with bad account_num raises SimplEthError"""
    assert Blockchain().is_valid_address(bad_address) is False
