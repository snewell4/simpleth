#! python3
"""Unit test of EthConvert() class"""

from simpleth import Blockchain
from simpethconvert import EthConvert
import simpprint as p

b = Blockchain()
c = EthConvert()

amount_eth = 50
amount_wei = c.to_wei(amount_eth, 'ether')
print(f'{amount_eth} ether converts to {amount_wei} wei')
print()

amount_eth = c.from_wei(amount_wei, 'ether')
print(f'{amount_wei} wei converts to {amount_eth} ether')
print()

denominations = c.get_denominations()
p.print_dict(denominations, indent=4)
print()
