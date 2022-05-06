"""Test Contract() with no mining delay class"""
# Uses ganache with automining set to 'on'

import pytest

from simpleth import Blockchain, Contract, SimplEthError, Results
import testconstants as constants


class TestContractConstructorGood:
    """Test case for Contract() with good args"""

    def test_constructor_with_good_contract_name(self):
        """Instantiate Contract() object with valid constructor arg"""
        assert Contract(constants.CONTRACT_NAME)._name is constants.CONTRACT_NAME


class TestContractConstructorBad:
    """Test cases for Contract() with bad args"""

    def test_constructor_with_bad_contract_name_raises_C_100_010(self):
        """SimplEthError is raised when constructor has bad contract name"""
        bad_name = 'bad_contract_name'
        with pytest.raises(SimplEthError) as excp:
            Contract(bad_name)
        assert excp.value.code == 'C-100-010'

    # noinspection PyArgumentList
    def test_constructor_with_missing_contract_name_raises_type_error(self):
        """TypeError is raised when constructor has no contract name"""
        with pytest.raises(TypeError):
            Contract()


@pytest.mark.usefixtures('connect_to_test_contract')
class TestContractDeployGood:
    """Test cases for Contract().deploy() with good test cases"""

    def test_deploy_with_good_args(self, connect_to_test_contract):
        """deploy() returns results with correct transaction name"""
        c = Contract(constants.CONTRACT_NAME)
        receipt = c.deploy(constants.CONSTRUCTOR_SENDER, constants.CONSTRUCTOR_ARG)
        results = Results(c, receipt)
        assert results.trx_name == 'deploy'

    def test_deploy_with_good_args_plus_gas_limit(
            self,
            connect_to_test_contract
            ):
        """deploy() with typical set of args plus specifying a gas limit
        large enough for the trx returns result for deploy trx"""
        c = Contract(constants.CONTRACT_NAME)
        receipt = c.deploy(
            constants.CONSTRUCTOR_SENDER,
            constants.CONSTRUCTOR_ARG,
            gas_limit=constants.CONSTRUCTOR_GAS_LIMIT
            )
        results = Results(c, receipt)
        assert results.trx_name == 'deploy'

    def test_deploy_with_good_args_plus_gas_limit_and_fees(
            self,
            connect_to_test_contract
            ):
        """deploy() with typical set of args plus specifying a gas limit
        large enough for the trx plus reasonable values for fees returns
        result for deploy trx"""
        c = Contract(constants.CONTRACT_NAME)
        receipt = c.deploy(
            constants.CONSTRUCTOR_SENDER,
            constants.CONSTRUCTOR_ARG,
            gas_limit=constants.CONSTRUCTOR_GAS_LIMIT,
            max_priority_fee_gwei=constants.MAX_PRIORITY_FEE_GWEI,
            max_fee_gwei=constants.MAX_FEE_GWEI
            )
        results = Results(c, receipt)
        assert results.trx_name == 'deploy'


@pytest.mark.usefixtures(
    'construct_test_contract',
    'construct_never_deployed_test_contract'
    )
class TestContractDeployBad:
    """Test cases for Contract().deploy() with bad values"""

    # Not testing bad values for ``max_priority_fee_gwei`` and
    # ``max_fee_gwei``. Neither of these are not yet supported
    # by Ganache. Add tests later once Ganache has support
    # for them.

    def test_deploy_with_bad_sender_raises_C_030_020(
            self,
            construct_test_contract
            ):
        """"Attempt to deploy with bad sender raises C-030-020"""
        c = construct_test_contract
        bad_sender = '123'
        with pytest.raises(SimplEthError) as excp:
            c.deploy(bad_sender, constants.CONSTRUCTOR_ARG)
        assert excp.value.code == 'C-030-020'

    def test_deploy_with_wrong_type_constructor_arg_raises_C_030_030(
            self,
            construct_test_contract
            ):
        """"Attempt to deploy with bad constructor arg type raises
        C-030-030"""
        c = construct_test_contract
        bad_constructor_arg = '123'
        with pytest.raises(SimplEthError) as excp:
            c.deploy(constants.CONSTRUCTOR_SENDER, bad_constructor_arg)
        assert excp.value.code == 'C-030-030'

    def test_deploy_with_too_many_constructor_args_raises_C_030_030(
            self,
            construct_test_contract
            ):
        """"Attempt to deploy with too many constructor args raises
        C-030-030"""
        c = construct_test_contract
        extra_constructor_arg = 20
        with pytest.raises(SimplEthError) as excp:
            c.deploy(
                constants.CONSTRUCTOR_SENDER,
                constants.CONSTRUCTOR_ARG,
                extra_constructor_arg
                )
        assert excp.value.code == 'C-030-030'

    def test_deploy_with_missing_constructor_arg_raises_C_030_030(
            self,
            construct_test_contract
            ):
        """"Attempt to deploy with missing constructor arg raises
        C-030-030"""
        c = construct_test_contract
        with pytest.raises(SimplEthError) as excp:
            c.deploy(constants.CONSTRUCTOR_SENDER)
        assert excp.value.code == 'C-030-030'

    def test_deploy_with_insufficient_gas_raises_C_030_040(
            self,
            construct_test_contract
            ):
        """"Attempt to deploy with gas limit arg too small to
        run the trx raises C-030-030"""
        c = construct_test_contract
        insufficient_gas_limit = constants.GAS_LIMIT_MIN
        with pytest.raises(SimplEthError) as excp:
            c.deploy(
                constants.CONSTRUCTOR_SENDER,
                constants.CONSTRUCTOR_ARG,
                gas_limit=insufficient_gas_limit
                )
        assert excp.value.code == 'C-030-040'

    def test_deploy_with_excessive_gas_raises_C_030_040(
            self,
            construct_test_contract
            ):
        """"Attempt to deploy with missing constructor arg raises
        C-030-030"""
        c = construct_test_contract
        excessive_gas_limit = constants.GAS_LIMIT_MAX + 1
        with pytest.raises(SimplEthError) as excp:
            c.deploy(
                constants.CONSTRUCTOR_SENDER,
                constants.CONSTRUCTOR_ARG,
                gas_limit=excessive_gas_limit
                )
        assert excp.value.code == 'C-030-040'


