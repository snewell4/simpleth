"""Test Filter() class"""
import pytest

from simpleth import Filter, SimplEthError, Results, Contract
import testconstants as constants


@pytest.mark.usefixtures('construct_test_contract')
class TestFilterConstructorGood:
    """Test case for Filter() constructor with good arg."""

    def test_constructor_with_good_contract_object(
            self,
            construct_test_contract
            ):
        """Instantiate Filter() object with valid constructor arg"""
        c = construct_test_contract
        assert Filter(c)


@pytest.mark.usefixtures('construct_test_contract')
class TestFilterConstructorBad:
    """Test case for Filter() constructor with bad args."""

    def test_constructor_with_missing_contract_object(
            self,
            construct_test_contract
            ):
        """Missing constructor arg"""
        with pytest.raises(TypeError):
            Filter()

    def test_constructor_with_bogus_contract_object(
            self,
            construct_test_contract
            ):
        """Test bogus constructor arg"""
        with pytest.raises(AttributeError):
            Filter('bogus')


@pytest.mark.usefixtures('deploy_test_contract')
class TestFilterCreateFilterGood:
    """Test cases for Filter().create_filter() with good test cases"""

    def test_create_filter(self, deploy_test_contract):
        """Create filter for storeNums() trx."""
        c = deploy_test_contract
        f = Filter(c)
        store_nums_filter = f.create_filter(constants.EVENT_NAME)
        assert isinstance(store_nums_filter, object)


@pytest.mark.usefixtures('deploy_test_contract')
class TestFilterCreateFilterBad:
    """Test cases for Filter().create_filter() with bad args"""

    def test_create_filter_with_missing_arg(self, deploy_test_contract):
        """Missing event name"""
        c = deploy_test_contract
        f = Filter(c)
        with pytest.raises(TypeError):
            f.create_filter()

    def test_create_filter_with_bogus_arg(self, deploy_test_contract):
        """Wrong type of event name"""
        c = deploy_test_contract
        f = Filter(c)
        with pytest.raises(TypeError):
            f.create_filter(123)

    def test_create_filter_with_bad_event_name(self, deploy_test_contract):
        """Bogus event name"""
        c = deploy_test_contract
        f = Filter(c)
        with pytest.raises(SimplEthError) as excp:
            f.create_filter('bogus')
        assert excp.value.code == 'F-020-010'


@pytest.mark.usefixtures(
    'deploy_test_contract',
    'run_test_trx_to_store_nums',
    'run_test_trx_to_store_nums_again'
    )
class TestFilterGetOldEventsGood:
    """Test cases for Filter().get_old_events() with good test cases"""

    def test_get_old_events_two(
            self,
            deploy_test_contract,
            run_test_trx_to_store_nums,
            run_test_trx_to_store_nums_again
            ):
        """Run two store_num() trxs. Verify get two events by looking
        in the past two blocks."""
        c = deploy_test_contract
        f = Filter(c)
        run_test_trx_to_store_nums
        run_test_trx_to_store_nums_again
        events = f.get_old_events(constants.EVENT_NAME, 3)
        assert len(events) == 2

    def test_get_old_events_one(
            self,
            deploy_test_contract,
            run_test_trx_to_store_nums,
            run_test_trx_to_store_nums_again
            ):
        """Run two store_num() trxs. Verify get one event by looking
        in just the most recent block."""
        c = deploy_test_contract
        run_test_trx_to_store_nums
        run_test_trx_to_store_nums_again
        f = Filter(c)
        events = f.get_old_events(constants.EVENT_NAME, 1)
        assert len(events) == 1


@pytest.mark.usefixtures(
    'deploy_test_contract',
    'run_test_trx_to_store_nums',
    'run_test_trx_to_store_nums_again'
    )
