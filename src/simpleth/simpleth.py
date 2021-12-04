"""Simple Ethereum is a facade of `web3.py` to simplify use of an
Ethereum blockchain and interaction with Solidity contracts.

Classes
-------
- `Blockchain` - interact with Ethereum blockchain
- `Contract` - interact with Solidity contracts
- `Filter` - search for events emitted by transactions

Exceptions
----------
- `SimplEthError` - raised on errors from methods in `Blockchain` or
  `Contract`.

"""
import sys
import json
import json.decoder
import datetime
from typing import List, Optional, Union, Any
from web3 import Web3
from web3 import exceptions as web3e
from web3.logs import DISCARD

__all__ = ['Blockchain', 'Contract', 'SimplEthError']
__author__ = 'Stephen Newell'
__copyright__ = 'Copyright 2021, Stephen Newell'
__license__ = 'MIT'
__version__ = '0.17'
__maintainer__ = 'Stephen Newell'
__email__ = 'snewell4@gmail.com'
__status__ = 'Prototype'


#
# Transaction processing defaults
#

# This is the maximum amount of gas any single transaction can consume.
# If the transaction requires more gas, it will revert. This value is
# arbitrarily set slightly below the Ganache default value for Gas Limit.
GAS_LIMIT: int = 6_000_000
"""Gas limit for a transaction, in units of gas."""

# Currently has no effect with Ganache. It is valid for main net.
MAX_BASE_FEE_GWEI: Union[int, float] = 100
"""Maximum tip to pay the miners, per unit of gas in gwei."""

# Currently has no effect with Ganache. It is valid for main net.
MAX_PRIORITY_FEE_GWEI: Union[int, float] = 2
"""Maximum tip to pay the miners, per unit of gas in gwei."""

# Currently has no effect with Ganache. It is valid for main net.
MAX_FEE_GWEI: Union[int, float] = \
    MAX_BASE_FEE_GWEI + MAX_PRIORITY_FEE_GWEI
"""Maximum total to pay the miners, per unit of gas in gwei."""

TIMEOUT: Union[int, float] = 120
"""Time to wait for transaction to be mined, in seconds."""

POLL_LATENCY: Union[int, float] = 0.1
"""Time between checking if mining is finished, in seconds."""

#
# Directories and filenames
#
PROJECT_HOME: str = 'C:/Users/snewe/OneDrive/Desktop/simpleth'
"""Directory for the prototype project home"""

ARTIFACT_SUBDIR: str = 'artifacts'
"""Directory, under home directory, for the artifact files."""

ABI_SUFFIX: str = 'abi'
"""Filename suffix for the ABI files."""

BYTECODE_SUFFIX: str = 'bin'
"""Filename suffix for the bytecode files."""

ADDRESS_SUFFIX: str = 'addr'
"""Filename suffix for the contract address files."""

BIN_RUNTIME_SUFFIX: str = 'bin-runtime'
"""Filename suffix for bin-runtime files. Used to get compiled size."""

#
# Ganache
#
GANACHE_URL: str = 'http://127.0.0.1:7545'
"""URL to connect to Ganache Ethereum blockchain running on laptop"""

#
# Formatting
#
TIME_FORMAT: str = '%Y-%m-%d %H:%M:%S'
"""Default ``datetime`` format coding used to represent time values"""

#
# Type Hint aliases
#
# Using anything besides, Any, causes pylint to complain that it it
# a class name and doesn't conform to PascalCase naming style. For now,
# easiest to just use Any for all.
#
T_ABI = Any
"""``ABI`` type is a list with JSON read from the `artifact` file."""

T_BYTECODE = Any
"""``bytecode`` type is HexBytes read from the `artifact` file.
Use `Any` for now."""

T_CONTRACT_EVENT = Any
"""`contract_event`` type is ``web3._utils.datatypes.<event_name>'``.
Use ``Any`` for now."""

T_TRANSACTION = Any
"""``Transaction`` type is class `web3.datastructures.AttributeDict`.
Use `Any` for now. Created by `web3.py` `getTransaction()`.  """

T_HASH = Any
"""``Transaction hash`` type is HexBytes in ``web3.py``. It is cast to
a string for use in ``simpleth``."""

T_RECEIPT = Any
"""``Transaction receipt`` type is AttributeDict. Use `Any` for now.
Created by `web3.py` methods."""

T_RESULT = Any
"""``Transaction result`` is a class object with the various outcomes
from mining a transaction. Created by the `simpleth` class,
``Result``. Use Any for now."""

T_EXC_INFO = Any
"""``Transaction exception info`` type is a tuple returned by
`sys.exc_info()` after an exception. Use `Any` for now."""

T_DEPLOYED_CODE = Any
"""``Deployed code`` type is class `HexBytes`. Use
`str` for now.  Created by `web3.py` method."""

T_BLOCKCHAIN_OBJ = Any
"""``Blockchain object`` type is `simpleth.Blockchain`. Use `Any` for now.
Created by `simpleth` methods. See ``T_result`` about those single quotes."""

T_ETH_OBJ = Any
"""``Eth object`` type is `web3.eth.Eth`. Use `Any` for now.
Created by `web3.py` methods."""

T_EVENT_LOG = Any
"""``Event log`` type is an ``AttributeDict``. Use ``Any`` for now."""

T_FILTER_OBJ = Any
"""``Filter object`` type is `web3._utils.filters.LogFilter`.
Use `Any` for now. Created by `web3.py` methods."""

T_FILTER_LIST = Any
"""``Filter list`` type is created by `web3.py` `event_filter`.
Use `Any` for now."""

T_WEB3_OBJ = Any
"""``Web3 object`` type is `web3.main.Web3 object`. Use `Any` for now.
Created by `web3.py` methods."""

T_WEB3_ETH_OBJ = Any
"""``Web3 object`` type is `TODO - fill in`. Use `Any` for now."""

T_WEB3_CONTRACT_OBJ = Any
"""``Web3 contract object`` type is ``web3._utils.datatypes.Contract``
object. Use ``Any`` for now."""

T_WEB3_EXC = Any
"""``Web3 Exception`` type is `module web3.exceptions`.
Use `Any` for now. Provided by `web3.py`"""

T_DECIMAL = Any
"""``Decimal`` type. Use ``Any`` for now."""


