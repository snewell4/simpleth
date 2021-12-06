Introduction
============
``simpleth`` (*Simple Ethereum*) simplifies
the use of Solidity smart contracts on an Ethereum blockchain.

`simpleth` is a set of five Python facade classes that use the ``web3.py`` API
to interact with the smart contracts through a Ganache Ethereum client.

`simpleth` only supports a portion of the `web3.py` functionality - the
portion that a Python developer uses to interact with contracts.

The aim is to provide Python developers a quick and easy way to:

-  **deploy** contracts onto the blockchain
-  **run transactions** in those contracts
-  **call functions** in those contracts
-  **get values** for public state variables in those contracts
-  **use filters** to find events emitted by those contracts
-  **get data** about the blockchain, contracts, transactions, and events

The intended audience:

-  Python developers who want to:

   -  learn to code smart contracts in Solidity
   -  play around with Ethereum and smart contracts using the interpreter
      and scripts
   -  build proof-of-concept dapps with scripts or `flask`
   -  build production dapps in a single-user test environment
   -  see a working example of the `web3.py` API by looking at `simpleth`
      internals

-  Solidity developers looking for examples of:

   -  basic functions in a smart contract, esp. if just starting out
   -  more advanced functions in a smart contract, esp. for use in
      medium-complexity dapps.

Motivation
**********
As someone who prefers Python to JavaScript and new to Solidity,
I found it daunting to learn the ``web3.py`` API, found few thorough
examples of using Python for interacting with smart contracts, and found
few wide-ranging sets of example Solidity contracts. This combination
made my learning curve steep and long.

This package is intended to make it easier to get started
with Ganache, Solidity, and Python to build simple- to medium-complexity
blockchain apps for learning or prototyping.

The first version of `simpleth` was created as part of an academic
research project to design a supply chain for non-profit organizations
A single-user `Flask` app was created for a medium-complexity proof
of concept that used `simpleth`.

Limitations
***********

-  Windows (have not tried it on iOS or Linux)
-  Python 3
-  Ganache blockchain
-  Solidity contracts

Framework/Tools used
********************

-  PyCharm
-  pylint
-  mypy
-  <testing>

Installation / Getting Started
******************************

See starting.rst

Documentation
*************

Link to Read The Docs
Shows example snippets for all methods

