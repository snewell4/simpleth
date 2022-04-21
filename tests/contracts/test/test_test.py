"""Test the 'test' smart contract"""

import pytest

from simpleth import Blockchain, \
    Contract, \
    Results, \
    Filter, \
    Convert, \
    SimplEthError


def test_test_deploy():
    """Deploy test.sol and check for successful trx. """
    init_num = 42
    u = Blockchain().address(0)
    c = Contract('test')
    receipt = c.deploy(u, init_num)
    results = Results(receipt, c)
    assert results.trx_name == 'deploy'


def test_test_deploy_constructor():
    """Check constructor event was emitted."""
    init_num = 42    # from above test case doing deploy()
    u = Blockchain().address(0)     # ditto
    n = 1  # number of recent blocks to look for event
    c = Contract('test')
    c.connect()
    f = Filter(c)
    event = f.get_old_events('TestConstructed', n)
    assert event[0]['args']['initNum'] == init_num and \
        event[0]['args']['sender'] == u


def test_test_divideInitNum():
    """Test trx that divides the initNum."""
    divisor = 2
    u = Blockchain().address(0)
    c = Contract('test')
    c.connect()
    receipt = c.run_trx(u, 'divideInitNum', divisor)
    result = Results(receipt, c)
    assert result.trx_name == 'divideInitNum'


def test_test_divideInitNum_event():
    """Test trx that divides the initNum emitted expected values."""
    divisor = 2
    new_init_num = 42 / divisor
    n = 1  # number of recent blocks to look for event
    c = Contract('test')
    c.connect()
    f = Filter(c)
    event = f.get_old_events('InitNumDivided', n)
    assert event[0]['args']['result'] == new_init_num and \
        event[0]['args']['divisor'] == divisor


def test_test_setOwner():
    """Test trx that changes the owner of the contract."""
    current_owner = Blockchain().address(0)  # from deploy() test case
    new_owner = Blockchain().address(1)
    c = Contract('test')
    c.connect()
    receipt = c.run_trx(current_owner, 'setOwner', new_owner)
    result = Results(receipt, c)
    assert result.trx_name == 'setOwner'


def test_test_setOwner_event():
    """Test trx that set the owner emitted expected value."""
    new_owner = Blockchain().address(1)
    n = 1  # number of recent blocks to look for event
    c = Contract('test')
    c.connect()
    f = Filter(c)
    event = f.get_old_events('OwnerSet', n)
    assert event[0]['args']['newOwner'] == new_owner


def test_test_setOwner_with_bad_owner():
    """Test trx reverts if non-owner attempts to set a new owner"""
    bogus_owner = Blockchain().address(5)
    new_owner = Blockchain().address(1)
    c = Contract('test')
    c.connect()
    with pytest.raises(SimplEthError) as excp:
        c.run_trx(bogus_owner, 'setOwner', new_owner)
    assert excp.value.code == 'C-080-090'


def test_test_storeNum():
    """Test trx that stores one number into nums array."""
    new_num = 100
    nums_index = 0
    u = Blockchain().address(0)  # btw, this account is no longer owner
    c = Contract('test')
    c.connect()
    c.run_trx(u, 'storeNum', nums_index, new_num)
    assert c.get_var('nums', nums_index) == new_num


def test_test_storeNum_event():
    """Test trx that stored one number emitted expected values."""
    n = 1  # number of recent blocks to look for event
    new_num = 100     # must match test_storeNum() above
    nums_index = 0     # ditto
    c = Contract('test')
    c.connect()
    f = Filter(c)
    event = f.get_old_events('NumStored', n)
    assert event[0]['args']['index'] == nums_index and \
        event[0]['args']['num'] == new_num


def test_test_storeNums():
    """Test trx that stores new numbers into nums array."""
    new_nums = [1000, 2000, 3000]
    u = Blockchain().address(0)  # btw, this account is no longer owner
    c = Contract('test')
    c.connect()
    c.run_trx(u, 'storeNums', new_nums[0], new_nums[1], new_nums[2])
    assert c.call_fcn('getNums') == new_nums


