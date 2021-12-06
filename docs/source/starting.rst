Getting Started
===============

Pre-requisites
**************

#.  Ganache must be installed and running. See: http://trufflesuite.com/ganache/
#.  ``web3.py`` and ``hexbytes`` must be added to your Python environment.
    You can install with:

.. code-block:: python

   pip install web3
   pip install hexbytes

Installation
************
The package has not yet been installed on PyPi.
It **cannot** be installed using *pip*.

For now, the suggested method is to put the file, ``simpleth.py``, in
same directory as your source files.

Customizing
***********
`simpleth` needs to know your project's home directory.
Edit ``simpleth.py`` and change the line:

.. code-block:: python

   PROJECT_HOME: str = 'C:/Users/snewe/OneDrive/Desktop/simpleth'

Put in your full path to the directory where you installed ``simpleth.py``.

Usage
*****
To use `simpleth` from your interpreter, script, or app, include the
following line.

.. code-block:: python

   from simpleth import Blockchain, Contract, Filter

*Note:* You may not need all three classes. Import just the classes you
need.