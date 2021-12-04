#!
"""Unit test of EthConvert() class"""

from simpleth import Blockchain
import s_ethconv as e
import s_print as p

b = Blockchain()

amount_eth = 50
amount_wei = e.convert(amount_eth, 'ether', 'wei')
print(f'{amount_eth} ether converts to {amount_wei} wei')
print()

amount_gwei = -0.21
amount_eth = e.convert(amount_gwei, 'gwei', 'ether')
print(f'{amount_gwei} gwei converts to {amount_eth} ether')
print()

denominations = e.denominations()
p.print_dict(denominations, indent=4)
print()