@pytest.mark.usefixtures('construct_test_contract')
class TestContractConnectBad:
    """Test cases for Contract().connect() with bad values"""

    # The good test case has already been run in fixtures
    # and elsewhere. No test class TestContractConnectGood.

    def test_connect_without_args(self, construct_test_contract):
        """Test normal, expected use. Should pass."""
        c = construct_test_contract
        contract_address = c.connect()
        assert Blockchain().is_valid_address(contract_address)

    def test_connect_with_unexpected_arg_raises_type_error(
            self,
            construct_test_contract
            ):
        """Test bad use of putting in an arg. Should raise TypeError."""
        c = construct_test_contract
        unexpected_arg = 'bad_arg'
        with pytest.raises(TypeError):
            c.connect(unexpected_arg)


@pytest.mark.usefixtures('connect_to_test_contract')
class TestContractPropertiesGood:
    """Test cases for Contract() properties"""

    # There are no bad test cases. There are no args for
    # any of these properties.

    def test_address(self, connect_to_test_contract):
        """Test contract address is a valid address"""
        c = connect_to_test_contract
        assert Blockchain().is_valid_address(c.address)

    def test_blockchain(self, connect_to_test_contract):
        """Test blockchain is a Blockchain() object"""
        c = connect_to_test_contract
        assert isinstance(c.blockchain, Blockchain)

    def test_bytecode(self, connect_to_test_contract):
        """Test bytecode is a string"""
        c = connect_to_test_contract
        assert isinstance(c.bytecode, str)

    def test_deployed_code(self, connect_to_test_contract):
        """Test deployed_code is a string"""
        c = connect_to_test_contract
        assert isinstance(c.deployed_code, str)

    def test_events(self, connect_to_test_contract):
        """Test events is a list"""
        c = connect_to_test_contract
        assert isinstance(c.event_names, list)

    def test_functions(self, connect_to_test_contract):
        """Test functions is a list"""
        c = connect_to_test_contract
        assert isinstance(c.functions, list)

    def test_name(self, connect_to_test_contract):
        """Test name is the test contract name"""
        c = connect_to_test_contract
        assert c.name is constants.CONTRACT_NAME

    def test_size(self, connect_to_test_contract):
        """Test size is an integer"""
        c = connect_to_test_contract
        assert isinstance(c.size, int)

    def test_web3_contract(self, connect_to_test_contract):
        """Test web3_contract is an object"""
        c = connect_to_test_contract
        assert isinstance(c.web3_contract, object)

    def test_web3e(self, connect_to_test_contract):
        """Test web3e is an object"""
        c = connect_to_test_contract
        assert isinstance(c.web3e, object)