def test_test_storeNums_event():
    """Test trx that stored new numbers emitted expected values."""
    n = 1  # number of recent blocks to look for event
    new_nums = [1000, 2000, 3000]  # must match test_storeNums() above
    c = Contract('test')
    c.connect()
    f = Filter(c)
    event = f.get_old_events('NumsStored', n)
    assert event[0]['args']['num0'] == new_nums[0] and \
        event[0]['args']['num1'] == new_nums[1] and \
        event[0]['args']['num2'] == new_nums[2]


def test_test_storeNumsAndPay():
    """Test trx that stores new numbers into nums array and payment is
    received."""

    # Easiest to just test contract balance. User balance also has
    # gas deducted.
    new_nums = [1001, 2001, 3001]
    payment_eth = 1
    payment_wei = int(
        Convert().convert_ether(payment_eth, 'ether', 'wei')
        )
    b = Blockchain()
    u = b.address(0)
    c = Contract('test')
    c.connect()
    init_contract_bal_wei = b.balance(c.address)
    c.run_trx(u,
              'storeNumsAndPay',
              new_nums[0],
              new_nums[1],
              new_nums[2],
              value_wei=payment_wei
              )
    end_contract_bal_wei = init_contract_bal_wei + payment_wei
    assert (c.call_fcn('getNums') == new_nums) and \
           end_contract_bal_wei == b.balance(c.address)


def test_test_storeNumsAndPay_event():
    """Test trx that stored new numbers emitted expected values."""
    n = 1  # number of recent blocks to look for event
    new_nums = [1001, 2001, 3001]  # must match test_storeNumsAndPay()
    payment_eth = 1   # ditto
    payment_wei = int(
        Convert().convert_ether(payment_eth, 'ether', 'wei')
        )
    b = Blockchain()
    c = Contract('test')
    c.connect()
    f = Filter(c)
    event = f.get_old_events('NumsStoredAndPaid', n)
    assert event[0]['args']['num0'] == new_nums[0] and \
        event[0]['args']['num1'] == new_nums[1] and \
        event[0]['args']['num2'] == new_nums[2] and \
        event[0]['args']['paid'] == payment_wei and \
        event[0]['args']['balance'] == b.balance(c.address)


def test_test_storeNumsAndSum():
    """Test trx that stores new numbers into nums array."""
    new_nums = [20, 30, 50]
    u = Blockchain().address(0)  # btw, this account is no longer owner
    c = Contract('test')
    c.connect()
    c.run_trx(u, 'storeNumsAndSum', new_nums[0], new_nums[1], new_nums[2])
    assert c.call_fcn('getNums') == new_nums


def test_test_storeNumsAndSum_NumsStored_event():
    """Test trx emitted its NumsStored event."""
    n = 1  # number of recent blocks to look for event
    new_nums = [20, 30, 50]  # must match test_storeNumsAndSum() above
    c = Contract('test')
    c.connect()
    f = Filter(c)
    event = f.get_old_events('NumsStored', n)
    assert event[0]['args']['num0'] == new_nums[0] and \
        event[0]['args']['num1'] == new_nums[1] and \
        event[0]['args']['num2'] == new_nums[2]


def test_test_storeNumsAndSum_NumsSummed_event():
    """Test trx call the sumNums() function and that fcn, in turn,
    emitted its NumsSummed event."""
    n = 1  # number of recent blocks to look for event
    new_nums = [20, 30, 50]  # must match test_storeNumsAndSum() above
    nums_total = sum(new_nums)
    c = Contract('test')
    c.connect()
    f = Filter(c)
    event = f.get_old_events('NumsSummed', n)
    assert event[0]['args']['num0'] == new_nums[0] and \
        event[0]['args']['num1'] == new_nums[1] and \
        event[0]['args']['num2'] == new_nums[2] and \
        event[0]['args']['total'] == nums_total