class Blockchain:
    """Interact with an Ethereum blockchain.

    Sets up the `Web3` object which establishes the
    connection to a an Ethereum blockchain and supports access
    to various values and functions related to the blockchain.

    :warning: This has only been tested with `Ganache`.
    :see also: `Web3` API documentation at
        https://web3py.readthedocs.io/en/stable/web3.main.html

    """
    def __init__(self, url: str = constant.GANACHE_URL) -> None:
        """Create blockchain instance.

        :param url: Ethereum blockchain web address (optional,
            default: :const:`constant.GANACHE_URL`)
        :type url: str
        :rtype: None
        :example:
            >>> from simpleth import Blockchain
            >>> b = Blockchain()

        :raises SimplEthError: if unable to connect to blockchain
            client

        """
        self._web3 = Web3(Web3.HTTPProvider(url))
        """private `web3` object that represents the blockchain"""
        if not self._web3.isConnected():
            message: str = (
                'ERROR in Blockchain().init(): '
                'Unable to connect to Web3.\n'
                'HINT 1: Is Ganache running?\n'
                'HINT 2: If not using Ganache, is your blockchain client '
                'running?\n'
                )
            raise SimplEthError(message, code='B-010-010') from None

        self._eth: constant.T_WEB3_ETH_OBJ = self.web3.eth
        """private ``web3.eth`` object"""
        self._web3e: constant.T_WEB3_EXC = web3e
        """private module to catch exceptions from Web3 API"""
        self._accounts: List[str] = self.eth.accounts
        """private list of addresses in the Ganache-provided
            accounts"""
        self._api_version: str = self.web3.api
        """private `web3` API version"""
        self._client_version: str = self.web3.clientVersion
        """private Ethereum client version"""

    @property
    def accounts(self) -> List:
        """Return list of accounts provided by the blockchain client.

        :rtype: list
        :return: list of blockchain `addresses`
        :example:
            >>> from simpleth import Blockchain
            >>> Blockchain().accounts
            ['0x235A686386d03a5Bb986Fb13E71A0dC86846c636',   ..snip..

        """
        return self._accounts

    @property
    def api_version(self) -> str:
        """Return the installed 'web3` API version.

        :rtype: str
        :return: API version number
        :example:
            >>> from simpleth import Blockchain
            >>> b = Blockchain()
            >>> b.api_version
            '5.24.0'

        """
        return self._api_version

    @property
    def block_number(self) -> int:
        """Return the number of the last block added to the chain.

        :rtype: integer
        :return: sequence number of last block at the end of the chain
        :example:
            >>> from simpleth import Blockchain
            >>> b = Blockchain()
            >>> b.block_number
            2284

        """
        return self.eth.block_number

    @property
    def client_version(self) -> str:
        """Return the blockchain client version description.

        :rtype: str
        :return: client version number
        :example:
            >>> from simpleth import Blockchain
            >>> b = Blockchain()
            >>> b.client_version
            'EthereumJS TestRPC/v2.13.1/ethereum-js'

        """
        return self._client_version

    @property
    def eth(self) -> constant.T_ETH_OBJ:
        """Return the ``web3.eth`` object.

        :rtype: object
        :return: `Eth` object
        :example:
            >>> from simpleth import Blockchain
            >>> b = Blockchain()
            >>> b.eth
            <web3.eth.Eth object at 0x0000019CEBAC8760>

        :notes:
            - This can be used to access any of the ``web3.eth``
              methods not provided by `simpleth`.

        """
        return self._eth

    @property
    def web3(self) -> constant.T_WEB3_OBJ:
        """Return the ``web3`` object.

        :rtype: object
        :return: `web3` object
        :example:
            >>> from simpleth import Blockchain
            >>> b = Blockchain()
            >>> b.web3
            <web3.main.Web3 object at 0x0000019CE7AF3520>

        :notes:
            - This can be used to access any of the ``web3`` methods not
              provided by `simpleth`.

        """
        return self._web3

    def account_num(
            self,
            account_address: str
            ) -> Optional[int]:
        """Return account number for the specified address.

        :param account_address: address to convert to account number
        :type account_address: str
        :rtype: int | None
        :return:
            - index of the account in the list Ganache-provided accounts
            - ``None`` if ``account_address`` not one provided by Ganache

        :warning:
            - This is only relevant for `Ganache`. Other blockchain
              clients do not provide a list of account addresses to
              use.

        :example:
            >>> from simpleth import Blockchain
            >>> b = Blockchain()
            >>> user = b.accounts[6]
            >>> b.account_num(user)
            6
            >>> bogus_address='0xCd6afD0f6E431DEddCBb9F631cC9E71c6b69b577'
            >>> b.account_num(bogus_address)

        :see also:
            - :meth:`accounts` for the list of all Ganache account
              addresses.

        """
        try:
            account_num: Optional[int] = \
               self._accounts.index(account_address)
        except ValueError:
            # account_num not in list
            account_num = None
        return account_num

    def address(self, account_num: int) -> str:
        """Return the blockchain address of the specified account number.

        :param account_num: index into the account list for the account of
            interest
        :type account_num: int
        :rtype: str
        :return: blockchain ``address`` of the requested account
        :raises SimplEthError: if ``account_num`` is bad
        :example:

        :see also:
            - :meth:`accounts` to get all addresses.

        """
        try:
            address: str = self.accounts[account_num]
        except IndexError as exception:
            message: str = (
                f'ERROR in get_account_address({account_num}): '
                f'IndexError says: {exception}.\n'
                f'HINT: account_num arg is out of range for the number of '
                f'accounts.\n'
                )
            raise SimplEthError(message, code='B-020-010') from None
        return address

    def balance(self, address: str) -> int:
        """Return the amount of ether owned by the account at the given ``address``.

        :param address: blockchain `address` of account to check
        :type address: str
        :rtype: int
        :return: account's ether balance, in wei

        :raises SimplEthError: if ``address`` is bad
        :example:
            >>> from simpleth import Blockchain
            >>> b = Blockchain()
            >>> user0 = b.address(0)
            >>> b.balance(user0)
            99977013240000000000

        """
        try:
            balance: int = self.eth.getBalance(address)
        except TypeError as exception:
            message: str = (
                f'ERROR in get_balance(): '
                f'TypeError says: {exception}.\n'
                f'HINT: Did you use a string for the account address?\n'
                )
            raise SimplEthError(message, code='B-030-010') from None
        except self._web3e.InvalidAddress as exception:
            message = (
                f'ERROR in get_balance(): '
                f'InvalidAddress says: {exception}.\n'
                f'HINT: Did you use a string with a valid account address?\n'
                )
            raise SimplEthError(message, code='B-030-020') from None
        return balance

    def fee_history(self, num_blocks: int = 3) -> dict:
        """Return fee information use with recent blocks.

        This could be used to determine a reasonable ``max_fee_gwei`` and
        ``max_priority_fee_gwei`` to offer when submitting a new transaction.

        :param num_blocks: information for the last ``num_blocks`` will be
            returned
        :type num_blocks: int
        :rtype: dict
        :returns: dictionary with:

            -  ``'reward'``: list with the low and high `reward` amounts offered for
               transactions in this block: low is the 10th percentile; high is the
               90th percentile
            -  ``'baseFeePerGas'``: ``base fee`` set by the network for this block
            -  ``'gasUsedRatio'``: ``gasUsed``/``gasLimit`` for this block
            -  ``'oldestBlock'``: ``block number`` for the oldest block in the list
               and will be :attr:`block_number` - ``num_blocks``

        :warning: This does not work. The ``w3.eth.fee_history()` method is
          specified in the ``web3.py`` documentation but does not seem to be
          supported by Ganache yet. Currently, it throws a ``ValueError``
          exception.
        :example:

        :note: this method is being included in ``simpleth`` in hopes it is
          soon implemented by Ganache. The method has value for using ``simpleth``
          and for now will be coded up and ready to use.

        """
        try:
            history: dict = self.eth.fee_history(num_blocks, 'latest', [10, 90])
        except ValueError as exception:
            message: str = (
                f'ERROR in fee_history().\n'
                f'ValueError says: {exception}\n'
                f'HINT: method not yet implemented in Ganache.\n'
                )
            raise SimplEthError(message, code='B-040-010') from None
        return dict(history)     # cast from AttributeDict to dict

    def block_time_epoch(self, block_number: int) -> int:
        """Return time, as epoch seconds, when a block was mined.

        :param block_number: number of the block on the chain
        :type block_number: int
        :rtype: int
        :return: time block was mined, in epoch seconds.

        """
        return self.eth.get_block(block_number).timestamp

    def block_time_string(
            self,
            block_number: int,
            time_format: str = constant.TIME_FORMAT
         ) -> str:
        """Return time, as a string, when a block was mined.

        :param block_number: number of the block on the chain
        :type block_number: int
        :param time_format: format codes used to create time string
            (optional, default: :const:`constant.TIME_FORMAT`)
        :type time_format: str
        :rtype: str
        :return: time block was mined, in local timezone, as a string.
        :see also:
            - List of format codes:
              https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes

        """
        epoch_seconds = self.block_time_epoch(block_number)
        return datetime.datetime. \
            fromtimestamp(epoch_seconds). \
            strftime(time_format)

    def is_valid_address(self, address: str) -> bool:
        """Test for valid blockchain address

        :param address: blockchain `address` to verify
        :rtype: boolean
        :return:
            - `True` if valid
            - `False` otherwise

        :example:
            >>> from simpleth import Blockchain
            >>> b = Blockchain()
            >>> user0 = b.address(0)
            >>> b.is_valid_address(user0)
            True
            >>> a = '0x380A36BE82A06A63395D'
            >>> b.is_valid_address(a)
            False

        """
        return self._web3.isAddress(address)

    def send_ether(
            self,
            sender: str,
            receiver: str,
            amount_wei: int
            ) -> constant.T_HASH:
        """Transfer Ether from one account to another.

        ``amount`` is deducted from ``sender`` account and added to
        ``receiver`` account.

        :param sender: `address` of the account that sends the Ether
        :type sender: str
        :param receiver: `address` of the account that receives
                the Ether
        :type receiver: str
        :param amount_wei: amount of Ether transferred; denominated
            in `wei`
        :type amount_wei: int
        :rtype: str
        :return: ``trx_hash`` of the transfer transaction
        :raises SimplEthError:
            - if ``sender`` is bad
            - if ``receiver`` is bad
            - if ``amount`` is not an int
            - if ``amount`` exceeds the ``sender`` balance
            - if ``receiver`` is a `non-payable` contract

        :example:
            >>> from simpleth import Blockchain
            >>> b = Blockchain()
            >>> user4 = b.address(4)
            >>> user8 = b.address(8)
            >>> b.send_ether(user4, user8, 1000)

        """
        try:
            trx_hash: str = self._web3.eth.sendTransaction(
                {
                    'to': receiver,
                    'from': sender,
                    'value': amount_wei
                }
            ).hex()      # cast to a string from HexBytes
        except ValueError as exception:
            message = (
                f'ERROR in transfer(): '
                f'ValueError says: {exception}.\n'
                f'HINT 1: Amount exceeds sender balance\n'
                f'HINT 2: Amount must be positive\n'
                )
            raise SimplEthError(message, code='B-050-010') from None
        except TypeError as exception:
            message = (
                f'ERROR in transfer(): '
                f'TypeError says: {exception}.\n'
                f'HINT: Amount must be an int. Did you use a float?\n'
                )
            raise SimplEthError(message, code='B-050-020') from None
        except AttributeError as exception:
            message = (
                f'ERROR in transfer(): '
                f'AttributeError says: {exception}.\n'
                f'HINT: Did you attempt to send Ether to a non-payable '
                f'contract?\n'
                )
            raise SimplEthError(message, code='B-050-030') from None
        return trx_hash

    def transaction(self, trx_hash: str) -> constant.T_TRANSACTION:
        """Return details about the transaction identified by the transaction hash.

        :param trx_hash: transaction hash
        :type trx_hash: str
        :rtype: dict
        :return: transaction details as a dictionary

        """
        try:
            transaction: dict = dict(self.eth.get_transaction(trx_hash))
        except self._web3e.TransactionNotFound as exception:
            message: str = (
                f'ERROR in transaction(): '
                f'TransactionNotFound says: {exception}\n'
                f'HINT: Did you use a valid trx_hash?'
                )
            raise SimplEthError(message, code='B-060-010') from None
        return transaction

    def trx_count(self, address: str) -> int:
        """Return the number of transactions sent by an account.

        :param address: blockchain `address` of account to check
        :type address: str
        :rtype: int
        :return: number of transactions, since start of the blockchain,
                the account at this address has submitted
        :raises SimplEthError: if ``address`` is bad
        :example:
            >>> from simpleth import Blockchain
            >>> b = Blockchain()
            >>> user0 = b.address(0)
            >>> b.trx_count(user0)
            48

        """
        try:
            count: int = self.eth.getTransactionCount(address)
        except TypeError as exception:
            message: str = (
                f'ERROR in get_trx_count(): '
                f'TypeError says: {exception}.\n'
                f'HINT: Did you use a string with a valid account address?\n'
                )
            raise SimplEthError(message, code='B-070-010') from None
        except self._web3e.InvalidAddress as exception:
            message = (
                f'ERROR in get_trx_count(): '
                f'InvalidAddress says: {exception}.\n'
                f'HINT: Did you use a string with a valid account address?\n'
                )
            raise SimplEthError(message, code='B-070-020') from None
        return count

    def trx_sender(self, trx_hash: str) -> str:
        """Return the account address that sent this transaction to be mined.

       :param trx_hash: transaction hash
        :type trx_hash: str
        :rtype: str
        :return: address that sent the transaction
        :example:

        """
        return self.transaction(trx_hash)['from']
# end of Blockchain()


