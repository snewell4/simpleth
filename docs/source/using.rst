Using
=====
`Hello World <../html/starting.html>`_ is an
introduction to using very simple contracts with `simpleth`.

This document goes further. It shows many of the basic
interactions with a contract as well as compiling a
contract.

.. image:: ../images/section_separator.png


Test Contract
*************
The examples will use the ``Test.sol`` contract.
It was created for ``simpleth`` unit and integration testing.
It has no purpose except to provide a variety of
transactions and variables for testing.
We'll use it to show ``simpleth`` usage.

.. note::
    If you'd like to look at the contract while going through the examples:

    - The Natspec comments in the source file provide reference documentation
      for the contract in, :doc:`Smart Contract Reference <contracts>`.
    - A copy of the source code is in the document,
      :doc:`Test Contract <TestContract>`.
    - The source file will be found in
      ``<Python sys.prefix dir>/contracts/Test.sol``


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


Setup interpreter session
*************************
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

   Line 4: Likewise, assign another account address to ``user``. This
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
   - Line 7 - get the third element of ``nums`` .

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

Unlike a function, a transaction does not return any value.
If you want to confirm a transaction, you might check for
expected changes in contract state variables or for
the emission of expected events.

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
   ``user`` and one ``owner``.  We'll be looking at checks in
   a transaction that can restrict which account(s) are permitted
   to run the transaction.

   You can compare this approach to the upcoming examples of
   ``Submit transactions`` and ``Get transaction receipts``.

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
The checking starts with creating an ``EventSearch`` object . The first call
to ``get_new`` returns any events emitted since the object was created. The
next call returns any events emitted since the first call. The second call
returns events since the first call and so on.

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
A simple approach is to have a program that checks for the event,
sleeps for a period of time, and repeats. Here's an example:


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

   The program is found in ``<Python sys.prefix>/examples`` directory.

The next two sessions show a single test of ``event_poll.py`` .
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


Search for events with event arguments
**************************************
:class:`simpleth.EventSearch` has an optional parameter to specify
``event_args``. This allows you to narrow the search to events with
a desired value for an event parameter.

You setup and call either :meth:`simpleth.EventSearch.get_old` or
:meth:`simpleth.EventSearch.get_new` as above. But, they will only
return events where the the event argument and its value match
the ``event_args`` you specified in :class:`simpleth.EventSearch`.

You can specify multiple args and values in the ``event_args`` dictionary.
These will be ANDed together. Your search will return only events that
meet all the criteria. You should specify the name of an event argument
only once. If the dictionary repeats a key, only the last one is used.

.. code-block:: python
  :linenos:
  :caption: Get old and new events with event args

    >>> import pprint
    >>> pp = pprint.PrettyPrinter(indent=4)
    >>> from simpleth import EventSearch, Contract
    >>> c = Contract('Test')
    >>> c.connect()
    >>> all_nums_stored = EventSearch(c, 'NumsStored')
    >>> pp.pprint(all_nums_stored.get_old(-5))
    [   {   'args': {'num0': 10, 'num1': 10, 'num2': 10, 'timestamp': 1659807711},
            'block_number': 6940,
            'trx_hash': '0xac4da74d96c3854b276c138e9b1984638f1d78d0c0e739973bd669e6cde0de47'},
        {   'args': {'num0': 10, 'num1': 10, 'num2': 20, 'timestamp': 1659807729},
            'block_number': 6941,
            'trx_hash': '0xba5c070b1e39de9520c3f75bef2a3e85d9070d967d5235c427d4c3104125bf5a'},
        {   'args': {'num0': 10, 'num1': 20, 'num2': 20, 'timestamp': 1659807737},
            'block_number': 6942,
            'trx_hash': '0x5158aeb329c780da6bc508ae43cad8cf83a114dd07cd44b101a48b0dcaf246af'},
        {   'args': {'num0': 20, 'num1': 20, 'num2': 20, 'timestamp': 1659807752},
            'block_number': 6943,
            'trx_hash': '0x5d573d5d636b8ebad2d1d9d0e767ff51547e050220b4e53cef54bb5220707b51'}]
    >>> num0_is_10 = EventSearch(c, 'NumsStored', {'num0': 10})
    >>> pp.pprint(num0_is_10.get_old(-5))
    [   {   'args': {'num0': 10, 'num1': 10, 'num2': 10, 'timestamp': 1659807711},
            'block_number': 6940,
            'trx_hash': '0xac4da74d96c3854b276c138e9b1984638f1d78d0c0e739973bd669e6cde0de47'},
        {   'args': {'num0': 10, 'num1': 10, 'num2': 20, 'timestamp': 1659807729},
            'block_number': 6941,
            'trx_hash': '0xba5c070b1e39de9520c3f75bef2a3e85d9070d967d5235c427d4c3104125bf5a'},
        {   'args': {'num0': 10, 'num1': 20, 'num2': 20, 'timestamp': 1659807737},
            'block_number': 6942,
            'trx_hash': '0x5158aeb329c780da6bc508ae43cad8cf83a114dd07cd44b101a48b0dcaf246af'}]
    >>> pp.pprint(num0_is_10.get_old(from_block=6942))
    [   {   'args': {'num0': 10, 'num1': 20, 'num2': 20, 'timestamp': 1659807737},
            'block_number': 6942,
            'trx_hash': '0x5158aeb329c780da6bc508ae43cad8cf83a114dd07cd44b101a48b0dcaf246af'}]
    >>> num0_is_10_and_num1_is_10 = EventSearch(c, 'NumsStored', {'num0': 10, 'num1':10})
    >>> pp.pprint(num0_is_10_and_num1_is_10.get_old(-5))
    [   {   'args': {'num0': 10, 'num1': 10, 'num2': 10, 'timestamp': 1659807711},
            'block_number': 6940,
            'trx_hash': '0xac4da74d96c3854b276c138e9b1984638f1d78d0c0e739973bd669e6cde0de47'},
        {   'args': {'num0': 10, 'num1': 10, 'num2': 20, 'timestamp': 1659807729},
            'block_number': 6941,
            'trx_hash': '0xba5c070b1e39de9520c3f75bef2a3e85d9070d967d5235c427d4c3104125bf5a'}]
    >>> all_nums_are_20 = EventSearch(c, 'NumsStored', {'num0': 10, 'num1':10, 'num2':10})
    >>> pp.pprint(all_nums_are_20.get_old(-5))
    [   {   'args': {'num0': 10, 'num1': 10, 'num2': 10, 'timestamp': 1659807711},
            'block_number': 6940,
            'trx_hash': '0xac4da74d96c3854b276c138e9b1984638f1d78d0c0e739973bd669e6cde0de47'}]
    >>>
    >>> num0_is_10.get_new()
    []
    >>> r = c.run_trx(u, 'storeNums', 10, 100, 1000)
    >>> pp.pprint(num0_is_10.get_new())
    [   {   'args': {   'num0': 10,
                        'num1': 100,
                        'num2': 1000,
                        'timestamp': 1659808773},
            'block_number': 6944,
            'trx_hash': '0x00965e2e84c9b6940ac3129bc1f2a97a720b7b56085e029ad1828a7afc1cb0d3'}]