def test_test_storeNumsAndSum_NumsStoredAndSummed_event():
    """Test trx emitted its second event."""

    # This event only emits timestamp. Easiest to test if the
    # event was found and assume timestamp is OK.
    n = 1  # number of recent blocks to look for event
    c = Contract('test')
    c.connect()
    f = Filter(c)
    event = f.get_old_events('NumsStoredAndSummed', n)
    assert len(event) == 1


def test_test_storeNumsWithNoEvent():
    """Test trx that stores new numbers into nums array."""

    # This trx does not emit an event. This is the only test for this
    # trx.
    new_nums = [70, 80, 90]
    u = Blockchain().address(0)  # btw, this account is no longer owner
    c = Contract('test')
    c.connect()
    c.run_trx(u, 'storeNumsWithNoEvent', new_nums[0], new_nums[1], new_nums[2])
    assert c.call_fcn('getNums') == new_nums


def test_test_storeNumsWithThreeEvents():
    """Test trx that stores new numbers and emits multiple events"""
    new_nums = [200, 300, 500]
    u = Blockchain().address(0)  # btw, this account is no longer owner
    c = Contract('test')
    c.connect()
    c.run_trx(u,
              'storeNumsWithThreeEvents',
              new_nums[0],
              new_nums[1],
              new_nums[2]
              )
    assert c.call_fcn('getNums') == new_nums


def test_test_storeNumsWithThreeEvents_NumXStored_event():
    """Test trx emitted its NumsStored event."""
    n = 1  # number of recent blocks to look for event
    new_nums = [200, 300, 500]  # must match test_storeNumsWithThreeEvents()
    c = Contract('test')
    c.connect()
    f = Filter(c)
    event0 = f.get_old_events('Num0Stored', n)
    event1 = f.get_old_events('Num1Stored', n)
    event2 = f.get_old_events('Num2Stored', n)
    assert event0[0]['args']['num0'] == new_nums[0] and \
        event1[0]['args']['num1'] == new_nums[1] and \
        event2[0]['args']['num2'] == new_nums[2]


def test_test_typesStored():
    """Test trx that stores various data types as parameters"""
    test_uint = 42
    test_int = -42
    test_addr = Blockchain().address(4)
    test_str = 'Test String.'
    u = Blockchain().address(0)  # btw, this account is no longer owner
    c = Contract('test')
    c.connect()
    receipt = c.run_trx(u,
                        'storeTypes',
                        test_uint,
                        test_int,
                        test_addr,
                        test_str
                        )
    results = Results(receipt, c)
    assert results.trx_name == 'storeTypes'


def test_test_typesStored_storeTypes_event():
    """Test trx emitted its event."""
    n = 1  # number of recent blocks to look for event
    test_uint = 42   # must match test_typesStored() above
    test_int = -42    # ditto
    test_addr = Blockchain().address(4)   # ditto
    test_str = 'Test String.'   # ditto
    c = Contract('test')
    c.connect()
    f = Filter(c)
    event = f.get_old_events('TypesStored', n)
    assert event[0]['args']['test_uint'] == test_uint and \
        event[0]['args']['test_int'] == test_int and \
        event[0]['args']['test_addr'] == test_addr and \
        event[0]['args']['test_str'] == test_str


def test_test_getNum0():
    """Test fcn that returns nums[0]"""
    new_num0 = 123
    u = Blockchain().address(0)  # btw, this account is no longer owner
    c = Contract('test')
    c.connect()
    c.run_trx(u, 'storeNum', 0, new_num0)
    assert c.call_fcn('getNum0') == new_num0


def test_test_getNum():
    """Test fcn that returns selected nums[i]"""
    new_num = 321
    i = 2
    u = Blockchain().address(0)  # btw, this account is no longer owner
    c = Contract('test')
    c.connect()
    c.run_trx(u, 'storeNum', i, new_num)
    assert c.call_fcn('getNum', i) == new_num