class TestFilterGetOldEventsBad:
    """Test cases for Filter().get_old_events() with bad test cases"""

    def test_get_old_events_with_no_num_blocks(
            self,
            deploy_test_contract,
            run_test_trx_to_store_nums
            ):
        """Test without specifying the number of blocks"""
        c = deploy_test_contract
        f = Filter(c)
        run_test_trx_to_store_nums
        with pytest.raises(TypeError):
            f.get_old_events(constants.EVENT_NAME)

    def test_get_old_events_with_no_event_name(
            self,
            deploy_test_contract,
            run_test_trx_to_store_nums
            ):
        """Test without specifying the event name"""
        c = deploy_test_contract
        f = Filter(c)
        run_test_trx_to_store_nums
        with pytest.raises(TypeError):
            f.get_old_events(1)

    def test_get_old_events_with_no_args(
            self,
            deploy_test_contract,
            run_test_trx_to_store_nums
            ):
        """Test without specifying any args"""
        c = deploy_test_contract
        f = Filter(c)
        run_test_trx_to_store_nums
        with pytest.raises(TypeError):
            f.get_old_events()

    def test_get_old_events_with_bad_num_blocks_type(
            self,
            deploy_test_contract,
            run_test_trx_to_store_nums
            ):
        """Test a string as the num blocks"""
        c = deploy_test_contract
        run_test_trx_to_store_nums
        f = Filter(c)
        with pytest.raises(SimplEthError) as excp:
            f.get_old_events(constants.EVENT_NAME, 'abc')
        assert excp.value.code == 'F-030-010'

    def test_get_old_events_with_bad_num_blocks(
            self,
            deploy_test_contract,
            run_test_trx_to_store_nums
            ):
        """Test a negative block number"""
        c = deploy_test_contract
        run_test_trx_to_store_nums
        f = Filter(c)
        with pytest.raises(SimplEthError) as excp:
            f.get_old_events(constants.EVENT_NAME, -1)
        assert excp.value.code == 'F-030-020'

    def test_get_old_events_with_bad_event_name(
            self,
            deploy_test_contract,
            run_test_trx_to_store_nums
            ):
        """Test a bogus event name"""
        c = deploy_test_contract
        run_test_trx_to_store_nums
        f = Filter(c)
        with pytest.raises(SimplEthError) as excp:
            f.get_old_events('bogus', 1)
        assert excp.value.code == 'F-030-030'

    def test_get_old_events_with_bad_event_name_type(
            self,
            deploy_test_contract,
            run_test_trx_to_store_nums
            ):
        """Test an integer as the event name"""
        c = deploy_test_contract
        run_test_trx_to_store_nums
        f = Filter(c)
        with pytest.raises(SimplEthError) as excp:
            f.get_old_events(123, 1)
        assert excp.value.code == 'F-030-040'


@pytest.mark.usefixtures(
    'deploy_test_contract',
    'run_test_trx_to_store_nums',
    'run_test_trx_to_store_nums_again'
    )
class TestFilterGetNewEventsGood:
    """Test cases for Filter().get_new_events() with good test cases"""
    # 4/14/22 - I'm stumped. I can run this in Python interpreter. Just
    # don't know why I get 0 new events instead of 2. Giving it a rest for now.

    def test_get_new_events(
            self,
            deploy_test_contract,
            run_test_trx_to_store_nums,
            run_test_trx_to_store_nums_again
            ):
        """Create filter and run two trx. Should return 2 event"""
        c = deploy_test_contract
        c = Contract('test')
        c.connect()
        print(c)
        print()
        f = Filter(c)
        print(f)
        print()
        store_nums_filter = f.create_filter(constants.EVENT_NAME)
        print(constants.EVENT_NAME)
        print(store_nums_filter)
        print()
        r1=run_test_trx_to_store_nums
        print(r1)
        print()
        r2=run_test_trx_to_store_nums_again
        print(r2)
        print()
        events = f.get_new_events(store_nums_filter)
        print(events)
        assert len(events) == 2


@pytest.mark.usefixtures(
    'deploy_test_contract',
    'run_test_trx_to_store_nums',
    'run_test_trx_to_store_nums_again'
    )
class TestFilterGetNewEventsBad:
    """Test cases for Filter().get_new_events() with bad test cases"""

    def test_get_new_events_with_bad_filter_arg_type(
            self,
            deploy_test_contract,
            run_test_trx_to_store_nums
            ):
        """Create filter and run one trx. Should return 1 event"""
        c = deploy_test_contract
        f = Filter(c)
        f.create_filter(constants.EVENT_NAME)
        run_test_trx_to_store_nums
        with pytest.raises(AttributeError):
            f.get_new_events('bad')

    def test_get_new_events_with_missing_filter_arg(
            self,
            deploy_test_contract,
            run_test_trx_to_store_nums
            ):
        """Create filter and run one trx. Should return 1 event"""
        c = deploy_test_contract
        f = Filter(c)
        f.create_filter(constants.EVENT_NAME)
        run_test_trx_to_store_nums
        with pytest.raises(TypeError):
            f.get_new_events()