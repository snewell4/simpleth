Getting Started - Hello World(s)
================================
Four simple `Solidity` **hello world** contracts are used as examples.
They grow progressively more complicated with ``simpleth`` Python
examples to interact with each.

Solidity contracts can not print a string in a terminal window.
The four contracts take different approaches in returning
a `Hello World` string.

The Solidity source for the contracts is found in
``<project dir>/src/contracts/HelloWorld*.sol`` .
A copy of the source shown below.

The contracts have been compiled and are ready to deploy.
The final example shows the end-to-end steps to compile a
contract and deploy it.

If you look at the Solidity source files for the contracts,
you will see a number of lines starting with `//` or `///` .
These are comments and are not included in the examples below.
The lines with `///` are `NatSpec` (Ethereum Natural Language
Specification Format) and can be used to automatically generate
documentation. This documentation for the four contracts is
found in the `simpleth` :doc:`Smart Contracts <contracts>` document.
For more info on the `NatSpec` format see the
`Solidity Documentation <https://docs.soliditylang.org/en/v0.8.13/natspec-format.html>`_

1) HelloWorld1 Contract
***********************
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

**Comments:**

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


**Comments:**

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


**Comments:**

Once a contract has been deployed it remains on the blockchain.
In all future sessions, you only need to
:meth:`simpleth.Contract.connect` to it to use it.

- Line 2: As before, we need a :class:`Contract` object before
  doing anything with the contract.
- Line 3: Connect the `contract object` to the deployed contract.
- Line 4: :meth:`connect` returns the blockchain address of the
  contract. Your address will differ.
- Line 5: Same as before: get the `greeting` variable's value.



2) HelloWorld2 Contract
***********************
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

**Comments:**

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


3) HelloWorld3 Contract
***********************
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

**Comments:**

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

**Comments:**

- Line 1 to 3: Similar to examples above.
- Line 4: Get the greeting. The contract code does not set an initial value.
- Line 5: `getGreeting` returns an empty string.
- Line 6: Set the greeting by running the transaction `setGreeting` and pass
  in one arg: the greeting string.
- Line 7: Use `getGreeting` again. This time it returns the string we just
  set.




4) HelloWorld4 Contract
***********************
This is the last `Hello World` contract lets us
set an initial greeting when we :meth:`deploy`
this contract and still lets us change the
greeting after deployment.

This contract also makes use of ``events`` to record
actions taken by transactions.

.. code-block::
  :linenos:
  :caption: HelloWorld3.sol

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


**Comments:**

- Line x:


.. code-block:: python
  :linenos:
  :caption: Deploy contract, run transaction to set greeting, and run function to return greeting

  >>> user = Blockchain().address(0)
  >>> c = Contract('HelloWorld4')
  >>> receipt = c.deploy(user, 'Hello World')
  >>> c.call_fcn('getGreeting')
  'Hello World'
  >>> receipt = c.run_trx(user, 'setGreeting', 'Hello World!!!')
  >>> c.call_fcn('getGreeting')
  'Hello World!!!'
  >>> from simpleth import EventSearch
  >>> e = EventSearch(c, 'HelloWorld4Constructed')
  >>> construct_events = e.get_old(-10)
  >>> len(construct_events)
  1
  >>> construct_events
  [{'block_number': 6646, 'args': {'timestamp': 1652813801, 'sender': '0xa894b8d26Cd25eCD3E154a860A86f7c75B12D993', 'initGreeting': 'Hello World', 'HelloWorld4': '0x2D14841dcE16c698Eb2B9304C74bA7b29A6137ae'}, 'trx_hash': '0x91a1898f42c8291c4d61f35e9d47e1478d909a69846468a4eafeb97f678a0b1d'}]
  >>> e2 = EventSearch(c, 'GreetingSet')
  >>> e2.get_old()
  [{'block_number': 6647, 'args': {'timestamp': 1652813868, 'sender': '0xa894b8d26Cd25eCD3E154a860A86f7c75B12D993', 'greeting': 'Hello World!!!'}, 'trx_hash': '0xadb823085350ffdc2f411c57d8b0b074f4ca6391465061ce5cff68e85a874a6c'}]


**Comments:**

- Line 1 to 3: Similar to examples above.