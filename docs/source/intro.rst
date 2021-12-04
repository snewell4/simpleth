Introduction
============
``simpleth`` (*Simple Ethereum*) is a set of three Python classes to simplify
the use of Solidity smart contracts on a Ganache blockchain.

The aim is to provide Python developers a quick and easy way to:

- **deploy** contracts onto the blockchain
- **run transactions** in those contracts
- **call functions** in those contracts
- **get values** for public state variables in those contracts
- **use filters** to find events emitted by those contracts
- **get data** about the blockchain, contracts, transactions, and events

`simpleth` is built using ``web3.py``. `simpleth` only supports a portion
of `web3.py` functionality - the portion that a Python developer would
use to interact with contracts.

Motivation
**********
As someone who prefers Python to JavaScript and a newbie to Solidity,
I found it daunting to learn the ``web3.py`` API and found few thorough
examples of using Python for interacting with smart contracts. That
learning curve, for me, was steep and long.

This package is intended to (hopefully) make it easier to get started
with Ganache, Solidity, and Python to build simple- to medium-complexity
blockchain apps for learning or prototyping.

The first version of `simpleth` was created as part of a research project
to design a supply chain for non-profit organizations. A single-user
`Flask` app was created for a medium-complexity proof of concept that
used `simpleth`.

Limitations
***********
- Windows
- Python 3
- Ganache blockchain
- Solidity contracts
