.. image:: ../images/contract_separator.png


HelloWorld4
***********
:Description: HelloWorld4

:Purpose:  Adding more functionality to the contract saying hello.

:Notes:  The constructor sets an initial greeting. Uses a transaction to set the greeting and a function to return the greeting. Emits an event when constructed and another when the greeting is set.

:Author:  Stephen Newell

.. image:: ../images/section_separator.png

STATE VARIABLES
^^^^^^^^^^^^^^^

:greeting: the greeting to display



.. image:: ../images/section_separator.png

METHODS
^^^^^^^
constructor()
-------------
:Purpose:  Create a new HelloWorld4 contract on the blockchain.

:Notes:  Emits HelloWord4().

**Parameters:**

:\_initGreeting: set as the greeting string



________________________________________

getGreeting()
-------------
:Purpose:  Gets greeting

:Notes:  Function; not a transaction

**Returns:**

:greeting\_: contract greeting value



________________________________________

setGreeting(string)
-------------------
:Purpose:  Sets a new greeting

:Notes:  Emits GreetingSet()

**Parameters:**

:\_greeting: becomes the contract greeting value



.. image:: ../images/section_separator.png

EVENTS
^^^^^^
GreetingSet(uint256,address,string)
-----------------------------------
:Purpose:  Emitted when greeting was changed


**Parameters:**

:greeting: new greeting
:sender: address sending in the change
:timestamp: block time when change was changed



________________________________________

HelloWorld4Constructed(uint256,address,string,address)
------------------------------------------------------
:Purpose:  Emitted when contract is constructed


**Parameters:**

:HelloWorld4: address of the newly deployed contract
:initGreeting: constructor arg with a greeting
:sender: address sending the constructor
:timestamp: block time when constructed


