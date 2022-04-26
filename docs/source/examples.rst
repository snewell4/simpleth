Examples
========
These examples all rely on using the Solidity smart contract, ``TestTrx.sol``.
Take a look at that source file as you try these examples. You can see
how the Python code references the constructor param and event as well
as referencing the `storeNums` transaction, its params, and event.

Example 1 - deploying and using a contract
******************************************
.. code-block:: python

   from simpleth import Blockchain, Contract
   b = Blockchain()
   user = b.accounts[0]
   c = Contract('TestTrx')
   r = c.deploy(user, 42, constructor_event_name='TestTrxConstructed')
   print(r)
   r = c.run_trx(user, 'storeNums', 1, 2, 3, event_name='NumsStored')
   print(r)

Example 2 - using a deployed contract
*************************************
.. code-block:: python

   from simpleth import Blockchain, Contract
   b = Blockchain()
   user = b.accounts[0]
   c = Contract('TestTrx')
   c.connect()
   c.run_trx(user, 'storeNums', 1, 2, 3, event_name='NumsStored')

Example 3 - finding events emitted by a transaction
***************************************************
.. code-block:: python

   from simpleth import Blockchain, Contract, EventSearch
   b = Blockchain()
   user = b.accounts[0]
   c = Contract('TestTrx')
   f = EventSearch(c)
   events = f.get_old_events('NumsStored', 10)
   print(events)
   filter = f.create_filter('NumsStored')
   events = f.get_new_events(filter)
   len(events)
   c.run_trx(user, 'storeNums', 10, 20, 30, event_name='NumsStored')
   c.run_trx(user, 'storeNums', 40, 50, 60, event_name='NumsStored')
   c.run_trx(user, 'storeNums', 70, 70, 70, event_name='NumsStored')
   events = f.get_new_events(filter)
   len(events)
   print(events)