class Contract:
    """Use to interact with Solidity contracts on an Ethereum blockchain.

    Will deploy a contract onto the blockchain, connect to a previously
    deployed contract, submit transactions to be run, get results of a
    transaction, call functions, and get public
    state variable values.

    """
    def __init__(self, name: str) -> None:
        """Create instance for the named contract.

        :param name: contract name
        :type name: str
        :rtype: None
        :example: shown above
        :raises SimplEthError: when ``name`` is misspelled or has
            not been compiled.
        :example:
            >>> from simpleth import Contract
            >>> Contract('TestTrx')
            <simpleth.Contract object at 0x0000028A7262B580>

        :notes: ``name`` must match the Solidity filename for the
            contract source code. For example, if the Solidity file is
            ``Example.sol``, use ``Contract(\'Example\')``. Due to
            DOS filename convention case does not matter and
            ``Contract(\'example\')`` will also work.

        """
        self._name: str = name
        """Private name of the contract this object represents"""

        self._artifact_dir: str = \
            constant.PROJECT_HOME + '/' + \
            constant.ARTIFACT_SUBDIR
        """Private filepath to the directory with artifact files"""

        self._artifact_abi_filepath: str = \
            self._artifact_dir + '/' + \
            self._name + '.' + \
            constant.ABI_SUFFIX
        """Private filepath to the ABI file"""

        self._artifact_address_filepath: str = \
            self._artifact_dir + '/' + \
            self._name + '.' + \
            constant.ADDRESS_SUFFIX
        """Private filepath to the address file"""

        self._artifact_bytecode_filepath: str = \
            self._artifact_dir + '/' + \
            self._name + '.' + \
            constant.BYTECODE_SUFFIX
        """Private filepath to the bytecode file"""

        self._blockchain: constant.T_BLOCKCHAIN_OBJ = Blockchain()
        """Private :class:`Blockchain` object used to access
            blockchain methods"""

        self._web3e: constant.T_WEB3_EXC = web3e
        """Private instance to catch exceptions from Web3 API"""
        self._abi: List = self._get_artifact_abi()
        """Private contract Application Binary Interface"""
        self._bytecode: str = self._get_artifact_bytecode()
        """Private contract Bytecode"""

        # The following attributes are initialized to `None` or empty.
        # They are filled in with a `connect()` and this happens when
        # a user calls `connect()` or `deploy()` (a `deploy()` does
        # a `connect()`).
        self._deployed_code: constant.T_DEPLOYED_CODE = ''
        """Private contract code as deployed on blockchain"""
        self._address: str = ''
        """Private contract blockchain address"""
        self._web3_contract: constant.T_WEB3_CONTRACT_OBJ = None
        """Private instance of the ``web3._utils.datatypes.Contract``
            used to access methods for that object."""
        self._events: List = []
        """Private list of events emitted by the contract"""
        self._functions: List = []
        """Private list of functions provided by the contract"""
        self._size: int = 0
        """Private contract size on the blockchain, in bytes"""

    @property
    def abi(self) -> List:
        """Return the contract ABI (Application Binary Interface).

        :rtype: list
        :return: list with details of all function interfaces
        :example:
            >>> from simpleth import Contract
            >>> c = Contract('TestTrx')
            >>> c.abi
            [{'inputs': [{'internalType': 'int256', 'name':  ...snip...

        """
        return self._abi

    @property
    def address(self) -> str:
        """Return blockchain address of the deployed contract.

        :rtype: str
        :return: blockchain address of the contract
        :example:
            >>> from simpleth import Contract
            >>> c = Contract('TestTrx')
            >>> c.connect()
            >>> c.address
            '0x0F802Cf8C7929C5E0CC140314d1501e21b18a6A8'

        :notes: Returns empty string if no ``connect()`` was done.
        """
        return self._address

    @property
    def blockchain(self) -> constant.T_BLOCKCHAIN_OBJ:
        """Return `web3.py` ``blockchain`` object."""
        return self._blockchain

    @property
    def bytecode(self) -> str:
        """Return contract bytecode.

        :rtype: str
        :return: bytecode of contract
        :example:
            >>> from simpleth import Contract
            >>> c = Contract('TestTrx')
            >>> c.connect()
            >>> c.bytecode
            '6080604052602a60015534801561001557600080  ...snip...

        :notes: Contract bytecode is not the same as the contract
            :attr:`deployed_code`. The bytecode is larger and
            includes the instructions to deploy the contract.
        """
        return self._bytecode

    @property
    def deployed_code(self) -> constant.T_DEPLOYED_CODE:
        """Return contract bytecode as deployed on blockchain.

        :rtype: str
        :return: contract code as deployed on chain.
        :example:


        :notes:
            - :attr:`deployed_code` contains the bytes that
              are on the blockchain. This is the same as the
              :attr:`bytecode` without its additional code to deploy.

        """
        return self._deployed_code

    @property
    def events(self) -> List[str]:
        """Return the names of the events emitted by the contract.

        :rtype: list
        :return: the names of the events emitted by transactions in
             this contract
        :example:
            >>> from simpleth import Contract
            >>> c = Contract('TestTrx')
            >>> c.connect()
            >>> c.events
            ['NumsStored', 'TestTrxConstructed', 'TypesStored']

        """
        return self._events

    @property
    def functions(self) -> List[str]:
        """Return the names of the functions provided by this contract.

        :rtype: list
        :return: signatures of all public functions.
        :example:
            >>> from simpleth import Contract
            >>> c = Contract('TestTrx')
            >>> c.connect()
            >>> c.functions
            ['getContractSize(address)', 'getNum(uint8)',  ...snip...

        :notes:
            - The list of functions includes all transactions, all
              public functions, and all getters for public state
              variables.

        """
        return self._functions

    @property
    def name(self) -> str:
        """Return the name of the contract.

        :rtype: str
        :return: contract name
        :example:
            >>> from simpleth import Contract
            >>> c = Contract('TestTrx')
            >>> c.name
            'TestTrx'

        """
        return self._name

    @property
    def size(self) -> int:
        """Return deployed contract size.

        :rtype: int
        :return: size of the contract, in bytes
        :example:
            >>> from simpleth import Contract
            >>> c = Contract('TestTrx')
            >>> c.connect()
            >>> c.size
            2022

        :notes:
            - This is the number of bytes required to store the
              contract on the blockchain. It is the same as
              `len( `:attr:`deployed_code` `)`.
        """
        return self._size

    @property
    def web3_contract(self) -> constant.T_WEB3_CONTRACT_OBJ:
        """Return web3.py contract object.

        :rtype: object
        :return: ``web3.py`` ``contract`` object

        """
        return self._web3_contract

    @property
    def web3e(self) -> constant.T_WEB3_EXC:
        """Return web3.py Exceptions class.

        :rtype: object
        :return: web3 exception object

        """
        return self._web3e

    def call_fcn(
            self,
            fcn_name: str,
            *fcn_args: Optional[Union[int, str, float]]
            ) -> Union[int, str, list]:
        """Return results from calling a contract function.

        :param fcn_name: name of a function in the Solidity contract
        :type fcn_name: str
        :param fcn_args: argument(s), if any, required by the function
        :type fcn_args: int | float | str | None
        :raises SimplEthError:
            - if ``fcn_name`` is bad
            - if ``fcn_args`` are the wrong type or number
            - if contract has been destroyed

        :rtype: int | float | string | list
        :return: value returned from the Solidity function
        :Example:
            >>> from simpleth import Contract
            >>> c = Contract('testtrx')
            >>> c.connect()
            >>> c.call_fcn('getNum0')
            1
            >>> c.call_fcn('getNum', 2)
            3

        :notes:
            - Works for Solidity pure and view functions only.
            - ``fcn_name`` must match the spelling and capitalization of
              the function as specified in the Solidity contract.

        """
        try:
            fcn_return: Union[int, str, list] = getattr(
                self._web3_contract.functions,
                fcn_name
                )(*fcn_args).call()
        except AttributeError as exception:
            message: str = (
                f'ERROR in {self.name}().call_fcn().\n'
                f'AttributeError says: {exception}\n'
                f'HINT: Do you need to do a connect()?\n'
                )
            raise SimplEthError(message, code='C-010-010') from None
        except self._web3e.ValidationError as exception:
            message = (
                f'ERROR in {self.name}().call_fcn().\n'
                f'Function "{fcn_name}" was given bad arguments.\n'
                f'ValidationError says {exception}\n'
                f'HINT 1: Check you specified the correct number of '
                f'arguments.\n'
                f'HINT 2: Check you specified the correct types for the '
                f'arguments.\n'
                )
            raise SimplEthError(message, code='C-010-020') from None
        except self._web3e.BadFunctionCallOutput as exception:
            message = (
                f'ERROR in {self.name}().call_fcn().\n'
                f'Unable to call function {fcn_name}.\n'
                f'BadFunctionCallOutput says {exception}\n'
                )
            raise SimplEthError(message, code='C-010-030') from None
        except self._web3e.ContractLogicError as exception:
            message = (
                f'ERROR in {self.name}().call_fcn().\n'
                f'ContractLogicError says: {exception}\n'
                f'HINT: Did you use an out of bounds array index?\n'
                )
            raise SimplEthError(message, code='C-010-040') from None
        except TypeError as exception:
            message = (
                f'ERROR in {self.name}().call_fcn().\n'
                f'TypeError says: {exception}'
                )
            raise SimplEthError(message, code='C-010-050') from None
        return fcn_return

    def connect(self) -> str:
        """Enable the use of a deployed contract.

        After instantiating a :class:`Contract` object you must do a
        :meth:`connect()` to make it possible to use the methods for
        the contract. It is akin to doing a file `open()` to use a file.

        :rtype: str
        :return:  ``address`` of the contract

        :example:
            >>> from simpleth import Contract
            >>> c = Contract('testtrx')
            >>> c.connect()

        :notes:
            - Use :meth:`deploy` to install a contract onto the
              blockchain. Thereafter, use :meth:`connect` to use
              that contract.
            - You may have multiple instances of the contract on the
              blockchain. :meth:`connect()` will use the most recently
              deployed version.

        """
        self._address = self._get_artifact_address()
        self._web3_contract = self._blockchain.eth.contract(
            address=self.address,
            abi=self.abi
            )
        self._events = self._get_contract_events()
        self._functions = self._get_contract_functions()
        self._deployed_code = self._get_deployed_code()
        self._size = self._get_size()
        return self._address

    def deploy(
            self,
            sender: str,
            *constructor_args: Union[int, float, str, list],
            constructor_event_name: str = '',
            gas_limit: int = constant.GAS_LIMIT,
            max_priority_fee_gwei: Union[float, int] = constant.MAX_PRIORITY_FEE_GWEI,
            max_fee_gwei: Union[float, int] = constant.MAX_FEE_GWEI,
            ) -> constant.T_RESULT:
        """Deploy the contract onto the blockchain.

        :param sender: address of account requesting the deploy
        :type sender: str
        :param constructor_args: argument(s) for the contract
            constructor (optional)
        :type constructor_args: int, string, None
        :param constructor_event_name: Event name emitted by contract
            constructor (optional, default: `''`)
        :type constructor_event_name: str
        :param gas_limit: maximum amount of gas units allowed for the deploy
            (optional, default: :const:`constant.GAS_LIMIT`)
        :type gas_limit: int
        :param max_priority_fee_gwei: maximum ``sender`` will pay from
            account balance as a tip for a miner to mine this
            transaction, in gwei (optional, default:
            :const:`constant.MAX_PRIORITY_FEE_GWEI`)
        :type max_priority_fee_gwei: int
        :param max_fee_gwei: maximum ``sender`` will pay to have this
            transaction mined, in gwei (optional, default:
            :const:`constant.MAX_FEE_GWEI`)
        :type max_fee_gwei: int
        :rtype: Result
        :return: :class:`trx_result` holding the details of mining
            of this transaction

        :raises SimplEthError:
            - if unable to get artifact info and create contract class
            - if ``sender`` address is bad
            - if ``constructor_args`` are bad
            - if the `deploy` ran out of gas
            - if ``gas_limit`` was too high and exceeded the block
              limit

        :example:
            >>> from simpleth import Contract, Blockchain
            >>> c = Contract('testtrx')
            >>> c.connect()
            >>> user = Blockchain().accounts[0]
            >>> c.deploy(user, 20,
            ... constructor_event_name='TestTrxConstructed')
            {'address': '0x8DAEaf6D1e702Ab068BB9DED7026b8A3   ..snip..

        """
        trx_result: constant.T_RESULT = []
        try:
            self._web3_contract = self._blockchain.eth.contract(
                    abi=self.abi,
                    bytecode=self.bytecode
                    )
        except ValueError as exception:
            message: str = (
                f'ERROR in {self.name}().deploy(): '
                f'ValueError says {exception}\n'
                f'HINT: Did you use the correct contract name?\n'
                )
            raise SimplEthError(message, code='C-030-010') from None

        try:
            trx_hash: constant.T_HASH = \
                self._web3_contract.constructor(
                        *constructor_args
                    ).transact(
                        {
                            'from': sender,
                            'gas': gas_limit,
                            'maxFeePerGas': max_fee_gwei,
                            'maxPriorityFeePerGas': max_priority_fee_gwei
                        }
                    ).hex()
        except self._web3e.InvalidAddress:
            message = (
                f'ERROR in {self.name}().deploy(): '
                f'Used bad sender arg; not a valid address.\n'
                )
            raise SimplEthError(message, code='C-030-020') from None
        except TypeError as exception:
            message = (
                f'ERROR in {self.name}().deploy(): '
                f'TypeError says {exception}.\n'
                f'HINT: Check contract constructor args.\n'
                )
            raise SimplEthError(message, code='C-030-030') from None
        except ValueError as exception:
            message = (
                f'ERROR in {self.name}().deploy(): '
                f'ValueError says {exception}\n'
                f'HINT 1: If you specified a gas limit, did it exceed the '
                f'block limit?\n'
                f'HINT 2: You may have run out of gas. Try a higher '
                f'gas_limit.\n'
                )
            raise SimplEthError(message, code='C-030-040') from None

        try:
            trx_receipt = self._blockchain.eth.waitForTransactionReceipt(
                trx_hash,
                timeout=constant.TIMEOUT,
                poll_latency=constant.POLL_LATENCY
                )
        except self._web3e.TimeExhausted:
            # Timed out. Trx not yet mined. Return empty result
            return trx_result

        self._set_artifact_address(trx_receipt.contractAddress)
        self.connect()

        trx_result = _Result(
            'deploy',
            trx_hash,
            trx_receipt,
            self,
            self.web3_contract,
            constructor_event_name
            )
        return trx_result

    def get_gas_estimate(
            self,
            sender: str,
            trx_name: str,
            *args: Any
            ) -> int:
        """Return the units of gas estimated to run a transaction.

        Does not run the transaction. It estimates the gas that will be
        required to run the transaction with the given ``args``.

        :param sender: account address requesting the estimate
        :type sender: str
        :param trx_name: name of the transaction
        :type trx_name: str
        :param args: transaction arguments, if any
        :type args: int | float | str | None
        :rtype: int
        :return: estimated number of gas units to run the transaction
        :raises SimplEthError:
            - if ``trx_name`` is bad
            - if ``args`` are bad
            - if :meth:`connect` is needed
            - if ``sender`` is bad

        :example:
            >>> from simpleth import Contract
            >>> from simpleth import Blockchain
            >>> c = Contract('testtrx')
            >>> c.connect()
            >>> b = Blockchain()
            >>> user = b.accounts[0]
            >>> c.get_gas_estimate(user, 'storeNums', 1, 2, 3)
            38421

        """
        # TODO can you send a list as an arg? If so, add to the docstring
        # and Type Hints
        try:
            gas_estimate: int = getattr(
                self._web3_contract.functions,
                trx_name
                )(*args).estimateGas(
                    {
                        'from': sender
                    }
                    )
        except self._web3e.ABIFunctionNotFound:
            message: str = (
                f'ERROR in {self.name}().submit_trx(): '
                f'transaction {trx_name}() not found in contract.\n'
                f'HINT: Check spelling of transaction name.\n'
                )
            raise SimplEthError(message, code='C-040-010') from None
        except self._web3e.ValidationError:
            message = (
                f'ERROR in {self.name}().submit_trx(): '
                f'Wrong number or type of args for transaction "{trx_name}".\n'
                f'HINT: Check transaction definition in contract.\n'
                )
            raise SimplEthError(message, code='C-040-020') from None
        except self._web3e.BadFunctionCallOutput:
            message = (
                f'ERROR in {self.name}().submit_trx(): '
                f'Can not run transaction {trx_name}.\n'
                f'HINT 1: Has the contract been destroyed?\n'
                f'HINT 2: If you just switched Ganache workspace, has '
                f'        the contract been deployed yet?\n'
                )
            raise SimplEthError(message, code='C-040-030') from None
        except self._web3e.ContractLogicError as exception:
            message = (
                f'ERROR in {self.name}().submit_trx(): '
                f'ContractLogicError says: {exception}\n'
                f'HINT: Did you use an out of bounds index value?\n'
                )
            raise SimplEthError(message, code='C-040-040') from None
        except self._web3e.InvalidAddress:
            message = (
                f'ERROR in {self.name}().submit_trx(): '
                f'sender arg has a bad address.\n'
                )
            raise SimplEthError(message, code='C-040-050') from None
        except AttributeError:
            message = (
                f'ERROR in {self._name}().submit_trx(): '
                f'Contract does not have a valid contract object.\n'
                f'HINT: Do you need to do a connect()?\n'
                )
            raise SimplEthError(message, code='C-040-060') from None
        except TypeError:
            message = (
                f'ERROR in {self.name}().submit_trx(): '
                f'Bad type for trx_name: "{trx_name}"\n'
                f'HINT 1: Check transaction argument types.\n'
                f'HINT 2: Check all transaction arguments were specified.\n'
                )
            raise SimplEthError(message, code='C-040-070') from None
        except ValueError as exception:
            value_error_message: str = \
                dict(exception.args[0])['message']
            if 'revert' in value_error_message:
                revert_message: str = self._format_revert_message(
                    value_error_message
                    )
                raise SimplEthError(revert_message, code='C-040-080') from None

            message = (
                f'ERROR in {self.name}().get_gas_estimate(): '
                f'ValueError says {value_error_message}\n'
                f'HINT 1: Did you divide by zero?\n'
                f'HINT 2: Did you pass in an out-of-bounds array index?\n'
                f'HINT 3: Did you pass in a bad address?\n'
                )
            raise SimplEthError(message, code='C-040-090') from None
        return gas_estimate

    def get_trx_result(
            self,
            trx_hash: constant.T_HASH,
            trx_name: str,
            event_name: str = ''
            ) -> constant.T_RESULT:
        """Return the results of a transaction.

        This is used after :meth:`submit_trx` to get the results of the
        transaction. If the transaction is not yet mined, the results
        will be empty.

        If a valid ``event_name`` is provided, the event args will be
        included in the results.

        :param trx_hash: transaction hash from :meth:`submit_trx`
        :type trx_hash: str
        :param trx_name: transaction name
        :type trx_name: str
        :param event_name: event name, if any, emitted by this
            transaction (optional, default: `''`)
        :type event_name: str
        :rtype: object
        :return: :class:`Result` with transaction outcome
        :example:
            >>> from simpleth import Contract
            >>> from simpleth import Blockchain
            >>> c = Contract('testtrx')
            >>> c.connect()
            >>> b = Blockchain()
            >>> user = b.accounts[0]
            >>> t_hash = c.submit_trx(user, 'storeNums', 7, 8, 9)
            >>> c.get_trx_result(
            ...     t_hash,
            ...     'storeNums',
            ...     event_name='NumsStored'
            ...     )
            {'address': None, 'gas_used': 83421,  ...snip...

        :notes:
            - ``trx_name`` must match the name used in :meth:`submit_trx`.
            - Only the event args from the ``trx_name`` transaction are
              returned in ``Result``. If this transaction, in turn
              calls other transactions, those subsequent transactions
              may have their own events, but they will not be returned
              as part of the ``Result``.

        :see also:
            - :meth:`submit_trx` for submitting a transaction to be
              mined and returning the ``trx_hash``.
            - :meth:`get_trx_result_wait` which will make repeated
              checks on the transaction and returns when the mining
              has completed (or it has timed out).

        """
        try:
            trx_receipt = self._blockchain.eth.getTransactionReceipt(
                trx_hash
                )
        except self._web3e.TransactionNotFound:
            # Receipt not found. Not yet mined. Will return empty trx_result
            trx_result: Optional[constant.T_RESULT] = None
        else:
            trx_result = _Result(
                trx_name,
                trx_hash,
                trx_receipt,
                self,
                self._web3_contract,
                event_name
                )
        return trx_result

    def get_trx_result_wait(
            self,
            trx_hash: constant.T_HASH,
            trx_name: str,
            event_name: str = '',
            timeout: Union[int, float] = constant.TIMEOUT,
            poll_latency: Union[int, float] = constant.POLL_LATENCY
            ) -> constant.T_RESULT:
        """Wait for transaction to be mined and then return the results
           of that transaction.

        This is used after :meth:`submit_trx` to get the results of the
        transaction. Will block the caller and wait until either the
        transaction is mined or ``timeout`` is reached. The results
        will be empty if it returns after timing out.

        If a valid ``event_name`` is provided, the event args will be
        included in the results.

        Setting ``timeout`` and ``poll_latency`` gives the caller
        flexiblity in the timing of checking for the transaction
        completion.

        :param trx_hash: transaction hash
        :type trx_hash: str
        :param trx_name: transaction name
        :type trx_name: str
        :param event_name: event name, if any, emitted by this
            transaction (optional, default: ``None``)
        :type event_name: str
        :param timeout: maximum number of seconds to wait for
            mining to finish
            (optional, default: :const:`constant.TIMEOUT`)
        :type timeout: int | float
        :param poll_latency: number of seconds between checking
            for transaction completion (optional, default:
            :const:`constant.POLL_LATENCY`)
        :type poll_latency: int | float
        :rtype: Result
        :return: :class:`Result` with transaction outcomes
        :example:
            >>> from simpleth import Blockchain, Contract
            >>> c = Contract('TestTrx')
            >>> c.connect()
            >>> b = Blockchain()
            >>> user = b.accounts[0]
            >>> t_hash = c.submit_trx(user, 'storeNums', 7, 8, 9)
            >>> r = c.get_trx_result_wait(
            ...     t_hash,
            ...     'storeNums',
            ...     event_name='NumsStored'
            ...     )
            >>> print(r)
            Address        = None
            Gas used       = 38463
            Gas price      = 20000000000
            Value          = 0
            Block number   = 170
            Trx hash       = 0x17dfef38cc30a8e4cb486f73ac60ec0fe   ..snip...
            Event name     = NumsStored
            Event args     =
                num0 : 7
                num1 : 8
                num2 : 9

        :notes:
            - ``event_name`` must match the spelling and capitalization
              of an event in the Solidity function.
            - Typically, :meth:`get_trx_result_wait` is used following
              :meth:`submit_trx` which sends the transaction to be mined
              and returns the ``trx_hash``.
            - Only the event args from the `trx_name` transaction are
              returned in ``Result``. If this transaction, in turn
              calls other transactions, those subsequent transactions
              may have their own events, but they will not be returned
              as part of the ``Result``.
            - If it times out, you can use :meth:`get_trx_result` or
              :meth:`get_trx_result_wait` to continue periodicall
              checking for completion.

        :see also:
            - :meth:`submit_trx` for submitting a transaction to be
              carried out and mined and returning the ``trx_hash``.
            - :meth:`get_trx_result` which will make one check and
              either return the results or an empty ``Result``.
            - :meth:`run_trx` which combines the call to
              :meth:`submit_trx` and :meth:`get_trx_result_wait`.

        """
        try:
            trx_receipt = self._blockchain.eth.waitForTransactionReceipt(
                trx_hash,
                timeout=timeout,
                poll_latency=poll_latency
                )
        except self._web3e.TimeExhausted:
            # Timed out. Trx not yet mined. Will return None for trx_result.
            return None
        else:
            trx_result: constant.T_RESULT = _Result(
                trx_name,
                trx_hash,
                trx_receipt,
                self,
                self.web3_contract,
                event_name
                )
        return trx_result

    def get_var(
            self,
            var_name: str,
            *args: Any
            ) -> Optional[Union[int, float, str, list]]:
        """Return the value of a contract variable.

        :param var_name: variable name of a public state variable
        :type var_name: str
        :param args: args for the variable, typically an index value
            into an array (optional)
        :type args: int | float | str
        :rtype: int | string | float | list | None
        :return: value of the variable
        :raises SimplEthError:
            - if ``var_name`` is bad
            - if ``args`` specifies an out of bound index value
            - if a :meth:`connect` is needed

        :example:
            >>> from simpleth import Contract
            >>> c = Contract('testtrx')
            >>> c.get_var('specialNum')
            42

        :notes:
            - Uses the built-in Solidity public getter.

        """
        # TODO - what are the possible types for args? Just int?
        try:
            var_value: Union[int, str, float, list] = getattr(
                self._web3_contract.functions,
                var_name
                )(*args).call()
        except self._web3e.ABIFunctionNotFound as exception:
            message: str = (
                f'ERROR in {self.name}().getvar(): '
                f'Unable to get public state variable {var_name}.\n'
                f'ABIFunctionNotFound says {exception}\n'
                f'HINT: Check spelling of variable name.\n'
                )
            raise SimplEthError(message, code='C-060-010') from None
        except self._web3e.BadFunctionCallOutput as exception:
            message = (
                f'ERROR in {self.name}().getvar(): '
                f'Unable to get variable {var_name}.\n'
                f'BadFunctionCallOutput says {exception}\n'
                f'HINT: Check spelling of variable name.\n'
                )
            raise SimplEthError(message, code='C-060-020') from None
        except self._web3e.ValidationError as exception:
            message = (
                f'ERROR in {self.name}().getvar(): '
                f'Unable to get public state variable {var_name}.\n'
                f'ValidationError says: {exception}\n'
                )
            raise SimplEthError(message, code='C-060-030') from None
        except self._web3e.ContractLogicError as exception:
            message = (
                f'ERROR in {self.name}().getvar(): '
                f'Unable to get public state variable {var_name}.\n'
                f'ContractLogicError says: {exception}\n'
                f'HINT: Did you use an out of bounds index value?\n'
                )
            raise SimplEthError(message, code='C-060-040') from None
        except AttributeError as exception:
            message = (
                f'ERROR in {self.name}().getvar(): '
                f'Unable to get public state variable {var_name}.\n'
                f'AttributeError says: {exception}\n'
                f'HINT: Do you need to do a connect()?\n'
                )
            raise SimplEthError(message, code='C-060-050') from None
        return var_value

    def run_trx(
            self,
            sender: str,
            trx_name: str,
            *args: Any,
            event_name: str = '',
            gas_limit: int = constant.GAS_LIMIT,
            max_priority_fee_gwei: Union[int, float] = constant.MAX_PRIORITY_FEE_GWEI,
            max_fee_gwei: Union[int, float] = constant.MAX_FEE_GWEI,
            value_wei: int = 0,
            timeout: Union[int, float] = constant.TIMEOUT,
            poll_latency: Union[int, float] = constant.POLL_LATENCY
            ) -> constant.T_RESULT:
        """"Send a transaction and return the results.

        This is the method typically used for running transactions.

        :meth:`run_trx` is a combination of :meth:`submit_trx` and
        :meth:`get_trx_result_wait`. The caller uses a single method
        to submit a transaction to the blockchain and get back the
        results of the transaction after it is mined.

        The caller is blocked until :meth;`run_trx` returns or times out.

        :param sender: address of account requesting transaction
        :type sender: str
        :param trx_name: name of transaction
        :type trx_name: str
        :param args: argument(s) required by the transaction (optional, default: none)
        :type args: int | float | string | list
        :param event_name: event name emitted by this transaction
            (optional, default: `''`)
        :type event_name: str
        :param gas_limit: max gas sender will allow for this
            transaction in units of gas (optional, default:
            :const:`constant.GAS_LIMIT`)
        :type gas_limit: int
        :param max_priority_fee_gwei: max amount of Ether (in gwei) the
            sender will pay as a tip
        :type max_priority_fee_gwei: int | float
        :param max_fee_gwei: max amount of Ether (in gwei) the sender
            will pay for the transaction
        :type max_fee_gwei: int | float
        :param value_wei: amount of Ether (in wei) to be sent with the
            transaction (optional, default: `0`)
        :type value_wei: int
        :param timeout: maximum number of seconds to wait for
            mining to finish
            (optional, default: :const:`constant.TIMEOUT`)
        :type timeout: int | float
        :param poll_latency: number of seconds between checking
            for transaction completion (optional, default:
            :const:`constant.POLL_LATENCY`)
        :type poll_latency: int | float
        :rtype: Result
        :return: :class:``Result`` with transaction result
        :raises SimplEthError:
            - if no ``trx_hash`` was returned from :meth:`submit_trx`

        :example:
            >>> from simpleth import Blockchain, Contract
            >>> c = Contract('TestTrx')
            >>> c.connect()
            >>> b = Blockchain()
            >>> user = b.accounts[0]
            >>> results = c.run_trx(
            ...     user,
            ...     'storeNums',
            ...     2, 4, 6,
            ...     event_name='NumsStored'
            ...     )
            >>> print(results)
            Address        = None
            Gas used       = 38463
            Gas price      = 20000000000
            Value          = 0
            Block number   = 171
            Trx hash       = 0xfbdcf37404df872274f021574e23   ..snip...
            Event name     = NumsStored
            Event args     =
                num0 : 2
                num1 : 4
                num2 : 6

        :see also:
            - Since :meth:`run_trx` is a combination of
              :meth:`submit_trx` and :meth:`get_trx_result_wait` see
              the `Extended Summary` and `Notes` sections of both of
              those for more explanation of fees, value, timing, and
              other args.

        """
        trx_hash: constant.T_HASH = self.submit_trx(
            sender,
            trx_name,
            *args,
            gas_limit=gas_limit,
            max_priority_fee_gwei=max_priority_fee_gwei,
            max_fee_gwei=max_fee_gwei,
            value_wei=value_wei
            )
        if not trx_hash:
            message = (
                f'ERROR in {self.name}().run_trx():\n'
                f'No transaction hash was returned after submit_trx() of '
                f'transaction: {trx_name}.\n'
                )
            raise SimplEthError(message, code='C-070-010') from None

        trx_result: constant.T_RESULT = self.get_trx_result_wait(
            trx_hash,
            trx_name,
            event_name=event_name,
            timeout=timeout,
            poll_latency=poll_latency
            )
        if not trx_result:
            message = (
                f'ERROR in {self.name}().run_trx():\n'
                f'No trx results were returned from '
                f'get_trx_result_wait() for transaction "{trx_name}" '
                f'when it timed out after {timeout} seconds.\n'
                f'trx_hash = {trx_hash}\n'
                f'Use get_trx_result() or get_trx_result_wait() with '
                f'that hash to get the results.\n'
                f'In the future, consider:\n'
                f'HINT 1: Use a higher value for the timeout parameter.\n'
                f'HINT 2: Make sure poll_frequency is less than the '
                f'timeout.\n'
                )
            raise SimplEthError(message, code='C-070-020') from None
        return trx_result

    def submit_trx(
            self,
            sender: str,
            trx_name: str,
            *args: Any,
            gas_limit: int = constant.GAS_LIMIT,
            max_priority_fee_gwei: Union[int, float] = constant.MAX_PRIORITY_FEE_GWEI,
            max_fee_gwei: Union[int, float] = constant.MAX_FEE_GWEI,
            value_wei: int = 0
            ) -> constant.T_HASH:
        """Send a transaction to this contract.

        This is used to request a contract carry out a transaction.

        This method returns immediately. It does not check to see if
        transaction was mined nor if it was successful. You can
        follow up with either :meth:`get_trx_results()` or
        :meth'get_trx_results_wait` to check for the completion of
        the transaction.

        About the fees:

            -  ``max_fee_gwei`` = `Base Fee` + ``max_priority_fee``
            -  The `Base Fee` is set by the network and is adjusted after each block
               based on transaction volume. Paying the Base Fee is mandatory.
            -  The `Priority Fee` is the tip you can offer to the miners to attract
               their attention to your transaction. It is also call a `'tip'`.
               Paying the Priority Fee is optional but might be a near necessity
               if the network is busy with a high transaction volume. In that
               case, miners will be processing transactions with tips and ignoring
               low- or no-tip transactions.
            -  ``max_fee_gwei`` is the maximum you will spend and ``max_priority_fee``
               is the most you will offer a miner. If the Base Fee being charged
               by the network is higher than expected, your Priority Fee may be cut.
            -  https://www.blocknative.com/blog/eip-1559-fees has a more thorough
               explanation plus a recommended Max Fee to use: double the current
               Base Fee and add the most you would like to tip. In other words:
               ``max_fee_gwei`` = (2 * current `Base Fee`) + ``max_priority_fee_gwei``

        :param sender: address of account requesting transaction
        :type sender: str
        :param trx_name: name of transaction
        :type trx_name: str
        :param args: argument(s) required by the transaction (optional)
        :type args: int | string
        :param gas_limit: max gas sender will allow for thexi
            transaction in units of gas(optional, default is
            :const:`constant.GAS_LIMIT`)
        :type gas_limit: int
        :param max_priority_fee_gwei: max amount of Ether (in gwei) the
            sender will pay as a tip
        :type max_priority_fee_gwei: int | float
        :param max_fee_gwei: max amount of Ether (in gwei) the sender
            will pay for the transaction
        :type max_priority_fee_gwei: int | float
        :param value_wei: amount of Ether (in wei) to be sent with the
            transaction (optional, default: `0`)
        :type value_wei: int
        :rtype: str
        :return: ``trx_hash``
        :raises SimplEthError:

            -  if ``trx_name`` is bad
            -  if ``args`` are missing, wrong number of args, or wrong type
            -  if ``args`` had an out of bounds index value for an array
            -  if ``sender`` is a bad address
            -  if :meth:`connect` is needed
            -  if ``args`` caused a divied-by-zero in the transaction
            -  if ``gas_limit`` was too low and you ran out of gas
            -  if a transaction `Guard` failed and the transaction was
               reverted
            -  if a transaction `require()` failed and the transaction
               was reverted

        :example:
            >>> from simpleth import Blockchain, Contract
            >>> c = Contract('TestTrx')
            >>> b = Blockchain()
            >>> c.connect()
            >>> user = b.accounts[0]
            >>> c.submit_trx(user, 'storeNums', 4, 5, 6)
            HexBytes('0x6fc9deaf6052504a8  ..snip.. 50af2cb320278b476')

        :notes:

            -  These are Type 2 transactions which conform to EIP-1559 (aka
               the London Fork). They use the new max fee and max priority
               fee fields instead of a gas price field.
            -  ``trx_hash`` is the transaction hash that can be used
               to check for the transaction outcome in :meth:`get_trx_result`
               or :meth:get_trx_result_wait`
            -  ``trx_name`` must match the spelling and capitalization
               of a function in the Solidity contract.
            -  ``value`` is Ether that is sent to the transaction. It is
               a payment from the sender to the contract. The transaction
               should be defined as a `payable` function in the Solidity
               contract or the contract will need a TODO (what's the
               default payable thing?)

        :warnings: I'm making the assumption that all `ValueError`
            exceptions that contain `revert` in their message are due
            to those `Guard` modifiers. I'm just going by all my
            testing. So far, this seems to be the case. However,
            there may be other type(s) of `ValueError(s)` that say
            `revert` and are not due to a Guard modifier failing.
            If you see one, add it to the lengthy code of all the
            exceptions.

        :see also:

            -  :meth:`get_trx_result` and :meth:`get_trx_result_wait`
               to retrieve the result of the transaction using the
               ``trx_hash``.
            -  :meth:`run_trx` which combines the call to
               :meth:`submit_trx` with a call to
               :meth:`get_trx_result_wait`.

        """
        try:
            trx_hash: constant.T_HASH = getattr(
                self._web3_contract.functions,
                trx_name
                )(*args).transact(
                    {
                        'from': sender,
                        'gas': gas_limit,
                        'maxFeePerGas': max_fee_gwei,
                        'maxPriorityFeePerGas': max_priority_fee_gwei,
                        'value': value_wei
                    }
                    ).hex()
        except self._web3e.ABIFunctionNotFound:
            message: str = (
                f'ERROR in {self.name}().submit_trx(): '
                f'transaction {trx_name}() not found in contract.\n'
                f'HINT: Check spelling of transaction name.\n'
                )
            raise SimplEthError(message, code='C-080-010') from None
        except self._web3e.ValidationError:
            message = (
                f'ERROR in {self.name}().submit_trx(): '
                f'Wrong number or type of args for transaction "{trx_name}".\n'
                f'HINT: Check parameter definition(s) of transaction in '
                f'contract.\n'
                )
            raise SimplEthError(message, code='C-080-020') from None
        except self._web3e.BadFunctionCallOutput:
            message = (
                f'ERROR in {self.name}().submit_trx(): '
                f'Can not run transaction {trx_name}.\n'
                f'HINT 1: Has the contract been destroyed?\n'
                f'HINT 2: If you just switched Ganache workspace, has '
                f'        the contract been deployed yet?\n'
                )
            raise SimplEthError(message, code='C-080-030') from None
        except self._web3e.ContractLogicError as exception:
            message = (
                f'ERROR in {self.name}().submit_trx(): '
                f'ContractLogicError says: {exception}\n'
                f'HINT: Did you use an out of bounds index value?\n'
                )
            raise SimplEthError(message, code='C-080-040') from None
        except self._web3e.InvalidAddress:
            message = (
                f'ERROR in {self.name}().submit_trx(): '
                f'sender arg has a bad address.\n'
                )
            raise SimplEthError(message, code='C-080-050') from None
        except AttributeError:
            message = (
                f'ERROR in {self.name}().submit_trx(): '
                f'Contract does not have a valid contract object.\n'
                f'HINT: Do you need to do a connect()?\n'
                )
            raise SimplEthError(message, code='C-080-060') from None
        except TypeError:
            message = (
                f'ERROR in {self.name}().submit_trx(): '
                f'Bad type for trx_name: "{trx_name}"\n'
                f'HINT 1: Check transaction argument types.\n'
                f'HINT 2: Check all transaction arguments were specified.\n'
                )
            raise SimplEthError(message, code='C-080-070') from None
        except ValueError as exception:
            value_error_message: str = \
                dict(exception.args[0])['message']
            if 'revert' in value_error_message:
                message = self._format_revert_message(value_error_message)
            else:
                message = (
                    f'ERROR in {self.name}().submit_trx(): '
                    f'ValueError says {value_error_message}\n'
                    f'HINT 1: Did you divide by zero?\n'
                    f'HINT 2: Did you pass in an out-of-bounds array index?\n'
                    f'HINT 3: Did you pass in a bad sender address?\n'
                    f'HINT 4: If base fee exceeds gas limit, you ran out '
                    f'of gas. Use a higher gas_limit.\n'
                    f'HINT 5: If you exceeded block gas limit, you set the '
                    f'gas_limit too high. Use a lower gas_limit.\n'
                    f'HINT 6: Fee args need to be integers. Did you use '
                    f'float?\n'
                    )
            raise SimplEthError(message, code='C-080-080') from None
        return trx_hash

    def _format_revert_message(self, value_error_msg: str) -> str:
        """Return a message to explain why a transaction was reverted.

        A `ValueError` exception message will have one of two strings
        that will be reformatted:
        1) 'VM Exception while processing transaction: revert
           <modifier's message>'
        2) 'VM Exception while processing transaction: revert'

        The first is due to a `GUARD` modifier and the failure reason is
        the <modifier's message>, which comes from the Solidity code.
        This is the more typical case.

        The second is due to a transaction being reverted. So far, the
        only reason I have seen that is when the initial transaction
        calls other transactions and one of those called transactions
        fails.

        This method will parse the ValueError message, determine
        which of the conditions caused the exception, and return an
        explanation the caller can put in the ``SimplEthError`` back to
        the user.

        :param value_error_msg: `ValueError` exception message.
        :type value_error_msg: str
        :rtype: str
        :return: message explaining the Solidity transaction revert

        :note: This is the method that adds the eye catcher, `GUARDMSG:`,
            that appears in the SimplEthError explanation message
            to flag a transaction was stopped because it failed to
            pass one of the pre-conditions in a modifier for the
            contract.  You can change this eye catcher but some apps
            may be watching for that string.

        """
        # TODO - what happens when a contract transaction assert()
        # fails? Does that go through this as well?
        # TODO - does this get called when a transaction sends
        # Ether to a non-payable contract? If so, update the docstrings
        # to explain that as well.
        revert_reason: str = value_error_msg.split('revert')[1].strip()
        if revert_reason == '':
            revert_message: str = (
                f'Transaction from {self._name} was reverted. '
                f'Possible reasons:\n'
                f'1) This trx called another trx which failed.\n'
                f'2) Attempt to send Ether to non-payable trx.\n'
                )
        else:
            revert_message = 'GUARDMSG: ' + revert_reason
        return revert_message

    def _get_artifact_abi(self) -> List[str]:
        """ Return the contract abi saved in the abi file.

        When the Solidity compiler runs it writes the abi to the
        `<contract>.abi` file in the artifact directory.

        Open the file, read the abi, and return to caller.

        :rtype: list
        :return: `abi` for the contract found in the `artifact`
            directory

        :raises SimplEthError: if abi artifact file not found

        """
        try:
            with open(
                self._artifact_abi_filepath,
                encoding='UTF-8'
            ) as abi_file:
                abi: constant.T_ABI = json.load(abi_file)
        except FileNotFoundError:
            message: str = (
                f'ERROR in {self.name}()._get_artifact_abi(). '
                f'Unable to read ABI file.\n'
                f'Full path: {self._artifact_abi_filepath}\n'
                f'HINT 1: Check the spelling of the contract name.\n'
                f'HINT 2: You may need to do a new compile.\n'
                )
            raise SimplEthError(message, code='C-100-010') from None
        return abi

    def _get_artifact_address(self) -> str:
        """Return the contract blockchain address saved in the address
        file.

        The address is stored in the <contract>.addr file in the artifact
        directory.

        This address is written to the file when the contract is deployed.

        Open the file, get the address, and return it.

        :rtype: str
        :return: Blockchain address of the contract.
        :raises SimplEthError:

            -  if artifact address file is not found.
            -  if the address is not valid.

        """
        try:
            with open(
                self._artifact_address_filepath,
                encoding='UTF-8'
            ) as address_file:
                artifact_address: str = address_file.read().rstrip()
        except FileNotFoundError:
            message: str = (
                f'ERROR in {self.name}()._get_artifact_address(): '
                f'Unable to read address file.\n'
                f'Full path: {self._artifact_address_filepath}\n'
                f'Either using bad contract name or file does not exist.\n'
                f'HINT: Deploy() might fix missing file.\n'
                )
            raise SimplEthError(message, code='C-110-010') from None

        if not self._blockchain.is_valid_address(artifact_address):
            message = (
                f'ERROR in {self.name}()._get_artifact_address(): '
                f'Address for contract {self.name} is invalid.\n'
                f'Address read from file: {artifact_address}.\n'
                )
            raise SimplEthError(message, code='C-110-020') from None
        return artifact_address

    def _get_artifact_bytecode(self) -> str:
        """ Return the contract bytecode saved in the bytecode file.

        When the Solidity compiler runs it writes the bytecode to the
        `<contract>.bytecode` file in the artifact directory.

        Open the file, read the bytecode, and return to caller.

        :rtype: str
        :return: bytecode for the contract found in the `artifact`
                directory

        """
        try:
            with open(
                self._artifact_bytecode_filepath,
                encoding='UTF-8'
            ) as bytecode_file:
                bytecode: constant.T_BYTECODE = bytecode_file.read()
        except FileNotFoundError:
            message: str = (
                f'ERROR in {self.name}()._get_artifact_bytecode(): '
                f'Unable to read bytecode file for {self.name}.\n'
                f'Full path: {self._artifact_bytecode_filepath}\n'
                f'HINT: You may need to do a new compile.\n'
                )
            raise SimplEthError(message, code='C-120-010') from None
        return bytecode

    def _get_contract_events(self) -> List[str]:
        """Return the events emitted by the contract.

        :rtype: list
        :return: events, if any, defined in the Solidity contract
        :raises SimplEthError: if a :meth:`connect` is needed

        """
        try:
            events = self.web3_contract.events
        except AttributeError as exception:
            message: str = (
                f'ERROR in {self.name}()._get_contract_events(): '
                f'AttributeError says {exception}\n'
                f'HINT: Did you do a connect()?\n'
                )
            raise SimplEthError(message, code='C-130-010') from None
        event_list: List = [
            str(event).
            removeprefix("<class 'web3._utils.datatypes.").
            removesuffix("'>")
            for event in events
            ]
        return event_list

    def _get_contract_functions(self) -> List[str]:
        """Return the functions for the contract.

        :rtype: list
        :return: functions defined in the Solidity contract.
        :raises SimplEthError: if a :meth:`connect` is needed

        """
        try:
            function_list: List[str] = self._web3_contract.all_functions()
        except AttributeError as exception:
            message: str = (
                f'ERROR in {self.name}()._get_contract_functions(): '
                f'AttributeError says {exception}\n'
                f'HINT: Did you do a connect()?\n'
                )
            raise SimplEthError(message, code='C-140-010') from None
        else:
            functions: List[str] = [
                str(f).removeprefix('<Function ').removesuffix('>')
                for f in function_list
                ]
        return functions

    def _get_deployed_code(self) -> constant.T_DEPLOYED_CODE:
        """Return the bytecode at the `contract` `address` on the
        blockchain.

        :rtype: HexBytes
        :return: bytes of Solidity code deployed on chain for the
            contract
        :note:

            -  `bytecode` returned by :meth:`bytecode` contains the
               instructions for the contract plus the instructions
               to do the deployment of the contract.
               the `bytecode` returned by :meth:`deployed_code` and
               by this method is the same contract code as it is
               stored on the blockchain without the instructions for
               deployment.
            -  Type hint of `any` since `HexBytes` does not have a
               hint defined.

        """
        deployed_code: constant.T_DEPLOYED_CODE = \
            self._blockchain.eth.getCode(self.address).hex()
        return deployed_code

    def _get_size(self) -> int:
        """Return the size, in bytes, of the deployed contract
        bytecode.

        :rtype: int
        :return: number of bytes the `contract` uses on the blockchain.

        """
        return len(self._deployed_code)

    def _set_artifact_address(self, contract_address: str) -> bool:
        """Save the contract address in the address artifact file

        :param contract_address: address of the deployed contract
        :type contract_address: str
        :rtype: bool
        :return: ``True`` if successfully set the address
        :raises SimplEthError:

            -  if ``contract_address`` is bad
            -  if unable to write to the artifact `address` file

        """
        if not self._blockchain.is_valid_address(contract_address):
            message: str = (
                f'ERROR in {self.name}()._set_artifact_address(): '
                f'Address for contract {self.name} is invalid.\n'
                f'Address was not written to address file.\n'
                )
            raise SimplEthError(message, code='C-150-010') from None

        try:
            with open(
                self._artifact_address_filepath,
                'w',
                encoding='UTF-8'
            ) as address_file:
                address_file.write(contract_address)
        except FileNotFoundError:
            message = (
                f'ERROR in {self.name}()._set_artifact_address(): '
                f'Unable to write address file for {self.name}.\n'
                f'Full path: {self._artifact_address_filepath}'
                )
            raise SimplEthError(message, code='C-150-020') from None
        return True
