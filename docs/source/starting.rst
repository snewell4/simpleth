Hello World
===========
Four simple `Solidity` **hello world** contracts are used as examples.
Each takes a different approach, growing slightly more complex, in
returning the `Hello World!` string.

Solidity smart contracts by themselves can not print a string.
There is a separate Python program for each
contract that uses ``simpleth`` get and print the string.

The Python programs are found in ``<Python sys.prefix dir>/examples``. They
and the contracts are ready for you to try.

The Solidity source for the contracts is found in
``<Python sys.prefix dir>/contracts``.

.. image:: ../images/section_separator.png


HelloWorld1 Contract
********************
The simplest way to display `Hello World!` is to set that string as
the initial value of a public state variable in the contract
and use `simpleth` to get that variable and display the string.

.. code-block::
   :caption: HelloWorld1.sol

   pragma solidity ^0.8;
   contract HelloWorld1 {
       string public greeting = "Hello World!";
   }

.. code-block:: python
   :caption: helloworld1.py - deploy contract / get greeting variable / print

   sender = Blockchain().address(0)
   c = Contract('HelloWorld1')
   c.deploy(sender)
   greeting = c.get_var('greeting')
   print(greeting)

.. code-block:: shell-session
   :caption: Running helloworld1.py

   $ python hello_world1.py
   Hello World!

.. image:: ../images/section_separator.png


HelloWorld2 Contract
********************
This contract has one function that returns the greeting string.

.. code-block::
  :caption: HelloWorld2.sol

  pragma solidity ^0.8;
  contract HelloWorld2 {
      function getGreeting() public pure returns (string memory) {
          return 'Hello World!';
      }
  }

.. code-block:: python
  :caption: helloworld2.py - deploy contract / call the function to return the greeting / print

   from simpleth import Blockchain, Contract

   sender = Blockchain().address(0)
   c = Contract('HelloWorld2')
   c.deploy(sender)
   greeting = c.call_fcn('getGreeting')
   print(greeting)

.. code-block:: shell-session
   :caption: Running helloworld2.py

   $ python hello_world2.py
   Hello World!

.. image:: ../images/section_separator.png


HelloWorld3 Contract
********************
This contract has a transaction that lets us set the greeting
and a function to return the greeting.

.. code-block::
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

.. code-block:: python
  :caption: helloworld3.py - Deploy contract / run transaction to set greeting / run function to return greeting / print

  from simpleth import Blockchain, Contract

  sender = Blockchain().address(0)
  c = Contract('HelloWorld3')
  c.deploy(sender)
  c.run_trx(sender, 'setGreeting', 'Hello World!')
  greeting = c.call_fcn('getGreeting')
  print(greeting)

.. code-block:: shell-session
   :caption: Running helloworld3.py

   $ python hello_world3.py
   Hello World!

.. image:: ../images/section_separator.png


HelloWorld4 Contract
********************
This contract uses a constructor that takes the greeting as an arg and emits
an event with the greeting.

.. code-block::
  :linenos:
  :caption: HelloWorld4.sol

  pragma solidity ^0.8;
  contract HelloWorld4 {
      string public greeting;

      event HelloWorld4Constructed(
          uint timestamp,
          address sender,
          string initGreeting,
          address HelloWorld4
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
  }

.. code-block:: python
  :caption: helloworld4.py - Deploy contract with greeting / get event / print greeting

  from simpleth import Blockchain, Contract, EventSearch

  sender = Blockchain().address(0)
  c = Contract('HelloWorld4')
  c.deploy(sender, 'Hello World!')
  e = EventSearch(c, 'HelloWorld4Constructed')
  event = e.get_old()
  print(event[0]['args']['initGreeting'])

.. code-block:: shell-session
   :caption: Running helloworld4.py

   $ python hello_world4.py
   Hello World!

