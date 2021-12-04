"""Contains defaults and constants used by simpleth"""

from typing import Union, Any

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
# Authorship information
#
__author__ = 'Stephen Newell'
__copyright__ = 'Copyright 2021, Stephen Newell'
__license__ = 'MIT'
__version__ = '0.17'
__maintainer__ = 'Stephen Newell'
__email__ = 'snewell4@gmail.com'
__status__ = 'Prototype'