# end Contract()


class Filter:
    """Create event filter and use to search for events

    """
    def __init__(self, contract: Contract) -> None:
        """Create instance for filters using the contract instance.

        This ``Filter`` will be used to find events emitted by
        ``Contract`` transactions.

        :param contract: contract object created by ``Contract``
        :type contract: Contract
        :example:

        """
        self._contract: Contract = contract
        self._web3_contract: constant.T_WEB3_CONTRACT_OBJ = \
            self._contract.web3_contract

    def create_filter(self, event_name: str) -> constant.T_FILTER_OBJ:
        """Return a filter used to watch for a specific event.

        Create a filter to be used when watching for future emissions
        of ``event_name``.

        Use the filter in :meth:`get_new_events` to watch for the
        ``event_name`` being emitted.

        :param event_name: name of the event emitted by this contract
        :type event_name: str
        :rtype: object
        :return: `event_filter` object
        :raises SimplEthError:

            -  if ``event_name`` is bad
            -  if a :meth:`connect` is needed

        :example:


        :see also:

            -  :meth:`get_new_events()` for using this new `event_filter`
               to watch for the event.
            -  :attr:`events` for the list of valid events emitted by this
               contract.

        """
        try:
            event_filter: constant.T_FILTER_OBJ = getattr(
                self._web3_contract.events,
                event_name
                )().createFilter(fromBlock='latest')
        except self._contract.web3e.ABIEventFunctionNotFound:
            message: str = (
                f'ERROR in create({event_name}).\n'
                f'The event: {event_name} was not found.\n'
                f'Valid event_names: {self._contract.events}\n'
                f'HINT: Check the spelling of your event_name.\n'
                )
            raise SimplEthError(message, code='F-020-010') from None
        except AttributeError as exception:
            message = (
                f'ERROR in create({event_name}).\n'
                f'Attribute Error says: {exception}.\n'
                f'HINT: Did you do a connect()?\n'
                )
            raise SimplEthError(message, code='F-020-020') from None
        return event_filter

    def get_new_events(self, event_filter: constant.T_FILTER_OBJ) -> List:
        """Search newly mined blocks for a specific event.

        Each call checks the blocks mined since the previous call.

        :param event_filter: specifies the event to find
        :type event_filter: object
        :rtype: list
        :return:

            -  list with one item for each event emitted since the
               previous call
            -  empty list if no events were emitted since previous call

        :example:

        :notes:

            -  ``event_filter`` is created by using
               :meth:`create_event_filter`.
            -  The first time it is called it will return an empty list.
               The second,and each subsequent, time it is called
               it checks the blocks mined since the previous call.
            -  :meth:`get_past_events` looks backward and searches old
               blocks. :meth:`get_new_events` looks forward at the
               newly mined blocks.
            -  Filters can be more sophisticated than just searching
               backwards based on the ``event_name``. The `web3.py` API
               documentation describes the full power at
               https://web3py.readthedocs.io/en/stable/web3.eth.html#filters.
               :attr:`Blockchain.eth` can be used to access the methods
               described.

        :see also: :meth:`create_event_filter` to create ``event_filter``.

        """
        filter_list: constant.T_FILTER_LIST = event_filter.get_new_entries()
        return self._create_simple_events(filter_list)

    def get_old_events(
            self,
            event_name: str,
            num_preceding_blocks: int
            ) -> List:
        """Search previously mined blocks for a specific event.

        :param event_name: name of the event to find
        :type event_name: str
        :param num_preceding_blocks: number of mined blocks to search
        :type num_preceding_blocks: int
        :rtype: list
        :return:

            -  list with one item holding the details for each
               event found
            -  empty list if no events were found

        :raises SimplEthError:

            -  if ``event_name`` was bad
            -  if no :meth:`connect`

        :example:

        :notes:

            -  Unlike :meth:`get_new_events`, an `event_filter` is not
               needed. This method builds its own event filter based on
               ``event_name``.
            -  :meth:`get_past_events` looks backward and searches old
               blocks. :meth:`get_new_events` looks forward at the
               newly mined blocks.
            -  Filters can be more sophisticated than just searching
               backwards based on the ``event_name``. The `web3.py` API
               documentation describes the full power at
               https://web3py.readthedocs.io/en/stable/web3.eth.html#filters.
               :attr:`Blockchain.eth` can be used to access the methods
               described.

        """
        latest_block: int = self._contract.blockchain.block_number
        if not 1 <= num_preceding_blocks <= latest_block:
            message: str = (
                f'ERROR in get_old_events({event_name}).\n'
                f'num_preceding_blocks = {num_preceding_blocks} is invalid.\n'
                f'It must be between 1 and {latest_block} (the latest block '
                f'on the chain).\n'
                f'HINT: Provide a valid number for num_preceding_blocks.\n'
                )
            raise SimplEthError(message, code='F-030-010') from None

        from_block: int = latest_block - (num_preceding_blocks - 1)
        to_block: Union[str, int] = 'latest'
        try:
            event_filter: constant.T_FILTER_OBJ = getattr(
                self._web3_contract.events,
                event_name
                )().createFilter(
                fromBlock=from_block,
                toBlock=to_block
                )
        except self._contract.web3e.ABIEventFunctionNotFound:
            message = (
                f'ERROR in get_old_events({event_name}).\n'
                f'The event: {event_name} was not found in contract.\n'
                f'Valid event_names: {self._contract.events}\n'
                f'HINT: Check spelling of event_name arg.\n'
                )
            raise SimplEthError(message, code='F-030-020') from None
        except AttributeError as exception:
            message = (
                f'ERROR in get_old_events({event_name}).\n'
                f'Attribute Error says: {exception}.\n'
                f'HINT: Did you do a connect()?\n'
                )
            raise SimplEthError(message, code='F-030-030') from None
        except TypeError as exception:
            message = (
                f'ERROR in get_old_events({event_name}).\n'
                f'Type Error says: {exception}.\n'
                f'HINT: Check the type for the args.\n'
                )
            raise SimplEthError(message, code='F-030-030') from None

        # getattr() worked and we have a valid filter to use
        filter_list: constant.T_FILTER_LIST = event_filter.get_all_entries()
        return self._create_simple_events(filter_list)

    @staticmethod
    def _create_simple_events(filter_list: constant.T_FILTER_LIST) -> List:
        """Return a list of events with the essential data.

        The filter list is an AttributeDict with args, event name, logIndex,
        transactionIndex, transactionHash, address, blockHash, and blockNumber.
        For simpleth, just return the essential data: blockNumber, args, and
        transactionHash.

        :param filter_list: the list returned from ``event_filter.get_all_entries`` or
            ``event_filter.get_new_entries``
        :type filter_list: AttributeDict
        :rtype: list
        :return: list of same events with only ``args`` and ``block_number``

        """
        simple_events: list = []
        for event in filter_list:
            simple_event = {
                'block_number': event['blockNumber'],
                'args': dict(event['args']),
                'trx_hash': event['transactionHash'].hex()
                }
            simple_events.append(simple_event)
        return simple_events
