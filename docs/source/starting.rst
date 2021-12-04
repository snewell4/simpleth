Getting Started
===============

Pre-reqs
********

#.  Ganache must be installed and running. See: http://trufflesuite.com/ganache/
#.  ``web3.py`` must be added to your Python environment. You can install with:

.. code-block:: python

   pip install web3

Installation
************
The package has not yet been installed on PyPi.
It **cannot** be installed using *pip*.

For now, the suggested method is to put the file, ``simpleth.py``, in
same directory as your source files.

Usage
*****
To use `simpleth` from your interpreter, script, or app, include the
following line.

.. code-block:: python

   from simpleth import Blockchain, Contract, Filter

*Note:* You may not need all three classes. Import just the classes you
need.