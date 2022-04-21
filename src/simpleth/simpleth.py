"""Simple Ethereum is a facade of `web3.py` to simplify use of an
Ethereum blockchain and interaction with Solidity contracts.

Classes
-------
- `Blockchain` - interact with Ethereum blockchain
- `Contract` - interact with Solidity contracts
- `Convert` - conversion methods for Ether denominations and time values
- `Results` - outcomes resulting from a transaction being mined
- `Filter` - search for events emitted by transactions

Exceptions
----------
- `SimplEthError` - raised on errors from methods in `Blockchain`,
  `Contract`, or `Filter`.

"""
import sys
import json
import json.decoder
import datetime
import time
from typing import List, Optional, Union, Dict, Any
from decimal import Decimal, getcontext
from web3 import Web3
from web3 import exceptions as web3e
from web3.logs import DISCARD

__all__ = [
    'Blockchain',
    'Contract',
    'Convert',
    'Filter',
    'Results',
    'SimplEthError'
    ]
__author__ = 'Stephen Newell'
__copyright__ = 'Copyright 2021, Stephen Newell'
__license__ = 'MIT'
__version__ = '0.17'
__maintainer__ = 'Stephen Newell'
__email__ = 'snewell4@gmail.com'
__status__ = 'Prototype'


#
# Directories and filenames
#
# TBD - I think all SUFFIX should have a leading "."
PROJECT_HOME: str = 'C:/Users/snewe/OneDrive/Desktop/simpleth'
"""Directory for the prototype project home"""

ARTIFACT_SUBDIR: str = 'artifacts'
"""Directory, under project directory, for the artifact files."""

SOLC_SUBDIR: str = 'solc'
"""Directory, under project directory, for the Solidity compiler."""

RST_DOC_SUBDIR: str = 'docs/source'
"""Directory, under project directory, for the rST files."""

ABI_SUFFIX: str = 'abi'
"""Filename suffix for the ABI files."""

BYTECODE_SUFFIX: str = 'bin'
"""Filename suffix for the bytecode files."""

ADDRESS_SUFFIX: str = 'addr'
"""Filename suffix for the contract address files."""

BIN_RUNTIME_SUFFIX: str = 'bin-runtime'
"""Filename suffix for bin-runtime files. Used to get compiled size."""

SOLIDITY_CONTRACT_SUFFIX: str = '.sol'
"""Filename suffix for smart contract source file."""

SOLC_FILENAME: str = 'solc.exe'
"""Filename of the Solidity compiler executable."""

#
# Transaction processing defaults
#

# This is the maximum amount of gas any single transaction can consume.
# If the transaction requires more gas, it will revert. This value is
# arbitrarily set slightly below the Ganache default value for Gas Limit.
GAS_LIMIT: int = 6_000_000
"""Gas limit for a transaction, in units of gas."""

# Currently, has no effect with Ganache. It is valid for main net.
MAX_BASE_FEE_GWEI: Union[int, float] = 100
"""Maximum tip to pay the miners, per unit of gas in gwei."""

# Currently, has no effect with Ganache. It is valid for main net.
MAX_PRIORITY_FEE_GWEI: Union[int, float] = 2
"""Maximum tip to pay the miners, per unit of gas in gwei."""

# Currently, has no effect with Ganache. It is valid for main net.
MAX_FEE_GWEI: Union[int, float] = \
    MAX_BASE_FEE_GWEI + MAX_PRIORITY_FEE_GWEI
"""Maximum total to pay the miners, per unit of gas in gwei."""

TIMEOUT: Union[int, float] = 120
"""Time to wait for transaction to be mined, in seconds."""

POLL_LATENCY: Union[int, float] = 0.1
"""Time between checking if mining is finished, in seconds."""

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
# Conversion
#
PRECISION = 40
"""Level of precision for `Decimal` values used in Ether denomination
conversions. Arbitrary value. Consider a better value."""

#
# Type Hint aliases
#
T_ABI = Any
"""``ABI`` type is a list with JSON read from the `artifact` file."""

T_ATTRIBUTE_DICT = Any
"""``AttributeDict`` type is not known to type hint. Use `Any` for now."""

T_BLOCKCHAIN_OBJ = Any
"""``Blockchain object`` type is `simpleth.Blockchain`. Use `Any` for now.
Created by `simpleth` methods. See ``T_result`` about those single quotes."""

T_BYTECODE = Any
"""``bytecode`` type is HexBytes read from the `artifact` file.
Use `Any` for now."""

T_CONTRACT_EVENT = Any
"""`contract_event`` type is ``web3._utils.datatypes.<event_name>'``.
Use ``Any`` for now."""

T_DECIMAL = Any
"""``Decimal`` type. Use ``Any`` for now."""

T_DEPLOYED_CODE = Any
"""``Deployed code`` type is class `HexBytes`. Use
`Any` for now.  Created by `web3.py` method."""

T_EXC_INFO = Any
"""``Transaction exception info`` type is a tuple returned by
`sys.exc_info()` after an exception. Use `Any` for now."""

T_ETH_OBJ = Any
"""``Eth object`` type is `web3.eth.Eth`. Use `Any` for now.
Created by `web3.py` methods."""

T_EVENT = Any
"""``Event`` type is an ``AttributeDict``. Use ``Any`` for now."""

T_EVENT_LOG_OBJ = list
"""``Event log`` type is a list of T_EVENT items."""

T_FILTER_OBJ = Any
"""``Filter object`` type is `web3._utils.filters.LogFilter`.
Use `Any` for now. Created by `web3.py` methods."""

T_FILTER_LIST = Any
"""``Filter list`` type is created by `web3.py` `event_filter`.
Use `Any` for now."""

T_HASH = Any
"""``Transaction hash`` type is HexBytes in ``web3.py``. Use `Any`
for now."""

T_HEX_BYTE = Any
"""``HexByte`` type is not known to type hint. Use `Any` for now."""

T_RECEIPT = Any
"""``Transaction receipt`` type is AttributeDict. Use `Any` for now.
Created by `web3.py` methods."""

T_RESULT = Any
"""``Transaction result`` is a class object with the various outcomes
from mining a transaction. Created by the `simpleth` class,
``Results``. Use Any for now."""

T_TRANSACTION = Any
"""``Transaction`` type is class `web3.datastructures.AttributeDict`.
Use `Any` for now. Created by `web3.py` `getTransaction()`.  """

T_WEB3_OBJ = Any
"""``Web3 object`` type is `web3.main.Web3 object`. Use `Any` for now.
Created by `web3.py` methods."""

T_WEB3_ETH_OBJ = Any
"""``Web3 object`` type is `web3.eth.Eth object`. Use `Any` for now."""

T_WEB3_CONTRACT_OBJ = Any
"""``Web3 contract object`` type is ``web3._utils.datatypes.Contract``
object. Use ``Any`` for now."""

T_WEB3_EXC = Any
"""``Web3 Exception`` type is `module web3.exceptions`.
Use `Any` for now. Provided by `web3.py`"""