@pytest.mark.usefixtures('deploy_test_contract')
class TestCallFcnGood:
    """Test cases for Contract().call_fcn() with good values"""

    # Safest to deploy a new contract every time to insure we get the
    # expected initialization values.

    def test_call_fcn_getNum0(self, deploy_test_contract):
        """Test call_fcn with function that has no args and returns
        a single value"""
        c = deploy_test_contract
        assert c.call_fcn('getNum0') == constants.INIT_NUM0

    def test_call_fcn_getNums(self, deploy_test_contract):
        """Test call_fcn with function that returns a row from an
        array"""
        c = deploy_test_contract
        expected_nums = [
            constants.INIT_NUM0,
            constants.INIT_NUM1,
            constants.INIT_NUM2
            ]
        assert c.call_fcn('getNums') == expected_nums

    def test_call_fcn_getNum(self, deploy_test_contract):
        """Test call_fcn with function that has an arg"""
        c = deploy_test_contract
        assert c.call_fcn('getNum', 2) == constants.INIT_NUM2


@pytest.mark.usefixtures(
    'construct_never_deployed_test_contract',
    'connect_to_test_contract'
    )
class TestCallFcnBad:
    """Test cases for Contract().call_fcn() with bad values"""

    # OK to just do connect() instead of deploy(). These tests
    # all give bad args so doesn't matter that we have a fresh
    # contract.

    # I don't know how to create the error that causes the
    # exception with code of C-010-020.

    def test_call_fcn_with_no_fcn_name_raises_type_error(
            self,
            connect_to_test_contract
            ):
        """"Attempt to call_fcn with missing fcn_name fails"""
        c = connect_to_test_contract
        with pytest.raises(TypeError):
            c.call_fcn()

    def test_call_fcn_with_bad_fcn_name_raises_C_010_010(
            self,
            connect_to_test_contract
            ):
        """"Attempt to call_fcn with bad fcn_name raises C-010-010"""
        c = connect_to_test_contract
        bad_fcn_name = 'bad'
        with pytest.raises(SimplEthError) as excp:
            c.call_fcn(bad_fcn_name)
        assert excp.value.code == 'C-010-010'

    def test_call_fcn_with_unconnected_contract_raises_C_010_010(
            self,
            construct_never_deployed_test_contract
            ):
        """Test call_fcn() fails if connect() is needed."""
        c = construct_never_deployed_test_contract
        with pytest.raises(SimplEthError) as excp:
            c.call_fcn('getNum0')
        assert excp.value.code == 'C-010-010'

    def test_call_fcn_with_bad_arg_type_raises_C_010_020(
            self,
            connect_to_test_contract
            ):
        """"Attempt to call_fcn with bad arg type fails"""
        c = connect_to_test_contract
        bad_arg_type = 'bad'
        with pytest.raises(SimplEthError) as excp:
            c.call_fcn('getNum', bad_arg_type)
        assert excp.value.code == 'C-010-020'

    def test_call_fcn_with_wrong_num_args_raises_C_010_020(
            self,
            connect_to_test_contract
            ):
        """"Attempt to call_fcn with bad number of args fails"""
        c = connect_to_test_contract
        with pytest.raises(SimplEthError) as excp:
            c.call_fcn('getNum', 1, 2)
        assert excp.value.code == 'C-010-020'

    def test_call_fcn_with_out_of_bounds_arg_raises_C_010_040(
            self,
            connect_to_test_contract
            ):
        """"Attempt to call_fcn with an out of bounds arg fails"""
        c = connect_to_test_contract
        with pytest.raises(SimplEthError) as excp:
            c.call_fcn('getNum', 3)
        assert excp.value.code == 'C-010-040'


@pytest.mark.usefixtures('connect_to_test_contract')
class TestContractGetGasEstimateGood:
    """Test cases for Contract().get_gas_estimate() with good values"""

    def test_get_gas_estimate_with_good_args(
            self,
            connect_to_test_contract
            ):
        """Test normal, expected use. Should pass."""
        c = connect_to_test_contract
        gas_estimate = c.get_gas_estimate(
            constants.TRX_SENDER,
            constants.TRX_NAME,
            constants.TRX_ARG0,
            constants.TRX_ARG1,
            constants.TRX_ARG2
            )
        assert gas_estimate > constants.GAS_LIMIT_MIN


@pytest.mark.usefixtures(
    'connect_to_test_contract',
    'construct_never_deployed_test_contract'
    )