.. note::
   - Line 6: Create an event search to find all `NumsStored`.
   - Line 7: Get all 'NumsStored' events in last five mined blocks and pretty
     print them
   - Line 20: Create a second event search to find events where 'num0' was
     set to 10.
   - Line 21: Finds three of those in the last five blocks.
   - Line 31: Shows how to check if block number 6942 has a transaction
     that emitted 'NumsStored' with num0 equal to 10. One is found.
   - Line 35: Shows how to specify multiple arguments/values. Here we want
     to find StoredNum events have both num1 and num2 equal to 10.
     There are two in the last five blocks mined.
   - Line 43: Go a step further and look for events where all three numbers
     were set to 10. There is one found.
   - Line 49: Switch to showing how ``get_new()`` operates. We can look
     for any newly mined transactions where num0 is 10. Line 51 shows that
     there have been none since `num0_is_10` EventSearch was defined back on
     line 20.
   - Line 51: Run a transaction that has num0 equal to 10. (Defining the
     sender ``u`` is not shown.)
   - Line 52: As expected. when we check for a new transaction it is
     returned.


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

.. image:: ../images/section_separator.png


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

   - Line 23: You can specify a denomination to get the value in `wei`.
     See the the `Example` for :meth:`simpleth.Convert.denominations_to_wei`
     for the list of valid denominations.
   - Line 6: :meth:`convert_ether` is the usual way to compute
     a conversion between denominations. This line shows the number
     of `gwei` in 20 `ether`. For best precision, the method returns
     a ``decimal`` type. This example casts to an integer.
   - Line 13: Get `user` balance in `ether`.
   - Line 15: ``Test`` contract has a balance of 10 `wei`.
   - Line 20: Move 10 `wei` from ``owner`` to ``user``.
   - Line 24: ``user`` balance increased by 10 `wei`. Line 43 is
     the *before* balance.
   - Line 26: Example of sending ether to a transaction. The ``Test``
     contract has the function, :meth:`storeNumsAndPay` that is
     identical to our trusty, :meth:`storeNums`, except it is
     defined as ``payable`` in the contract. This allows us to
     send Ether when we run the transaction. Here, we are sending
     10 `wei` .
   - Line 27: Get the :meth:`trx_value_wei` sent to the
     transaction. As expected, line 52 shows it is 100 `wei`.
   - Line 30: Confirms that 100 `wei` were sent. The balance is
     now 100 `wei` more than the *before* balance on line 49
   - Line 31: You can also send ether to a contract. Here, 500
     `wei` is sent to the ``Test`` contract. This is confirmed
     in line 58 where the balance increased by 500 from the
     *before* balance on line 54. **Important**: the contract must have
     a ``payable`` `fallback` function in order to receive ether.
     The ``Test`` contract has such a function as the final
     function in the contract.

.. image:: ../images/section_separator.png


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

.. image:: ../images/section_separator.png


simpleth exceptions
*******************
:class:`simpleth.SimplethError` throws exceptions for errors in all
``simpleth`` classes. The intent is to let you code to catch this
single exception to simplify error-handling and provide hints to
quickly identify the cause of the error.

.. code-block:: python
   :linenos:
   :caption: Getting a SimplethError in the Python interpreter

    >>> c = Contract('bogus')
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "C:\Users\snewe\OneDrive\Desktop\simpleth\src\simpleth\simpleth.py", line 943, in __init__
        self._abi: List = self._get_artifact_abi()
      File "C:\Users\snewe\OneDrive\Desktop\simpleth\src\simpleth\simpleth.py", line 2151, in _get_artifact_abi
        raise SimplethError(message, code='C-100-010') from None
    simpleth.SimplethError: [C-100-010] ERROR in bogus()._get_artifact_abi(). Unable to read ABI file.
    Full path: C:/Users/snewe/OneDrive/Desktop/simpleth/artifacts/bogus.abi
    Contract name of "bogus" is bad.
    HINT 1: Check the spelling of the contract name.
    HINT 2: You may need to do a new compile.