# end of Filter


class SimplEthError(Exception):
    """Simple Ethereum Error exception class.

    It is used by `Contract()` and `Blockchain()` to throw exceptions for
    errors resulting from interacting with Solidity contracts and the
    Ethereum blockchain.

    :note: ``SimplEthError`` is used for two main reasons:

        1) The caller only needs to check for one exception.
           `web3.py` throws a variety of exceptions and a caller would
           need to know about all of them and their various reasons.
        2) Most `SimplEthError` exceptions will print out a hint(s)
           for what might be wrong or how to resolve. Some of the
           exceptions as thrown by `web3.py` can be cryptic and
           difficult to understand the source of error, esp. if the
           exception is from something that happened in the Solidity
           contract. As I was developing this module, I tried to add
           hints as I ran across how errors were thrown

    """
    def __init__(self, message: str, code: str = '') -> None:
        """Create error exception.

        :param message: error message with a description of error
        :type message: str
        :param code: unique identifier of this error (optional,
            default: `''`)
        :type code: str
        :example:
            >>> from simpleth import SimplEthError
            >>> try:
            ...     raise SimplEthError('test')
            ... except SimplEthError as e:
            ...     print(f'{e}')
            ...
            test
            >>> try:
            ...     raise SimplEthError('test', '10')
            ... except SimplEthError as e:
            ...     print(f'{e}')
            ...
            [10] test
            >>> from simpleth import SimplEthError
            >>> try:
            ...     raise SimplEthError('test', 'ERR-020')
            ... except SimplEthError as e:
            ...     print(f'e = {e}')
            ...     print(f'code = {e.code}')
            ...     print(f'message = {e.message}')
            ...     print(f'exc_info = {e.exc_info}')
            ...
            e = [ERR-020] test
            code = ERR-020
            message = test
            exc_info = (None, None, None)

        :note: ``code`` can serve several purposes. It could be
            easily tested in unit tests to make sure a test case is
            causing a specific error.  It makes it easy to search
            simpleth for the line of code that raised a specifid
            SimplEthException.

        """
        self.code: str = ''
        """Exception instance variable with ``code``"""
        self.exc_info: constant.T_EXC_INFO = sys.exc_info()
        """Exception instance variable with exception
        info: (`type`, `value`, `traceback`)"""
        self.message: str = message
        """Exception instance variable with ``message``"""

        if code:
            self.code = code
            msg: str = f'[{code}] {message}'
        else:
            msg = f'{message}'

        super().__init__(msg)    # let Exception take over