class TestContractGetGasEstimateBad:
    """Test cases for Contract().get_gas_estimate() with bad values"""

    def test_get_gas_estimate_with_no_args_raises_type_error(
            self,
            connect_to_test_contract
            ):
        """"Attempt to get_gas_estimate() with no args fails"""
        c = connect_to_test_contract
        with pytest.raises(TypeError):
            c.get_gas_estimate()

    def test_get_gas_estimate_with_bad_trx_name_raises_C_040_010(
            self,
            connect_to_test_contract
            ):
        """Test get_gas_estimate() with a bad trx name"""
        c = connect_to_test_contract
        bad_trx_name = 'bad_trx'
        with pytest.raises(SimplEthError) as excp:
            c.get_gas_estimate(
                constants.TRX_SENDER,
                bad_trx_name,
                constants.TRX_ARG0,
                constants.TRX_ARG1,
                constants.TRX_ARG2
                )
        assert excp.value.code == 'C-040-010'

    def test_get_gas_estimate_with_too_few_trx_args_raises_C_040_020(
            self,
            connect_to_test_contract
            ):
        """Test get_gas_estimate() with too few trx args"""
        c = connect_to_test_contract
        with pytest.raises(SimplEthError) as excp:
            c.get_gas_estimate(
                constants.TRX_SENDER,
                constants.TRX_NAME,
                constants.TRX_ARG0,
                constants.TRX_ARG1
                )
        assert excp.value.code == 'C-040-020'

    def test_get_gas_estimate_with_too_many_trx_args_raises_C_040_020(
            self,
            connect_to_test_contract
            ):
        """Test get_gas_estimate() with too many trx args"""
        c = connect_to_test_contract
        with pytest.raises(SimplEthError) as excp:
            c.get_gas_estimate(
                constants.TRX_SENDER,
                constants.TRX_NAME,
                constants.TRX_ARG0,
                constants.TRX_ARG1,
                constants.TRX_ARG2,
                constants.TRX_ARG2
                )
        assert excp.value.code == 'C-040-020'

    def test_get_gas_estimate_with_TBD_raises_C_040_030(
            self,
            connect_to_test_contract
            ):
        """Test get_gas_estimate() for a destroyed contract
        Don't know how to do this yet. Just do assert True
        for now. """
        assert True

    def test_get_gas_estimate_with_oob_arg_raises_C_040_040(
            self,
            connect_to_test_contract
            ):
        """Test get_gas_estimate() with out-of-bounds arg"""
        c = connect_to_test_contract
        with pytest.raises(SimplEthError) as excp:
            c.get_gas_estimate(
                constants.OOB_TRX_SENDER,
                constants.OOB_TRX_NAME,
                constants.OOB_TRX_ARG0,
                constants.OOB_TRX_ARG1
                )
        assert excp.value.code == 'C-040-040'

    def test_get_gas_estimate_with_db0_arg_raises_C_040_040(
            self,
            connect_to_test_contract
            ):
        """Test get_gas_estimate() with an arg that causes a
        divide-by-zero error"""
        c = connect_to_test_contract
        with pytest.raises(SimplEthError) as excp:
            c.get_gas_estimate(
                constants.DB0_TRX_SENDER,
                constants.DB0_TRX_NAME,
                constants.DB0_TRX_ARG0
                )
        assert excp.value.code == 'C-040-040'

    def test_get_gas_estimate_with_bad_sender_raises_C_040_050(
            self,
            connect_to_test_contract
            ):
        """Test get_gas_estimate() with a bad sender address"""
        c = connect_to_test_contract
        bad_sender = '123'
        with pytest.raises(SimplEthError) as excp:
            c.get_gas_estimate(
                bad_sender,
                constants.TRX_NAME,
                constants.TRX_ARG0,
                constants.TRX_ARG1,
                constants.TRX_ARG2
                )
        assert excp.value.code == 'C-040-050'

    def test_get_gas_estimate_using_never_deployed_contract_raises_C_040_060(
            self,
            construct_never_deployed_test_contract
            ):
        """Test get_gas_estimate() without doing a `connect()` first"""
        c = construct_never_deployed_test_contract
        with pytest.raises(SimplEthError) as excp:
            c.get_gas_estimate(
                constants.NEVER_DEPLOYED_TRX_SENDER,
                constants.NEVER_DEPLOYED_TRX_NAME
                )
        assert excp.value.code == 'C-040-060'

    def test_get_gas_estimate_with_missing_sender_raises_C_040_070(
            self,
            connect_to_test_contract
            ):
        """Test get_gas_estimate() with a missing sender arg"""
        c = connect_to_test_contract
        with pytest.raises(SimplEthError) as excp:
            c.get_gas_estimate(
                constants.TRX_NAME,
                constants.TRX_ARG0,
                constants.TRX_ARG1,
                constants.TRX_ARG2
                )
        assert excp.value.code == 'C-040-070'


@pytest.mark.usefixtures(
    'run_test_trx_to_store_array',
    'run_test_trx_to_store_all_types'
    )
