Hello World
===========
Four simple `Solidity` **hello world** contracts are used as examples.
They grow progressively more complicated with ``simpleth`` Python
examples to interact with each.

Solidity contracts can not print a string in a terminal window.
The four contracts take different approaches in returning
a `Hello World` string.

The Solidity source for the contracts is found in
``<project dir>/src/contracts/HelloWorld*.sol`` .
A copy of the source shown below, without comments.

The contracts have been compiled and are ready to deploy.
The final example shows the end-to-end steps to compile a
contract and deploy it.

.. image:: ../images/section_separator.png


HelloWorld1 Contract
********************
The simplest way to display `Hello World!` is to set that string as
the initial value of a public state variable in the contract
and use `simpleth` to get that variable and display the string.

There are two Python sessions shown:

#. For the very first use, deploy the contract and get the
   variable value.
#. For any subsequent use, connect to the deployed contract
   and get the variable value.

.. code-block::
  :linenos:
  :caption: HelloWorld1.sol

  pragma solidity ^0.8;
  contract HelloWorld1 {
      string public greeting = "Hello World!";
  }

.. note::

  - Line 3: The only action the contract takes is to
    set the `greeting` to `Hello World!`


.. code-block:: python
  :linenos:
  :caption: Deploy contract and get variable value

  >>> from simpleth import Blockchain, Contract
  >>> user = Blockchain().address(0)
  >>> c = Contract('HelloWorld1')
  >>> receipt = c.deploy(user)
  >>> c.get_var('greeting')
  'Hello World!'


.. note::

  - Line 2: We need the address of the account that will deploy
    the contract. `Ganache` provides ten addresses. Use the first
    in the list of those addresses.
  - Line 3: Create a :class:`Contract` object for the
    `HelloWorld1` contract. This allows us to interact with that
    contract.
  - Line 4: `user` uses :meth:`simpleth.Contract.deploy` to send
    the transaction to deploy   the `HelloWorld` contract onto the
    blockchain. The `transaction receipt` is returned.
  - Line 5: Now that the contract is on the blockchain, we
    can get the value of the `greeting` variable.


.. code-block:: python
  :linenos:
  :caption: Connect to deployed contract and get variable value

  >>> from simpleth import Blockchain, Contract
  >>> c = Contract('HelloWorld1')
  >>> c.connect()
  '0x7b70ff8eeeca4ebDeC0950347C592BDf7D1C047A'
  >>> c.get_var('greeting')
  'Hello World!'


.. note::

  Once a contract has been deployed it remains on the blockchain.
  In all future sessions, you only need to
  :meth:`simpleth.Contract.connect` to it to use it.

  - Line 2: As before, we need a :class:`Contract` object before
    doing anything with the contract.
  - Line 3: Connect the `contract object` to the deployed contract.
  - Line 4: :meth:`connect` returns the blockchain address of the
    contract. Your address will differ.
  - Line 5: Same as before: get the `greeting` variable's value.

.. image:: ../images/section_separator.png


HelloWorld2 Contract
********************
This contract uses a slightly more complicated way to return
`Hello World!`. The contract has one function that
returns the greeting string.

The first use of the contract requires a user to deploy it and
is shown below. The `import` statement is assumed to have been
issued and is not shown.

Subsequent sessions would only need to do a `connect`. That
example is not shown. See above for using ``connect``.

.. code-block::
  :linenos:
  :caption: HelloWorld2.sol

  pragma solidity ^0.8;
  contract HelloWorld2 {
      function getGreeting() public pure returns (string memory) {
          return 'Hello World!';
      }
  }

.. note::

  - Line 3: Defines the function `getGreeting` that returns the
    string of `Hello World!` .


.. code-block:: python
  :linenos:
  :caption: Deploy contract and run function to return greeting

  >>> user = Blockchain().address(4)
  >>> c = Contract('HelloWorld2')
  >>> receipt = c.deploy(user)
  >>> c.call_fcn('getGreeting')
  'Hello World!'

**Comments:**

- Line 1: This time use the fifth account address in the list
  of ten provided by Ganache to send the `deploy` transaction.
- Line 4: Ask the contract to call the ``getGreeting()`` function.
- Line 5: The value returned from the function is displayed.

.. image:: ../images/section_separator.png


HelloWorld3 Contract
********************
This contract has a transaction that lets us set the greeting
and a function to return the greeting.

