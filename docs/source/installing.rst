Installing
==========

1) Pre-requisites
*****************

#.  Ganache must be installed and running. See: http://trufflesuite.com/ganache/
#.  ``web3.py`` and ``hexbytes`` must be added to your Python environment.
    You can install with:

.. code-block:: shell-session

   $ pip install web3
   $ pip install hexbytes

2) Installation
***************
The package has not yet been installed on PyPi.
It **cannot** be installed using `pip`.

For now, the suggested method is to download ``sipmleth.py`` , found in
``src/simpleth``, and put the file,
``simpleth.py``, under your ``<project dir>`` in same directory as your
Python source files.

3) Download Solidity compiler
*****************************
Download from
https://github.com/ethereum/solidity/releases
and save it as ``<project dir>/solc/solc.exe``.
It is safest to use the version found in
:ref:`tested levels <sw_levels_label>` . If you
have a different version you wish to use, download
it and save it as ``solc.exe`` in the `solc`
directory.



4) Customizing
**************

simpleth.py
"""""""""""
`simpleth` needs to know your project's home directory.
Edit ``simpleth.py`` and change the line:

.. code-block:: python

   PROJECT_HOME: str = 'C:/Users/snewe/OneDrive/Desktop/simpleth'

Put in your full path to the directory where you installed ``simpleth.py``.

App association
"""""""""""""""
Using Windows Settings -> Apps -> Default apps, associate ``.py`` to ``Python``.
This will allow you to enter the name of a command, like ``compile.py``
on a terminal command line.
(TODO - hmmm, what about my virtual environment? Can I use that version of
Python?)


5) Usage
********
To use `simpleth` from your interpreter, script, or app, include the
following line.

.. code-block:: python

   from simpleth import Blockchain, Contract, EventSearch

*Note:* You may not need all three classes. Import just the classes you
need.