class TestContractGetVarGood:
    # Move this after testing `run_trx()`. `get_var()`
    # test cases, good and bad, depend on running trx for
    # fixtures.
    """Test cases for Contract().get_var() with good values"""

    def test_get_var_for_int(
            self,
            run_test_trx_to_store_all_types
            ):
        """Test getting an int public state variable."""
        c = run_test_trx_to_store_all_types
        int_value = c.get_var(constants.INT_VAR_NAME)
        assert int_value == constants.INT_VAR_VALUE

    def test_get_var_for_uint(
            self,
            run_test_trx_to_store_all_types
            ):
        """Test getting a uint public state variable."""
        c = run_test_trx_to_store_all_types
        uint_value = c.get_var(constants.UINT_VAR_NAME)
        assert uint_value == constants.UINT_VAR_VALUE

    def test_get_var_for_str(
            self,
            run_test_trx_to_store_all_types
            ):
        """Test getting a str public state variable."""
        c = run_test_trx_to_store_all_types
        str_value = c.get_var(constants.STR_VAR_NAME)
        assert str_value == constants.STR_VAR_VALUE

    def test_get_var_for_addr(
            self,
            run_test_trx_to_store_all_types
            ):
        """Test getting an addr public state variable."""
        c = run_test_trx_to_store_all_types
        addr_value = c.get_var(constants.ADDR_VAR_NAME)
        assert addr_value == constants.ADDR_VAR_VALUE

    def test_get_var_for_array_element(
            self,
            run_test_trx_to_store_array
            ):
        """Test getting first element from uint array."""
        c = run_test_trx_to_store_array
        addr_value = c.get_var(constants.ARRAY_VAR_NAME, 0)
        assert addr_value == constants.ARRAY_VAR_VALUE


@pytest.mark.usefixtures(
    'construct_never_deployed_test_contract',
    'run_test_trx_to_store_array',
    'run_test_trx_to_store_all_types'
    )
class TestContractGetVarBad:
    """Test cases for Contract().get_var() with bad args"""
    # Don't know how to create the error condition that raises
    # code of C-060-020.

    def test_get_missing_var_name_raises_type_error(
            self,
            run_test_trx_to_store_all_types
            ):
        """Test get_var() with bad var name."""
        c = run_test_trx_to_store_all_types
        with pytest.raises(TypeError):
            c.get_var()

    def test_get_var_with_bad_var_name_raises_C_060_010(
            self,
            run_test_trx_to_store_all_types
            ):
        """Test get_var() with bad var name."""
        c = run_test_trx_to_store_all_types
        bad_var_name = 'bad_name'
        with pytest.raises(SimplEthError) as excp:
            c.get_var(bad_var_name)
        assert excp.value.code == 'C-060-010'

    def test_get_var_with_bad_type_index_raises_C_060_030(
            self,
            run_test_trx_to_store_array
            ):
        """Test get_var() for array element with str for an index."""
        c = run_test_trx_to_store_array
        bad_type_index = 'string'
        with pytest.raises(SimplEthError) as excp:
            c.get_var(constants.ARRAY_VAR_NAME, bad_type_index)
        assert excp.value.code == 'C-060-030'

    def test_get_var_with_missing_index_raises_C_060_030(
            self,
            run_test_trx_to_store_array
            ):
        """Test get_var() with array element without an index."""
        c = run_test_trx_to_store_array
        with pytest.raises(SimplEthError) as excp:
            c.get_var(constants.ARRAY_VAR_NAME)
        assert excp.value.code == 'C-060-030'

    def test_get_var_with_unneeded_index_raises_C_060_030(
            self,
            run_test_trx_to_store_all_types
            ):
        """Test get_var() with an index for a non-array."""
        c = run_test_trx_to_store_all_types
        with pytest.raises(SimplEthError) as excp:
            c.get_var(constants.INT_VAR_NAME, 0)
        assert excp.value.code == 'C-060-030'

    def test_get_var_with_oob_index_raises_C_060_040(
            self,
            run_test_trx_to_store_array
            ):
        """Test get_var() for array element with out-of-bounds
        index."""
        c = run_test_trx_to_store_array
        oob_index = 100
        with pytest.raises(SimplEthError) as excp:
            c.get_var(constants.ARRAY_VAR_NAME, oob_index)
        assert excp.value.code == 'C-060-040'

    def test_get_var_with_unconnected_contract_raises_C_060_050(
            self,
            construct_never_deployed_test_contract
            ):
        """Test get_var() raises C-060-050 if connect() is needed."""
        c = construct_never_deployed_test_contract
        with pytest.raises(SimplEthError) as excp:
            c.get_var(constants.INT_VAR_NAME)
        assert excp.value.code == 'C-060-050'


@pytest.mark.usefixtures(
    'deploy_test_contract',
    'connect_to_test_contract'
    )