.. code-block::
  :linenos:
  :caption: HelloWorld3.sol

  pragma solidity ^0.8;
  contract HelloWorld3 {
      string public greeting;

      function setGreeting(string memory _greeting) public {
          greeting = _greeting;
      }

      function getGreeting() public view returns (string memory) {
          return greeting;
      }
  }

.. note::

  - Line 5: Defines the transaction `setGreeting` which allows
    us pass in the greeting string.
  - Line 8: Same function we had in `HelloWorld2` to return
    the greeting string.


.. code-block:: python
  :linenos:
  :caption: Deploy contract, run transaction to set greeting, and run function to return greeting

  >>> user = Blockchain().address(4)
  >>> c = Contract('HelloWorld3')
  >>> receipt = c.deploy(user)
  >>> c.call_fcn('getGreeting')
  ''
  >>> receipt = c.run_trx(user, 'setGreeting', 'Good Morning World!')
  >>> c.call_fcn('getGreeting')
  'Good Morning World!'

.. note::

  - Line 1 to 3: Similar to examples above.
  - Line 4: Get the greeting. The contract code does not set an initial value.
  - Line 5: `getGreeting` returns an empty string.
  - Line 6: Set the greeting by running the transaction `setGreeting` and pass
    in one arg: the greeting string.
  - Line 7: Use `getGreeting` again. This time it returns the string we just
    set.

.. image:: ../images/section_separator.png


HelloWorld4 Contract
********************
This is the last `Hello World` contract. It builds
on `HelloWorld3` and adds two new capabilities. First,
this contract's constructor has a parameter to set
the greeting when we :meth:`deploy` the contract.
Second, it makes use of ``events`` to record
actions taken by transactions.

You will find three Python sessions for this example.
The first one shows setting and getting the greeting.
The second shows how to search for a specific event,
retrieve the that event, and display the
greeting from the event information. And, third,
by creating a :class:`Results` object and display
an attribute that holds the greeting.


.. code-block::
  :linenos:
  :caption: HelloWorld4.sol

  contract HelloWorld4 {
      string public greeting;

      event HelloWorld4Constructed(
          uint timestamp,
          address sender,
          string initGreeting,
          address HelloWorld4
      );

      event GreetingSet(
          uint timestamp,
          address sender,
          string greeting
      );


      constructor(string memory _initGreeting) {
          greeting = _initGreeting;
          emit HelloWorld4Constructed(
              block.timestamp,
              msg.sender,
              greeting,
              address(this)
          );
      }

      function setGreeting(string memory _greeting) public {
          greeting = _greeting;
          emit GreetingSet(
              block.timestamp,
              msg.sender,
              greeting
          );
      }

      function getGreeting() public view returns (string memory) {
          return greeting;
      }
  }


