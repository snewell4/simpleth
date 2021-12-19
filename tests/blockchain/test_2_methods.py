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


def test_send_ether():
    """send_ether() transfers Ether from one account to another"""
    user6 = Blockchain().address(6)
    user7 = Blockchain().address(7)
    start_bal6 = Blockchain().balance(user6)
    start_bal7 = Blockchain().balance(user7)
    amount = 2_000_000_000  # wei
    Blockchain().send_ether(user6, user7, amount)
    end_bal6 = Blockchain().balance(user6)
    end_bal7 = Blockchain().balance(user7)
    # user6's end bal = start_bal6 - amount - cost of send_ether() trx
    # The amount and cost of gas is not computed here. Just check
    # that user6's end balance is less than
    assert (
        (end_bal6 < (start_bal6 - amount)) and
        (end_bal7 == (start_bal7 + amount))
        )


def test_send_ether_with_too_big_amount_raises_b_070_010():
    """send_ether() with amount > from balance raises SimplEthError"""
    user6 = Blockchain().address(6)
    user7 = Blockchain().address(7)
    amount = Blockchain().balance(user6) + 1
    with pytest.raises(SimplEthError) as excp:
        Blockchain().send_ether(user6, user7, amount)
    assert excp.value.code == 'B-070-010'


@pytest.mark.parametrize('invalid_address',
                         ['0xF0E9C98500f34BE7C7c4a99700e4c56C0D9d6e6', 'xxx']
                         )
def test_send_ether_with_invalid_from_raises_b_070_010(invalid_address):
    """send_ether() with bad address for from raises SimplEthError"""
    user6 = invalid_address
    user7 = Blockchain().address(7)
    amount = 2_000_000_000
    with pytest.raises(SimplEthError) as excp:
        Blockchain().send_ether(user6, user7, amount)
    assert excp.value.code == 'B-070-010'


@pytest.mark.parametrize('invalid_address',
                         ['0xF0E9C98500f34BE7C7c4a99700e4c56C0D9d6e6', 'xxx']
                         )
def test_send_ether_with_invalid_to_raises_b_070_010(invalid_address):
    """send_ether() with bad address for to raises SimplEthError"""
    user6 = Blockchain().address(6)
    user7 = invalid_address
    amount = 2_000_000_000
    with pytest.raises(SimplEthError) as excp:
        Blockchain().send_ether(user6, user7, amount)
    assert excp.value.code == 'B-070-010'


def test_send_ether_with_bad_type_to_raises_b_070_020():
    """send_ether() with bad address for to raises SimplEthError"""
    user6 = Blockchain().address(6)
    user7 = 123456
    amount = 2_000_000_000
    with pytest.raises(SimplEthError) as excp:
        Blockchain().send_ether(user6, user7, amount)
    assert excp.value.code == 'B-070-020'


def test_send_ether_with_bad_type_from_raises_b_070_020():
    """send_ether() with bad address for to raises SimplEthError"""
    user6 = 123456
    user7 = Blockchain().address(7)
    amount = 2_000_000_000
    with pytest.raises(SimplEthError) as excp:
        Blockchain().send_ether(user6, user7, amount)
    assert excp.value.code == 'B-070-020'


def test_send_ether_with_float_amount_raises_b_070_020():
    """send_ether() with a float amount raises SimplEthError"""
    user6 = Blockchain().address(6)
    user7 = Blockchain().address(7)
    amount = 2_000_000_000.00
    with pytest.raises(SimplEthError) as excp:
        Blockchain().send_ether(user6, user7, amount)
    assert excp.value.code == 'B-070-020'


def test_send_ether_raises_b_070_030_placeholder():
    """send_ether() to a non-payable account raises SimplEthError"""
    # This requires a non-payable contract to be deployed on chain.
    # Will run this test when testing Contract().
    # Just a placeholder to remind me to make sure an appropriate
    # test case is included in the future.
    assert True


@pytest.mark.parametrize('bad_address',
                         ['0xF0E9C98500f34BE7C7c4a99700e4c56C0D9d6e6',
                          'xxx', 123]
                         )