class TestContractRunTrxGood:
    """Test cases for Contract().run_trx() with good values"""
    # Since run_trx() is a combination of submit_trx() and
    # get_trx_receipt_wait(), separate tests for those two
    # methods are not needed. These run_trx() tests cover the
    # good values tests for them.

    def test_run_trx_with_typical_good_args(
            self,
            connect_to_test_contract
            ):
        """Test run_trx() with the typical set of args"""
        c = connect_to_test_contract
        receipt = c.run_trx(
            constants.TRX_SENDER,
            constants.TRX_NAME,
            constants.TRX_ARG0,
            constants.TRX_ARG1,
            constants.TRX_ARG2
            )
        assert receipt is not None

    def test_run_trx_with_all_good_args(
            self,
            connect_to_test_contract
            ):
        """Test run_trx() with all params specified."""
        c = connect_to_test_contract
        receipt = c.run_trx(
            constants.TRX_SENDER,
            'storeNumsAndPay',
            constants.TRX_ARG0,
            constants.TRX_ARG1,
            constants.TRX_ARG2,
            gas_limit=1_000_000,
            max_priority_fee_gwei=4,
            max_fee_gwei=50,
            value_wei=50_000,
            timeout=3,
            poll_latency=0.2
            )
        assert receipt is not None


@pytest.mark.usefixtures(
    'connect_to_test_contract',
    'construct_never_deployed_test_contract'
    )
