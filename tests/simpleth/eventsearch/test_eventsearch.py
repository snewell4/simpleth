"""Test EventSearch() class"""
import pytest

from simpleth import EventSearch, SimplEthError, Contract, Blockchain


class TestEventSearchConstructorGood:
    """Test case for EventSearch() constructor with good arg."""

    def test_constructor_with_good_contract_object(self):
        """Instantiate EventSearch() object with valid constructor arg"""
        u = Blockchain().address(0)
        c = Contract('Test')
        c.deploy(u, 42)
        assert EventSearch(c, 'NumsStored')


class TestEventSearchConstructorBad:
    """Test case for EventSearch() constructor with bad event name"""

    def test_constructor_with_bad_event_name(self):
        """Create EventSearch with bad event name"""
        c = Contract('Test')
        c.connect()
        with pytest.raises(SimplEthError) as excp:
            EventSearch(c, 'bogus')
        assert excp.value.code == 'E-010-010'


class TestEventSearchMethodsGood:
    def test_event_name(self):
        """Check event name is set correctly"""
        u = Blockchain().address(0)
        c = Contract('Test')
        c.deploy(u, 42)
        event_name = 'NumsStored'
        e = EventSearch(c, event_name)
        assert e.event_name == event_name


class TestEventSearchGetOldGood:
    """Test cases for EventSearch().get_old() with good test cases"""

    def test_get_old_with_none_and_negative_args(self):
        """Run three store_num() trxs. Verify get_old() with negative args"""
        c = Contract('Test')
        c.connect()
        u = Blockchain().address(0)
        e = EventSearch(c, 'NumsStored')
        c.run_trx(u, 'storeNums', 1, 1, 1)
        c.run_trx(u, 'storeNums', 2, 2, 2)
        c.run_trx(u, 'storeNums', 3, 3, 3)
        e1 = len(e.get_old())
        e2 = len(e.get_old(-2))
        e3 = len(e.get_old(-3))
        assert e1 == 1 and e2 == 2 and e3 == 3

    def test_get_old_one_arg(self):
        """Run three store_num() trxs. Verify get_old() with single arg"""
        c = Contract('Test')
        c.connect()
        u = Blockchain().address(0)
        e = EventSearch(c, 'NumsStored')
        c.run_trx(u, 'storeNums', 1, 1, 1)
        c.run_trx(u, 'storeNums', 2, 2, 2)
        c.run_trx(u, 'storeNums', 3, 3, 3)
        n = Blockchain().block_number
        e1 = len(e.get_old(n))
        e2 = len(e.get_old(n-1))
        e3 = len(e.get_old(n-2))
        assert e1 == 1 and e2 == 2 and e3 == 3

    def test_get_old_range(self):
        """Run three store_num() trxs. Verify get_old() with range args"""
        c = Contract('Test')
        c.connect()
        u = Blockchain().address(0)
        e = EventSearch(c, 'NumsStored')
        c.run_trx(u, 'storeNums', 1, 1, 1)
        c.run_trx(u, 'storeNums', 2, 2, 2)
        c.run_trx(u, 'storeNums', 3, 3, 3)
        n = Blockchain().block_number
        e1 = len(e.get_old(n, n))
        e2 = len(e.get_old(n-1, n))
        e3 = len(e.get_old(n-2, n))
        assert e1 == 1 and e2 == 2 and e3 == 3


class TestEventSearchGetOldBad:
    """Test cases for EventSearch().get_old() with bad test cases"""

    def test_get_old_bad_from_type(self):
        """Test get_old() with string for from"""
        c = Contract('Test')
        c.connect()
        e = EventSearch(c, 'NumsStored')
        with pytest.raises(SimplEthError) as excp:
            e.get_old('bogus', 100)
        assert excp.value.code == 'E-030-010'

    def test_get_old_bad_to_type(self):
        """Test get_old() with string for to"""
        c = Contract('Test')
        c.connect()
        e = EventSearch(c, 'NumsStored')
        with pytest.raises(SimplEthError) as excp:
            e.get_old(100, 'bogus')
        assert excp.value.code == 'E-030-020'

    def test_get_old_bad_relative_search(self):
        """Test get_old() relative search with bad to block"""
        c = Contract('Test')
        c.connect()
        e = EventSearch(c, 'NumsStored')
        with pytest.raises(SimplEthError) as excp:
            e.get_old(-2, 20)
        assert excp.value.code == 'E-030-030'

    def test_get_old_oob_from(self):
        """Test get_old() with from beyond start of change (out of bounds)"""
        c = Contract('Test')
        c.connect()
        e = EventSearch(c, 'NumsStored')
        with pytest.raises(SimplEthError) as excp:
            e.get_old(-(Blockchain().block_number + 1))
        assert excp.value.code == 'E-030-040'

    def test_get_old_bad_range(self):
        """Test get_old() relative search with from greater than to"""
        c = Contract('Test')
        c.connect()
        e = EventSearch(c, 'NumsStored')
        with pytest.raises(SimplEthError) as excp:
            e.get_old(30, 20)
        assert excp.value.code == 'E-030-050'

    def test_get_old_bad_from(self):
        """Test get_old() with from greater than last block on chain"""
        c = Contract('Test')
        c.connect()
        e = EventSearch(c, 'NumsStored')
        n = Blockchain().block_number
        with pytest.raises(SimplEthError) as excp:
            e.get_old(n+1, n+2)
        assert excp.value.code == 'E-030-060'

    def test_get_old_bad_to(self):
        """Test get_old() with to greater than last block on chain"""
        c = Contract('Test')
        c.connect()
        e = EventSearch(c, 'NumsStored')
        n = Blockchain().block_number
        with pytest.raises(SimplEthError) as excp:
            e.get_old(n-1, n+2)
        assert excp.value.code == 'E-030-070'


class TestEventSearchGetNewGood:
    """Test cases for EventSearch().get_new() with good test cases"""

    def test_get_new_with_zero_one_two_good_events(self):
        """Test get_new() of zero, one, and two events"""
        c = Contract('Test')
        c.connect()
        u = Blockchain().address(0)
        e = EventSearch(c, 'NumsStored')
        e0 = len(e.get_new())
        c.run_trx(u, 'storeNums', 1, 1, 1)
        e1 = len(e.get_new())
        c.run_trx(u, 'storeNums', 2, 2, 2)
        c.run_trx(u, 'storeNums', 3, 3, 3)
        e2 = len(e.get_new())
        assert e0 == 0 and e1 == 1 and e2 == 2