class Blockchain:
    """Interact with an Ethereum blockchain.

    Sets up the `Web3` object which establishes the
    connection to an Ethereum blockchain and supports access
    to various values and functions related to the blockchain.

    **PROPERTIES**

    -  :meth:`accounts` - List of Ganache account addresses
    -  :meth:`api_version` - `web3` API version in use
    -  :meth:`block_number` - Sequence number of last block on chain
    -  :meth:`client_version` - `Ethereum` client version in use
    -  :meth:`eth` - `web3.eth` object
    -  :meth:`web3` - `web3` object

    **METHODS**

    -  :meth:`account_num` - Return account number for an address
    -  :meth:`address` - Return blockchain address for an account number
    -  :meth:`balance` - Return amount of Ether for an address
    -  :meth:`fee_history` - Return fee info for recent blocks
       (**not currently supported by `Ganache`**)
    -  :meth:`block_time_epoch` - Return time block was mined in
       epoch seconds
    -  :meth:`block_time_string` - Return time block was mined in
       a time-format string
    -  :meth:`is_valid_address` - Test for valid blockchain address
    -  :meth:`send_ether` - Transfer ether from one account to another
    -  :meth:`transaction` - Return details about a transaction
    -  :meth:`trx_count` - Return number of transactions sent by
       an address
    -  :meth:`trx_sender` - Return address that sent a transaction

    :warning:

    -  This has only been tested with `Ganache`.
    -  Since it is a list, ``accounts[-1]`` returns ``accounts[9]``.
       Should I try to fix this?

    :see: `Web3` API documentation at
        https://web3py.readthedocs.io/en/stable/web3.main.html

    """
    def __init__(self, url: str = GANACHE_URL) -> None:
        """Create blockchain instance.

        :param url: Ethereum blockchain web address (optional,
            default: `GANACHE_URL`)
        :type url: str
        :rtype: None
        :raises SimplEthError: if unable to connect to the blockchain
            client
        :example:
            >>> from simpleth import Blockchain
            >>> b = Blockchain()

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

        self._eth: T_WEB3_ETH_OBJ = self.web3.eth
        """private ``web3.eth`` object"""
        self._web3e: T_WEB3_EXC = web3e
        """private module to catch exceptions from Web3 API"""
        self._accounts: List[str] = self.eth.accounts
        """private list of addresses in the Ganache-provided
            accounts"""
        self._api_version: str = self.web3.api
        """private `web3` API version"""
        self._client_version: str = self.web3.clientVersion
        """private Ethereum client version"""

    @property
    def accounts(self) -> list:
        """Return list of accounts provided by `Ganache`.

        :rtype: list
        :return: list of blockchain `addresses`
        :example:
            >>> from simpleth import Blockchain
            >>> Blockchain().accounts
            ['0x235A686386d03a5Bb986Fb13E71A0dC86846c636',   ...snip... ]

        """
        return self._accounts

    @property
    def api_version(self) -> str:
        """Return the installed `web3` API version.

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

        :rtype: int
        :return: sequence number of the block at the end of the chain
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
        :return: blockchain client version
        :example:
            >>> from simpleth import Blockchain
            >>> b = Blockchain()
            >>> b.client_version
            'EthereumJS TestRPC/v2.13.1/ethereum-js'

        """
        return self._client_version

    @property
    def eth(self) -> T_ETH_OBJ:
        """Return the ``web3.eth`` object.

        :rtype: object
        :return: `web3.eth` object
        :example:
            >>> from simpleth import Blockchain
            >>> b = Blockchain()
            >>> b.eth
            <web3.eth.Eth object at 0x0000019CEBAC8760>
            >>> b.eth.gas_price
            20000000000

        :notes: This can be used to access any of the ``web3.eth``
              methods not provided by `simpleth`.
        :see: `web3,eth API` documentation at:
            https://web3py.readthedocs.io/en/stable/web3.eth.html

        """
        return self._eth

    @property
    def web3(self) -> T_WEB3_OBJ:
        """Return the ``web3`` object.

        :rtype: object
        :return: `web3` object
        :example:
            >>> from simpleth import Blockchain
            >>> b = Blockchain()
            >>> b.web3
            <web3.main.Web3 object at 0x0000019CE7AF3520>
            >>> b.web3.toWei(1, 'ether')
            1000000000000000000

        :notes: This can be used to access any of the
            ``web3`` methods not provided by `simpleth`.
        :see: `Web3 API` documentation at:
            https://web3py.readthedocs.io/en/stable/web3.main.html
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
            - `None` if ``account_address`` not one provided by Ganache

        :example:
            >>> from simpleth import Blockchain
            >>> b = Blockchain()
            >>> user = b.accounts[6]
            >>> b.account_num(user)
            6

        :see: :meth:`accounts` for the list of all
            account addresses.

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

        :param account_num: index into the account list
        :type account_num: int
        :rtype: str
        :return: blockchain ``address`` of the requested account
        :raises SimplEthError: if ``account_num`` is bad
        :example:
            >>> from simpleth import Blockchain
            >>> b=Blockchain()
            >>> b.address(2)
            '0x02F6903D426Be890BA4F882eD19cF6780ecdfA5b'

        :see: :meth:`accounts` to get all addresses.

        """
        if account_num in range(0, len(self.accounts)):
            return self.accounts[account_num]

        message: str = (
            f'ERROR in get_account({account_num}): '
            f'the account_num must be an integer between 0 and '
            f'{len(self.accounts)}.\n'
            f'HINT: account_num is bad.\n'
            )
        raise SimplEthError(message, code='B-020-010') from None

    def balance(self, address: str) -> int:
        """Return the amount of Ether owned by an account.

        :param address: blockchain `address` of the account
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
            balance: int = self.eth.get_balance(address)
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
                f'HINT: Did you specify a valid account address?\n'
                )
            raise SimplEthError(message, code='B-030-020') from None
        return balance

    def block_time_epoch(self, block_num: int) -> int:
        """Return the time, as epoch seconds, when a block was mined.

        :param block_num: number of the block on the chain
        :type block_num: int
        :rtype: int
        :return: time block was mined, in epoch seconds.
        :raises SimplEthError: if block_num is bad
        :example:
            >>> from simpleth import Blockchain
            >>> b = Blockchain()
            >>> b.block_time_epoch(20)
            1638120893

        """
        if block_num not in range(0, self.block_number + 1):
            message: str = (
                f'ERROR in block_time_epoch({block_num}): '
                f'the block_num must be an integer between '
                f'0 and {self.block_number}.\n'
                f'HINT: check type and value for block_num.\n'
                )
            raise SimplEthError(message, code='B-040-010') from None
        return self.eth.get_block(block_num).timestamp

    def block_time_string(
            self,
            block_number: int,
            time_format: str = TIME_FORMAT
         ) -> str:
        """Return the time, as a string, when a block was mined.

        :param block_number: number of the block on the chain
        :type block_number: int
        :param time_format: format codes used to create time string
            (**optional**, default: `TIME_FORMAT`)
        :type time_format: str
        :rtype: str
        :return: time block was mined, in local timezone, as a string
        :example:
            >>> from simpleth import Blockchain
            >>> Blockchain().block_time_string(20)
            '2021-11-28 11:34:53'
            >>> Blockchain().block_time_string(20, '%A %I:%M %p')
            'Sunday 11:34 AM'

        :see: List of format codes:
              https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes

        """
        if isinstance(time_format, str):
            epoch_seconds: int = self.block_time_epoch(block_number)
            return datetime.datetime. \
                fromtimestamp(epoch_seconds). \
                strftime(time_format)
        message = (
            f'ERROR in block_time_string({block_number}, {time_format}).\n'
            f'time_format must be a string.\n'
            f'HINT: Use a string of valid strftime format codes for '
            f'time_format.')
        raise SimplEthError(message, code='B-050-010') from None

    def fee_history(self, num_blocks: int = 3) -> dict:
        """Return fee information for recently mined blocks.

        This could be used to determine a reasonable ``max_fee_gwei`` and
        ``max_priority_fee_gwei`` to offer when submitting a new transaction.

        :param num_blocks: information for the last ``num_blocks`` will be
            returned (**optional**, default: 3)
        :type num_blocks: int
        :rtype: dict
        :returns: dictionary with:

            -  `'reward'`: a list with the `low` and `high` reward
               amounts offered for transactions in this block: `low`
               is the 10th percentile; `high` is the 90th percentile
            -  `'baseFeePerGas'`: `base fee` set by the network for
               this block
            -  `'gasUsedRatio'`: `gasUsed`/`gasLimit` for this block
            -  `'oldestBlock'`: `block number` for the oldest block in
               the list and will be :attr:`block_number` - ``num_blocks``

        :warning: **This does not work.** The `w3.eth.fee_history()`
          method is specified in the `web3.py` documentation but does
          not seem to be supported by Ganache yet. Currently, it
          throws a ``ValueError`` exception.
        :example:
            >>> from simpleth import Blockchain
            >>> b = Blockchain()
            >>> b.fee_history()
            ...
            HINT: method not yet implemented in Ganache.

        :note: this method is being included in `simpleth` in hopes
          it is soon implemented by Ganache. The method has value
          for using ``simpleth`` and for now will be coded up and
          ready to use.

        """
        try:
            history: dict = self.eth.fee_history(num_blocks, 'latest', [10, 90])
        except ValueError as exception:
            message: str = (
                f'ERROR in fee_history().\n'
                f'ValueError says: {exception}\n'
                f'HINT: method not yet implemented in Ganache.\n'
                )
            raise SimplEthError(message, code='B-060-010') from None
        return dict(history)     # cast from AttributeDict to dict

    def is_valid_address(self, address: str) -> bool:
        """Test for valid blockchain address

        :param address: blockchain `address` to verify
        :rtype: bool
        :return:

            - `True` if valid
            - `False` otherwise

        :example:
            >>> from simpleth import Blockchain
            >>> b = Blockchain()
            >>> user0 = b.address(0)
            >>> b.is_valid_address(user0)
            True
            >>> bogus = '0x380A36BE82A06A63395D'
            >>> b.is_valid_address(bogus)
            False

        """
        return self._web3.isAddress(address)

    def send_ether(
            self,
            sender: str,
            receiver: str,
            amount_wei: int
            ) -> T_HASH:
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
        :return: `trx_hash` of the transfer transaction
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

        :see:

            - :meth:`balance` to get amount of Ether owned by
              an account.
            - :meth:`transaction` to get details of the transfer
              transaction using the `trx_hash`.

        """
        try:
            trx_hash: str = self._web3.eth.send_transaction(
                    {
                        'to': receiver,
                        'from': sender,
                        'value': amount_wei
                        }
                ).hex()      # cast to a string from HexBytes
        except ValueError as exception:
            message: str = (
                f'ERROR in transfer(): '
                f'ValueError says: {exception}.\n'
                f'HINT 1: Amount exceeds sender balance\n'
                f'HINT 2: Amount must be positive\n'
                f'HINT 3: Bad address used for to or from\n'
                )
            raise SimplEthError(message, code='B-070-010') from None
        except TypeError as exception:
            message = (
                f'ERROR in transfer(): '
                f'TypeError says: {exception}.\n'
                f'HINT1: Amount must be an int. Did you use a float?\n'
                f'HINT2: Did you use a non-string used for the from or '
                f'to address?\n'
                )
            raise SimplEthError(message, code='B-070-020') from None
        except AttributeError as exception:
            message = (
                f'ERROR in transfer(): '
                f'AttributeError says: {exception}.\n'
                f'HINT: Did you attempt to send Ether to a non-payable '
                f'contract?\n'
                )
            raise SimplEthError(message, code='B-070-030') from None
        return trx_hash

    def transaction(self, trx_hash: str) -> T_TRANSACTION:
        # noinspection SpellCheckingInspection
        """Return details about the transaction.

        :param trx_hash: transaction hash to identify the
            transaction of interest
        :type trx_hash: str
        :rtype: dict
        :return: transaction details as a dictionary
        :example:
            >>> from simpleth import Blockchain
            >>> t = '0xe6bbbc34f53ef4137de80dc63f156b820d71f9f176b8210a42 ...'
            >>> Blockchain().transaction(t)
            {'hash': HexBytes('0xe6bbbc34f53ef4137de80dc63f156b820d71 )...}'

        :see: :meth:`run_trx` and :meth:`send_trx` return a
            ``trx_hash``

        """
        try:
            transaction: dict = dict(self.eth.get_transaction(trx_hash))
        except self._web3e.TransactionNotFound as exception:
            message: str = (
                f'ERROR in transaction({trx_hash}): '
                f'TransactionNotFound says: {exception}\n'
                f'HINT: Did you use a valid trx_hash?'
                )
            raise SimplEthError(message, code='B-080-010') from None
        except ValueError as exception:
            message = (
                f'ERROR in transaction({trx_hash}): '
                f'ValueError says: {exception}\n'
                f'HINT: Was trx_hash a hex value?'
                )
            raise SimplEthError(message, code='B-080-020') from None
        return transaction

    def trx_count(self, address: str) -> int:
        """Return the number of transactions sent by an address.

        This is the total number of transactions on the blockchain
        that were sent by ``address``.

        :param address: blockchain `address` of account to check
        :type address: str
        :rtype: int
        :return: number of transactions
        :raises SimplEthError: if ``address`` is bad
        :example:
            >>> from simpleth import Blockchain
            >>> b = Blockchain()
            >>> user0 = b.address(0)
            >>> b.trx_count(user0)
            48

        """
        try:
            count: int = self.eth.get_transaction_count(address)
        except TypeError as exception:
            message: str = (
                f'ERROR in get_trx_count(): '
                f'TypeError says: {exception}.\n'
                f'HINT: Did you use a string with a valid account address?\n'
                )
            raise SimplEthError(message, code='B-090-010') from None
        except self._web3e.InvalidAddress as exception:
            message = (
                f'ERROR in get_trx_count(): '
                f'InvalidAddress says: {exception}.\n'
                f'HINT: Did you use a valid account address?\n'
                )
            raise SimplEthError(message, code='B-090-020') from None
        return count

    def trx_sender(self, trx_hash: str) -> str:
        """Return the account address that sent this transaction.

        :param trx_hash: transaction hash of the transaction
        :type trx_hash: str
        :rtype: str
        :return: address that sent the transaction
        :example:

            >>> from simpleth import Blockchain, Contract
            >>> user = Blockchain().accounts[3]
            >>> c = Contract('Test')
            >>> c.connect()
            '0x3F1c8adCB6E8F89dc2d0a32c947CaA6Af95d4448'
            >>> r = c.run_trx(user,'storeNums',1,2,3)
            >>> thash = r.trx_hash
            >>> Blockchain().trx_sender(thash)
            '0xfEeB074976F8a2B53d2F8c737BD94cd16ad599F0'

        """
        return self.transaction(trx_hash)['from']
# end of Blockchain()


class Contract:
    """Use to interact with Solidity contracts.

    Will deploy a contract onto the blockchain, connect to a previously
    deployed contract, submit transactions to be run, get results of a
    transaction, call functions, and get public
    state variable values.

    **PROPERTIES**

    -  :meth:`abi` - contract ABI
    -  :meth:`address` - contract address on blockchain
    -  :meth:`blockchain` - `web3` blockchain object
    -  :meth:`bytecode` - contract bytecode
    -  :meth:`deployed_code` - contract bytecode as deployed on chain
    -  :meth:`event_names` - event names defined in contract
    -  :meth:`functions` - function names defined in contract
    -  :meth:`name` - name of contract
    -  :meth:`size` - deployed contract size, in bytes
    -  :meth:`web3_contract` - `web3` contract object
    -  :meth:`web3e` - `web3` exception module

    **METHODS**

    -  :meth:`call_fcn` - return results from calling a contract function
    -  :meth:`connect` - enable the use of a deployed contract
    -  :meth:`deploy` - deploy a contract onto the blockchain
    -  :meth:`get_gas_estimate` - return units of gas to run a transaction
    -  :meth:`get_trx_receipt` - get the results of a transaction
    -  :meth:`get_trx_receipt_wait` - wait for the results of a transaction
    -  :meth:`get_var` - return value of a contract variable
    -  :meth:`run_trx` - submit a transaction and wait for the results
    -  :meth:`submit_trx` - send a transaction to be mined

    """
    def __init__(self, name: str) -> None:
        """Create instance for the named contract.

        :param name: contract name
        :type name: str
        :rtype: None
        :raises SimplEthError: if ``name`` is misspelled or has
            not been compiled.
        :example:
            >>> from simpleth import Contract
            >>> Contract('Test')
            <simpleth.Contract object at 0x0000028A7262B580>

        :notes:
            - ``name`` must match the Solidity filename for the
              contract source code. For example, if the Solidity file is
              ``Example.sol``, use ``Contract(\'Example\')``.
            - Due to DOS filename convention case does not matter and
              ``Contract(\'example\')`` will also work.

        """
        self._name: str = name
        """Private name of the contract this object represents"""

        self._artifact_dir: str = \
            PROJECT_HOME + '/' + \
            ARTIFACT_SUBDIR
        """Private filepath to the directory with artifact files"""

        self._artifact_abi_filepath: str = \
            self._artifact_dir + '/' + \
            self._name + '.' + \
            ABI_SUFFIX
        """Private filepath to the ABI file"""

        self._artifact_address_filepath: str = \
            self._artifact_dir + '/' + \
            self._name + '.' + \
            ADDRESS_SUFFIX
        """Private filepath to the address file"""

        self._artifact_bytecode_filepath: str = \
            self._artifact_dir + '/' + \
            self._name + '.' + \
            BYTECODE_SUFFIX
        """Private filepath to the bytecode file"""

        self._blockchain: T_BLOCKCHAIN_OBJ = Blockchain()
        """Private :class:`Blockchain` object used to access
            blockchain methods"""

        self._web3e: T_WEB3_EXC = web3e
        """Private instance to catch exceptions from Web3 API"""
        self._abi: List = self._get_artifact_abi()
        """Private contract Application Binary Interface"""
        self._bytecode: str = self._get_artifact_bytecode()
        """Private bytecode for contract"""

        # The following attributes are initialized to `None` or empty.
        # They are filled in with a `connect()`.
        # This happens when a user calls `connect()` or `deploy()`.
        # A `deploy()` does a `connect()`.
        self._deployed_code: T_DEPLOYED_CODE = ''
        """Private contract code as deployed on blockchain"""
        self._address: str = ''
        """Private blockchain address of contract"""
        self._web3_contract: T_WEB3_CONTRACT_OBJ = None
        """Private instance of the `web3._utils.datatypes.Contract`
            used to access methods for that object."""
        self._event_names: List = []
        """Private list of event names emitted by the contract"""
        self._functions: List = []
        """Private list of contract functions provided by the contract"""
        self._size: int = 0
        """Private contract size on the blockchain, in bytes"""

    @property
    def abi(self) -> List:
        """Return the contract ABI (Application Binary Interface).

        :rtype: list
        :return: list with signature of all contract functions
        :example:
            >>> from simpleth import Contract
            >>> c = Contract('Test')
            >>> c.abi
            [{'inputs': [{'internalType': 'int256', 'name':  ...snip... } ]

        """
        return self._abi

    @property
    def address(self) -> str:
        """Return blockchain address of the deployed contract.

        :rtype: str
        :return: blockchain address of the contract
        :example:
            >>> from simpleth import Contract
            >>> c = Contract('Test')
            >>> c.connect()
            >>> c.address
            '0x0F802Cf8C7929C5E0CC140314d1501e21b18a6A8'

        :notes: Returns empty string if no ``connect()`` was done.
        """
        return self._address

    @property
    def blockchain(self) -> T_BLOCKCHAIN_OBJ:
        """Return web3.py blockchain object.

        This can be used to access :class:`Blockchain` methods
        and attributes

        :rtype: object
        :return: :class:`Blockchain` object
        :example:
            >>> from simpleth import Contract
            >>> c = Contract('Test')
            >>> c.connect()
            '0x3F1c8adCB6E8F89dc2d0a32c947CaA6Af95d4448'
            >>> c.blockchain
            <simpleth.Blockchain object at 0x000001E867C698A0>

        """
        return self._blockchain

    @property
    def bytecode(self) -> str:
        """Return contract bytecode.

        :rtype: str
        :return: bytecode of contract
        :example:
            >>> from simpleth import Contract
            >>> c = Contract('Test')
            >>> c.connect()
            >>> c.bytecode
            '6080604052602a60015534801561001557600080  ...snip...

        :notes: Contract bytecode is not the same as the contract
            :attr:`deployed_code`. The :attr:`bytecode` is
            larger and includes the instructions to deploy
            the contract.
        """
        return self._bytecode

    @property
    def deployed_code(self) -> T_DEPLOYED_CODE:
        """Return contract bytecode as deployed on blockchain.

        :rtype: str
        :return: contract code as deployed on chain.
        :example:
            >>> from simpleth import Contract
            >>> c = Contract('Test')
            >>> c.connect()
            '0xF37b6b8180052B6753Cc34192Dfb901a48732ed0'
            >>> c.deployed_code
            '0x608060405234801561001057600080fd5b50600436106100ea576

        :notes: :attr:`deployed_code` contains the bytes that
            are on the blockchain. This is the same as the
            :attr:`bytecode` without its additional code to deploy.

        :TBD: Play with this a bit. After doing a lot of gonzo
            hand-testing to create examples and debug, I had Test
            already deployed that would run storeNums() but showed
            deployed_code == 'x0'. Did a fresh deploy() and all worked.

        """

        return self._deployed_code

    @property
    def event_names(self) -> List[str]:
        """Return the event names defined in the contract.

        :rtype: list
        :return: names of the events defined in the contract
        :example:
            >>> from simpleth import Contract
            >>> c = Contract('Test')
            >>> c.connect()
            '0xF37b6b8180052B6753Cc34192Dfb901a48732ed0'
            >>> c.event_names
            ['NumsStored', 'TestConstructed', 'TypesStored']

        """
        return self._event_names

    @property
    def functions(self) -> List[str]:
        """Return the functions in the contract.

        :rtype: list
        :return: signatures of all functions.
        :example:
            >>> from simpleth import Contract
            >>> c = Contract('Test')
            >>> c.connect()
            >>> c.functions
            ['getContractSize(address)', 'getNum(uint8)',  ...snip... ]

        :notes: The list of functions includes all transactions, all
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
            >>> c = Contract('Test')
            '0xF37b6b8180052B6753Cc34192Dfb901a48732ed0'
            >>> c.name
            'Test'

        """
        return self._name

    @property
    def size(self) -> int:
        """Return deployed contract size.

        :rtype: int
        :return: size of the contract, in bytes
        :example:
            >>> from simpleth import Contract
            >>> c = Contract('Test')
            >>> c.connect()
            '0xF37b6b8180052B6753Cc34192Dfb901a48732ed0'
            >>> c.size
            4218

        :notes: This is the number of bytes required to store the
            contract on the blockchain. It is the same as
            `len(c.deployed_code)`.
        """
        return self._size

    @property
    def web3_contract(self) -> T_WEB3_CONTRACT_OBJ:
        """Return web3.py contract object.

        This can be used to access methods provided by `web3`.
        It is typically not needed for simpler use of `simpleth`.

        :rtype: object
        :return: `web3._utils.datatypes.Contract` object
        :example:
            >>> from simpleth import Contract
            >>> c = Contract('Test')
            >>> c.connect()
            '0xF37b6b8180052B6753Cc34192Dfb901a48732ed0'
            >>> c.web3_contract
            <web3._utils.datatypes.Contract object at 0x000001E867CFABF0>

        """
        return self._web3_contract

    @property
    def web3e(self) -> T_WEB3_EXC:
        """Return module to process web3 exceptions.

        This is used by `simpleth` internals to handle `web3`
        exceptions. It is typically not needed for simpler use
        of `simpleth`.

        :rtype: module
        :return: web3 exception module
        :example:
            >>> from simpleth import Contract
            >>> c = Contract('Test')
            >>> c.connect()
            '0xF37b6b8180052B6753Cc34192Dfb901a48732ed0'
            >>> c.web3_contract
            <module 'web3.exceptions' ... >

        """
        return self._web3e

    def call_fcn(
            self,
            fcn_name: str,
            *fcn_args: Optional[Union[int, str, float]]
            ) -> Union[int, str, list]:
        """Return results from calling a contract function.

        Contract functions are those that do not alter state
        variables. They are defined in the Solidity code as
        `public view` or `public pure`.

        :param fcn_name: name of a function in the Solidity contract
        :type fcn_name: str
        :param fcn_args: argument(s) required by the function
            (**optional**, default: None)
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
            '0xF37b6b8180052B6753Cc34192Dfb901a48732ed0'
            >>> c.call_fcn('getNum0')
            1
            >>> c.call_fcn('getNum', 2)
            3
            >>> c.call_fcn('getNums')
            [1, 2, 3]

        :notes: ``fcn_name`` must match the spelling and capitalization of
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
                f'HINT1 - Do you need to do a connect()?\n'
                f"HINT2 - Check spelling of the function.\n"
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

        return fcn_return

    def connect(self) -> str:
        """Enable the use of a deployed contract.

        After instantiating a deployed :class:`Contract` object you
        must do a :meth:`connect()` to make it possible to use the
        methods for the contract. It is akin to doing a file `open()`
        to use a file.

        :rtype: str
        :return:  `address` of the contract

        :example:
            >>> from simpleth import Contract
            >>> c = Contract('testtrx')
            >>> c.connect()
            '0x6FDce3428A455372AE43b3cE90B60E6B0cb95188'
            >>> c.name
            'Test'

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
        self._event_names = self._get_contract_events()
        self._functions = self._get_contract_functions()
        self._deployed_code = self._get_deployed_code()
        self._size = self._get_size()
        return self._address

    def deploy(self,
               sender: str,
               *constructor_args: Union[int, float, str, list],
               gas_limit: int = GAS_LIMIT,
               max_priority_fee_gwei: Union[float, int] = MAX_PRIORITY_FEE_GWEI,
               max_fee_gwei: Union[float, int] = MAX_FEE_GWEI
               ) -> T_RECEIPT:
        """Deploy the contract onto the blockchain.

        This installs the contract onto the blockchain and
        makes it ready for immediate use. You only need to
        deploy the contract once. Subsequent sessions only require
        a :meth:`connect` to use the deployed contract.

        :param sender: address of account requesting deploy()
        :type sender: str
        :param constructor_args: argument(s) for the contract
            constructor (**optional**, default: None)
        :type constructor_args: int | float | string | list | None
        :param gas_limit: maximum amount of gas units allowed for
            deploy (**optional**, default: :const:`GAS_LIMIT`)
        :type gas_limit: int
        :param max_priority_fee_gwei: maximum ``sender`` will pay from
            account balance as a tip for a miner to mine this
            transaction, in gwei (**optional**, default:
            :const:`MAX_PRIORITY_FEE_GWEI`)
        :type max_priority_fee_gwei: int
        :param max_fee_gwei: maximum ``sender`` will pay to have this
            transaction mined, in gwei (**optional**, default:
            :const:`MAX_FEE_GWEI`)
        :type max_fee_gwei: int
        :rtype: T_RECEIPT
        :return: transaction receipt for `deploy()`

        :raises SimplEthError:
            - if unable to get artifact info and create contract class
            - if ``sender`` address is bad
            - if ``constructor_args`` are bad
            - if the `deploy` ran out of gas
            - if ``gas_limit`` exceeded the block limit

        :example:

            >>> from simpleth import Contract, Blockchain
            >>> c = Contract('testtrx')
            >>> c.connect()
            '0x6FDce3428A455372AE43b3cE90B60E6B0cb95188'
            >>> user = Blockchain().accounts[0]
            >>> r = c.deploy(user,42)

        :TBD: Can you have a list for a constructor arg?

        """
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
            trx_hash: T_HASH = \
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
                f'HINT: Check contract constructor args: type and number.\n'
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
            trx_receipt: T_RECEIPT = \
                self._blockchain.eth.wait_for_transaction_receipt(
                    trx_hash,
                    timeout=TIMEOUT,
                    poll_latency=POLL_LATENCY
                    )
        except self._web3e.TimeExhausted:
            # Timed out. Trx not yet mined. Return empty result
            return None

        self._set_artifact_address(trx_receipt.contractAddress)
        self.connect()
        return trx_receipt

    def get_gas_estimate(
            self,
            sender: str,
            trx_name: str,
            *args: Any
            ) -> int:
        """Return the units of gas needed to run a transaction.

        Does not run the transaction. It estimates the gas that will be
        required to run the transaction with the given ``args``.

        :param sender: account address requesting the estimate
        :type sender: str
        :param trx_name: name of the transaction
        :type trx_name: str
        :param args: transaction arguments (**optional**,
            default: None)
        :type args: Any
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
            '0xD34dB707D084fdd1D99Cf9Af77896283a083c470'
            >>> b = Blockchain()
            >>> user = b.accounts[0]
            >>> c.get_gas_estimate(user, 'storeNums', 1, 2, 3)
            38421

        """
        # TBD can you send a list as an arg? If so, add to the docstring
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
                f'HINT1: Has the contract been destroyed?\n'
                f'HINT2: If you just switched Ganache workspace, has '
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
                f'HINT1: Check transaction argument types.\n'
                f'HINT2: Check all transaction arguments were specified.\n'
                f'HINT3: Check sender arg was provided.\n'
                )
            raise SimplEthError(message, code='C-040-070') from None
        return gas_estimate

    def get_trx_receipt(self, trx_hash: T_HASH) -> Union[T_RECEIPT | None]:
        """Return the receipt after a transaction has been mined.

        This is used after :meth:`submit_trx` to get the mining receipt.
        Returns ``None`` if the transaction has not yet been mined.

        :param trx_hash: transaction hash from :meth:`submit_trx`
        :type trx_hash: str
        :rtype: T_RECEIPT | None
        :return: `web3` transaction receipt
        :example:

            >>> from simpleth import Contract, Blockchain
            >>> c = Contract('testtrx')
            >>> c.connect()
            '0xD34dB707D084fdd1D99Cf9Af77896283a083c470'
            >>> b = Blockchain()
            >>> user = b.accounts[0]
            >>> t_hash = c.submit_trx(user, 'storeNums', 7, 8, 9)
            >>> c.get_trx_receipt(t_hash)
            {'address': None, 'gas_used': 83421,  ...snip... }

        :see:
            - :meth:`submit_trx` for submitting a transaction to be
              mined and returning ``trx_hash``.
            - :meth:`get_trx_receipt_wait` which will make repeated
              checks on the transaction and returns when the mining
              has completed (or times out).
            - :class:`Results` to examine the outcome.

        """
        try:
            trx_receipt: T_RECEIPT = \
                self._blockchain.eth.getTransactionReceipt(trx_hash)
        except self._web3e.TransactionNotFound:
            # Receipt not found. Not yet mined. Will return empty trx_result
            return None
        return trx_receipt

    def get_trx_receipt_wait(
            self,
            trx_hash: T_HASH,
            timeout: Union[int, float] = TIMEOUT,
            poll_latency: Union[int, float] = POLL_LATENCY
            ) -> Union[T_RECEIPT | None]:
        """Wait for transaction to be mined and then return the receipt
           for that transaction.

        This is used after :meth:`submit_trx` to get the results of the
        transaction. Will block the caller and wait until either the
        transaction is mined or ``timeout`` is reached. The return
        will be ''None'' if it times out.

        Setting ``timeout`` and ``poll_latency`` gives the caller
        flexiblity in the frequency of checking for the transaction
        completion and the length of time to keep checking before
        timing out.

        :param trx_hash: transaction hash
        :type trx_hash: str
        :param timeout: maximum number of seconds to wait for
            mining to finish
            (optional, default: :const:`TIMEOUT`)
        :type timeout: int | float
        :param poll_latency: number of seconds between checking
            for transaction completion (optional, default:
            :const:`POLL_LATENCY`)
        :type poll_latency: int | float
        :rtype: T_RECEIPT | None
        :return: transaction receipt
        :example:

            >>> from simpleth import Blockchain, Contract
            >>> c = Contract('Test')
            >>> c.connect()
            '0xD34dB707D084fdd1D99Cf9Af77896283a083c470'
            >>> b = Blockchain()
            >>> user = b.accounts[0]
            >>> t_hash = c.submit_trx(user, 'storeNums', 7, 8, 9)
            >>> r = c.get_trx_receipt_wait(t_hash)
            >>> print(r)
            Address        = None
                ...

        :notes:
            - Typically, :meth:`get_trx_receipt_wait` is used following
              :meth:`submit_trx` which sends the transaction to be mined
              and returns the ``trx_hash``.
            - If it times out, you can use :meth:`get_trx_receipt` or
              :meth:`get_trx_receipt_wait` to continue to periodically
              check for completion.

        :see:
            - :meth:`submit_trx` for submitting a transaction to be
              carried out and mined and returning ``trx_hash``.
            - :meth:`get_trx_receipt` which will make one check and
              either return the results or an empty ``Results``.
            - :meth:`run_trx` which combines the call to
              :meth:`submit_trx` and :meth:`get_trx_receipt_wait`.
            - :class:`Results` to examine the outcome.

        """
        try:
            trx_receipt: T_RECEIPT = \
                self._blockchain.eth.wait_for_transaction_receipt(
                    trx_hash,
                    timeout=timeout,
                    poll_latency=poll_latency
                    )
        except self._web3e.TimeExhausted:
            # Timed out. Trx not yet mined. Will return None for trx_result.
            return None
        return trx_receipt

    def get_var(
            self,
            var_name: str,
            *args: Any
            ) -> Optional[Union[int, float, str, list]]:
        """Return the value of a contract variable.

        The variable must be declared as `public` in the Solidity
        contract.

        :param var_name: name of the contract variable
        :type var_name: str
        :param args: args for the variable, typically an index value
            into an array (**optional**, default: None)
        :type args: int
        :rtype: int | string | float | list | None
        :return: value of the variable
        :raises SimplEthError:
            - if ``var_name`` is bad
            - if ``args`` specifies an out of bound index value
            - if a :meth:`connect` is needed

        :example:
            >>> from simpleth import Contract
            >>> c = Contract('testtrx')
            '0xD34dB707D084fdd1D99Cf9Af77896283a083c470'
            >>> c.get_var('specialNum')
            42

        :notes:
            - Uses the built-in Solidity public getter.

        """
        # TBD - what are the possible types for args? Just int?
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
                f'HINT1: Did you specify an array index arg with a non-array '
                f'variable name?\n'
                f'HINT2: Did you specify an array variable but did not '
                f'specify an index value?\n'
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

    def run_trx(self,
                sender: str,
                trx_name: str,
                *args: Any,
                gas_limit: int = GAS_LIMIT,
                max_priority_fee_gwei: Union[int, float] = MAX_PRIORITY_FEE_GWEI,
                max_fee_gwei: Union[int, float] = MAX_FEE_GWEI,
                value_wei: int = 0,
                timeout: Union[int, float] = TIMEOUT,
                poll_latency: Union[int, float] = POLL_LATENCY
                ) -> Union[T_RECEIPT | None]:
        """Submit a transaction to be mined and return the receipt.

        This is the method typically used for running transactions.

        :meth:`run_trx` is a combination of :meth:`submit_trx` and
        :meth:`get_trx_receipt_wait`. The caller uses a single method
        to submit a transaction to the blockchain and get back the
        results of the transaction after it is mined.

        The caller is blocked until :meth:`run_trx` returns or times out.

        Returns ``None`` if it times out waiting for the mining to
        be completed. Try running again with higher value for
        ``timeout``. Or, consider using :meth:`submit_trx` along with
        either :meth:`get_trx_receipt` or :meth:`get_trx_receipt_wait`
        to give you more flexibility and control.

        :param sender: address of account sending the transaction
        :type sender: str
        :param trx_name: name of transaction
        :type trx_name: str
        :param args: argument(s) required by the transaction
            (**optional**, default: None)
        :type args: int | float | string | list
        :param gas_limit: max `gas` ``sender`` will allow for this
            transaction, in units of `gas` (**optional**, default:
            :const:`GAS_LIMIT`)
        :type gas_limit: int
        :param max_priority_fee_gwei: max amount of Ether, in `gwei`,
            the sender will pay as a tip
            (**optional**, default: :const:`MAX_PRIORITY_FEE_GWEI`)
        :type max_priority_fee_gwei: int | float
        :param max_fee_gwei: max amount of Ether, in `gwei`, the sender
            will pay for the transaction
            (**optional**, default: :const:`MAX_FEE_GWEI`)
        :type max_fee_gwei: int | float
        :param value_wei: amount of Ether, in `wei`, to be sent
            with the transaction (**optional**, default: `0`)
        :type value_wei: int
        :param timeout: maximum number of seconds to wait for
            mining to finish
            (**optional**, default: :const:`TIMEOUT`)
        :type timeout: int | float
        :param poll_latency: number of seconds between checking
            for transaction completion
            (**optional**, default: :const:`POLL_LATENCY`)
        :type poll_latency: int | float
        :rtype: T_RECEIPT | None
        :return: `web3` transaction receipt
        :raises SimplEthError: if unable to submit the transaction

        :example:

            >>> from simpleth import Blockchain, Contract
            >>> c = Contract('Test')
            >>> c.connect()
            '0xD34dB707D084fdd1D99Cf9Af77896283a083c470'
            >>> b = Blockchain()
            >>> user = b.accounts[0]
            >>> results = c.run_trx(user,'storeNums',2,4,6)
            >>> print(results)
            Address        = None
                 ...

        :see: Description section for :meth:`submit_trx` for an
            explanation about fees.

        """
        trx_hash: T_HASH = self.submit_trx(
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

        trx_receipt: T_RECEIPT = self.get_trx_receipt_wait(
            trx_hash,
            timeout=timeout,
            poll_latency=poll_latency
            )
        if not trx_receipt:
            return None

        return trx_receipt

    def submit_trx(
            self,
            sender: str,
            trx_name: str,
            *args: Any,
            gas_limit: int = GAS_LIMIT,
            max_priority_fee_gwei: Union[int, float] = MAX_PRIORITY_FEE_GWEI,
            max_fee_gwei: Union[int, float] = MAX_FEE_GWEI,
            value_wei: int = 0
            ) -> T_HASH:
        """Send a contract transaction to be mined.

        This is used to request a contract carry out a transaction.

        This method returns immediately. It does not check to see if
        transaction was mined nor if it was successful. You can
        follow up with either :meth:`get_trx_results()` or
        :meth:`get_trx_results_wait` to check for the completion of
        the transaction.

        About the fees:

            -  ``max_fee_gwei`` = `Base Fee` + ``max_priority_fee``
            -  The `Base Fee` is set by the network and is adjusted
               after each block based on transaction volume. Paying
               the `Base Fee` is mandatory.
               `Base Fee` is in `gwei` and is paid for each unit of
               gas used by the transaction.
            -  The `Priority Fee` is the tip you can offer to the
               miners to attract their attention to your transaction,
               denominated in 'gwei', and paid for every unit of gas
               used by the transaction.
               It is also call a `'tip'`. Paying the `Priority Fee`
               is optional but might be a near necessity if the
               network is busy with a high transaction volume. In that
               case, miners will be processing transactions with
               tips and ignoring low- or no-tip transactions.
            -  ``max_fee_gwei`` is the maximum you will spend and
               ``max_priority_fee`` is the most you will offer a
               miner. If the `Base Fee` being charged by the network
               is higher than expected, your `Priority Fee` may be
               cut.
            -  https://www.blocknative.com/blog/eip-1559-fees has a
               more thorough explanation plus a recommended `Max Fee`
               to use:
               ::

                   Double the current Base Fee and add the most you would like to tip, i.e.:

                   max_fee_gwei = (2 * current Base Fee) + max_priority_fee_gwei

        :param sender: address of account sending the transaction
        :type sender: str
        :param trx_name: name of transaction
        :type trx_name: str
        :param args: argument(s) required by the transaction
            (**optional**, default: None)
        :type args: int | float | str | None
        :param gas_limit: maximum gas sender will allow for this
            transaction, in units of gas
            (**optional**, default is :const:`GAS_LIMIT`)
        :type gas_limit: int
        :param max_priority_fee_gwei: maximum amount of Ether, in `gwei`,
            the sender will pay as a tip
            (**optional**, default: :const:`MAX_PRIORITY_FEE_GWEI`)
        :type max_priority_fee_gwei: int | float
        :param max_fee_gwei: max amount of Ether, in `gwei`, the sender
            will pay for the transaction
            (**optional**, default: :const:`MAX_FEE_GWEI`)
        :type max_fee_gwei: int | float
        :param value_wei: amount of Ether, `in wei`, to be sent with the
            transaction
            (**optional**, default: `0`)
        :type value_wei: int
        :rtype: str
        :return: ``trx_hash`` the transaction hash that identifies
           this transaction on the blockchain
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
            >>> c = Contract('Test')
            >>> b = Blockchain()
            >>> c.connect()
            >>> user = b.accounts[0]
            >>> c.submit_trx(user, 'storeNums', 4, 5, 6)
            HexBytes('0x6fc9deaf6052504a8  ..snip.. 50af2cb320278b476')

        :notes:

            -  These are Type 2 transactions which conform to EIP-1559 (aka
               `London Fork`). They use the new max fee and max priority
               fee fields instead of a gas price field.
            -  ``trx_hash`` is the transaction hash that can be used
               to check for the transaction outcome in :meth:`get_trx_receipt`
               or :meth:`get_trx_receipt_wait`
            -  ``trx_name`` must match the spelling and capitalization
               of a function in the Solidity contract.
            -  ``value`` is Ether that is sent to the transaction. It is
               a payment from the sender to the contract. The transaction
               should be defined as a `payable` function in the Solidity
               contract or the contract will need a TBD (what's the
               default payable thing?)
            -  See https://ethereum.org/en/developers/docs/gas/ for the
               details on fees and gas.

        :warnings: I'm making the assumption that all `ValueError`
            exceptions that contain `revert` in their message are due
            to those `Guard` modifiers. I'm just going by all my
            testing. So far, this seems to be the case. However,
            there may be other type(s) of `ValueError(s)` that say
            `revert` and are not due to a Guard modifier failing.
            If you see one, add it to the lengthy code of all the
            exceptions.

        :see:

            -  :meth:`get_trx_receipt` and :meth:`get_trx_receipt_wait`
               to retrieve the result of the transaction using the
               ``trx_hash``.
            -  :meth:`run_trx` which combiness the call to
               :meth:`submit_trx` with a call to
               :meth:`get_trx_receipt_wait`.

        """
        try:
            trx_hash: T_HASH = getattr(
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
        except self._web3e.InvalidTransaction as exception:
            message = (
                f'ERROR in {self.name}().submit_trx(): '
                f'InvalidTransaction says: {exception}\n'
                f'HINT1: Do you need to swap max priority fee and max fee?.\n'
                f'HINT2: Max_fee_gwei (total you will be willing to pay) must ',
                f'be >= Max_priority_fee_gwei (the tip).\n'
                )
            raise SimplEthError(message, code='C-080-060') from None
        except AttributeError:
            message = (
                f'ERROR in {self.name}().submit_trx(): '
                f'Contract does not have a valid contract object.\n'
                f'HINT: Do you need to do a connect()?\n'
                )
            raise SimplEthError(message, code='C-080-070') from None
        except TypeError:
            message = (
                f'ERROR in {self.name}().submit_trx(): '
                f'Bad type for trx_name: "{trx_name}"\n'
                f'HINT 1: Check transaction argument types.\n'
                f'HINT 2: Check all transaction arguments were specified.\n'
                )
            raise SimplEthError(message, code='C-080-080') from None
        except ValueError as exception:
            value_error_message: str = dict(exception.args[0])['message']
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
            raise SimplEthError(message, code='C-080-090') from None
        return trx_hash

    def _format_revert_message(self, value_error_msg: str) -> str:
        """Return a message to explain why a transaction was reverted.

        A `ValueError` exception message will have one of two strings
        that will be reformatted:
        1) 'VM Exception while processing transaction: revert
           <modifier's message>'
        2) 'VM Exception while processing transaction: revert'

        The first is due to a `GUARD` modifier and the failure reason is
        the `<modifier's message>`, which comes from the Solidity code.
        This is the more typical case.

        The second is due to a transaction being reverted. So far, the
        only reason I have seen that is when the initial transaction
        calls other transactions and one of those called transactions
        fails.

        This method will parse the `ValueError` message, determine
        which of the conditions caused the exception, and return an
        explanation the caller can put in the ``SimplEthError`` back to
        the user.

        :param value_error_msg: `ValueError` exception message.
        :type value_error_msg: str
        :rtype: str
        :return: message explaining the Solidity transaction revert

        :note: This is the method that adds the eye-catcher, `GUARDMSG:`,
            that appears in the SimplEthError explanation message
            to flag a transaction was stopped because it failed to
            pass one of the pre-conditions in a modifier for the
            contract.  You can change this eye-catcher but some apps
            may be watching for that string.

        """
        # TBD - what happens when a contract transaction assert()
        # fails? Does that go through this as well?
        # TBD - does this get called when a transaction sends
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
        """Return the contract ABI saved in the ABI file.

        When the Solidity compiler runs it writes the ABI to the
        `<contract>.abi` file in the artifact directory.

        Open the file, read the ABI, and return to caller.

        :rtype: list
        :return: contract `ABI`

        :raises SimplEthError: if ABI artifact file not found

        """
        try:
            with open(self._artifact_abi_filepath, encoding='UTF-8') as abi_file:
                abi: T_ABI = json.load(abi_file)
        except FileNotFoundError:
            message: str = (
                f'ERROR in {self.name}()._get_artifact_abi(). '
                f'Unable to read ABI file.\n'
                f'Full path: {self._artifact_abi_filepath}\n'
                f'Contract name of "{self._name}" is bad.\n'
                f'HINT 1: Check the spelling of the contract name.\n'
                f'HINT 2: You may need to do a new compile.\n'
                )
            raise SimplEthError(message, code='C-100-010') from None
        return abi

    def _get_artifact_address(self) -> str:
        """Return the contract blockchain address saved in the address
        file.

        The address is stored in the `<contract>.addr` file in the
        artifact directory.

        This address is written to the file when the contract is
        deployed.

        Open the file, get the address, and return it.

        :rtype: str
        :return: contract blockchain address
        :raises SimplEthError:

            -  if artifact address file is not found
            -  if the address is not valid

        """
        try:
            with open(self._artifact_address_filepath, encoding='UTF-8') as address_file:
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
        `<contract>.bytecode` file in the `artifact` directory.

        Open the file, read the bytecode, and return to caller.

        :rtype: str
        :return: contract bytecode

        """
        try:
            with open(self._artifact_bytecode_filepath, encoding='UTF-8') as bytecode_file:
                bytecode: T_BYTECODE = bytecode_file.read()
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

    def _get_deployed_code(self) -> T_DEPLOYED_CODE:
        """Return the bytecode deployed on the blockchain.

        :rtype: str
        :return: deployed bytecode
        :note:

            -  `bytecode` returned by :meth:`bytecode` contains the
               instructions for the contract plus the instructions
               to do the deployment of the contract.
               The `bytecode` returned by :meth:`deployed_code` and
               by this method is the same `bytecode` without the
               instructions for deployment.

        """
        deployed_code: T_DEPLOYED_CODE = \
            self._blockchain.eth.get_code(self.address).hex()
        return deployed_code

    def _get_size(self) -> int:
        """Return the size of the deployed bytecode.

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
            with open(self._artifact_address_filepath, 'w', encoding='UTF-8') as address_file:
                address_file.write(contract_address)
        except FileNotFoundError:
            message = (
                f'ERROR in {self.name}()._set_artifact_address(): '
                f'Unable to write address file for {self.name}.\n'
                f'Full path: {self._artifact_address_filepath}'
                )
            raise SimplEthError(message, code='C-150-020') from None
        return True
# end of Contract()


class Convert:
    """Conversion methods for Ether denominations and time values

    **METHODS**

    -  :meth:`convert_ether` - convert amount from one denomination to another
    -  :meth:`denominations_to_wei` - returns valid denominations and values
    -  :meth:`epoch_time` - returns current time in epoch seconds
    -  :meth:`local_time_string` - returns current local time as a string
    -  :meth:`to_local_time_string` - convert time in epoch seconds to
       time string, in local time

    :notes: The time conversion methods are standard one-line
        Python methods. I put them here, so I wouldn't have to look
        them up, and I'd always use the same method.

    """
    def convert_ether(
            self,
            amount: Union[int, float],
            from_denomination: str,
            to_denomination: str
            ) -> T_DECIMAL:
        """Convert the amount from one Ether denomination to another.

        :param amount: amount to be converted
        :type amount: int | float
        :param from_denomination: unit of denomination of ``amount``
        :type from_denomination: str
        :param to_denomination: unit of denomination of `result`
        :type to_denomination: str
        :rtype: Decimal
        :return: converted ``amount``
        :example:
            >>> from simpleth import Convert
            >>> c = Convert()
            >>> c.convert_ether(100, 'wei', 'ether')
            Decimal('1.00E-16')
            >>> c.convert_ether(100, 'ether', 'wei')
            Decimal('100000000000000000000')
            >>> int(c.convert_ether(25, 'ether', 'gwei'))
            25000000000

        :note: `web3.py` has two conversion methods: `to_wei()` and
            `from_wei()`. This function is more flexible and does
            not require a `Blockchain` object to use.

        :see: :meth:`denominations_to_wei` for valid strings to use
            for ``from_denomination`` and ``to_denomination``.

        """
        if from_denomination not in self.denominations_to_wei():
            message: str = (
                f'ERROR in convert_ether({amount}, {from_denomination}, '
                f'{to_denomination}): \n'
                f'the from_denomination is bad.\n'
                f'HINT: Check spelling and make sure it is a string.'
                )
            raise SimplEthError(message, code='V-010-010') from None
        if to_denomination not in self.denominations_to_wei():
            message = (
                f'ERROR in convert_ether({amount}, {from_denomination}, '
                f'{to_denomination}): \n'
                f'the to_denomination is bad.\n'
                f'HINT: Check spelling and make sure it is a string.'
                )
            raise SimplEthError(message, code='V-010-020') from None
        from_units_wei = self.denominations_to_wei()[from_denomination]
        to_units_wei = self.denominations_to_wei()[to_denomination]

        getcontext().prec = PRECISION
        conversion_factor: T_DECIMAL = Decimal(str(from_units_wei)) / \
            Decimal(str(to_units_wei))
        converted_amount: T_DECIMAL = Decimal(str(amount)) * conversion_factor
        return converted_amount

    @staticmethod
    def denominations_to_wei() -> Dict[str, int]:
        """Return denominations and their value in units of wei.

        :rtype: dict
        :return:
            -  `key` is the name of an Ether `denomination`
            -  `value` is the amount in wei for one of that denomination

        :example:
            >>> from simpleth import Convert
            >>> c = Convert()
            >>> c.convert_ether(100, 'wei', 'ether')
            Decimal('1.00E-16')
            >>> c.convert_ether(100, 'ether', 'wei')
            Decimal('100000000000000000000')
            >>> int(c.convert_ether(25, 'ether', 'gwei'))
            25000000000
            >>> c.denominations_to_wei()['finney']
            1000000000000000
            >>> import math
            >>> for key, value in c.denominations_to_wei().items():
            ...     print(f'{key:10} = 10**{int(math.log10(value)):<2} = {value:<41,} wei')
            ...
            wei        = 10**0  = 1                                         wei
            kwei       = 10**3  = 1,000                                     wei
            babbage    = 10**3  = 1,000                                     wei
            femtoether = 10**3  = 1,000                                     wei
            mwei       = 10**6  = 1,000,000                                 wei
            lovelace   = 10**6  = 1,000,000                                 wei
            picoether  = 10**6  = 1,000,000                                 wei
            gwei       = 10**9  = 1,000,000,000                             wei
            shannon    = 10**9  = 1,000,000,000                             wei
            nanoether  = 10**9  = 1,000,000,000                             wei
            nano       = 10**9  = 1,000,000,000                             wei
            szabo      = 10**12 = 1,000,000,000,000                         wei
            microether = 10**12 = 1,000,000,000,000                         wei
            micro      = 10**12 = 1,000,000,000,000                         wei
            finney     = 10**15 = 1,000,000,000,000,000                     wei
            milliether = 10**15 = 1,000,000,000,000,000                     wei
            milli      = 10**15 = 1,000,000,000,000,000                     wei
            ether      = 10**18 = 1,000,000,000,000,000,000                 wei
            kether     = 10**21 = 1,000,000,000,000,000,000,000             wei
            grand      = 10**21 = 1,000,000,000,000,000,000,000             wei
            mether     = 10**24 = 1,000,000,000,000,000,000,000,000         wei
            gether     = 10**27 = 1,000,000,000,000,000,000,000,000,000     wei
            tether     = 10**30 = 1,000,000,000,000,000,000,000,000,000,000 wei

        :notes: These are the denominations recognized by :meth:`convert_ether`.
        :see: Source:
              https://web3py.readthedocs.io/en/stable/examples.html?highlight=denominations#converting-currency-denominations

        """
        return {
            'wei': 1,
            'kwei': 10**3,
            'babbage': 10**3,
            'femtoether': 10**3,
            'mwei': 10**6,
            'lovelace': 10**6,
            'picoether': 10**6,
            'gwei': 10**9,
            'shannon': 10**9,
            'nanoether': 10**9,
            'nano': 10**9,
            'szabo': 10**12,
            'microether': 10**12,
            'micro': 10**12,
            'finney': 10**15,
            'milliether': 10**15,
            'milli': 10**15,
            'ether': 10**18,
            'kether': 10**21,
            'grand': 10**21,
            'mether': 10**24,
            'gether': 10**27,
            'tether': 10**30
            }

    @staticmethod
    def epoch_time() -> float:
        """Return current time in epoch seconds.

        :rtype: float
        :return: current time, in epoch seconds
        :example:
            >>> from simpleth import Convert
            >>> Convert().epoch_time()
            1638825195.6231368

        """
        return time.time()

    @staticmethod
    def local_time_string(t_format: str = TIME_FORMAT) -> str:
        """Return current local time as a time string.

        :param t_format: format of outputted time using `strftime` codes
            (**optional**, default: :const:`TIME_FORMAT`)
        :param t_format: str
        :rtype: str
        :return: current time
        :example:
            >>> from simpleth import Convert
            >>> c = Convert()
            >>> c.local_time_string()
            '2021-12-06 15:35:28'
            >>> c.local_time_string('%A %I:%M:%S %p')
            'Monday 03:36:48 PM'

        :see: https://strftime.org/ for time format codes.

        """
        try:
            local_time_string: str = time.strftime(
                t_format,
                time.localtime()
                )
        except TypeError as exception:
            message: str = (
                f'ERROR in local_time_string({t_format}: '
                f'TypeError says {exception}.\n'
                f't_format must be a string with strftime format codes.\n'
                f'HINT: Make sure t_format is a string.'
                )
            raise SimplEthError(message, code='V-020-010') from None
        return local_time_string

    @staticmethod
    def to_local_time_string(
            epoch_sec: Union[int, float],
            t_format: str = TIME_FORMAT
            ) -> str:
        """Convert epoch seconds into local time string.

        :param epoch_sec: epoch time, in seconds
        :type epoch_sec: int | float
        :param t_format: format of outputted time using `strftime` codes
            (**optional**, default: :const:`TIME_FORMAT`)
        :param t_format: str
        :rtype: str
        :return: local time equivalent to epoch seconds
        :example:
                >>> from simpleth import Convert
                >>> c = Convert()
                >>> epoch = c.epoch_time()
                >>> epoch
                1638825248.9298458
                >>> c.to_local_time_string(epoch)
                '2021-12-06 15:14:08'
                >>> c.to_local_time_string(epoch, '%A %I:%M:%S %p')
                'Monday 03:14:08 PM'

        :see: https://strftime.org/ for time format codes.

        """
        try:
            to_local_time_string: str = time.strftime(
                t_format,
                time.localtime(epoch_sec)
                )
        except TypeError as exception:
            message: str = (
                f'ERROR in local_time_string({t_format}: '
                f'TypeError says {exception}\n'
                f't_format must be a string with strftime format codes.\n'
                f'HINT: Make sure t_format is a string.'
                )
            raise SimplEthError(message, code='V-030-010') from None
        return to_local_time_string
# end of Convert()


class Filter:
    """Create event filter and use to search for events.

    In order to search for particular events emitted by transactions,
    you create a filter with the search criteria and use that filter
    to perform your search.

    `simpleth` implements the ability to search for events by `event name`.
    You can search blocks already on the blockchain using
    :meth:`get_old_events()`.
    Besides, the name of the event, you specify how far back, by giving the
    number of blocks, to search. You can watch new blocks as they are
    added to the blockchain with :meth:`get_new_events()`.

    **PROPERTIES**

    -  None

    **METHODS**

    -  :meth:`create_filter` - return a filter for an event
    -  :meth:`get_new_events` - return event info from newly mined blocks
    -  :meth:`get_old_events` - return event info from blocks on chain

    :notes:
        -  The `web3.py` API documentation describes more powerful filters
           at: https://web3py.readthedocs.io/en/stable/web3.eth.html#filters.
        -  :attr:`Blockchain.eth` can be used to access the methods
           described.

    """
    def __init__(self, contract: Contract) -> None:
        """Create instance for filters using the contract instance.

        This ``Filter`` will be used to find events emitted by
        transactions in ``Contract``.

        :param contract: :class:`Contract` object
        :type contract: object
        :example:
            >>> from simpleth import Contract, Filter
            >>> c = Contract('Test')
            >>> f = Filter(c)
            >>> f
            <simpleth.Filter object at 0x0000021FB2FD5DE0>

        """
        self._contract: Contract = contract
        """Private :class"`Contract' instance"""
        self._web3_contract: T_WEB3_CONTRACT_OBJ = \
            self._contract.web3_contract
        """Private :attr:`Contract.web3_contract` instance"""

    def create_filter(self, event_name: str) -> T_FILTER_OBJ:
        """Return a filter used to watch for a specific event.

        Only needed for use with :meth:`get_new_events` to
        create a filter to be used when watching for future emissions
        of ``event_name``.

        :param event_name: name of the event
        :type event_name: str
        :rtype: object
        :return: `web3._utils.filters.LogFilter` object
        :raises SimplEthError:

            -  if ``event_name`` is bad
            -  if a :meth:`connect` is needed

        :example:
            >>> from simpleth import Contract, Filter
            >>> c = Contract('Test')
            >>> c.connect()
            '0xD34dB707D084fdd1D99Cf9Af77896283a083c470'
            >>> f = Filter(c)
            >>> f_NumsStored = f.create_filter('NumsStored')
            >>> f_NumsStored
            <web3._utils.filters.LogFilter object at 0x0000021FB2FB1C

        :see:

            -  :meth:`get_new_events()` for using this new `event_filter`
               to watch for the event.
            -  :attr:`Contract.events` for the list of valid events emitted
               by this contract.

        """
        try:
            event_filter: T_FILTER_OBJ = getattr(
                self._web3_contract.events,
                event_name
                )().createFilter(fromBlock='latest')
        except self._contract.web3e.ABIEventFunctionNotFound:
            message: str = (
                f'ERROR in create({event_name}).\n'
                f'The event: {event_name} was not found.\n'
                f'Valid event_names: {self._contract.event_names}\n'
                f'HINT: Check the spelling of your event_name.\n'
                )
            raise SimplEthError(message, code='F-020-010') from None
        return event_filter

    def get_new_events(self, event_filter: T_FILTER_OBJ) -> List:
        """Search newly mined blocks for a specific event.

        The first call checks for the event in the blocks mined
        since ``event_filter`` was created. Each subsequent call
        checks for the event in the blocks mined since the previous call.

        :param event_filter: specifies the event to find
        :type event_filter: object
        :rtype: list
        :return:

            -  list with one item for each event emitted since the
               previous use of ``event_filter``.
            -  empty list if no events were emitted since previous
               use of ``event_filter``.

        :example:

            >>> from simpleth import Blockchain, Contract, Filter
            >>> b = Blockchain()
            >>> user = b.accounts[3]
            >>> c = Contract('Test')
            >>> c.connect()
            '0xD34dB707D084fdd1D99Cf9Af77896283a083c470'
            >>> f = Filter(c)
            >>> filter_NumsStored = f.create_filter('NumsStored')
            >>> result_NumsStored =_NumsStored = c.run_trx(user,'storeNums',5,6,7)
            >>> events_NumsStored = f.get_new_events(filter_NumsStored)
            >>> len(events_NumsStored)
            1
            >>> events_NumsStored
            [{'block_number': 137, 'args': {'num0': 5, 'num1': 6, ... c44a'}  }]
            >>> result1_NumsStored = c.run_trx(user,'storeNums',5,6,7)
            >>> result2_NumsStored = c.run_trx(user,'storeNums',5,6,7)
            >>> result3_NumsStored = c.run_trx(user,'storeNums',5,6,7)
            >>> result4_NumsStored = c.run_trx(user,'storeNums',5,6,7)
            >>> events_NumsStored = f.get_new_events(filter_NumsStored)
            >>> len(events_NumsStored)
            4
            >>> events_NumsStored
            [{'block_number': 138, 'args': {'num0': 5, 'num1':  ... }}]

        :notes: :meth:`get_past_events` looks backward and searches old
            blocks. :meth:`get_new_events` looks forward at the
            newly mined blocks.

        :see:
            -  :meth:`create_filter` to create ``event_filter``.
            -  :attr:`Contract.events` for the list of valid events
               emitted by this contract.

        """
        filter_list: T_FILTER_LIST = event_filter.get_new_entries()
        return self._create_simple_events(filter_list)

    def get_old_events(
            self,
            event_name: str,
            num_blocks: int
            ) -> List:
        """Search previously mined blocks for a specific event.

        :param event_name: name of the event to find
        :type event_name: str
        :param num_blocks: number of mined blocks to search
        :type num_blocks: int
        :rtype: list
        :return: one item for each event found; empty list if
            no events found

        :raises SimplEthError:

            -  if ``event_name`` was bad
            -  if no :meth:`connect`

        :example:
            >>> from simpleth import Contract, Filter
            >>> c = Contract('Test')
            >>> c.connect()
            '0xD34dB707D084fdd1D99Cf9Af77896283a083c470'
            >>> f = Filter(c)
            >>> events_NumsStored = f.get_old_events('NumsStored', 3)
            >>> len(events_NumsStored)
            3
            >>> events_NumsStored
            [{'block_number': 139, 'args': {'num0': 5, 'num1': 6, ...}}]

        :notes:

            -  Unlike :meth:`get_new_events`, an ``event_filter`` is not
               needed. This method builds its own event filter based on
               ``event_name``.
            -  :meth:`get_old_events` looks backward and searches old
               blocks. :meth:`get_new_events` looks forward at the
               newly mined blocks.
            -  Future: could add get_old_events_range(event_name, from, to)
               that is similar but will search in the range of blocks
               specified.
            -  Beware: seems like doing a meth:`get_old_events` after a
               meth:`deploy` doesn't work. You must do it after a
               meth:`connect`. See test_hello4:test_HelloWorld4_deploy.
               I tried to do a get_old_events() and check the initGreeting,
               but could not get it to work. web3_contract was null. Didn't make
               sense so I pulled that piece of the test.
               (TBD: investigate and fix)

        :see: :attr:`Contract.events` for the list of valid events
               emitted by this contract.

        """
        if not isinstance(num_blocks, int):
            message: str = (
                f'ERROR in get_old_events({event_name}).\n'
                f'num_blocks = {num_blocks} is invalid.\n'
                f'It must be between an integer.\n'
                f'HINT: Provide a valid number for num_blocks.\n'
                )
            raise SimplEthError(message, code='F-030-010') from None
        latest_block: int = self._contract.blockchain.block_number
        if not 1 <= num_blocks <= latest_block:
            message: str = (
                f'ERROR in get_old_events({event_name}).\n'
                f'num_blocks = {num_blocks} is invalid.\n'
                f'It must be between 1 and {latest_block} (the latest block '
                f'on the chain).\n'
                f'HINT: Provide a valid number for num_blocks.\n'
                )
            raise SimplEthError(message, code='F-030-020') from None

        from_block: int = latest_block - (num_blocks - 1)
        to_block: Union[str, int] = 'latest'
        try:
            event_filter: T_FILTER_OBJ = getattr(
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
                f'Valid event_names: {self._contract.event_names}\n'
                f'HINT: Check spelling of event_name arg.\n'
                )
            raise SimplEthError(message, code='F-030-030') from None
        except TypeError as exception:
            message = (
                f'ERROR in get_old_events({event_name}).\n'
                f'Type Error says: {exception}.\n'
                f'HINT: Check the type for the args.\n'
                )
            raise SimplEthError(message, code='F-030-040') from None

        # getattr() worked. we have a valid filter to use
        filter_list: T_FILTER_LIST = event_filter.get_all_entries()
        return self._create_simple_events(filter_list)

    @staticmethod
    def _create_simple_events(filter_list: T_FILTER_LIST) -> List:
        """Return a list of events with the essential data.

        The ''filter_list`` is an AttributeDict with args, event name, logIndex,
        transactionIndex, transactionHash, address, blockHash, and blockNumber.
        For `simpleth`, just return the essential data: blockNumber, args, and
        transactionHash.

        :param filter_list: the list returned from :meth:`get_new_entries`
            or :meth:`event_filter.get_new_entries`
        :type filter_list: AttributeDict
        :rtype: list
        :return: list of the same events with only `args`, `block_number`,
            and `hash`

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


class Results:
    """Data class created after a transaction is mined making most of
    the transaction information easily accessible.

    Users will not create `result` objects. Rather, the following
    create and return `result` objects:

    -  :meth:`Contract.run_trx`
    -  :meth:`Contract.get_trx_receipt`
    -  :meth:`Contract.get_trx_receipt_wait`

    By accessing the `result` object returned from one of these methods,
    the following properties make it simple to access the outcome
    details:

    **PROPERTIES**

    -  :meth:`block_number` - block number containing transaction
    -  :meth:`block_time_epoch` - time block mined, in epoch seconds
    -  :meth:`contract` - :class:`Contract` object and same as ``contract`` constructor arg
    -  :meth:`contract_address` - address of contract with the transaction
    -  :meth:`contract_name` - name of contract with the transaction
    -  :meth:`event_args` - arg(s) for event(s) emitted by transaction
    -  :meth:`event_logs` - event log(s) from transaction for ``event_name``
    -  :meth:`event_names` - event name(s) emitted by transaction
    -  :meth:`gas_price_wei` - price of gas used by transaction, in wei
    -  :meth:`gas_used` - units of gas needed for transaction
    -  :meth:`transaction` - `web3.eth` transaction dictionary info
    -  :meth:`trx_args` - arguments passed into transaction
    -  :meth:`trx_hash` - transaction hash to identify submitted transaction
    -  :meth:`trx_name` - name of transaction
    -  :meth:`trx_receipt` - receipt to identify mined transaction
    -  :meth:`trx_sender` - address sending the transaction
    -  :meth:`trx_value_wei` - amount of Ether, in wei, sent with transaction

    **METHODS**

    -  :meth:`__str__` - allows ``print(<result>)`` to output most properties

    **OTHER ATTRIBUTES**
    For debugging or using the `web3` data formatting the following attributes
    are available:

    -  ``_contract`` - :meth:`Contract` object passed in as arg to `Results()`
    -  ``web3_contract_object`` - `web3` object passed in as arg to `Results()`
    -  ``web3_event_logs`` - `web3` format of the event log(s) generated by
        the transaction
    -  ``web3_function_object`` - `web3` object for the Solidity function that
       ran the transaction.
    -  ``web3_receipt`` - `web3` format of the transaction receipt data. Should
       be the same as :meth:`receipt` but `web3` uses `AttributeDict` and
       `HexBytes`.
    -  ``web3_transaction`` - `web3` format of the transaction data. Should be
       same as :meth:`transaction` but `web3` uses `AttributeDict` and
       `HexBytes`.

    One of the easiest ways to use :class:`Results` is to `print` the `result`
    as shown below.

    :example:
        >>> from simpleth import Blockchain, Contract
        >>> b = Blockchain()
        >>> user = b.accounts[2]
        >>> c = Contract('Test')
        >>> c.connect()
        '0xD34dB707D084fdd1D99Cf9Af77896283a083c470'
        >>> trx_result = c.run_trx(user,'storeNums',30,20,10)
        >>> print(trx_result)
        Block number = 450
        Block time_epoch = 1640055579
        Contract address = 0x2f1E0A12de6741f26FCC34776764c87f46a1B7aA
        Contract name = Test
        Event args = {'num0': 4, 'num1': 5, 'num2': 6}
        Event log = [{'args': {'num0': 4, 'num1': 5, 'num2': 6}, ',
        Event name = NumsStored
        Gas price wei = 20000000000
        Gas used = 83443
        Transaction = {'hash': '0xc5e3fd42eddefdcf79b511438b4b5ef58c18ad1b
        Trx args = {'_num0': 4, '_num1': 5, '_num2': 6}
        Trx hash = 0xc5e3fd42eddefdcf79b511438b4b5ef58c18ad1b761b09f9790900718155f21f
        Trx name = storeNums
        Trx receipt = {'transactionHash': HexBytes('0xc5e3fd42eddefdcf79b511
        Trx sender = 0xa894b8d26Cd25eCD3E154a860A86f7c75B12D993
        Trx value_wei = 0

    """
    def __init__(self,
                 receipt: T_RECEIPT,
                 contract: Contract
                 ) -> None:
        """Create data object with the result of a transaction.

        :param receipt: transaction receipt created after the
             transaction was mined
        :type receipt: T_RECEIPT
        :param contract: :class:`Contract` containing the transaction
        :type contract: object

        """
        #
        # Gather information from the transaction's web3 receipt data
        #
        self.web3_receipt: T_RECEIPT = receipt
        self._trx_receipt: dict = self._to_simpleth_receipt(self.web3_receipt)
        self._gas_used: int = self._trx_receipt['gasUsed']
        self._trx_sender: str = self._trx_receipt['from']
        self._trx_hash: T_HASH = self._trx_receipt['transactionHash']
        self._block_number: int = self._trx_receipt['blockNumber']

        #
        # Gather information from the web3 transaction data
        #
        self.web3_transaction: T_TRANSACTION = \
            contract.blockchain.eth.get_transaction(self._trx_hash)
        self._transaction: dict = self._to_simpleth_transaction(
            self.web3_transaction)
        self._gas_price_wei: int = self._transaction['gasPrice']
        self._trx_value_wei: int = self._transaction['value']

        #
        # Gather information from the simpleth contract object
        #
        self._contract: Contract = contract
        self._contract_address: str = contract.address
        self._contract_name: str = contract.name
        self._block_time: int = \
            self._contract.blockchain.eth.get_block(self._block_number).timestamp
        self.web3_contract_object: T_WEB3_CONTRACT_OBJ = \
            self._contract.web3_contract

        #
        # Gather details on the transaction name and args
        #
        self._trx_name: str = ''
        self._trx_args: dict = {}
        self.web3_function_object = None
        if self._transaction['to']:
            # If there is a value for `to`, this was a transaction using
            # a deployed contract. Proceed to get interesting info.
            function_obj, function_params = \
                self.web3_contract_object.decode_function_input(
                    self._transaction['input']
                    )
            # Get trx_name from the name of the function object
            self._trx_name = \
                str(function_obj).strip('<Function ').split('(')[0]
            self._trx_args = function_params
            # Not surfaced as a property. Available as a private attribute only.
            self.web3_function_object = function_obj
        else:
            # This was a `deploy()`. The input is the ABI and can't be
            # decoded. Assign 'deploy' to the trx_name. (A `deploy()` does
            # not have a value for `to` since the contract does not yet have
            # an address nor does it have a function object.)
            self._trx_name = 'deploy'

        #
        # Gather details on event(s), if any, emitted by the transaction
        #
        self._event_names: list[str] = []
        self._event_args: list[dict] = []
        self._event_logs: list[dict] = []
        self.web3_event_logs: list[T_EVENT_LOG_OBJ] = []
        for event_name in self._contract.event_names:
            # for every event defined in the contract
            try:
                # use the event name to get the `web3` contract event object
                contract_event: T_CONTRACT_EVENT = getattr(
                    self.web3_contract_object.events,
                    event_name
                    )
            except self._contract.web3e.ABIEventFunctionNotFound as exception:
                message = (
                    f'ERROR in getting results for '
                    f'{self._contract_name}.{self._trx_name}().\n'
                    f'MismatchedABI says: {exception}\n'
                    f'The event, "{event_name}" was in the simpleth contract '
                    f'list of `event_names` but was not found in\n'
                    f'the `web3 contract` object list of `events`. This is not '
                    f'a typical error.\n'
                    f'HINT: try recompiling and redeploying the contract.'
                    )
                raise SimplEthError(message, code='R-010-020') from None

            try:
                # use the `web3` contract event object to get the details for the
                # event, an empty tuple is returned if event was not used. DISCARD
                # silently discards any logs that had errors and returns processed
                # logs that do not contain any errors.
                event_log: T_EVENT_LOG_OBJ = contract_event().processReceipt(
                        self.web3_receipt,
                        errors=DISCARD
                        )
                if event_log:
                    # This event had data, so it was emitted by the transaction.
                    # Add it to the event data list.
                    self.web3_event_logs.append(event_log)
                    self._event_logs.append(dict(self._to_simpleth_event(event_log[0])))
                    self._event_args = [e_log['args'] for e_log in self.event_logs]
                    self._event_names = [e_log['event'] for e_log in self.event_logs]

            except contract.web3e.MismatchedABI as exception:
                message = (
                    f'ERROR in getting results for '
                    f'{self._contract_name}.{self._trx_name}().\n'
                    f'MismatchedABI says: {exception}\n'
                    f'The event ABI in the contract definition does not match '
                    f'the ABI deployed on the chain.\n'
                    f'HINT1: are you connecting to the most recently compiled version '
                    f'of the contract?\n'
                    f'HINT2: try recompiling and redeploying the contract.'
                    )
                raise SimplEthError(message, code='R-010-020') from None

    @property
    def block_number(self) -> int:
        """Return block number of block containing the transaction.

        :rtype: int
        :return: number of block with transaction
        :example:
            >>> from simpleth import Blockchain, Contract
            >>> b = Blockchain()
            >>> user = b.accounts[8]
            >>> c = Contract('Test')
            >>> c.connect()
            '0xD34dB707D084fdd1D99Cf9Af77896283a083c470'
            >>> trx_result = c.run_trx(user,'storeNums',10,10,10)
            >>> trx_result.block_number
            142

        """
        return self._block_number

    @property
    def block_time_epoch(self) -> int:
        """Return time block with transaction was mined,
        in epoch seconds.

        :rtype: int
        :return: time, in epoch seconds, when block was mined.
        :example:
            >>> from simpleth import Blockchain, Contract
            >>> b = Blockchain()
            >>> user = b.accounts[8]
            >>> c = Contract('Test')
            >>> c.connect()
            '0xD34dB707D084fdd1D99Cf9Af77896283a083c470'
            >>> trx_result = c.run_trx(user,'storeNums',10,10,10)
            >>> trx_result.block_time_epoch
            1638751644

        """
        return self._block_time

    @property
    def contract(self) -> Contract:
        """Return `Contract` object for the transaction.

        This is the ``contract`` parameter used for :meth:``__init__``.

        :rtype: obj
        :return: `simpleth` :meth:`Contract` object
        :example:

        TBD

        """
        return self._contract

    @property
    def contract_address(self) -> str:
        """Return address of the transaction's contract.

        :rtype: str
        :return: address of contract
        :example:
            >>> from simpleth import Blockchain, Contract
            >>> b = Blockchain()
            >>> user = b.accounts[8]
            >>> c = Contract('Test')
            >>> c.connect()
            '0xD34dB707D084fdd1D99Cf9Af77896283a083c470'
            >>> trx_result = c.run_trx(user,'storeNums',10,10,10)
            >>> trx_result.contract_address
            '0xD34dB707D084fdd1D99Cf9Af77896283a083c470'

        """
        return self._contract_address

    @property
    def contract_name(self) -> str:
        """Return name of the contract issuing the transaction.

        :rtype: str
        :return: name of contract
        :example:
            >>> from simpleth import Blockchain, Contract
            >>> b = Blockchain()
            >>> user = b.accounts[8]
            >>> c = Contract('Test')
            >>> c.connect()
            '0xD34dB707D084fdd1D99Cf9Af77896283a083c470'
            >>> trx_result = c.run_trx(user,'storeNums',10,10,10)
            >>> trx_result.contract_name
            'Test'

        """
        return self._contract_name

    @property
    def event_args(self) -> list[dict]:
        """Return args for the event emitted by the transaction.

        :rtype: list[dict]
        :return: one dict for each event emitted; key is the arg name
             and the value is the value of the arg
        :notes:

        -  The event name that emitted these args is found in
           :meth:`event_names`. Use the same index into list to get the
           `event name`.

        :example:
            >>> from simpleth import Blockchain, Contract
            >>> b = Blockchain()
            >>> user = b.accounts[8]
            >>> c = Contract('Test')
            >>> c.connect()
            '0xD34dB707D084fdd1D99Cf9Af77896283a083c470'
            >>> trx_result = c.run_trx(user,'storeNums',10,10,10)
            >>> trx_result.event_args
            {'num0': 10, 'num1': 10, 'num2': 10}

        """
        return self._event_args

    @property
    def event_logs(self) -> list[dict]:
        """Return event logs resulting from transaction.

        This differs from the `web3.py` event logs in three ways:

        1)  `web3` returns the log as a list of tuples, each tuple has
            one event emitted.
        2)  `web3` returns the tuple item as an AttributeDict.
            This uses dicts. Likewise, within an event there are
            AttributeDicts and this uses dicts instead.
        3)  `web3` returns hashes as HexBytes and this uses strings.

        :rtype: list
        :return: one dict per event emitted
        :example:
            >>> from simpleth import Blockchain, Contract
            >>> b = Blockchain()
            >>> user = b.accounts[8]
            >>> c = Contract('Test')
            >>> c.connect()
            '0xD34dB707D084fdd1D99Cf9Af77896283a083c470'
            >>> trx_result = c.run_trx(user,'storeNums',10,10,10)
            >>> trx_result.event_logs
            [{'args': {'num0': 10, 'num1': 20, 'num2': 20}, 'event': 'NumsStored'

        """
        return self._event_logs

    @property
    def event_names(self) -> list[str]:
        """Return names of the event emitted by the transaction.

        :rtype: list[str]
        :return: list with names of each event emitted
        :notes:

        -  The event args that were emitted for this event are found in
           :meth:`event_args`. Use the same index into list to get the
           `event args`.

        :example:
            >>> from simpleth import Blockchain, Contract
            >>> b = Blockchain()
            >>> user = b.accounts[8]
            >>> c = Contract('Test')
            >>> c.connect()
            '0xD34dB707D084fdd1D99Cf9Af77896283a083c470'
            >>> trx_result = c.run_trx(user,'storeNums',10,10,10)
            >>> trx_result.event_names
            ['NumsStored']

        """
        return self._event_names

    @property
    def gas_price_wei(self) -> int:
        """Return price, in wei, charged for each unit of gas
        used by the transaction.

        :rtype: int
        :return: gas price, in wei
        :example:
            >>> from simpleth import Blockchain, Contract
            >>> b = Blockchain()
            >>> user = b.accounts[8]
            >>> c = Contract('Test')
            >>> c.connect()
            '0xD34dB707D084fdd1D99Cf9Af77896283a083c470'
            >>> trx_result = c.run_trx(user,'storeNums',10,10,10)
            >>> trx_result.gas_price_wei
            20000000000

        """
        return self._gas_price_wei

    @property
    def gas_used(self) -> int:
        """Return units of gas used by the transaction.

        :rtype: int
        :return: units of gas used to run transaction
        :example:
            >>> from simpleth import Blockchain, Contract
            >>> b = Blockchain()
            >>> user = b.accounts[8]
            >>> c = Contract('Test')
            >>> c.connect()
            '0xD34dB707D084fdd1D99Cf9Af77896283a083c470'
            >>> trx_result = c.run_trx(user,'storeNums',10,10,10)
            >>> trx_result.gas_used
            25863

        """
        return self._gas_used

    @property
    def transaction(self) -> T_TRANSACTION:
        """Return the transaction info kept by `web3 eth`.

        :rtype: dict
        :return: transaction info
        :example:
            >>> from simpleth import Blockchain, Contract
            >>> b = Blockchain()
            >>> user = b.accounts[8]
            >>> c = Contract('Test')
            >>> c.connect()
            '0xD34dB707D084fdd1D99Cf9Af77896283a083c470'
            >>> trx_result = c.run_trx(user,'storeNums',10,10,10)
            >>> trx_result.transaction
            {'hash': '0x81d725c47a94e71aa40561ff96da8d99ce105a1327239a867099bb0e480e492b',

        """
        return self._transaction

    @property
    def trx_args(self) -> dict:
        """Return arguments passed into the transaction.

        :rtype: dict
        :return: `key` is `param name`; `value` is arg value passed to
            transaction
        :example:
            >>> from simpleth import Blockchain, Contract
            >>> b = Blockchain()
            >>> user = b.accounts[8]
            >>> c = Contract('Test')
            >>> c.connect()
            '0xD34dB707D084fdd1D99Cf9Af77896283a083c470'
            >>> trx_result = c.run_trx(user,'storeNums',10,10,10)
            >>> trx_result.trx_args
            {'_num0': 10, '_num1': 10, '_num2': 10}

        """
        return self._trx_args

    @property
    def trx_hash(self) -> T_HASH:
        """Return transaction hash for the mined transaction.

        :rtype: str
        :return: hash that identifies this transaction on blockchain.
        :example:
            >>> from simpleth import Blockchain, Contract
            >>> b = Blockchain()
            >>> user = b.accounts[8]
            >>> c = Contract('Test')
            >>> c.connect()
            '0xD34dB707D084fdd1D99Cf9Af77896283a083c470'
            >>> trx_result = c.run_trx(user,'storeNums',10,10,10)
            >>> trx_result.trx_hash
            '0x0e36d22f42dbf641cef1e9f26daeb00f28a4850fccde39fb11886a980b8f59d6'

        """
        return self._trx_hash

    @property
    def trx_name(self) -> str:
        """Return name of the transaction.

        :rtype: str
        :return: name of transaction
        :example:
            >>> from simpleth import Blockchain, Contract
            >>> b = Blockchain()
            >>> user = b.accounts[8]
            >>> c = Contract('Test')
            >>> c.connect()
            '0xD34dB707D084fdd1D99Cf9Af77896283a083c470'
            >>> trx_result = c.run_trx(user,'storeNums',10,10,10)
            >>> trx_result.trx_name
            'storeNums'

        """
        return self._trx_name

    @property
    def trx_receipt(self) -> T_RECEIPT:
        """Return the transaction receipt.

        ``trx_receipt`` that is returned is a dict that does not use
        `AttributeDict` nor `HexBytes`. The `web3` formatted `receipt` that uses
        those data types is available as the attribute, :attr:`web3_receipt`.

        :rtype: dict
        :return: receipt after transaction was mined.
        :example:
            >>> from simpleth import Blockchain, Contract
            >>> b = Blockchain()
            >>> user = b.accounts[8]
            >>> c = Contract('Test')
            >>> c.connect()
            '0xD34dB707D084fdd1D99Cf9Af77896283a083c470'
            >>> trx_result = c.run_trx(user,'storeNums',10,10,10)
            >>> trx_result.trx_receipt
            {'transactionHash': HexBytes('0x0e36d22f42dbf641cef1e9f26daeb00f28a4850fccde39f ... ')}

        """
        # TBD simplethify()
        return dict(self._trx_receipt)

    @property
    def trx_sender(self) -> str:
        """Return the adddress of account that sent the transaction.

        :rtype: int
        :return: gas price, in wei
        :example:
            >>> from simpleth import Blockchain, Contract
            >>> b = Blockchain()
            >>> user = b.accounts[8]
            >>> c = Contract('Test')
            >>> c.connect()
            '0xD34dB707D084fdd1D99Cf9Af77896283a083c470'
            >>> trx_result = c.run_trx(user,'storeNums',10,10,10)
            >>> trx_result.trx_sender
            '0xB7fc6B28ea0c1c0d4ec54143A552aF67260905cF'

        """
        return self._trx_sender

    @property
    def trx_value_wei(self) -> int:
        """Return amount of Ether, in wei, sent with the transaction.

        :rtype: int
        :return: amount of Ether, in wei, sent with the transaction
        :example:
            >>> from simpleth import Blockchain, Contract
            >>> b = Blockchain()
            >>> user = b.accounts[8]
            >>> c = Contract('Test')
            >>> c.connect()
            '0xD34dB707D084fdd1D99Cf9Af77896283a083c470'
            >>> trx_result = c.run_trx(user,'storeNums',10,10,10)
            >>> trx_result.trx_value_wei
            0

        """
        return self._trx_value_wei

    @staticmethod
    def _to_simpleth_event(web3_event: T_EVENT) -> dict:
        """Return event log entry as a dictionary with strings.

        `web3.py` structures an event in the event log using
         `AttributeDict` and HexBytes.

        This converts event to using dictionaries and strings. This
        gives `simpleth` a simpler data structure.

        :param web3_event: one event entry from a transaction event log
        :type web3_event: AttributeDict
        :rtype: dict
        :returns: the same event data but using dict and string types
        throughout.
        :notes: I'm sure there is a way to make a generalized recursive
        method to replace `AttributeDict` and `HexBytes` but my first
        attempt did not work. Try again sometime.

        """
        return {
            'args': dict(web3_event['args']),
            'event': web3_event['event'],
            'logIndex': web3_event['logIndex'],
            'transactionIndex': web3_event['transactionIndex'],
            'transactionHash': web3_event['transactionHash'].hex(),
            'address': web3_event['address'],
            'blockHash': web3_event['blockHash'].hex(),
            'blockNumber': web3_event['blockNumber']
            }

    @staticmethod
    def _to_simpleth_receipt(web3_receipt: T_RECEIPT) -> dict:
        """Return transaction receipt as a dictionary with strings.

        `web3.py` structures a receipt using `AttributeDict` and HexBytes.

        This converts the receipt using dictionaries and strings. This
        gives `simpleth` a simpler data structure.

        :param web3_receipt: `web3` transaction receipt
        :type web3_receipt: AttributeDict
        :rtype: dict
        :returns: the same receipt data but using dict and string types
        throughout.
        :notes: I'm sure there is a way to make a generalized recursive
        method to replace `AttributeDict` and `HexBytes` but my first
        attempt did not work. Try again sometime.

        """
        simpleth_logs = []
        for log in web3_receipt['logs']:
            simpleth_log = {
                'logIndex': log['logIndex'],
                'transactionIndex': log['transactionIndex'],
                'transactionHash': log['transactionHash'].hex(),
                'blockHash': log['blockHash'].hex(),
                'blockNumber': log['blockNumber'],
                'address': log['address'],
                'data': log['data'],
                'topics': [topic.hex() for topic in log['topics']],
                'type': log['type']
                }
            simpleth_logs.append(simpleth_log)

        return {
            'transactionHash': web3_receipt['transactionHash'].hex(),
            'transactionIndex': web3_receipt['transactionIndex'],
            'blockHash': web3_receipt['blockHash'].hex(),
            'blockNumber': web3_receipt['blockNumber'],
            'from': web3_receipt['from'],
            'to': web3_receipt['to'],
            'gasUsed': web3_receipt['gasUsed'],
            'cumulativeGasUsed': web3_receipt['cumulativeGasUsed'],
            'contractAddress': web3_receipt['contractAddress'],
            'logs': simpleth_logs,
            'status': web3_receipt['status'],
            'logsBloom': web3_receipt['logsBloom'].hex()
            }

    @staticmethod
    def _to_simpleth_transaction(web3_trans: T_TRANSACTION) -> dict:
        """Return transaction AttributeDict as a dictionary with strings.

        `web3.py` structures a transaction using `AttributeDict` and
        HexBytes. This converts that transaction AttributedDict to one
        using dictionaries and strings. This gives `simpleth` a simpler
        data structure.

        :param web3_trans: transaction dictionary from `web3`
        :type web3_trans: AttributeDict
        :rtype: dict
        :returns: the same transaction data but uses dict and string
        types throughout.
        :notes: I'm sure there is a way to make a generalized recursive
        method to replace `AttributeDict` and `HexBytes` but my first
        attempt did not work. Try again sometime.

        """
        return {
            'hash': web3_trans['hash'].hex(),
            'nonce': web3_trans['nonce'],
            'blockHash': web3_trans['blockHash'].hex(),
            'blockNumber': web3_trans['blockNumber'],
            'transactionIndex': web3_trans['transactionIndex'],
            'from': web3_trans['from'],
            'to': web3_trans['to'],
            'value': web3_trans['value'],
            'gas': web3_trans['gas'],
            'gasPrice': web3_trans['gasPrice'],
            'input': web3_trans['input'],
            'v': web3_trans['v'],
            'r': web3_trans['r'].hex(),
            's': web3_trans['s'].hex()
            }

    def __str__(self) -> str:
        """Print most of the results properties.

        This overrides the print() function.

        User does:  `print(<results_oject>)`

        :rtype: str
        :return: multi-line output of most `Results` properties
        :example:
            >>> from simpleth import Blockchain, Contract
            >>> b = Blockchain()
            >>> user = b.accounts[8]
            >>> c = Contract('Test')
            >>> c.connect()
            '0xD34dB707D084fdd1D99Cf9Af77896283a083c470'
            >>> receipt = c.run_trx(user,'storeNums',4,5,6)
            >>> trx_results = Results(receipt, c)
            >>> print(trx_results)
            Block number = 450
            Block time_epoch = 1640055579
            Contract address = 0x2f1E0A12de6741f26FCC34776764c87f46a1B7aA
            Contract name = Test
            Event args = {'num0': 4, 'num1': 5, 'num2': 6}
            Event log = [{'args': {'num0': 4, 'num1': 5, 'num2': 6}, ',   }  ]
            Event name = NumsStored
            Gas price wei = 20000000000
            Gas used = 83443
            Transaction = {'hash': '0xc5e3fd42eddefdcf79b511438b4b5ef58c18ad1b
            Trx args = {'_num0': 4, '_num1': 5, '_num2': 6}
            Trx hash = 0xc5e3fd42eddefdcf79b511438b4b5ef58c18ad1b761b09f9790900718155f21f
            Trx name = storeNums
            Trx receipt = {'transactionHash': HexBytes('0xc5e3fd42eddefdcf79b511
            Trx sender = 0xa894b8d26Cd25eCD3E154a860A86f7c75B12D993
            Trx value_wei = 0

        :Notes:
        - Neither :meth:`event_log`, :meth:`transaction`, nor :meth:`receipt`
          are printed. They can be quite lengthy. You can add a print of them
          with:

            print(f'Event log = {r.event_log}\n'}
            print(f'Transacton = {r.transaction}\n')
            print(f'Receipt = {r.receipt}\n')

        """
        string = (
            f'Block number     = {self.block_number}\n'
            f'Block time epoch = {self.block_time_epoch}\n'
            f'Contract name    = {self.contract_name}\n'
            f'Contract address = {self.contract_address}\n'
            f'Trx name         = {self.trx_name}\n'
            f'Trx args         = {self.trx_args}\n'
            f'Trx sender       = {self.trx_sender}\n'
            f'Trx value wei    = {self.trx_value_wei}\n'
            f'Trx hash         = {self.trx_hash}\n'
            f'Gas price wei    = {self.gas_price_wei}\n'
            f'Gas used         = {self.gas_used}\n'
            )
        for i in range(len(self._event_names)):
            string += f'Event name[{i}]    = {self.event_names[i]}\n'
            string += f'Event args[{i}]    = {self.event_args[i]}\n'
        return string
# end of Results


class SimplEthError(Exception):
    """Simple Ethereum Error exception class.

    It is used by :class:`Contract()`, :class:`Blockchain()`
    and :class:`Filter` to throw exceptions for
    errors resulting from interacting with Solidity contracts and the
    Ethereum blockchain.

    The `web3` API throws many types of exceptions and
    its methods are not consistent in which they throw. :class:`SimplEthError`
    catches almost all of these (when new ones are found, they are added)
    and reports the details. This means you only have to have a `try/except`
    with just `SimplEthError` instead of having half-dozen Python exceptions
    in the `except`.

    Besides, passing back the details from the original Python exception,
    :class:`SimplEthError` offers hints as to the cause of the problem.
    Some exceptions, esp. the ones caused by a problem with the Solidity
    contract, can be rather mysterious, esp. to someone just starting out
    with Ethereum. The hints may quickly point you to the cause.

    At the time of the early version of `simpleth` (circa 2020), the exceptions
    being thrown had very little explanation and could be difficult to
    locate the cause. More recent versions of `web3.py` are adding good
    descriptions of the problem in their exception ``Message`` parameter.
    If all `web3.py` exceptions add helpful messages, one of the big
    reasons for `SimplEthError` is fixed and time to consider doing away
    with it.

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

        :notes:

        -  ``code`` can serve several purposes. It could be
           easily tested in unit tests to make sure a test case is
           causing a specific error.  It makes it easy to search
           simpleth for the line of code that raised a specified
           SimplEthException.
        -  The format for ``code``:

               ``<c>-<method>-<id>``

           Where:

           -  ``<c>`` is the first character of the class: **B** lockchain,
              **C** ontract, or **F** ilter.
           -  ``<method>`` is a 3-digit sequence number for the method
              in the class.
           -  ``<id>`` is a 3-digit sequence number for the exception
              in the class.

        :TBD: make exc_info, message, and code private, so they do not
            appear in doc.

        """
        self.code: str = ''
        """Exception instance variable with ``code``"""
        self.exc_info: T_EXC_INFO = sys.exc_info()
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
