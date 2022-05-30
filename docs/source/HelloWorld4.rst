.. image:: ../images/contract_separator.png


HelloWorld4
***********
:Description: HelloWorld4

:Purpose:  Adds an event to the constructor.

:Notes:  Find the greeting in the emitted event.

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



.. image:: ../images/section_separator.png

EVENTS
^^^^^^
HelloWorld4Constructed(uint256,address,string,address)
------------------------------------------------------
:Purpose:  Emitted when contract is constructed


**Parameters:**

:HelloWorld4: address of the newly deployed contract
:initGreeting: constructor arg with a greeting
:sender: address sending the constructor
:timestamp: block time when constructed


