Installing
==========

1) Install pre-requisites
*************************

#.  Ganache must be installed and running. See: http://trufflesuite.com/ganache/
#.  ``web3.py`` and ``hexbytes`` must be added to your Python environment.
    You can install with:

.. code-block:: shell-session

   $ pip install web3
   $ pip install hexbytes


2) Install simpleth package
***************************

.. code-block:: shell-session

   $ pip install simpleth


3) Create project directory structure
*************************************
This is not a required structure. You can use it to start and modify
as needed. It is easy to change in the future.

Project directories::

    <path to project>
    |
    +-----simpleth
            |
            +----- artifacts
            |
            +----- contracts
            |
            +----- solc

Where:

- ``simpleth`` is the project home directory
- ``artifacts`` holds Solidity smart contract compiler output files
- ``contracts`` holds Solidity smart contract source code files
- ``solc`` holds the Solidity compiler, ``solc.exe`` .

These commands will create the directories:

.. code-block:: shell-session
   :caption: Creating simpleth directory structure

   $ cd <path to project>
   $ mkdir simpleth
   $ cd simpleth
   $ mkdir artifacts
   $ mkdir contracts
   $ mkdir solc


3) Download Solidity compiler
*****************************
Download ``solc-windows.exe`` from
`Github page for ethereum//solidity <https://github.com/ethereum/solidity/releases>`_
and save it as ``<path to project>/simpleth/solc/solc.exe``.

It is safest to use the version found in
:ref:`tested levels <sw_levels_label>` .

If you prefer to use a different version, download
it and save it as ``solc.exe`` in the `solc` directory.


4) Download contracts
*********************
Download the five smart contract Solidity source code files to the ``contracts``
directory.

The files are:

- HelloWorld1.sol
- HelloWorld2.sol
- HelloWorld3.sol
- HelloWorld4.sol
- Test.sol


5) Download artifacts
*********************
Download the ten compiler output files to the ``artifacts`` directory.

There are two for each of the five contracts. One is suffixed with, `.abi`,
and the other with, `.bin`.


6) Set environment variable
***************************
Set ``SIMPLETH_ARTIFACT_DIR`` to ``<path to project>/simpleth/artifacts``


7) Confirm installation
***********************
These commands should run as shown and without error messages.

.. code-block:: shell-session
   :caption: Confirming simpleth installation


    $ dir %SIMPLETH_ARTIFACT_DIR%
    ... *see the 10 compiler output files* ...

    $ dir %SIMPLETH_SOLC_DIR%\\solc.exe
    ... *see solc.exe* ...

    $ python

    >>> import simpleth
    >>> exit()

    $ compile.py
    usage: compile.py [-h] [-c COMPILER] [-O OPTIONS] [-o OUT_DIR] contract [contract ...]
    compile.py: error: the following arguments are required: contract

**Congratulations!** ``simpleth`` is ready for use.