# end of SimplEthError


class _Result:
    """Transaction result data object.

    Has the various outcomes resulting from ``trx_name`` being mined.

    """
    def __init__(
            self,
            trx_name: str,
            trx_hash: constant.T_HASH,
            trx_receipt: constant.T_RECEIPT,
            contract: Contract,
            web3_contract_object: constant.T_WEB3_CONTRACT_OBJ,
            event_name: str
            ) -> None:
        """Create instance for the result of specified transaction.

        :param trx_name: transaction name
        :type trx_name: str
        :param trx_hash: transaction hash created when submitting the
             transaction for mining.
        :type trx_hash: T_hash
        :param trx_receipt: transaction receipt created after the
             transaction was mined.
        :type trx_receipt: T_receipt
        :param contract: contract containing the transaction
        :type contract: object
        :param event_name: event name emitted by this transaction (can
            be '')
        :type event_name: str
        :example:

        """
        transaction: constant.T_TRANSACTION = \
            contract.blockchain.eth.get_transaction(trx_hash)

        self._block_number: int = trx_receipt.blockNumber
        self._block_time: int = \
            contract.blockchain.eth.get_block(self._block_number).timestamp
        self._contract_address: str = contract.address
        self._contract_name: str = contract.name
        self._event_log: dict = {}
        """Event log created by the transaction"""
        self._gas_price_gwei: int = transaction.gasPrice
        self._gas_used: int = trx_receipt.gasUsed
        self._trx_hash: constant.T_HASH = trx_hash
        self._trx_name: str = trx_name
        self._trx_receipt: constant.T_RECEIPT = trx_receipt
        self._trx_sender: str = dict(trx_receipt)['from']
        self._trx_value_wei: int = transaction.value
        self._transaction: constant.T_TRANSACTION = transaction

        if event_name:
            # User gave us an event name. Find and add event log info to
            # trx_result. If either exception is thrown, return the
            # trx_result as built above without any event log info.
            try:
                contract_event: constant.T_CONTRACT_EVENT = getattr(
                    web3_contract_object.events,
                    event_name
                    )
            except web3_contract_object.web3e.ABIEventFunctionNotFound as exception:
                message = (
                    f'ERROR in getting transaction results for '
                    f'{self._contract_name}: event "{event_name}" '
                    f'was not found in trx "{self._trx_name}".\n'
                    f'Event information not added to result.\n'
                    f'MESSAGE: ABIEventFunctionNotFound says {exception}\n'
                    f'HINT: Check spelling of transaction event name.\n'
                    )
                raise SimplEthError(message, code='R-090-010') from None

            # use the trx_event object to get the transaction receipt.
            try:
                self._event_log = contract_event().processReceipt(
                    trx_receipt,
                    errors=DISCARD
                    )
                # Toss out any transaction log records that
                # can not be processed. This is expected when there is a
                # transaction that calls other transactions.
                # Using DISCARD returns only logs that match the event_name
                # event for the first transaction and discards records
                # from any transaction(s) called by that first transaction.
            except contract.web3e.MismatchedABI as exception:
                message = (
                    f'ERROR inf getting transaction results for '
                    f'{self._contract_name}.{self._trx_name}().\n'
                    f'MismatchedABI says: {exception}'
                    )
                raise SimplEthError(message, code='R-010-020') from None

    @property
    def block_number(self) -> int:
        """Block number of block with transaction."""
        return self._block_number

    @property
    def block_time_epoch(self) -> int:
        """Time block with transaction was mined, in epoch seconds."""
        return self._block_time

    @property
    def contract_address(self) -> str:
        """Address of contract issuing the transaction."""
        return self._contract_address

    @property
    def contract_name(self) -> str:
        """Name of contract issuing the transaction."""
        return self._contract_name

    @property
    def event_args(self) -> dict:
        """Args for the event emitted by the transaction."""
        return dict(self._event_log[0]['args'])

    @property
    def event_log(self) -> constant.T_EVENT_LOG:
        """Full event log resulting from transaction."""
        return self._event_log

    @property
    def event_name(self) -> str:
        """Name of the event emitted by the transaction."""
        return self._event_log[0]['event']

    @property
    def gas_price_gwei(self) -> int:
        """Price, in gwei, charged for each unit of gas used by the
            transaction."""
        return self._gas_price_gwei

    @property
    def gas_used(self) -> int:
        """Units of gas used by the transaction."""
        return self._gas_used

    @property
    def trx_hash(self) -> constant.T_HASH:
        """Transaction hash for the mined transaction.

        This was returned from :meth:`submit_trx`.

        """
        return self._trx_hash

    @property
    def trx_name(self) -> str:
        """Name of the transaction."""
        return self._trx_name

    @property
    def trx_receipt(self) -> constant.T_RECEIPT:
        """Transaction receipt."""
        return self._trx_receipt

    @property
    def trx_sender(self) -> str:
        """Address of account that sent the transaction for mining."""
        return self._trx_sender

    @property
    def trx_value_wei(self) -> int:
        """Amount of Ether, in wei, sent along with the transaction."""
        return self._trx_value_wei

    @property
    def transaction(self) -> constant.T_TRANSACTION:
        """Transaction object."""
        return self._transaction

    def block_time_string(
            self,
            time_format: str = constant.TIME_FORMAT
            ) -> str:
        """Time block was mined, in local timezone, as a string.

        :param time_format: format codes used to create time string
            (optional, default: :const:`constant.TIME_FORMAT`)
        :type time_format: str
        :rtype: str
        :return: time block was mined, in local timezone, as a string.
        :see also: List of format codes:
            https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes

        """
        epoch_seconds = self._block_time
        return datetime.datetime.\
            fromtimestamp(epoch_seconds).\
            strftime(time_format)

    def __str__(self) -> str:
        string = (
            f'Block number = {self.block_number}\n'
            f'Block time = {self.block_time_string}\n'
            f'Contract address = {self.contract_address}\n'
            f'Contract name = {self.contract_name}\n'
            f'Event args = {self.event_args}\n'
            f'Event name = {self.event_name}\n'
            f'Gas price gwei = {self.gas_price_gwei}\n'
            f'Gas used = {self.gas_used}\n'
            f'Trx hash = {self.trx_hash}\n'
            f'Trx name = {self.trx_name}\n'
            f'Trx sender = {self.trx_sender}\n'
            f'Trx value_wei = {self.trx_value_wei}\n'
            )
        return string
# end of _Result