.. note::

   - Line 1: Cause an exception with a bad `contract` name. This is the
     typical type of message you will see when using the Python interpreter.
   - Line 8: This is the start of the ``SimplethError`` message and hints
     on possible causes.

.. code-block:: shell-session
   :linenos:
   :caption: Handling a SimplethError

    >>> try:
    ...     c = Contract('bogus')
    ... except SimplethError as e:
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
   :caption: Properties of a SimplethError

    >>> import pprint
    >>> pp = pprint.PrettyPrinter(indent = 2)
    >>> try:
    ...     c = Contract('bogus')
    ... except SimplethError as e:
    ...     print(f'code = \n{e.code}')
    ...     print(f'message = \n{e.message}')
    ...     print(f'revert_msg = \n{e.revert_msg}')
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

    revert_msg =

    exc_info =
    { ( <class 'FileNotFoundError'>,
        FileNotFoundError(2, 'No such file or directory'),
        <traceback object at 0x00000231A2CDE6C0>)}

.. note::

   - Line 6: There are three properties you can access. First is the
     unique ``code`` string for the exception. It is accessed here and
     its value is printed on line 13.
   - Line 5: The text of the error message is accessed here and printed
     on lines 15 through 20.
   - Line 8: The ``revert_msg`` is sent back from a transaction that
     had a ``require()`` that failed or a ``revert()``. Otherwise,
     it is empty. Our empty string is shown on line 22.
   - Line 10: The exception information is accessed here and pretty
     printed on lines 24 through 26.

   You can access these properties instead of the entire message if
   that suits your purpose better in handling ``simpleth`` errors.

.. image:: ../images/section_separator.png


Transaction exceptions
**********************
Exceptions can be thrown by the Solidity Virtual Machine (VM) that runs
the transaction when it encounters runtime errors such as:

- divide by zero
- out of bounds array index
- out of gas
- out of range enum value
- ether sent to a non-payable transaction
- transaction sender was not valid
- insufficient ether in sender balance to run the transaction

These **transaction error exceptions** will cause ``SimplethError``
exceptions for your code to handle.

Other exceptions can be thrown by the VM which are coded into
a transaction. A contract may be checking for conditions where
the transaction should not be allowed to proceed and needs to
be `reverted`. The transaction can:

#. Use the Solidity operation, ``require`` , to validate a
   condition is met. If the condition is not met, a ``revert``
   is done and an optional message string will be available
   in the ``SimplethError``

   ``require`` is commonly used in a contract ``modifier`` and
   a frequent type of modifier is to limit access to a transaction
   to one or more specified accounts.

#. Use of the Solidity operation, ``assert`` , to confirm an
   expected condition. There is no message for a failed assert.

   ``assert`` is commonly used to double-check a value meets
   your expectations and should never fail.

#. Use of the Solidity operation, ``revert`` , will cause the
   transaction to stop and exit. There is no message for a
   revert.

   ``revert`` is used if conditions warrant stopping and undoing
   all actions by the transaction.

These **transaction exceptions** will cause ``SimplethError``
exceptions for your code to handle.

We'll go through some examples. First up is what a transaction error
exception thrown by an out of bounds index value looks like in the
Python interpreter and how it might look in your code with a
``try`` / ``except``:

.. code-block:: shell-session
   :linenos:
   :caption: Handling transaction error exceptions

    >>> c.run_trx(user, 'storeNum', 4, 42)
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "C:\Users\snewe\OneDrive\Desktop\simpleth\src\simpleth\simpleth.py", line 1838, in run_trx
        trx_hash: T_HASH = self.submit_trx(
      File "C:\Users\snewe\OneDrive\Desktop\simpleth\src\simpleth\simpleth.py", line 2128, in submit_trx
        f'HINT11: Was max_priority_fee_gwei a float? (It must be an int)\n'
    simpleth.SimplethError: [C-080-080] ERROR in Test().submit_trx(storeNum).
    ValueError says: VM Exception while processing transaction: revert
    HINT1:  Did you fail to pass a transaction require()?
    HINT2:  Did you fail to pass a transaction guard modifier()?
    HINT3:  Did you fail an assert()?
    HINT4:  Did the transaction do a revert()?
    HINT5:  Did you divide by zero?
    HINT6:  Did you pass in an out-of-bounds array index?
    HINT7:  Did you pass in an out-of-range enum value?
    HINT8:  Was the gas limit too low (less than the base fee)?
    HINT9:  Was the gas limit too high (greater than the block gas limit)?
    HINT10: Was max_fee_gwei a float? (It must be an int)
    HINT11: Was max_priority_fee_gwei a float? (It must be an int)
    HINT12: Did this trx call another trx, which failed?
    HINT13: Did you attempt to send ether to a non-payable trx?
    HINT14: Was sender a valid account that can submit a trx?
    HINT15: Does sender have enough Ether to run trx?

    >>> try:
    ...     c.run_trx(user, 'storeNum', 4, 42)
    ... except SimplethError as e:
    ...     print(e.code)
    ...     print(e.message)
    ...     print(e.revert_msg)
    ...     pp.pprint(e.exc_info)
    ...
    C-080-080
    ERROR in Test().submit_trx(storeNum).
    ValueError says: VM Exception while processing transaction: revert
    HINT1:  Did you fail to pass a transaction require()?
    HINT2:  Did you fail to pass a transaction guard modifier()?
    HINT3:  Did you fail an assert()?
    HINT4:  Did the transaction do a revert()?
    HINT5:  Did you divide by zero?
    HINT6:  Did you pass in an out-of-bounds array index?
    HINT7:  Did you pass in an out-of-range enum value?
    HINT8:  Was the gas limit too low (less than the base fee)?
    HINT9:  Was the gas limit too high (greater than the block gas limit)?
    HINT10: Was max_fee_gwei a float? (It must be an int)
    HINT11: Was max_priority_fee_gwei a float? (It must be an int)
    HINT12: Did this trx call another trx, which failed?
    HINT13: Did you attempt to send ether to a non-payable trx?
    HINT14: Was sender a valid account that can submit a trx?
    HINT15: Does sender have enough Ether to run trx?


    ( <class 'ValueError'>,
      ValueError({'message': 'VM Exception while processing transaction: revert', 'code': -32000, 'data': {'0x6f829f521ebd6bf7ab34feea51bb4c18b82c663229004af13fa4ea788f0117d9': {'error': 'revert', 'program_counter': 5528, 'return': '0x4e487b710000000000000000000000000000000000000000000000000000000000000032'}, 'stack': 'RuntimeError: VM Exception while processing transaction: revert\n    at Function.RuntimeError.fromResults (C:\\Program Files\\WindowsApps\\GanacheUI_2.5.4.0_x64__5dg5pnz03psnj\\app\\resources\\static\\node\\node_modules\\ganache-core\\lib\\utils\\runtimeerror.js:94:13)\n    at BlockchainDouble.processBlock (C:\\Program Files\\WindowsApps\\GanacheUI_2.5.4.0_x64__5dg5pnz03psnj\\app\\resources\\static\\node\\node_modules\\ganache-core\\lib\\blockchain_double.js:627:24)\n    at processTicksAndRejections (internal/process/task_queues.js:93:5)', 'name': 'RuntimeError'}}),
      <traceback object at 0x00000231A2E161C0>)

.. note::

   - Line 1: Let's cause the VM to throw an exception due to an out
     of bounds array index.  Here we are asking ``storeNum`` to put
     the value of `42` into ``nums[4]``. This is a bad index value.
     ``nums[]`` only has 3 elements.
   - Line 2: You see the Python interpreter output with the exception.
     The error output ends on line 25.
   - Line 26: In a Python program, you might put the statement
     in a ``try`` / ``except`` . The example prints out the properties
     you could access. Your code would probably take steps to notify
     the user of the error or other code to handle the problem; not just
     print error info.
   - Line 34: This is the error code for transaction error
     exceptions. (The `Hints` list covers the usual causes.)
   - Line 35: This is the start of the error message text created by
     ``simpleth``. The message text ends on line 52.
   - Line 53: This is the transaction's revert message. It is an empty
     string for an oob (out-of-bounds) error.
   - Line 53: This is the pretty print of the exception info property.
     A ``ValueError`` caused an exception. SimplethError caught it and
     threw its exception with a lot of added info. This lets you see
     the original info from the first exception.

Next up, let's start looking at exceptions that are coded into the ``Test``
contract. The transaction, ``sumTwoNums`` , has a ``require()`` that checks
for the ``owner`` of the contract to be the address that sent the transaction,
i.e., the owner is the only one allowed to use this transaction. The
``require()`` has a message that explains the problem.

.. code-block:: shell-session
   :linenos:
   :caption: Handling transaction thrown exceptions - require and its message

    >>> c.run_trx(user, 'sumTwoNums')
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "C:\Users\snewe\OneDrive\Desktop\simpleth\src\simpleth\simpleth.py", line 1838, in run_trx
        trx_hash: T_HASH = self.submit_trx(
      File "C:\Users\snewe\OneDrive\Desktop\simpleth\src\simpleth\simpleth.py", line 2128, in submit_trx
        f'HINT11: Was max_priority_fee_gwei a float? (It must be an int)\n'
    simpleth.SimplethError: [C-080-080] ERROR in Test().submit_trx(sumTwoNums).
    ValueError says: VM Exception while processing transaction: revert must be owner to sum two nums
    HINT1:  Did you fail to pass a transaction require()?
    HINT2:  Did you fail to pass a transaction guard modifier()?
    HINT3:  Did you fail an assert()?
    HINT4:  Did the transaction do a revert()?
    HINT5:  Did you divide by zero?
    HINT6:  Did you pass in an out-of-bounds array index?
    HINT7:  Did you pass in an out-of-range enum value?
    HINT8:  Was the gas limit too low (less than the base fee)?
    HINT9:  Was the gas limit too high (greater than the block gas limit)?
    HINT10: Was max_fee_gwei a float? (It must be an int)
    HINT11: Was max_priority_fee_gwei a float? (It must be an int)
    HINT12: Did this trx call another trx, which failed?
    HINT13: Did you attempt to send ether to a non-payable trx?
    HINT14: Was sender a valid account that can submit a trx?
    HINT15: Does sender have enough Ether to run trx?

    >>> try:
    ...     c.run_trx(user, 'sumTwoNums')
    ... except SimplethError as e:
    ...     msg = e.revert_msg
    ...
    >>> msg
    'must be owner to sum two nums'

.. note::

   - Line 1: ``user`` is not allowed to use this transaction. The transaction's
     ``require()`` reverts, throws an exception, and sends back a message.
   - Line 9: Shows the message. It has been passed back as part of the
     ``ValueError`` exception, which ``SimplethError`` catches.
   - Line 26: Uses a ``try`` / ``except`` to get the message from the
     failed ``require()``.
   - Line 31: ``msg`` has the message explaining why the transaction was
     reverted.

Let's look at a modifier that fails. ``Test`` has a transaction, ``setOwner``
that is guarded by a modifier ``isOwner``. This is implemented with a
``require()``. This example is included because modifiers are very common
and you'll see they act just like the previous example of a failed
``require()``

.. code-block:: python
   :linenos:
   :caption: Handling transaction thrown exceptions - modifier with message

    >>> try:
    ...     c.run_trx(user, 'setOwner', user)
    ... except SimplethError as e:
    ...     msg = e.revert_msg
    ...
    >>> msg
    'Must be owner'

.. note::

   - Line 2: This will fail the ``isOwner`` modifier since our ``user``
     account does not own ``Test`` .
   - Line 4: Shows how to obtain the message coded in the contract for the
     ``require()`` used in the ``modifier`` .
   - Line 6: Your program could now show this error message to your user.

This example shows a failed ``assert()``. There is no message associated
with an assert. If the test fails, the transaction is reverted and a Python
``ValueError`` is thrown.

.. code-block:: shell-session
   :linenos:
   :caption: Handling transaction thrown exceptions - assert

    >>> c.run_trx(user, 'assertGreaterThan10', 9)
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "C:\Users\snewe\OneDrive\Desktop\simpleth\src\simpleth\simpleth.py", line 1838, in run_trx
        trx_hash: T_HASH = self.submit_trx(
      File "C:\Users\snewe\OneDrive\Desktop\simpleth\src\simpleth\simpleth.py", line 2121, in submit_trx
        raise SimplethError(message, code='C-080-080') from None
    simpleth.SimplethError: [C-080-080] ERROR in Test().submit_trx(assertGreaterThan10).
    ValueError says:
    HINT1:  Did you fail to pass a transaction require()?
    HINT2:  Did you fail to pass a transaction guard modifier()?
    HINT3:  Did you fail an assert()?
    HINT4:  Did the transaction do a revert()?
    HINT5:  Did you divide by zero?
    HINT6:  Did you pass in an out-of-bounds array index?
    HINT7:  Did you pass in an out-of-range enum value?
    HINT8:  Was the gas limit too low (less than the base fee)?
    HINT9:  Was the gas limit too high (greater than the block gas limit)?
    HINT10: Was max_fee_gwei a float? (It must be an int)
    HINT11: Was max_priority_fee_gwei a float? (It must be an int)
    HINT12: Did this trx call another trx, which failed?
    HINT13: Did you attempt to send ether to a non-payable trx?
    HINT14: Was sender a valid account that can submit a trx?
    HINT15: Does sender have enough Ether to run trx?

    >>> try:
    ...     c.run_trx(user, 'assertGreaterThan10', 9)
    ... except SimplethError as e:
    ...     pp.pprint(e.exc_info)
    ...
    ( <class 'ValueError'>,
      ValueError({'message': 'VM Exception while processing transaction: revert', 'code': -32000, 'data': {'0x5d3bee4eee5c9b320eff083666910bf9ff0ab0bb9c9790f27226d4ec78685cb9': {'error': 'revert', 'program_counter': 5664, 'return': '0x4e487b710000000000000000000000000000000000000000000000000000000000000001'}, 'stack': 'RuntimeError: VM Exception while processing transaction: revert\n    at Function.RuntimeError.fromResults (C:\\Program Files\\WindowsApps\\GanacheUI_2.5.4.0_x64__5dg5pnz03psnj\\app\\resources\\static\\node\\node_modules\\ganache-core\\lib\\utils\\runtimeerror.js:94:13)\n    at BlockchainDouble.processBlock (C:\\Program Files\\WindowsApps\\GanacheUI_2.5.4.0_x64__5dg5pnz03psnj\\app\\resources\\static\\node\\node_modules\\ganache-core\\lib\\blockchain_double.js:627:24)\n    at runMicrotasks (<anonymous>)\n    at processTicksAndRejections (internal/process/task_queues.js:93:5)', 'name': 'RuntimeError'}}),
      <traceback object at 0x000001DE3411BAC0>)

.. note::

   - Line 1: This transaction will fail its ``assert()``. We are passing
     in an arg of `9`. The assert requires that arg to be greater than 10.
   - Line 2: This is the output in the interpreter and continues to line25.
     Note that there is nothing passed back in line 9. Unlike in some
     earlier examples where a message from the contract was shown.
   - Line 26: As before, use a ``try`` / ``except`` to pretty print
     the ``ValueError`` exception info. There's nothing unique to
     pass back to our user.

Finally, let's look at what happens when a transaction uses a ``revert()``
statement. ``Test`` has a transaction, ``revertTransaction`` with only
one statement, a ``revert()``. A ``revert()`` can have a message. We'll
look for it in the same manner we did for ``require()``:

.. code-block:: shell-session
   :linenos:
   :caption: Handling transaction thrown exceptions - revert with message

    >>> c.run_trx(user, 'revertTransaction')
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "C:\Users\snewe\OneDrive\Desktop\simpleth\src\simpleth\simpleth.py", line 1838, in run_trx
        trx_hash: T_HASH = self.submit_trx(
      File "C:\Users\snewe\OneDrive\Desktop\simpleth\src\simpleth\simpleth.py", line 2128, in submit_trx
        f'HINT11: Was max_priority_fee_gwei a float? (It must be an int)\n'
    simpleth.SimplethError: [C-080-080] ERROR in Test().submit_trx(revertTransaction).
    ValueError says: VM Exception while processing transaction: revert Revert this transaction.
    HINT1:  Did you fail to pass a transaction require()?
    HINT2:  Did you fail to pass a transaction guard modifier()?
    HINT3:  Did you fail an assert()?
    HINT4:  Did the transaction do a revert()?
    HINT5:  Did you divide by zero?
    HINT6:  Did you pass in an out-of-bounds array index?
    HINT7:  Did you pass in an out-of-range enum value?
    HINT8:  Was the gas limit too low (less than the base fee)?
    HINT9:  Was the gas limit too high (greater than the block gas limit)?
    HINT10: Was max_fee_gwei a float? (It must be an int)
    HINT11: Was max_priority_fee_gwei a float? (It must be an int)
    HINT12: Did this trx call another trx, which failed?
    HINT13: Did you attempt to send ether to a non-payable trx?
    HINT14: Was sender a valid account that can submit a trx?
    HINT15: Does sender have enough Ether to run trx?

    >>> try:
    ...     c.run_trx(user, 'revertTransaction')
    ... except SimplethError as e:
    ...     msg = e.revert_msg
    ...
    >>> msg
    'Revert this transaction.'

.. note::

   - Line 1: Call the transaction that always reverts.
   - Line 9: Here's the way the revert message will appear in the
     interpreter.
   - Line 32: Here's the revert message.

.. image:: ../images/section_separator.png


Selfdestruct
************
Solidity includes the ``selfdestruct()`` function.
The ``Test`` contract includes a transaction, :meth:`destroy`
which issues ``selfdestruct`` and makes the contract unusable. As far as
``simpleth`` goes this is just another transaction, but it makes for
an interesting example:

.. code-block:: shell-session
   :linenos:
   :caption: Destroying Test with a selfdestruct

    >>> b.balance(c.address)
    610
    >>> b.balance(b.accounts[3])
    99889613060000000010
    >>> receipt = c.run_trx(owner, 'destroy', b.accounts[3])

    >>> b.balance(c.address)
    0
    >>> b.balance(b.accounts[3])
    99889613060000000620
    >>> c.get_var('owner')
    Traceback (most recent call last):
    ... snip ...
    simpleth.SimplethError: [C-060-020] ERROR in Test().getvar(): Unable to get variable owner.
    BadFunctionCallOutput says Could not transact with/call contract function, is contract deployed correctly and chain synced?
    HINT1: Has contract been destroyed with selfdestruct()?
    HINT2: Has contract not yet been deployed on a new chain?

    >>> c.call_fcn('getNums')
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
      File "C:\Users\snewe\OneDrive\Desktop\simpleth\src\simpleth\simpleth.py", line 1253, in call_fcn
        raise SimplethError(message, code='C-010-030') from None
    simpleth.SimplethError: [C-010-030] ERROR in Test().call_fcn().
    Unable to call function getNums.
    BadFunctionCallOutput says Could not transact with/call contract function, is contract deployed correctly and chain synced?
    HINT1: Has contract been destroyed with a selfdestruct()?
    HINT2: Does contract need a new deploy?

    >>> receipt = c.run_trx(user, 'storeNums', 2, 4, 6)
    >>> print(Results(c, receipt))
    Block number     = 7580
    Block time epoch = 1653320103
    Contract name    = Test
    Contract address = 0x82592d5ae9E9ECc14b1740F330D3fAA00403a1F3
    Trx name         = storeNums
    Trx args         = {'_num0': 2, '_num1': 4, '_num2': 6}
    Trx sender       = 0x20e0A619E7Efb741a34b8EDC6251E2702e69bBDd
    Trx value wei    = 0
    Trx hash         = 0xb54e479495ea815943fa08069566c5cf68aaf70c6d42a23f7590bf399e0d6be1
    Gas price wei    = 20000000000
    Gas used         = 21484

    >>> e=EventSearch(c, 'NumsStored')
    >>> e.get_old()
    []

.. note::

   - Line 2: Ether balance of ``Test`` contract.
   - Line 4: Ether balance of the fourth Ganache account.
   - Line 5: Run :meth:`destroy`. It takes one argument, the address
     of an account to receive all the Ether in the contract's balance.
     Once you have destroyed a contract, you can no longer access its
     Ether. Save it now or lose it.
   - Line 8: Contract has no Ether.
   - Line 10: Fourth account got it.
   - Line 11: If you try to get a public state variable's value,
     you will get an error.
   - Line 19: If you try to call a function, you will get a
     slightly different error.
   - Line 30: Beware, if you try to run a transaction. It does not
     generate any error. For a destroyed contract, transactions will
     not be able to change any values on the blockchain. They look like
     they run, but they have no effect.
   - Line 31: The results do not show any event being emitted.
     :meth:`storeNums` always emits :meth:`NumsStored`.
   - Line 46: Confirms that the :meth:`NumsStored` event was not
     emitted. Because the contract is destroyed, the transaction
     did not alter the blockchain.

.. image:: ../images/section_separator.png


Send transactions / Get receipt
*******************************
The trio of ``simpleth`` methods described here are an alternative
to using :meth:`run_trx` . If you are happy with using `run_trx`,
you can skip this.

If you are curious, read on...

Ganache spoils us. It mines transactions immediately. You submit a
transaction and can immediately get the results.

In a production application, running on a testnet or the mainnet,
this is not the case. There is a delay
between the time you submit a transaction and the time in which it is
added to a block and mined. This delay could be a few seconds or many
hours (or never).

You might chose to use
:meth:`simpleth.Contract.send_trx` with
:meth:`simpleth.Contract.get_trx_receipt` or
:meth:`simpleth.Contract.get_trx_receipt_wait`
to give you more flexibility in managing the mining delay.

:meth:`send_trx` submits the transaction and
immediately returns the `transaction hash`.
The `hash` is a string that acts as the identifier of the
transaction.

Using that `hash` as a parameter, you can call :meth:`get_trx_receipt`
to do a quick check to see if the transaction has finished. If not,
you can wait for some period time and check again. You would repeat this
until the transaction finishes or you give up. :meth:`get_trx_receipt`
makes its check and returns immediately.

Alternatively, you can use the `hash` as a parameter
and call :meth:`get_trx_receipt_wait`. This does not return
immediately. It will periodically check to see if the transaction
has finished and returns when it has completed or
it times out before finding the transaction completed.
There are parameters for how frequently to poll and how long
to keep trying before timing out. Note that this call will
block until it returns.

Both :meth:`get_trx_receipt` and :meth:`get_trx_receipt_wait`
return either ``None`` if the transaction has not yet been
mined or ``transaction receipt`` if the transaction completed.
Just like with :meth:`run_trx`, you can use the `receipt` to
get the :class:`Results`.

Relationship to run_trx()
"""""""""""""""""""""""""
Under the covers, :meth:`run_trx` simply makes a call to
:meth:`send_trx` and then a call to :meth:`get_trx_receipt_wait`.
You see that the parameters for :meth:`run_trx` are the union of
the parameters of :meth:`send_trx` and :meth:`get_trx_receipt_wait`.

:meth:`run_trx` blocks until the transaction completes or it times out.

:meth:`run_trx` only throws one exception of its own.
When you use :meth:`run_trx` most the exceptions
are thrown by :meth:`send_trx` or :meth:`get_trx_receipt_wait` .

Using Ganache with a mining delay
"""""""""""""""""""""""""""""""""
You can simulate a delay in completing a transaction. Ganache
setting's allow you to change from the default of ``automine`` ,
where all transactions are mined immediately, to setting a constant number
of seconds before the transaction is put into a new block on the
chain. This allows you to, say, set a delay of ten seconds in
order to test use of the periodic checking in :meth:`get_trx_receipt_wait`
or :meth:`run_trx`.

.. code-block:: python
   :linenos:
   :caption: Send transaction and get the receipt
   :emphasize-lines: 1,2,18,21

    >>> trx_hash = c.submit_trx(user, 'storeNums', 1, 2, 3)
    >>> receipt = c.get_trx_receipt(trx_hash)
    >>> print(Results(c, receipt))
    Block number     = 7583
    Block time epoch = 1653324228
    Contract name    = Test
    Contract address = 0xe837B30EFA8Bd88De16276b6009a29ef70b1b693
    Trx name         = storeNums
    Trx args         = {'_num0': 1, '_num1': 2, '_num2': 3}
    Trx sender       = 0x20e0A619E7Efb741a34b8EDC6251E2702e69bBDd
    Trx value wei    = 0
    Trx hash         = 0xae9ac7ab7679b9f808e766153c5dd979fb78ed69cbed54c1e19ed9d0d5c8a881
    Gas price wei    = 20000000000
    Gas used         = 26164
    Event name[0]    = NumsStored
    Event args[0]    = {'timestamp': 1653324228, 'num0': 1, 'num1': 2, 'num2': 3}

    >>> trx_hash = c.submit_trx(user, 'storeNums', 1, 2, 3)
    >>> trx_hash
    '0x0fe19c89b66c424c4696b2323b68dd72ef2de731709520cc5c24a78b927027a8'
    >>> receipt = c.get_trx_receipt_wait(trx_hash, timeout=3600, poll_latency=15)
    >>> print(Results(c, receipt))
    Block number     = 7584
    Block time epoch = 1653324309
    Contract name    = Test
    Contract address = 0xe837B30EFA8Bd88De16276b6009a29ef70b1b693
    Trx name         = storeNums
    Trx args         = {'_num0': 1, '_num1': 2, '_num2': 3}
    Trx sender       = 0x20e0A619E7Efb741a34b8EDC6251E2702e69bBDd
    Trx value wei    = 0
    Trx hash         = 0x0fe19c89b66c424c4696b2323b68dd72ef2de731709520cc5c24a78b927027a8
    Gas price wei    = 20000000000
    Gas used         = 26164
    Event name[0]    = NumsStored
    Event args[0]    = {'timestamp': 1653324309, 'num0': 1, 'num1': 2, 'num2': 3}

.. note::

   - Line 1: Instead of ``run_trx`` use ``submit_trx`` to run :meth:`storeNums`
     transaction. The transaction's `hash` is returned.
   - Line 2: Use that `hash` to get the transaction's `receipt`.
   - Line 3: As before, we can get the results using that `receipt`.
   - Line 18: Sumit again.
   - Line 20: Here's our `hash`.
   - Line 21: Use ``get_trx_receipt_wait`` this time and specify overrides
     to the defaults for ``timeout`` and ``poll_latency``. Since my Ganache is not
     doing any mining delay these parameters do not come into play and
     this returns immediately with the `receipt`.
   - Line 22: Get and print the results.


.. image:: ../images/section_separator.png


Compiling a contract
********************
After creating a contract or making any code changes to an existing contract
you need to compile it before it can be deployed on the blockchain.

You use the Solidity compiler, ``solc.exe``, to create two output files
and store them in the directory named in the environment variable,
``SIMPLETH_ARTIFACTS_DIR``.

After a successful compile, the contract is ready to deploy.

Using solc
""""""""""
Use ``solc.exe`` with the arguments shown below to make a contract
ready to deploy by ``simpleth``:

.. code-block:: shell-session
   :caption: Command to compile a smart contract for use by simpleth

   solc --abi --bin --optimize --overwrite -o <ARTIFACTS_DIR> <CONTRACT>

Where:

- ``abi`` writes the application binary interface file
- ``bin`` writes the binary file
- ``optimize`` enables the bytecode optimizer to create more efficient
  contracts.
- ``overwrite`` replaces any existing copies of the files
- ``o`` specifies the path to the output directory for the files
- ``<ARTIFACTS_DIR>`` is the path to the directory to hold the compiler
  output flies.
- ``<CONTRACT>`` is the path to the Solidity smart contract source
  file to compile


.. code-block:: shell-session
   :caption: Example of compiling the Test.sol contract
   :linenos:

   $ solc --abi --bin --optimize --overwrite -o %SIMPLETH_ARTIFACTS_DIR% contracts\Test.sol
   Compiler run successful. Artifact(s) can be found in directory "<%SIMPLETH_ARTIFACTS_DIR%>".

.. note::

   - Line 1 - the example runs from the ``simpleth`` directory.
   - Line 2 - uses the environment variable for the path to the output directory
   - Line 3 - success message from compiler

    See `Solidity compiler documentation \
    <https://docs.soliditylang.org/en/v0.8.7/using-the-compiler.html#using-the-compiler>`_
    for compiler details.


.. artifact_directory_label:

Artifact directory
******************
The artifact directory is crucial to ``simpleth``. It holds the information
about compiled contracts for the :class:`Contract` methods to use. The
environment variable, ``SIMPLETH_ARTIFACTS_DIR``, stores the path to the
directory.

There are up to five files for each contract stored in the artifact directory.
All files have ``<contract>`` as the filename. The suffixes are explained
below:

+------------+-------------+-----------------------------------------------------------------------------------------------+
| **Suffix** | **Creator** | **Purpose**                                                                                   |
+------------+-------------+-----------------------------------------------------------------------------------------------+
| .abi       | solc.exe    | ABI file. Created with ``--abi`` arg. Must be present to :meth:`deploy` or :meth:`connect`.   |
+------------+-------------+-----------------------------------------------------------------------------------------------+
| .addr      | Contract()  | Blockchain address. Written at deploy(). Required for :meth:`connect`.                        |
+------------+-------------+-----------------------------------------------------------------------------------------------+
| .bin       | solc.exe    | BIN file. Created with ``--bin`` arg. Must be present to :meth:`deploy` or :meth:`connect`.   |
+------------+-------------+-----------------------------------------------------------------------------------------------+
| .docdev    | solc.exe    | Developer Natspec comments JSON file. Created with ``--docdev`` arg. Used for documentation.  |
+------------+-------------+-----------------------------------------------------------------------------------------------+
| .docuser   | solc.exe    | User Natspec comments JSON file. Created with ``--docuser`` arg. Used for documentation.      |
+------------+-------------+-----------------------------------------------------------------------------------------------+

.. code-block:: shell-session
   :caption: Example of Test contract files in the artifact directory
   :linenos:

    $ cd %SIMPLETH_ARTIFACTS_DIR%
    $ dir Test.*
    ... snip ....

    05/29/2022  09:06 AM            11,865 Test.abi
    05/29/2022  08:02 AM                42 test.addr
    05/29/2022  09:06 AM            12,100 Test.bin


.. note::
   - Line 8: Due to DOS file naming convention, upper and lower
     case does not matter in the file names. The `.addr` file will
     be present after a contract is deployed.

When :meth:`deploy` runs, it uses the environment variable to look in
that directory for the ABI and BIN files needed to install the contract
on the blockchain. :meth:`deploy` will write the address of the newly
installed contract to the ``<contract>.addr`` file.
If a contract has been compiled, but not yet deployed, there will be
no `.addr` file in the directory. After the first-ever deployment the
`.addr` file is written to  the directory. Any subsequent :meth:`deploy`
will update the contract's address stored in the file.

When :meth:`connect` runs, it uses that environment variable to
load up information about the deployed contract, including the address
of the deployed contract.

If you destroy an `.addr` file, that contract is lost to ``simpleth``.
You will not be able to access that installed instance of the contract.

.. warning::
   If you do not set ``SIMPLETH_ARTIFACTS_DIR``, it will default to, ``.``,
   the current working directory.