class TestContractRunTrxBad:
    """Test cases for Contract().run_trx() with bad values"""
    # Since run_trx() is a combination of submit_trx() and
    # get_trx_receipt_wait(), separate tests for those two
    # methods are not needed. These run_trx() tests cover the
    # error values tests for them, with one exception. run_trx()
    # will throw C-070-010 if no hash is returned from the
    # submit_trx(). I don't know how to create that error
    # condition. That stanza of the code is not tested.

    def test_run_trx_with_no_args_raises_type_error(
            self,
            connect_to_test_contract
            ):
        """"Attempt to run_trx() with no args fails"""
        c = connect_to_test_contract
        with pytest.raises(TypeError):
            c.run_trx()

    def test_run_trx_with_bad_trx_name_raises_C_080_010(
            self,
            connect_to_test_contract
            ):
        """Test run_trx() with a bad trx name"""
        c = connect_to_test_contract
        bad_trx_name = 'bad_trx'
        with pytest.raises(SimplEthError) as excp:
            c.run_trx(
                constants.TRX_SENDER,
                bad_trx_name,
                constants.TRX_ARG0,
                constants.TRX_ARG1,
                constants.TRX_ARG2
                )
        assert excp.value.code == 'C-080-010'

    def test_run_trx_with_too_few_trx_args_raises_C_080_020(
            self,
            connect_to_test_contract
            ):
        """Test run_trx() with too few trx args"""
        c = connect_to_test_contract
        with pytest.raises(SimplEthError) as excp:
            c.run_trx(
                constants.TRX_SENDER,
                constants.TRX_NAME,
                constants.TRX_ARG0,
                constants.TRX_ARG1
                )
        assert excp.value.code == 'C-080-020'

    def test_run_trx_with_too_many_trx_args_raises_C_080_020(
            self,
            connect_to_test_contract
            ):
        """Test run_trx() with too many trx args"""
        c = connect_to_test_contract
        with pytest.raises(SimplEthError) as excp:
            c.run_trx(
                constants.TRX_SENDER,
                constants.TRX_NAME,
                constants.TRX_ARG0,
                constants.TRX_ARG1,
                'extra arg'
                )
        assert excp.value.code == 'C-080-020'

    @pytest.mark.skip(reason='no way to currently test a destroyed contract')
    def test_run_trx_with_TBD_destroyed_contract_raises_C_080_030(
            self,
            connect_to_test_contract
            ):
        """Test run_trx() for a destroyed contract.
        Don't know how to do this yet. Just do assert True
        for now. """
        assert True

    def test_run_trx_with_bad_sender_raises_C_080_040(
            self,
            connect_to_test_contract
            ):
        """Test run_trx() with a bad sender address"""
        c = connect_to_test_contract
        bad_sender = '123'
        with pytest.raises(SimplEthError) as excp:
            c.run_trx(
                bad_sender,
                constants.TRX_NAME,
                constants.TRX_ARG0,
                constants.TRX_ARG1,
                constants.TRX_ARG2
                )
        assert excp.value.code == 'C-080-040'

    def test_run_trx_with_bad_max_fee_gwei_raises_C_080_050(
            self,
            connect_to_test_contract
            ):
        """Test run_trx() with max fee < max priority fee."""
        c = connect_to_test_contract
        with pytest.raises(SimplEthError) as excp:
            c.run_trx(
                constants.TRX_SENDER,
                'storeNumsAndPay',
                constants.TRX_ARG0,
                constants.TRX_ARG1,
                constants.TRX_ARG2,
                max_priority_fee_gwei=4,
                max_fee_gwei=1
                )
        assert excp.value.code == 'C-080-050'

    def test_run_trx_using_unconnected_contract_raises_C_080_060(
            self,
            construct_never_deployed_test_contract
            ):
        """Test run_trx() without doing a `connect()` first"""
        c = construct_never_deployed_test_contract
        with pytest.raises(SimplEthError) as excp:
            c.run_trx(
                constants.NEVER_DEPLOYED_TRX_SENDER,
                constants.NEVER_DEPLOYED_TRX_NAME
                )
        assert excp.value.code == 'C-080-060'

    def test_run_trx_with_missing_sender_raises_C_080_070(
            self,
            connect_to_test_contract
            ):
        """Test run_trx() without the sender arg"""
        c = connect_to_test_contract
        with pytest.raises(SimplEthError) as excp:
            c.run_trx(
                constants.TRX_NAME,
                constants.TRX_ARG0,
                constants.TRX_ARG1,
                constants.TRX_ARG2
                )
        assert excp.value.code == 'C-080-070'

    def test_run_trx_with_missing_trx_name_raises_C_080_070(
            self,
            connect_to_test_contract
            ):
        """Test run_trx() without the trx_name arg"""
        c = connect_to_test_contract
        with pytest.raises(SimplEthError) as excp:
            c.run_trx(
                constants.TRX_SENDER,
                constants.TRX_ARG0,
                constants.TRX_ARG1
                )
        assert excp.value.code == 'C-080-070'

    def test_run_trx_with_GUARD_fail_raises_C_080_080(
            self,
            connect_to_test_contract
            ):
        """Test run_trx() with a GUARD for isOwner by a non-owner"""
        c = connect_to_test_contract
        non_owner = Blockchain().address(9)
        with pytest.raises(SimplEthError) as excp:
            c.run_trx(
                non_owner,
                'setOwner',
                non_owner
                )
        assert excp.value.code == 'C-080-080'

    def test_run_trx_with_require_fail_raises_C_080_080(
            self,
            connect_to_test_contract
            ):
        """Test run_trx() with require(owner) with non-owner"""
        c = connect_to_test_contract
        non_owner = Blockchain().address(9)
        with pytest.raises(SimplEthError) as excp:
            c.run_trx(
                non_owner,
                'sumTwoNums'
                )
        assert excp.value.code == 'C-080-080'

    def test_run_trx_with_db0_arg_raises_C_080_080(
            self,
            connect_to_test_contract
            ):
        """Test run_trx() with an arg that causes a
        divide-by-zero error"""
        c = connect_to_test_contract
        with pytest.raises(SimplEthError) as excp:
            c.run_trx(
                constants.DB0_TRX_SENDER,
                constants.DB0_TRX_NAME,
                constants.DB0_TRX_ARG0
                )
        assert excp.value.code == 'C-080-080'

    def test_run_trx_with_oob_arg_raises_C_080_080(
            self,
            connect_to_test_contract
            ):
        """Test run_trx() with out-of-bounds arg"""
        c = connect_to_test_contract
        with pytest.raises(SimplEthError) as excp:
            c.run_trx(
                constants.OOB_TRX_SENDER,
                constants.OOB_TRX_NAME,
                constants.OOB_TRX_ARG0,
                constants.OOB_TRX_ARG1
                )
        assert excp.value.code == 'C-080-080'

    def test_run_trx_with_low_gas_limit_raises_C_080_080(
            self,
            connect_to_test_contract
            ):
        """Test run_trx() with too low gas limit."""
        c = connect_to_test_contract
        with pytest.raises(SimplEthError) as excp:
            c.run_trx(
                constants.TRX_SENDER,
                constants.TRX_NAME,
                constants.TRX_ARG0,
                constants.TRX_ARG1,
                constants.TRX_ARG2,
                gas_limit=1_000
                )
        assert excp.value.code == 'C-080-080'

    def test_run_trx_with_high_gas_limit_raises_C_080_080(
            self,
            connect_to_test_contract
            ):
        """Test run_trx() with too high gas limit."""
        c = connect_to_test_contract
        with pytest.raises(SimplEthError) as excp:
            c.run_trx(
                constants.TRX_SENDER,
                constants.TRX_NAME,
                constants.TRX_ARG0,
                constants.TRX_ARG1,
                constants.TRX_ARG2,
                gas_limit=10_000_000
                )
        assert excp.value.code == 'C-080-080'

    def test_run_trx_with_float_max_fee_raises_C_080_080(
            self,
            connect_to_test_contract
            ):
        """Test run_trx() with a float value for max_fee_gwei"""
        c = connect_to_test_contract
        with pytest.raises(SimplEthError) as excp:
            c.run_trx(
                constants.TRX_SENDER,
                constants.TRX_NAME,
                constants.TRX_ARG0,
                constants.TRX_ARG1,
                constants.TRX_ARG2,
                max_fee_gwei=10.7
                )
        assert excp.value.code == 'C-080-080'

    def test_run_trx_with_float_max_priority_fee_raises_C_080_080(
            self,
            connect_to_test_contract
            ):
        """Test run_trx() with a float value for max_priority_fee_gwei"""
        c = connect_to_test_contract
        with pytest.raises(SimplEthError) as excp:
            c.run_trx(
                constants.TRX_SENDER,
                constants.TRX_NAME,
                constants.TRX_ARG0,
                constants.TRX_ARG1,
                constants.TRX_ARG2,
                max_priority_fee_gwei=10.7
                )
        assert excp.value.code == 'C-080-080'

    def test_run_trx_calling_2nd_trx_that_fails_raises_C_080_080(
            self,
            connect_to_test_contract
            ):
        """Test run_trx() with trx1 calling trx2 and trx2 fails"""
        c = connect_to_test_contract
        with pytest.raises(SimplEthError) as excp:
            c.run_trx(
                constants.TRX_SENDER,
                'divideNums',
                0
                )
        assert excp.value.code == 'C-080-080'

    def test_send_ether_to_non_payable_trx_raises_C_080_080(
            self,
            connect_to_test_contract
            ):
        """Test run_trx() with trx1 calling trx2 and trx2 fails"""
        c = connect_to_test_contract
        with pytest.raises(SimplEthError) as excp:
            c.run_trx(
                constants.TRX_SENDER,
                constants.TRX_NAME,
                constants.TRX_ARG0,
                constants.TRX_ARG1,
                constants.TRX_ARG2,
                value_wei=100
                )
        assert excp.value.code == 'C-080-080'

    @pytest.mark.skip(reason='do not know a test case for ContractLogicError')
    def test_run_trx_with_TBD_contract_logic_error_raises_C_080_090(
            self,
            connect_to_test_contract
            ):
        """Test run_trx() for ContractLogicError. This exception
        is in the list for web3 exceptions and I saw a mention of
        it in forum posts. submit_trx() will catch it and print
        the exception message. I haven't been able to throw it in
        any of my testing.  Just leaving this test case as a placeholder
        and reminder. Just do assert True for now. """
        assert True