.. note::

  - Line 4: Defines an event to be emitted when the contract is
    deployed. The definition continues to line 9. It shows the
    names of the parameters that will be written as part of the
    event.
  - Line 11: Defines a second event to be emitted each time the
    greeting is set. The definition continues to line 15. It
    shows the names of the parameters that will be written.
  - Line 18: Defines the `constructor`. This is run when a
    `deploy` is done. Two actions will occur. A string for the
    initial greeting will be passed in via the `deploy()` and
    the `HelloWorld4Constructed`` event is emitted with the
    appropriate values for the arguments.
  - Line 28: Defines the `setGreeting`. It is an expansion of
    the function using in `HelloWorld3`. This function adds
    emitting the `GreetingSet` event with the args shown.
  - Line 37: Finally, the usual `getGreeting` function will
    return the greeting string.


Using a constructor argument
""""""""""""""""""""""""""""
Set the greeting at deployment time and then get it.

.. code-block:: python
  :linenos:
  :caption: Session 1: Deploy contract with a greeting, get the greeting, update the greeting, get updated greeting

  >>> user = Blockchain().address(0)
  >>> c = Contract('HelloWorld4')
  >>> receipt = c.deploy(user, 'Hello World')
  >>> c.call_fcn('getGreeting')
  'Hello World'
  >>> receipt = c.run_trx(user, 'setGreeting', 'Hello World!!!')
  >>> c.call_fcn('getGreeting')
  'Hello World!!!'

.. note::

  - Line 3: Note this ``deploy()`` passes in an arg to the
    ``constructor()``. This string becomes the contract's
    greeting. Line 4 gets that greeting.
  - Line 6: Updates the greeting.
  - Line 7: Gets that updated greeting with the value shown on line 8.


Using events
""""""""""""
Here's yet another way to say `Hello World` - by getting the greetings
from events emitted by the transactions.

.. code-block:: python
  :linenos:
  :caption: Session 2: Retrieve the initial greeting and the updated greeting from events

  >>> from simpleth import EventSearch
  >>> e1 = EventSearch(c, 'HelloWorld4Constructed')
  >>> events1 = e.get_old(-10)
  >>> len(events1)
  1
  >>> events1[0]['args']['initGreeting']
  'Hello World'
  >>> e2 = EventSearch(c, 'GreetingSet')
  >>> events2 = e2.get_old()
  >>> events2[0]['args']['greeting']
  'Hello World!!!'
  >>> events2
  [{'block_number': 6647, 'args': {'timestamp': 1652813868, 'sender': '0xa894b8d26Cd25eCD3E154a860A86f7c75B12D993', 'greeting': 'Hello World!!!'}, 'trx_hash': '0xadb823085350ffdc2f411c57d8b0b074f4ca6391465061ce5cff68e85a874a6c'}]

.. note::

  - Line 1: We need to use the :class:`simpleth.EventSearch` class.
  - Line 2: Create an `EventSearch` object for the event named,
    `HelloWorld4Constructed` . You'll find that event defined on
    line 4 of the ``HelloWorld4.sol`` contract shown above.
  - Line 3: Search for the constructor's event in the past
    10 blocks on the chain and put any such events in a list
    in ``events1``
  - Line 4: How many of these events did we find in the most
    recent ten blocks?  Line 5 shows there was one.
  - Line 6: Retrieve the string passed to the constructor.
    ``initGreeting`` was defined in line 7 of ``HelloWorld4.sol``
    above. The value was passed as an arg in the contract's
    line 23 when the event is emitted in line 20 to 25.
  - Line 7: Shows the value of that constructor arg.
  - Line 8: Similarly, let's look at the greeting we set in
    line 3 of the first Python session shown above. Here,
    we create a second :class:`EventSearch` object to look
    for that event.
  - Line 9: Without an arg, ``simpleth.EventSearch.get_old``
    just searches the last block on the chain.
  - Line 10: Get the value of the event ``greeting`` parameter.
  - Line 11: Shows the value of the arg we used in line 6 of
    the first Python session above.
  - Line 12: If you are curious what is kept in one of the
    event list elements, line 13 displays the full list element.
    (Your values for `block_number`, `timestamp`, `sender`, and
    `trx_hash` will differ.)


Using Results
"""""""""""""
One final way to say `Hello World` - by looking at the results
of running a transaction.


.. code-block:: python
  :linenos:
  :caption: Session 3: Set greeting and show results

  >>> from simpleth import Results
  >>> receipt = c.run_trx(user, 'setGreeting', '**Hello World**')
  >>> r = Results(c, receipt)
  >>> print(r)
  Block number     = 6753
  Block time epoch = 1652901844
  Contract name    = HelloWorld4
  Contract address = 0x2D14841dcE16c698Eb2B9304C74bA7b29A6137ae
  Trx name         = setGreeting
  Trx args         = {'_greeting': '**Hello World**'}
  Trx sender       = 0xa894b8d26Cd25eCD3E154a860A86f7c75B12D993
  Trx value wei    = 0
  Trx hash         = 0x190cc46815dfb849e5b6334ce64f5877714dbff245c1cfdc5276bd6e8cb76d57
  Gas price wei    = 20000000000
  Gas used         = 32440
  Event name[0]    = GreetingSet
  Event args[0]    = {'timestamp': 1652901844, 'sender': '0xa894b8d26Cd25eCD3E154a860A86f7c75B12D993', 'greeting': '**Hello World**'}

  >>> r.trx_name
  'setGreeting'
  >>> r.event_args[0]['greeting']
  '**Hello World**'

.. note::

  - Line 1: We need the :class:`Results` class.
  - Line 2: Run the transaction to set a new greeting. Same as we have done before.
  - Line 3: ``r`` is a ``Results`` object. It is created by using the ``receipt``
    from the transaction and the ``contract`` object. ``r`` holds the information
    about the transaction.
  - Line 4: Prints the details of the transaction.
  - Line 19: Shows how to access one attribute of the results.
  - Line 21: Get the `greeting` arg from ``setGreeting`` event. Line 22
    displays out last *Hello World*.
