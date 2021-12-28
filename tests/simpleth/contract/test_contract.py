"""Test Contract() class"""
import pytest

from simpleth import Blockchain, Contract, SimplEthError
import testconstants as constants


class TestContractConstructorAll:
    """Test cases for Contract() with both good and bad test cases"""

    def test_constructor_with_good_contract_name(self):
        """Instantiate Contract() object with valid constructor arg"""
        assert Contract(constants.CONTRACT_NAME)._name is constants.CONTRACT_NAME

    def test_constructor_with_bad_contract_name_raises_c_100_010(self):
        """SimplEthError is raised when constructor has bad contract name"""
        bad_name = 'bad_contract_name'
        with pytest.raises(SimplEthError) as excp:
            Contract(bad_name)
        assert excp.value.code == 'C-100-010'

    def test_constructor_with_missing_contract_name_raises_type_error(self):
        """TypeError is raised when constructor has no contract name"""
        with pytest.raises(TypeError):
            Contract()


@pytest.mark.usefixtures('connect_to_test_contract')
class TestContractDeployGood:
    """Test cases for Contract().deploy() with good test cases"""

    def test_deploy_with_good_args(self, connect_to_test_contract):
        """deploy() with typical set of args returns result for deploy trx"""
        c = Contract(constants.CONTRACT_NAME)
        r = c.deploy(constants.CONSTRUCTOR_SENDER, constants.CONSTRUCTOR_ARG)
        assert r.trx_name == 'deploy'

    def test_deploy_without_constructor_event_name(
            self,
            connect_to_test_contract
            ):
        """deploy() with just sender and arg works and returns result for
        deploy trx"""
        c = Contract(constants.CONTRACT_NAME)
        r = c.deploy(constants.CONSTRUCTOR_SENDER, constants.CONSTRUCTOR_ARG)
        assert r.trx_name == 'deploy'

    def test_deploy_with_good_args_plus_gas_limit(
            self,
            connect_to_test_contract
            ):
        """deploy() with typical set of args plus specifying a gas limit
        large enough for the trx returns result for deploy trx"""
        c = Contract(constants.CONTRACT_NAME)
        r = c.deploy(constants.CONSTRUCTOR_SENDER, constants.CONSTRUCTOR_ARG, gas_limit=constants.CONSTRUCTOR_GAS_LIMIT)
        assert r.trx_name == 'deploy'

    def test_deploy_with_good_args_plus_gas_limit_and_fees(
            self,
            connect_to_test_contract
            ):
        """deploy() with typical set of args plus specifying a gas limit
        large enough for the trx plus reasonable values for fees returns
        result for deploy trx"""
        c = Contract(constants.CONTRACT_NAME)
        r = c.deploy(constants.CONSTRUCTOR_SENDER, constants.CONSTRUCTOR_ARG, gas_limit=constants.CONSTRUCTOR_GAS_LIMIT,
                     max_priority_fee_gwei=constants.MAX_PRIORITY_FEE_GWEI, max_fee_gwei=constants.MAX_FEE_GWEI)
        assert r.trx_name == 'deploy'


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

    def test_deploy_with_bad_sender_raises_c_030_020(
            self,
            construct_test_contract
            ):
        """"Attempt to deploy with bad sender raises C-030-020"""
        c = construct_test_contract
        bad_sender = '123'
        with pytest.raises(SimplEthError) as excp:
            c.deploy(bad_sender, constants.CONSTRUCTOR_ARG)
        assert excp.value.code == 'C-030-020'

    def test_deploy_with_wrong_type_constructor_arg_raises_c_030_030(
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

    def test_deploy_with_too_many_constructor_args_raises_c_030_030(
            self,
            construct_test_contract
            ):
        """"Attempt to deploy with too many constructor args raises
        C-030-030"""
        c = construct_test_contract
        extra_constructor_arg = 20
        with pytest.raises(SimplEthError) as excp:
            c.deploy(constants.CONSTRUCTOR_SENDER, constants.CONSTRUCTOR_ARG, extra_constructor_arg)
        assert excp.value.code == 'C-030-030'

    def test_deploy_with_missing_constructor_arg_raises_c_030_030(
            self,
            construct_test_contract
            ):
        """"Attempt to deploy with missing constructor arg raises
        C-030-030"""
        c = construct_test_contract
        with pytest.raises(SimplEthError) as excp:
            c.deploy(constants.CONSTRUCTOR_SENDER)
        assert excp.value.code == 'C-030-030'

    def test_deploy_with_insufficient_gas_raises_c_030_040(
            self,
            construct_test_contract
            ):
        """"Attempt to deploy with gas limit arg too small to
        run the trx raises C-030-030"""
        c = construct_test_contract
        insufficient_gas_limit = constants.GAS_LIMIT_MIN
        with pytest.raises(SimplEthError) as excp:
            c.deploy(constants.CONSTRUCTOR_SENDER, constants.CONSTRUCTOR_ARG, gas_limit=insufficient_gas_limit)
        assert excp.value.code == 'C-030-040'

    def test_deploy_with_excessive_gas_raises_c_030_040(
            self,
            construct_test_contract
            ):
        """"Attempt to deploy with missing constructor arg raises
        C-030-030"""
        c = construct_test_contract
        excessive_gas_limit = constants.GAS_LIMIT_MAX + 1
        with pytest.raises(SimplEthError) as excp:
            c.deploy(constants.CONSTRUCTOR_SENDER, constants.CONSTRUCTOR_ARG, gas_limit=excessive_gas_limit)
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


@pytest.mark.usefixtures('connect_to_test_contract')
class TestCallFcnBad:
    """Test cases for Contract().call_fcn() with bad values"""
    # OK to just do connect() instead of deploy(). These tests
    # all give bad args so doesn't matter that we have a fresh
    # contract.

    def test_call_fcn_with_bad_fcn_name_raises_c_010_010(
            self,
            connect_to_test_contract
            ):
        """"Attempt to call_fcn with bad fcn_name raises C-010-010"""
        c = connect_to_test_contract
        bad_fcn_name = 'bad'
        with pytest.raises(SimplEthError) as excp:
            c.call_fcn(bad_fcn_name)
        assert excp.value.code == 'C-010-010'

    def test_call_fcn_with_no_fcn_name_raises_type_error(
            self,
            connect_to_test_contract
            ):
        """"Attempt to call_fcn with missing fcn_name raises type
        error"""
        # SN_FIX - Don't understand why this doesn't raise SimplEthError
        # with code of C-010-050
        c = connect_to_test_contract
        with pytest.raises(TypeError):
            c.call_fcn()

    def test_call_fcn_with_bad_arg_type_raises_c_010_020(
            self,
            connect_to_test_contract
            ):
        """"Attempt to call_fcn with bad arg type raises C-010-020"""
        c = connect_to_test_contract
        bad_arg_type = 'bad'
        with pytest.raises(SimplEthError) as excp:
            c.call_fcn('getNum', bad_arg_type)
        assert excp.value.code == 'C-010-020'

    def test_call_fcn_with_wrong_num_args_raises_c_010_020(
            self,
            connect_to_test_contract
            ):
        """"Attempt to call_fcn with bad number of args raises
        C-010-020"""
        c = connect_to_test_contract
        with pytest.raises(SimplEthError) as excp:
            c.call_fcn('getNum', 1, 2)
        assert excp.value.code == 'C-010-020'

    def test_call_fcn_with_out_of_bounds_arg_raises_c_010_040(
            self,
            connect_to_test_contract
            ):
        """"Attempt to call_fcn with an out of bounds arg raises
        C-010-040"""
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

    def test_get_gas_estimate_with_bad_trx_name_raises_c_040_010(
            self,
            connect_to_test_contract
        ):
        """Test get_gas_estimate() with a bad trx name"""
        c = connect_to_test_contract
        bad_trx_name = 'bad_trx'
        with pytest.raises(SimplEthError) as excp:
            gas_estimate = c.get_gas_estimate(
                constants.TRX_SENDER,
                bad_trx_name,
                constants.TRX_ARG0,
                constants.TRX_ARG1,
                constants.TRX_ARG2
            )
        assert excp.value.code == 'C-040-010'

    def test_get_gas_estimate_with_too_few_trx_args_raises_c_040_020(
            self,
            connect_to_test_contract
        ):
        """Test get_gas_estimate() with too few trx args"""
        c = connect_to_test_contract
        with pytest.raises(SimplEthError) as excp:
            gas_estimate = c.get_gas_estimate(
                constants.TRX_SENDER,
                constants.TRX_NAME,
                constants.TRX_ARG0,
                constants.TRX_ARG1
            )
        assert excp.value.code == 'C-040-020'

    def test_get_gas_estimate_with_too_many_trx_args_raises_c_040_020(
            self,
            connect_to_test_contract
        ):
        """Test get_gas_estimate() with too many trx args"""
        c = connect_to_test_contract
        with pytest.raises(SimplEthError) as excp:
            gas_estimate = c.get_gas_estimate(
                constants.TRX_SENDER,
                constants.TRX_NAME,
                constants.TRX_ARG0,
                constants.TRX_ARG1,
                constants.TRX_ARG2,
                constants.TRX_ARG2
            )
        assert excp.value.code == 'C-040-020'

    def test_get_gas_estimate_with_TBD_raises_c_040_030(
            self,
            connect_to_test_contract
        ):
        """Test get_gas_estimate() a destroyed contract. Don't know how
        to do this yet. Just do an assert True for now. """
        assert True

    def test_get_gas_estimate_with_oob_arg_raises_c_040_040(
            self,
            connect_to_test_contract
        ):
        """Test get_gas_estimate() with too many trx args"""
        c = connect_to_test_contract
        with pytest.raises(SimplEthError) as excp:
            gas_estimate = c.get_gas_estimate(
                constants.OOB_TRX_SENDER,
                constants.OOB_TRX_NAME,
                constants.OOB_TRX_ARG0,
                constants.OOB_TRX_ARG1
            )
        assert excp.value.code == 'C-040-040'

    def test_get_gas_estimate_with_db0_arg_raises_c_040_040(
            self,
            connect_to_test_contract
        ):
        """Test get_gas_estimate() with an arg that causes a
        divide-by-zero error"""
        c = connect_to_test_contract
        with pytest.raises(SimplEthError) as excp:
            gas_estimate = c.get_gas_estimate(
                constants.DB0_TRX_SENDER,
                constants.DB0_TRX_NAME,
                constants.DB0_TRX_ARG0
            )
        assert excp.value.code == 'C-040-040'

    def test_get_gas_estimate_with_bad_sender_raises_c_040_050(
            self,
            connect_to_test_contract
        ):
        """Test get_gas_estimate() with a bad sender address"""
        c = connect_to_test_contract
        bad_sender = '123'
        with pytest.raises(SimplEthError) as excp:
            gas_estimate = c.get_gas_estimate(
                bad_sender,
                constants.TRX_NAME,
                constants.TRX_ARG0,
                constants.TRX_ARG1,
                constants.TRX_ARG2
            )
        assert excp.value.code == 'C-040-050'

    def test_get_gas_estimate_using_never_deployed_contract_raises_c_040_060(
            self,
            construct_never_deployed_test_contract
        ):
        """Test get_gas_estimate() without doing a `connect()` first"""
        c = construct_never_deployed_test_contract
        with pytest.raises(SimplEthError) as excp:
            gas_estimate = c.get_gas_estimate(
                constants.NEVER_DEPLOYED_TRX_SENDER,
                constants.NEVER_DEPLOYED_TRX_NAME
            )
        assert excp.value.code == 'C-040-060'

    def test_get_gas_estimate_with_missing_sender_raises_c_040_070(
            self,
            connect_to_test_contract
        ):
        """Test get_gas_estimate() with a missing sender arg"""
        c = connect_to_test_contract
        bad_sender = '123'
        with pytest.raises(SimplEthError) as excp:
            gas_estimate = c.get_gas_estimate(
                constants.TRX_NAME,
                constants.TRX_ARG0,
                constants.TRX_ARG1,
                constants.TRX_ARG2
            )
        assert excp.value.code == 'C-040-070'
