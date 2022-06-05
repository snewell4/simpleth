Installing
==========

1) Install Ganache
******************
Ganache is the Ethereum blockchain simulator that runs on your
local system. It must be running whenever you use ``simpleth``.

To install, go to https://trufflesuite.com/ganache/ and click on
the ``Download (Windows)`` button.

Follow the **Ganache Quickstart**
(https://trufflesuite.com/docs/ganache/quickstart/)
to install and create your blockchain.


2) Install simpleth package
***************************

.. code-block:: shell-session

   $ pip install simpleth


3) Set environment variable
***************************
Set ``SIMPLETH_ARTIFACT_DIR`` to ``<path to project>/simpleth/artifacts``


4) Download Solidity compiler
*****************************
You can run the `Hello World` contracts and do all the examples in the
`Using` document without installing the Solidity compiler.
If that is the extent of your planned use of ``simpleth``, you can
skip this step.

Otherwise, you will need to have a copy of the Solidity compiler
to compile your contracts before using ``simpleth`` to deploy and
use them.
Download ``solc-windows.exe`` from
`Github page for ethereum//solidity <https://github.com/ethereum/solidity/releases>`_.
At the start, you might make a subdirectory, `solc`, and save it in that
directory with the name, ``solc.exe``.

It is safest to use the version found in
:ref:`tested levels <sw_levels_label>` .

If you prefer to use a different version, download
it and save it as ``solc.exe`` in the `solc` directory.


5) Confirm installation
***********************
Make sure `ganache` is running and try these commands.
If your install is complete, they should run as shown and
without error messages.

.. code-block:: shell-session
   :caption: Confirming simpleth installation

    $ dir contracts
    ... see five smart contract files ...

    $ dir %SIMPLETH_ARTIFACT_DIR%
    ... see ten compiler output files ...

    $ python

    >>> from simpleth import Blockchain
    >>> Blockchain().block_number
        ... see sequence number of block at end of chain ...
    >>> exit()

    $ solc\solc --version
    ... see the compiler version number ...

.. note::

    The **contract files**:

        - HelloWorld1.sol
        - HelloWorld2.sol
        - HelloWorld3.sol
        - HelloWorld4.sol
        - Test.sol

    There are two **compiler output files** for each of the five contracts.
    One is suffixed with, `.abi`, and the other with, `.bin`.

**Congratulations!** ``simpleth`` is ready for use.