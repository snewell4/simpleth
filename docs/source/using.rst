Using simpleth - Examples
=========================
`Getting Started - Hello World(s) <../html/starting.html>`_ is an
introduction to using very simple contracts with `simpleth`
as well as compiling a contract for `simpleth's` use.

This document goes further. It shows many of the basic
interactions with a contract.

These examples will use the ``Test.sol`` contract.
It was created for `simpleth` unit and integration testing.
It has no purpose except to provide a variety of
transactions and variables for testing.
We'll use it to show `simpleth` usage.


.. image:: ../images/section_separator.png

Test Contract Details
*********************

- `Natspec comments <../html/contracts.html#test>`_
- `Source file <../../../tests/src/contracts/Test.sol>`_ (or
  open the file, ``<project home>/tests/src/contracts/Test.sol`` , in
  your favorite editor.)


.. image:: ../images/section_separator.png

Compile
*******
After any modification to a contract, including Natspec comments, you
need to compile the contract before you can deploy it. Let's compile
the Test contract.

.. code-block:: shell-session
  :linenos:
  :caption: Compile the Test contract

  (env) C:\Users\snewe\OneDrive\Desktop\simpleth\tests\src\contracts>compile.py Test.sol
  Compiler run successful. Artifact(s) can be found in directory "C:/Users/snewe/OneDrive/Desktop/simpleth/artifacts".

.. note::
   You can read about ``compile.py`` in the `Utilities document <../html/utils.html#module-compile>`_

.. image:: ../images/section_separator.png


Deploy
******
:meth:`simpleth.Contract.deploy` will add a contract to the blockchain.
After a contract is deployed, it is ready for use.

.. code-block:: python
  :linenos:

  >>> from simpleth import Blockchain, Contract
  >>> b = Blockchain()
  >>> owner = b.address(0)
  >>> c = Contract('Test')
  >>> special_num = 42
  >>> receipt = c.deploy(owner, special_num)
  >>> c.address
  '0x6074DEA05C4B02A8afc21c1E06b22a7212217CFd'

.. note::
   - Line 2: ``b`` is our :class:`simpleth.Blockchain` object for the examples.
   - Line 3: Assign the blockchain account
     :meth:`simpleth.Blockchain.address` for the first `Ganache` account
     to ``owner`` .
   - Line 4: ``c`` is our :class:`simpleth.Contract` object for the ``Test`` contract
     to be used in all examples.
   - Line 6: ``deploy`` adds the ``Test`` contract to the blockchain.
     ``Test`` has a constructor parameter that we need
     provide with the arg, ``special_num``. This becomes the contract's value
     for the state variable, ``initNum``.

     The contract's constructor function sets the account address that
     sent the transaction as the ``owner`` of the contract. Since the
     Python ``owner`` was used to ``deploy``, it becomes the Solidity
     ``owner``. This becomes important later. There are examples where
     only the Solidity contract ``owner`` can run a transaction.

     ``deploy`` returns the   `transaction receipt`. To avoid having
     this print out, I stored it in ``receipt``. We don't need to do
     anything with it for now.

   - Line 7: Gets the blockchain address where this contract now resides.
     It is the value of the :meth:`simpleth.Contract.address` property.
     The address is shown on line 8.

.. image:: ../images/section_separator.png


Setup session
*************
These Python statements are common to all the following
examples. They are shown here and assumed to have been
issued for the rest of the examples.

There is duplication of these statements and the `Deploy`
example. In most cases, a contract is already deployed
and you would start your Python session with the following
statements.

.. code-block:: python
  :linenos:

  >>> from simpleth import Blockchain, Contract, Results, EventSearch, Convert
  >>> b = Blockchain()
  >>> owner = b.address(0)
  >>> user = b.address(1)
  >>> c = Contract('Test')
  >>> c.connect()


.. important::
   Line 6: You must do a :meth:`simpleth.Contract.connect`
   before doing anything with a contract. A ``deploy`` includes a
   ``connect``; no need to do a connect after a deploy.

.. note::
   See the ``Deploy`` example above for comments relevant to lines
   2, 3, and 5.

   - Line 4: Likewise, assign another account address to ``user``. This
     will give us two accounts for our examples.


.. image:: ../images/section_separator.png


Get variables
*************
:meth:`simpleth.Contract.get_var` will retrieve the
specified ``public state`` variable.


.. code-block:: python
  :linenos:

  >>> c.get_var('initNum')
  42
  >>> c.get_var('owner')
  '0xa894b8d26Cd25eCD3E154a860A86f7c75B12D993'
  >>> c.get_var('nums', 1)
  1
  >>> c.get_var('nums', 2)
  2

.. note::
   - Line 1 - Get the variable that was set by the ``deploy``
     constructor arg.
   - Line 3 - The address of the ``owner`` account.
   - Line 5 - ``nums`` is an array of three unsigned ints.
     ``get_var`` can not return a list, only a single value.
     Ask for the value of the second element by providing
     an arg with the index of 1. (Note: the contract
     defines the initial value of ``nums`` as
     [0,1,2]. There are transactions to change and use
     those values. We'll get to those soon.)
   - Line 6 - get the third element of ``nums`` .

.. image:: ../images/section_separator.png


Call functions
**************
:meth:`simpleth.Contract.call_fcn` will execute a contract's
``public pure`` or ``public view`` functions and pass
back the returned value(s).

.. code-block:: python
  :linenos:

  >>> c.call_fcn('getNum0')
  0
  >>> c.call_fcn('getNum',2)
  2
  >>> c.call_fcn('getNums')
  [0, 1, 2]
  >>> c.call_fcn('getTypes')
  [True, 1, 10, -100, '0x20e0A619E7Efb741a34b8EDC6251E2702e69bBDd', 'test string', [10, 20, 30]]

.. note::

   - Line 1: ``getNum0`` returns one value: the int stored in nums[0].
   - Line 3: ``getNum`` returns one value: the int stored in
     nums[<index>].
     In this instance, we will get nums[2].
   - Line 5: ``getNums`` returns the full nums array as a Python list.
   - Line 7: ``getTypes`` returns seven values. (Note: I did a
     transaction to set these values that is not shown. We'll see it soon.)

.. image:: ../images/section_separator.png


Run transactions
****************
:meth:`simpleth.Contract.run_trx` will execute a contract's
``public`` functions. There is no value passed back.

You can compare this approach to the upcoming examples on
``Submit transactions`` and ``Get transaction receipts``.

:meth:`run_trx` is the typical and easiest way to use transactions
with `Ganache`.

.. code-block:: python
  :linenos:


Search for events
*****************




Transaction results
*******************




Handling Ether
**************
Convert.convert ether
Contract.balance
Contract.send_ether
Contract.run_trx - transactions with ether



Handling epoch time
*******************
Convert.to_local_time_string
Example of Results.block_time_epoch
Mention Blockchain.block_time_epoch and block_time_string

simpleth exceptions
*******************




Send transactions
*****************



Get transaction receipts
************************