@pytest.mark.usefixtures(
    'deploy_test_contract',
    'connect_to_test_contract'
    )
class TestContractSelfdestructGood:
    """Test cases for using selfdestruct() to destroy a deployed contract"""
    def test_selfdestruct_contract_with_good_arg(
            self,
            connect_to_test_contract
            ):
        """Test selfdestruct() in the destroy() trx"""
        c = connect_to_test_contract
        u6 = Blockchain().address(6)    # destroy() sends ether to u6
        receipt = c.run_trx(
            constants.TRX_SENDER,
            'destroy',
            u6
            )
        assert receipt is not None

    def test_get_var_fails_after_selfdestruct(
            self,
            connect_to_test_contract
            ):
        """Test get_var() throws expected exception"""
        c = connect_to_test_contract
        with pytest.raises(SimplEthError) as excp:
            c.get_var('initNum')
        assert excp.value.code == 'C-060-020'

    def test_call_fcn_fails_after_selfdestruct(
            self,
            connect_to_test_contract
            ):
        """Test call_fcn() throws expected exception"""
        c = connect_to_test_contract
        with pytest.raises(SimplEthError) as excp:
            c.call_fcn('getNums')
        assert excp.value.code == 'C-010-030'

    def test_run_trx_completes_after_selfdestruct(
            self,
            connect_to_test_contract
            ):
        """Test a transaction returns a receipt"""
        # A trx will successfully return a receipt from the destroyed
        # contract, but the trx will not have any effect. No chain
        # data is updated.
        c = connect_to_test_contract
        receipt = c.run_trx(
            constants.TRX_SENDER,
            constants.TRX_NAME,
            constants.TRX_ARG0,
            constants.TRX_ARG1,
            constants.TRX_ARG2
            )
        assert receipt is not None

    def test_get_gas_estimate_completes_after_selfdestruct(
            self,
            connect_to_test_contract
            ):
        """Test get gas estimate runs for a trx in a destroyed contract"""
        # The gas estimate will still be calculated even though the
        # contract is destroyed.
        c = connect_to_test_contract
        estimate = c.get_gas_estimate(
            constants.TRX_SENDER,
            constants.TRX_NAME,
            constants.TRX_ARG0,
            constants.TRX_ARG1,
            constants.TRX_ARG2
            )
        assert isinstance(estimate, int)
