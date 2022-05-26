Introduction
============
``simpleth`` (**Simple Ethereum**) simplifies
the use of Python to interact with an Ethereum blockchain and its Solidity
smart contracts.

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

-  **Python developers** who want to:

   -  learn to code smart contracts in Solidity
   -  play around with Ethereum and smart contracts using the Python interpreter
      and scripts
   -  build proof-of-concept dapps with Python scripts or `flask`
   -  build production dapps using Python in a single-user test environment
   -  see a working example of the `web3.py` API by looking at `simpleth`
      internals

-  **Solidity developers** looking for examples of:

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

An earlier version of `simpleth` was created as part of an academic
research project to design a supply chain for non-profit organizations
A single-user `Flask` app was created for a medium-complexity proof
of concept that used `simpleth`.


Limitations
***********
``simpleth`` is restricted to the following environment:

-  Windows 10 or 11 (have not tried it on iOS or Linux)
-  Python 3
-  Ganache blockchain
-  Solidity contracts
-  Learning / Prototyping / Proof of Concept

.. danger::
   Do not use ``simpleth`` in a production environment, especially one with
   cryptocurrency or other assets of value.

   No security audits have been done on ``simpleth``.

   No production dapps have used ``simpleth``.


.. _sw_levels_label:

Latest software pre-req levels tested
*************************************
Earlier versions have been used successfully. Here are the current
tested versions:

- Windows 11
- Python 3.10.4
- Ganache 2.5.4
- Solidity compiler 0.8.14
- web3 5.29.1


Framework/Tools used
********************

-  PyCharm - IDE
-  pytest - unit and integration testing
-  doctest - test simpleth docstring code examples
-  pylint - linter for code analysis
-  mypy - static type checking
-  git - version control

simpleth Documentation
**********************

+--------------+-------------------------------------------+
| Type         | Title (Hot-linked)                        |
+==============+===========================================+
| Installation | :doc:`Installing <installing>`            |
+--------------+-------------------------------------------+
| Tutorial     | :doc:`Hello World <starting>`             |
+--------------+-------------------------------------------+
| User Guide   | :doc:`Using <using>`                      |
+--------------+-------------------------------------------+
| Reference    | :doc:`Simpleth Reference <simpleth>`      |
+--------------+-------------------------------------------+

Other Documentation
*******************

.. glossary::

   :doc:`Smart Contract Reference <contracts>`
       Formatted ``Natspec`` comments in the contracts create a reference
       document for all contracts used for examples and testing.

   :doc:`Utilities for simpleth users <utils>`
       Python programs that simpleth users may find
       useful. Both are documented with formatted ``docstrings`` from
       the code.

   :doc:`Tools for simpleth developers <tools>`
       Windows batch scripts and Python programs that can be used by
       developers modifying the ``simpleth`` classes. The Python
       program documentation is formatted ``docstrings``

   :doc:`reST Style Guide <style>`
       Examples of ``reStructuredText`` formatting to be used in all
       ``simpleth`` documentation. Uses ``style.rst`` as input.