def test_send_ether_with_bad_from_raises_b_070_020(bad_address):
    """send_ethers() with bad address for from raises SimplEthError"""
    user6 = bad_address
    user7 = Blockchain().address(7)
    amount = 2_000_000_000.00
    with pytest.raises(SimplEthError) as excp:
        Blockchain().send_ether(user6, user7, amount)
    assert excp.value.code == 'B-070-020'


def test_transaction():
    """transaction() returns a string for the transaction result"""
    # Use the valid send_ether test to create a trx hash
    user6 = Blockchain().address(6)
    user7 = Blockchain().address(7)
    amount = 2_000_000_000  # wei
    trx_hash = Blockchain().send_ether(user6, user7, amount)
    assert Blockchain().transaction(trx_hash)['value'] == amount


@pytest.mark.parametrize('bad_hash',
                         ['0xF0E9C98500f34BE7C7c4a99700e4c56C0D9d6e6', 123]
                         )
def test_transaction_with_bad_hash_raises_b_080_010(bad_hash):
    """transaction() with bad trx_hash raises SimplEthError"""
    with pytest.raises(SimplEthError) as excp:
        Blockchain().transaction(bad_hash)
    assert excp.value.code == 'B-080-010'


def test_transaction_with_non_hex_hash_raises_b_080_020():
    """transaction() with trx_hash that is not a hex value raises SimplEthError"""
    non_hex_trx_hash = 'non_hex string'
    with pytest.raises(SimplEthError) as excp:
        Blockchain().transaction(non_hex_trx_hash)
    assert excp.value.code == 'B-080-020'


def test_trx_count():
    """trx_count() returns number of transactions"""
    # Use the valid send_ether test to create at least on trx for user6
    user6 = Blockchain().address(6)
    user7 = Blockchain().address(7)
    amount = 2_000_000_000  # wei
    Blockchain().send_ether(user6, user7, amount)
    num_trx = Blockchain().trx_count(user6)
    assert (isinstance(num_trx, int) and (num_trx > 0))


def test_trx_count_with_bad_address_type_raises_b_090_010():
    """trx_count() with bad address raises SimplEthError"""
    bad_address_type = 200
    with pytest.raises(SimplEthError) as excp:
        Blockchain().trx_count(bad_address_type)
    assert excp.value.code == 'B-090-010'


@pytest.mark.parametrize('bad_address',
                         ['0xF0E9C98500f34BE7C7c4a99700e4c56C0D9d6e6', 'xxx']
                         )
def test_trx_count_with_bad_address_raises_b_090_020(bad_address):
    """trx_count() with bad address raises SimplEthError"""
    with pytest.raises(SimplEthError) as excp:
        Blockchain().trx_count(bad_address)
    assert excp.value.code == 'B-090-020'


def test_trx_sender():
    """trx_sender() returns an account address"""
    # Use the valid send_ether test to create a trx hash
    user6 = Blockchain().address(6)
    user7 = Blockchain().address(7)
    amount = 2_000_000_000  # wei
    trx_hash = Blockchain().send_ether(user6, user7, amount)
    assert Blockchain().trx_sender(trx_hash) == user6


@pytest.mark.parametrize('bad_hash',
                         ['0xF0E9C98500f34BE7C7c4a99700e4c56C0D9d6e6', 123]
                         )
def test_trx_sender_with_bad_hash_raises_b_080_010(bad_hash):
    """trx_sender() with bad trx_hash raises SimplEthError"""
    with pytest.raises(SimplEthError) as excp:
        Blockchain().trx_sender(bad_hash)
    assert excp.value.code == 'B-080-010'


def test_trx_sender_with_non_hex_hash_raises_b_080_020():
    """trx_sender() with trx_hash that is not a hex value raises SimplEthError"""
    non_hex_trx_hash = 'non_hex string'
    with pytest.raises(SimplEthError) as excp:
        Blockchain().transaction(non_hex_trx_hash)
    assert excp.value.code == 'B-080-020'
    