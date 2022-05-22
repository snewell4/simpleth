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
  :caption: Deploy the Test contract

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
``public`` functions. :meth:`run_trx` is the typical and easiest
way to use transactions with `Ganache`.

You can compare this approach to the upcoming examples on
``Submit transactions`` and ``Get transaction receipts``.

Unlike a function, a transaction does not return any value.
If you want to confirm a transaction, you might check for
expected change(s) in contract state variable(s) or for
the emission of expected event(s).

Let's run a few transactions and check the updated
variable values:

.. code-block:: python
  :linenos:

  >>> receipt = c.run_trx(user, 'storeNum', 0, 1000)
  >>> c.get_var('nums', 0)
  1000
  >>> receipt = c.run_trx(user, 'storeNums', 12, 34, 56)
  >>> c.get_var('nums', 0)
  12
  >>> receipt = c.run_trx(owner, 'storeTypes', False, 2, 500, -500, c.address, 'new test string', [2, 4, 6])
  >>> c.get_var('testStr')
  'new test string'

.. note::

   - Line 1: The contract  transaction, ``storeNum`` , sets
     nums[0] to 1000. After the transaction completes, line 2
     gets the new value for nums[0], which is shown on line 3.
   - Line 4: Set the three values in nums[] to 12, 34, 56.
   - Line 7: Runs a transaction, ``storeTypes`` , that shows
     how to pass in seven different data types as args. Line
     9 confirms that the string arg was set properly.

   The Solidity transaction does not return any value, but
   ``call_fcn`` will return the `transaction receipt` which
   is created when the transaction is mined. You will be able
   to use this in the upcoming section about Results to see
   transaction information.

   A transaction always has a `sender`. This is the address
   of the account running the transaction. For the transactions
   shown the sender does not matter. Two of them were sent by
   `user`` and one ``owner``.  We'll be looking at checks in
   a transaction that can restrict which account(s) are permitted
   to run the transaction.

.. image:: ../images/section_separator.png


Search for events
*****************
:class:`simpleth.EventSearch` has two methods to find and retrieve
the information from events emitted by transactions:

#. :meth:`simpleth.EventSearch.get_old` returns event info
   from a specified range of previously mined blocks
#. :meth:`simpleth.EventSearch.get_new` returns event info
   from newly mined blocks.

.. code-block:: python
  :linenos:
  :caption: Get old events

  >>> from simpleth import EventSearch
  >>> nums_stored_search = EventSearch(c, 'NumsStored')
  >>> events = nums_stored_search.get_old()
  >>> len(events)
  1
  >>> events = nums_stored_search.get_old(-4)
  >>> len(events)
  4
  >>> last_block = b.block_number
  >>> events = nums_stored_search.get_old(last_block-3, last_block)
  >>> len(events)
  4
  >>> import pprint
  >>> pp = pprint.PrettyPrinter(indent=4)
  >>> pp.pprint(events)
  [   {   'args': {'num0': 10, 'num1': 10, 'num2': 10, 'timestamp': 1653095947},
          'block_number': 7084,
          'trx_hash': '0x38c917a6a5f27d88e4af57205f5a0ad231adcc5d519a2902feb7ab57885fe76a'},
      {   'args': {'num0': 20, 'num1': 20, 'num2': 20, 'timestamp': 1653095957},
          'block_number': 7085,
          'trx_hash': '0xc9846c27b90f5c0744e4049e8e3ea54477157d0741692db84ded3d1fae7b638a'},
      {   'args': {'num0': 30, 'num1': 30, 'num2': 30, 'timestamp': 1653095968},
          'block_number': 7086,
          'trx_hash': '0xed3ce6a50b8fb919c68c2555a8a525d3cf3b6e51ced660d28a7837961abfc385'},
      {   'args': {'num0': 40, 'num1': 40, 'num2': 40, 'timestamp': 1653095980},
          'block_number': 7087,
          'trx_hash': '0x9a02a390381f1053cc73b8f9589624b3b38a63c49722a15acc8fed5296e0011c'}]
  >>> events[1]['args']
  {'timestamp': 1653095957, 'num0': 20, 'num1': 20, 'num2': 20}
  >>> events[1]['args']['num0']
  20

.. note::
   - Line 2: Create the event search object we'll use to search for the event,
     ``NumsStored`` , which is emitted by the transaction, :meth:`storeNums` .
   - Line 3: Without an arg :meth:`get_old` looks in the last block on the
     chain for the event. Line 5 shows the block contains one such event.
   - Line 6: ``-4`` asks :meth:`get_old` to look in the last four blocks
     on the chain. Line 8 shows that four events were found.
   - Line 15: Print out the four events using Python's pretty print. You
     can see the information stored when the ``NumsStored`` event is emitted.
   - Line 28: Gets just the ``args`` values for the second event in the list.
   - Line 30: Narrows it down getting the value for the ``num0`` parameter.


:meth:`get_new` is used to check for an event in recently mined blocks.
It will look in the blocks created since the previous call for any new events.
The checking starts with creating the ``EventSearch`` . The first call to
``get_new`` returns any events emitted since object creating. The next call
returns any events emitted since the first call. Second call returns
events since the first call and so on.

.. code-block:: python
   :linenos:
   :caption: Get new events

   >>> nums_stored_search = EventSearch(c, 'NumsStored')
   >>> receipt = c.run_trx(user, 'storeNums', 50, 50, 50)
   >>> receipt = c.run_trx(user, 'storeNums', 60, 60, 60)
   >>> events = nums_stored_search.get_new()
   >>> len(events)
   2
   >>> events = nums_stored_search.get_new()
   >>> len(events)
   0
   >>> receipt = c.run_trx(user, 'storeNums', 70, 70, 70)
   >>> events = nums_stored_search.get_new()
   >>> len(events)
   1
   >>> pp.pprint(events)
   [   {   'args': {'num0': 70, 'num1': 70, 'num2': 70, 'timestamp': 1653097033},
           'block_number': 7090,
           'trx_hash': '0x5b60aafd384ec3cbfb86f28cc79911a8265899d0b38335cceb482f9cf9be9830'}]



.. note::

   - Line 1: Create the ``EventSearch`` object. This marks that stating point
     of checking for new ``NumsStored`` events.
   - Line 2: Run two transactions to emit two events.
   - Line 4: Check for new events. Two are found, as expected.
   - Line 7: Check for new events since that last check (on line 4). None
     found, as expected.
   - Line 10: Run one transaction, get it on line 11, and print it on line 14.

There is no way to be alerted to a new event without checking periodically.
There is no callback nor pub/sub available.
A simple approach is to have a program that does one check for the event,
waits for a period of time, and repeats those two steps. Here's an example:


.. code-block:: python
   :linenos:
   :caption: Python program (event_poll.py) to watch for events
   :emphasize-lines: 16

   """Simple program to periodically check for an event"""

   import time
   from simpleth import Contract, EventSearch

   poll_freq = 3    # number of seconds between checks
   num_polls = 10   # number of checks
   contract_name = 'TEST'    # contract emitting event
   event_name = 'NumsStore'  # check for this event

   c = Contract('Test')
   c.connect()
   e = EventSearch(c, 'NumsStored')

   while num_polls > 0:
       events = e.get_new()
       num_events = len(events)
       if num_events:
           print(f'Found {num_events} new events')
       else:
           print(f'No new events')
       num_polls = num_polls - 1
       time.sleep(poll_freq)

.. note::
   - Line 6: This program will check every three seconds
   - Line 7: Ten of these checks will be done before the program ends.
   - Line 16: **Highlighted**. Here is the periodic poll to check for
     any recent events.
   - Line 17: If zero events, tell the user nothing new found.
     If non-zero, tell user how many we found in this polling cycle.
   - Line 23: Sleep until time for the next check.

The next two sessions show a test of ``event_poll.py`` .
There are two windows in use:

#. Python interpreter where transactions were run
#. Command line window where ``event_poll.py`` runs.

I started ``event_poll.py`` and then switched to the Python interpreter
to run eight identical :meth:`storeNums` transactions at random
intervals.

The transactions:

.. code-block:: python
   :linenos:
   :caption: Interpreter session while event_poll.py runs

   >>> receipt = c.run_trx(user, 'storeNums', 500, 500, 500)
   >>> receipt = c.run_trx(user, 'storeNums', 500, 500, 500)
   >>> receipt = c.run_trx(user, 'storeNums', 500, 500, 500)
   >>> receipt = c.run_trx(user, 'storeNums', 500, 500, 500)
   >>> receipt = c.run_trx(user, 'storeNums', 500, 500, 500)
   >>> receipt = c.run_trx(user, 'storeNums', 500, 500, 500)
   >>> receipt = c.run_trx(user, 'storeNums', 500, 500, 500)
   >>> receipt = c.run_trx(user, 'storeNums', 500, 500, 500)


The program:

.. code-block:: shell-session
   :linenos:
   :caption: Running event_poll.py

   $ event_poll.py
   No new events
   No new events
   Found 2 new events
   No new events
   Found 3 new events
   Found 1 new events
   No new events
   No new events
   Found 2 new events
   No new events

.. note::
   - Line 2: No events emitted in the first 3 seconds.
   - Line 3: No events emitted in the next 3 seconds.
   - Line 4: Two events, from the transactions run in the Python interpreter,
     were emitted in the third 3 seconds.

   And so on.


After ``event_poll.py`` finished, use :meth:`get_old` to get the
eight events emitted. Print them.

.. code-block:: python
   :linenos:
   :caption: Getting the events emitted while event_poll.py ran

   >>> events = e.get_old(-8)
   >>> len(events)
   8
   >>> pp.pprint(events)
   [ { 'args': {'num0': 500, 'num1': 500, 'num2': 500, 'timestamp': 1653135341},
       'block_number': 7125,
       'trx_hash': '0xc258c1f566fbf9b76253afc2d89049fb7f7d7fe54f5c6b5a98a521f5bb0e9bc0'},
     { 'args': {'num0': 500, 'num1': 500, 'num2': 500, 'timestamp': 1653135341},
        'block_number': 7126,
       'trx_hash': '0x7f06283aa8c2326f558da4ea36d1d840fd198a92874ae587164b8950d9dd7259'},
     { 'args': {'num0': 500, 'num1': 500, 'num2': 500, 'timestamp': 1653135347},
       'block_number': 7127,
       'trx_hash': '0xcdf32bafe94c90f10ef93a4ed989a4f41f022ef62299076be549a713517a9667'},
     { 'args': {'num0': 500, 'num1': 500, 'num2': 500, 'timestamp': 1653135347},
       'block_number': 7128,
       'trx_hash': '0xa4c1fdaa89120cdf69ecc42300d6594098e90a443b5fdbda8bed91b355dcde8f'},
     { 'args': {'num0': 500, 'num1': 500, 'num2': 500, 'timestamp': 1653135348},
       'block_number': 7129,
       'trx_hash': '0x3763fbaf62eb8e422f33f41fc42607559a478152cbf10c437c5178381e8905ff'},
     { 'args': {'num0': 500, 'num1': 500, 'num2': 500, 'timestamp': 1653135349},
       'block_number': 7130,
       'trx_hash': '0xbfb52e30129dcf927a2ff07d426210302bea48e9f54c8c88a5a29b6b474bbfe0'},
     { 'args': {'num0': 500, 'num1': 500, 'num2': 500, 'timestamp': 1653135360},
       'block_number': 7131,
       'trx_hash': '0x18155d00b5305d15959536f107af1b533a877ee324989da475fb8e4744c888b3'},
     { 'args': {'num0': 500, 'num1': 500, 'num2': 500, 'timestamp': 1653135360},
       'block_number': 7132,
       'trx_hash': '0x14e74f83b9c544675cee2718212b31563914f81c5124d5df024b6b4bef8e7b7f'}]

.. note::
   - Line 1: Eight transactions were run in the Python interpreter.
     Get events in the most recent eight blocks. We do not need to
     create another ``EventSearch`` object. We use the same one used
     for ``get_new``.
   - Line 3: shows eight events emitted. This matches  the number
     that ``event_poll.py`` found.
   - Line 5: The events list has the eight events. You can see the
     (epoch) times, in seconds, when the transactions were mined in
     the ``timestamp`` args. The first two events have the same
     timestamp. This corresponds to ``event_poll.py`` finding two
     events in the third three-second check. The next three events
     were timestamped in a two-second period. They were found by
     ``event_poll.py`` in the fifth three-second check.

   And so on.


.. image:: ../images/section_separator.png


Transaction results
*******************
:class:`simpleth.Results` can be used after a transaction completes
to see the details about it.

.. code-block:: python
   :linenos:
   :caption: Get the results of a transaction

   >>> from simpleth import Results
   >>> receipt = c.run_trx(user, 'storeNums', 42, 42, 42)
   >>> r = Results(c, receipt)
   >>> r.block_number
   7238
   >>> r.gas_used
   38764
   >>> r.gas_price_wei
   20000000000
   >>> pp.pprint(r.transaction)
   { 'blockHash': '0x02d037b430ff01bec0395f63af90c9f497d31ff5f2270bd1410056f54d166db0',
     'blockNumber': 7238,
     'from': '0x20e0A619E7Efb741a34b8EDC6251E2702e69bBDd',
     'gas': 6000000,
     'gasPrice': 20000000000,
     'hash': '0xf73105578c2df584331431703b07fb4741fd1292d890febfc77ded9f4dfd0e91',
     'input': '0x3e50ca2c000000000000000000000000000000000000000000000000000000000000002a000000000000000000000000000000000000000000000000000000000000002a000000000000000000000000000000000000000000000000000000000000002a',
     'nonce': 209,
     'r': '0xdd4bd76385c7c3d5775db03951c03b3c529383288f036baca55a05f8c5088d54',
     's': '0x21c27b449376503812586b3ddf9edeb40a6e920b5f1f019d8f9f54243d2e29ad',
     'to': '0x82592d5ae9E9ECc14b1740F330D3fAA00403a1F3',
     'transactionIndex': 0,
     'v': 37,
     'value': 0}
   >>> print(r)
    Block number     = 7238
    Block time epoch = 1653156539
    Contract name    = Test
    Contract address = 0x82592d5ae9E9ECc14b1740F330D3fAA00403a1F3
    Trx name         = storeNums
    Trx args         = {'_num0': 42, '_num1': 42, '_num2': 42}
    Trx sender       = 0x20e0A619E7Efb741a34b8EDC6251E2702e69bBDd
    Trx value wei    = 0
    Trx hash         = 0xf73105578c2df584331431703b07fb4741fd1292d890febfc77ded9f4dfd0e91
    Gas price wei    = 20000000000
    Gas used         = 38764
    Event name[0]    = NumsStored
    Event args[0]    = {'timestamp': 1653156539, 'num0': 42, 'num1': 42, 'num2': 42}

.. note::

   - Line 3: Create a ``Results`` data object, ``r`` , for the ``storeNums``
     transaction.
   - Line 4: Get blockchain block number holding this mined transaction.
   - Line 6: Get the units of gas consumed to execute the transaction.
   - Line 8: Get the cost, in `wei` , for each unit of gas. This is a
     constant when using Ganache.
   - Line 10: Pretty print the ``web3.eth`` transaction information.
   - Line 25: A ``Results`` object can be printed. Here's the output.

   See :class:`simpleth.Results` documentation for the full list of
   properties, including more from ``web3.eth`` .


Handling Ether
**************
``simpleth`` has a handful of methods and properties for handling Ether:

#. :meth:`simpleth.Convert.denominations_to_wei` returns Ether
   denominations and values.
#. :meth:`simpleth.Convert.convert_ether` to convert amount from one
   denomination to another.
#. :meth:`simpleth.Blockchain.balance` returns the Ether balance,
   in `wei` , for a specified address.
#. :meth:`simpleth.Blockchain.send_ether` transfers the specified amount
   of Ether, in `wei` , from one address to another.
#. :meth:`simpleth.Contract.run_trx` has an optional parameter,
   ``value_wei`` which will send the specified amount of Ether,
   in `wei` , to the transaction.


.. code-block:: python
   :linenos:
   :caption: Methods and properties to handle ether

    >>> from simpleth import Convert
    >>> v = Convert()
    >>> pp.pprint(v.denominations_to_wei())
    { 'babbage': 1000,
      'ether': 1000000000000000000,
      'femtoether': 1000,
      'finney': 1000000000000000,
      'gether': 1000000000000000000000000000,
      'grand': 1000000000000000000000,
      'gwei': 1000000000,
      'kether': 1000000000000000000000,
      'kwei': 1000,
      'lovelace': 1000000,
      'mether': 1000000000000000000000000,
      'micro': 1000000000000,
      'microether': 1000000000000,
      'milli': 1000000000000000,
      'milliether': 1000000000000000,
      'mwei': 1000000,
      'nano': 1000000000,
      'nanoether': 1000000000,
      'picoether': 1000000,
      'shannon': 1000000000,
      'szabo': 1000000000000,
      'tether': 1000000000000000000000000000000,
      'wei': 1}
    >>> v.denominations_to_wei()['szabo']
    1000000000000

    >>> int(v.convert_ether(20, 'ether', 'gwei'))
    20000000000
    >>> float(v.convert_ether(100, 'wei', 'ether'))
    1e-16

    >>> b.balance(owner)
    57816514559996298520
    >>> float(v.convert_ether(b.balance(user), 'wei', 'ether'))
    99.52299804
    >>> b.balance(c.address)
    10

    >>> b.balance(user)
    99522998040000000000
    >>> trx_hash = b.send_ether(owner, user, 10)
    >>> b.balance(user)
    99522998040000000010

    >>> b.balance(c.address)
    10
    >>> receipt = c.run_trx(user, 'storeNumsAndPay', 10, 20, 30, value_wei=100)
    >>> Results(c, receipt).trx_value_wei
    100
    >>> b.balance(c.address)
    110
    >>> b.send_ether(user, c.address, 500)
    '0xcbbec5f820b25318d5654526d7390ba6d74231d194775304a7cddfc3b075a652'
    >>> b.balance(c.address)
    610

.. note::

   - Line 3: :meth:`denominations_to_wei` returns a dictionary of
     the names of all Ether denominations and the number of `wei`
     in each. The same list, with much better formatting, is shown
     in the `Example` for :meth:`simpleth.Convert.denominations_to_wei`
   - Line 27: You can specify a denomination to get the value in `wei`.
   - Line 30: :meth:`convert_ether` is the usual way to compute
     a conversion between denominations. This line shows the number
     of `gwei` in 20 `ether`. For best precision, the method returns
     a ``decimal`` type. This example casts to an integer.
   - Line 37: Get `user` balance in `ether`.
   - Line 39: ``Test`` contract has a balance of 10 `wei`.
   - Line 44: Move 10 `wei` from ``owner`` to ``user``.
   - Line 46: ``user`` balance increased by 10 `wei`. Line 43 is
     the *before* balance.
   - Line 50: Example of sending ether to a transaction. The ``Test``
     contract has the function, :meth:`storeNumsAndPay` that is
     identical to our trusty, :meth:`storeNums`, except it is
     defined as ``payable`` in the contract. This allows us to
     send Ether when we run the transaction. Here, we are sending
     10 `wei` .
   - Line 51: Get the :meth:`trx_value_wei` sent to the
     transaction. As expected, line 52 shows it is 100 `wei`.
   - Line 54: Confirms that 100 `wei` were sent. The balance is
     now 100 `wei` more than the *before* balance on line 49
   - Line 55: You can also send ether to a contract. Here, 500
     `wei` is sent to the ``Test`` contract. This is confirmed
     in line 58 where the balance increased by 500 from the
     *before* balance on line 54. **Important**: the contract must have
     a ``payable`` `fallback` function in order to receive ether.
     The ``Test`` contract has such a function as the final
     function in the contract.



Handling time
*************
``simpleth`` provides support for handing time, especially
epoch time:

#. :meth:`simpleth.Convert.epoch_time` returns the current time in epoch seconds.
#. :meth:`simpleth.Convert.local_time_string` returns the current time as a string.
#. :meth:`simpleth.Convert.to_local_time_string` converts epoch seconds to a
   time string.

.. code-block:: python
   :linenos:
   :caption: Handling time

    >>> v.local_time_string()
    '2022-05-21 18:03:41'
    >>> v.local_time_string('%A %I:%M:%S %p')
    'Saturday 06:04:19 PM'

    >>> now = v.epoch_time()
    >>> now
    1653175079.5026972
    >>> v.to_local_time_string(now)
    '2022-05-21 18:17:59'
    >>> v.to_local_time_string(now, '%A %I:%M:%S %p')
    'Saturday 06:17:59 PM'

    >>> receipt = c.run_trx(user, 'storeNums', 3, 5, 7)
    >>> r = Results(c, receipt)
    >>> r.block_time_epoch
    1653175121
    >>> r.event_args[0]['timestamp']
    1653175121
    >>> v.to_local_time_string(r.block_time_epoch)
    '2022-05-21 18:18:41'
    >>> v.to_local_time_string(r.event_args[0]['timestamp'])
    '2022-05-21 18:18:41'

.. note::

   - Line 1: Get the current time using the default time string format.
   - Line 2: Get the current time and specify the time string format
     codes.
   - Line 6: Get the current time in epoch seconds. It is shown on line 8.
   - Line 9: Convert that epoch time to the default time string.
   - Line 10: Convert it to the specified format.
   - Line 14: Run the usual transaction to show how time conversion might
     help. So far, we've always seen timestamps in epoch seconds.
     Converting to a time format string may make them more useful.
   - Line 17: Shows the transaction's block time in epoch seconds.
   - Line 21: Shows that block time in a time format string.
   - Line 19: Same for the ``NumsStored`` arg for the contract's
     ``block.timestamp``. Here's the epoch seconds used by Solidity
     and line 23 converts it to a time string.

   See the list of `Python Time String Format Codes \
   <https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes>`_
   for details on directives available for the strings.


simpleth exceptions
*******************
:class:`simpleth.SimplEthError` throws exceptions for errors in all
``simpleth`` classes. The intent is to let you code to catch this
single exception to simplify error-handling and provide hints to
quickly identify the cause of the error.

.. code-block:: python
   :linenos:
   :caption: Getting a SimplEthError in the Python interpreter

    >>> c = Contract('bogus')
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "C:\Users\snewe\OneDrive\Desktop\simpleth\src\simpleth\simpleth.py", line 943, in __init__
        self._abi: List = self._get_artifact_abi()
      File "C:\Users\snewe\OneDrive\Desktop\simpleth\src\simpleth\simpleth.py", line 2151, in _get_artifact_abi
        raise SimplEthError(message, code='C-100-010') from None
    simpleth.SimplEthError: [C-100-010] ERROR in bogus()._get_artifact_abi(). Unable to read ABI file.
    Full path: C:/Users/snewe/OneDrive/Desktop/simpleth/artifacts/bogus.abi
    Contract name of "bogus" is bad.
    HINT 1: Check the spelling of the contract name.
    HINT 2: You may need to do a new compile.

.. note::

   - Line 1: Cause an exception with a bad `contract` name. This is the
     typical type of message you will see when using the Python interpreter.
   - Line 8: This is the start of the ``SimplEthError`` message and hints
     on possible causes.

.. code-block:: shell-session
   :linenos:
   :caption: Handling a SimplEthError

    >>> try:
    ...     c = Contract('bogus')
    ... except SimplEthError as e:
    ...     print(e)
    ...
    [C-100-010] ERROR in bogus()._get_artifact_abi(). Unable to read ABI file.
    Full path: C:/Users/snewe/OneDrive/Desktop/simpleth/artifacts/bogus.abi
    Contract name of "bogus" is bad.
    HINT 1: Check the spelling of the contract name.
    HINT 2: You may need to do a new compile.

.. note::

   - Line 1: Use a ``try``/``except`` around the line to create the
     ``Contract`` object.
   - Line 4: Our only action with the exception is to print it.
     A program could take action to fix the problem at this point.


.. code-block:: shell-session
   :linenos:
   :caption: Properties of a SimplEthError

    >>> try:
    ...     c = Contract('bogus')
    ... except SimplEthError as e:
    ...     print(f'code = \n{e.code}')
    ...     print(f'message = \n{e.message}')
    ...     print(f'exc_info =')
    ...     pp.pprint({e.exc_info})
    ...
    code =
    C-100-010
    message =
    ERROR in bogus()._get_artifact_abi(). Unable to read ABI file.
    Full path: C:/Users/snewe/OneDrive/Desktop/simpleth/artifacts/bogus.abi
    Contract name of "bogus" is bad.
    HINT 1: Check the spelling of the contract name.
    HINT 2: You may need to do a new compile.

    exc_info =
    { ( <class 'FileNotFoundError'>,
        FileNotFoundError(2, 'No such file or directory'),
        <traceback object at 0x000001DE340EE240>)}

.. note::

   - Line 4: There are three properties you can access. First is the
     unique ``code`` string for the exception. It is accessed here and
     its value is printed on line 10.
   - Line 5: The text of the error message is accessed here and printed
     on lines 12 through 16.
   - Line 7: The exception information is accessed here and pretty
     printed on lines 19 through 21.

   You can access these properties instead of the entire message if
   that suits your purpose better in handling ``simpleth`` errors.


Checks
******
Guards
Assert
Revert



Send transactions
*****************



Get transaction receipts
************************


