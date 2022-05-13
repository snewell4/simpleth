.. image:: ../images/contract_separator.png


Test
====
:Description: Test Contract 

:Purpose:  This is used to for testing simpleth methods. It is designed  with very simple transactions, functions, and variables to support  a wide variety of test cases. 

:Notes:  All changes must be made with the Python unit tests in mind. Be  cautious that you do not break anything. See the `tests` directory for  PyTest tests that use this contract.

:Author:  Stephen Newell 

.. image:: ../images/section_separator.png

STATE VARIABLES
###############

:initNum: set by constructor. Has no other purpose.

:nums: used by the storeNums...() transactions

:numsTotal: used by sumNums() to hold the sum of nums[].

:owner: address that constructed and deployed the contract.

:testAddr: used to store an address

:testArray: used to store an array

:testBool: used to store a boolean

:testInt: used to store a signed integer

:testStr: used to store a string

:testUint: used to store an unsigned integer



.. image:: ../images/section_separator.png

METHODS
#######
constructor()
-------------
:Purpose:  Create a new Test contract on the blockchain.

:Notes:  msg.sender becomes contract owner. Emits TestConstructed().

**Parameters:**

:\_initNum: value is stored in initNum variable



________________________________________

assertGreaterThan10(int256)
---------------------------
:Purpose:  Allows test of assert()

:Notes:  If _value <= 10, assert will fail and pass back a message.

**Parameters:**

:\_value: only used in assert() test. Greater than 10 passes assert(). 10, or less, fails assert().



________________________________________

destroy(address)
----------------
:Purpose:  Destroy the deployed test contract. Make it unusable.

:Notes:  This is irreversible. Once destroyed, a contract is still on the blockchain and transactions can be sent to it, but they will not have any effect. Any ether in the contract's balance is sent to _to. After a contract is destroyed, its either is inaccessible. Emits Destroyed event. Must be owner to use.

**Parameters:**

:\_to: address to receive contract's ether balance



________________________________________

divideInitNum(int256)
---------------------
:Purpose:  Divides initNum by a divisor

:Notes:  Emits InitNumDivided(). Used to test for divide-by-zero errors by using 0 for divisor and for non-integer results by using 3, or other, for divisor

**Parameters:**

:\_divisor: divide initNum by this value



________________________________________

divideNums(uint256)
-------------------
:Purpose:  Divides values in nums[]. There is no test for _divisor being zero. This is used to test a transaction that fails.

:Notes:  Emits NumsDivided()


________________________________________

getNum(uint8)
-------------
:Purpose:  Function to return nums[index]

**Parameters:**

:index: specifies the nums[] entry to return



________________________________________

getNum0()
---------
:Purpose:  Function to return nums[0]


________________________________________

getNums()
---------
:Purpose:  Function to return all values in nums[]

:Notes:  Returns the three values in a list


________________________________________

revertTransaction()
-------------------
:Purpose:  Allows test of revert()

:Notes:  Always reverts. No event emitted. Passes back a message.


________________________________________

setOwner(address)
-----------------
:Purpose:  Allows current owner to assign a new owner

:Notes:  Emits OwnerSet().

**Parameters:**

:\_newOwner: address of the account to be the new owner



________________________________________

storeNum(uint256,uint256)
-------------------------
:Purpose:  Stores one of the nums[]

:Notes:  Emits NumStored(). Used to test for out of bounds errors by giving bad value to `_index`.

**Parameters:**

:\_index: selects which nums[]
:\_num: value to store in nums[`index`]



________________________________________

storeNums(uint256,uint256,uint256)
----------------------------------
:Purpose:  Stores the three args in nums[]

:Notes:  Emits NumsStored()

**Parameters:**

:\_num0: value to store in nums[0]
:\_num1: value to store in nums[1]
:\_num2: value to store in nums[2]



________________________________________

storeNumsAndDivide(uint256,uint256,uint256,uint256)
---------------------------------------------------
:Purpose:  Stores the three args in nums[] and call sumNums() to divide nums

:Notes:  Used to test calling a function that fails

**Parameters:**

:\_divisor: pass to divideNums() to divide the three nums
:\_num0: value to store in nums[0]
:\_num1: value to store in nums[1]
:\_num2: value to store in nums[2]



________________________________________

storeNumsAndPay(uint256,uint256,uint256)
----------------------------------------
:Purpose:  Stores the three args in nums[] and accepts a payment.

:Notes:  Emits NumsStored()

**Parameters:**

:\_num0: value to store in nums[0]
:\_num1: value to store in nums[1]
:\_num2: value to store in nums[2]



________________________________________

storeNumsAndSum(uint256,uint256,uint256)
----------------------------------------
:Purpose:  Stores the three args in nums[] and call sumNums() to sum the nums

:Notes:  Emits NumsStored() and NumsStoredAndSummed()

**Parameters:**

:\_num0: value to store in nums[0]
:\_num1: value to store in nums[1]
:\_num2: value to store in nums[2]



________________________________________

storeNumsWithNoEvent(uint256,uint256,uint256)
---------------------------------------------
:Purpose:  Stores the three args in nums[] but does not emit an event.

:Notes:  Same as NumsStored() but this transaction does not emit NumsStored()

**Parameters:**

:\_num0: value to store in nums[0]
:\_num1: value to store in nums[1]
:\_num2: value to store in nums[2]



________________________________________

storeNumsWithThreeEvents(uint256,uint256,uint256)
-------------------------------------------------
:Purpose:  Stores the three args in nums[] and emits three different events.

:Notes:  Same as NumsStored() but this transaction emits Num0Stored(), Num1Stored(), Num2Stored() instead of NumsStored().

**Parameters:**

:\_num0: value to store in nums[0]
:\_num1: value to store in nums[1]
:\_num2: value to store in nums[2]



________________________________________

storeTypes(bool,uint8,uint256,int256,address,string,uint256[3])
---------------------------------------------------------------
:Purpose:  Stores a variety of data types into public state variables

:Notes:  Emits TypesStored()

**Parameters:**

:\_addr: address to store into testAddr
:\_array: array of three unsigned integers to store in testArray
:\_bool: boolean to store in testBool
:\_enum: enumerated Size to store in testEnum
:\_int: signed integer to store into testUnt
:\_str: string to store into testStr
:\_uint: unsigned integer to store in testUint



________________________________________

sumNums()
---------
:Purpose:  Sums values in nums[] and stores in numsTotal

:Notes:  Emits NumsSummed()


________________________________________

sumTwoNums()
------------
:Purpose:  Sums values in nums[0] and nums[1] and stores in numsTotal. Required to be owner to call

:Notes:  Emits TwoNumsSummed()


.. image:: ../images/section_separator.png

EVENTS
######
Destroyed(uint256,uint256)
--------------------------
:Purpose:  Emitted when contract is destroyed


**Parameters:**

:amountGwei: contract's ether balance sent to owner
:timestamp: block time when paid



________________________________________

InitNumDivided(uint256,int256,int256)
-------------------------------------
:Purpose:  Emitted when new num1 is stored


**Parameters:**

:divisor: used to divide initNum
:result: resulting initNum
:timestamp: block time when initNum was updated



________________________________________

Num0Stored(uint256,uint256)
---------------------------
:Purpose:  Emitted when num0 is stored


**Parameters:**

:num0: stored in nums[0]
:timestamp: block time when nums were updated



________________________________________

Num1Stored(uint256,uint256)
---------------------------
:Purpose:  Emitted when new num1 is stored


**Parameters:**

:num1: stored in nums[1]
:timestamp: block time when nums were updated



________________________________________

Num2Stored(uint256,uint256)
---------------------------
:Purpose:  Emitted when new num2 is stored


**Parameters:**

:num2: stored in nums[2]
:timestamp: block time when nums were updated



________________________________________

NumStored(uint256,uint256,uint256)
----------------------------------
:Purpose:  Emitted when a selected nums[] is stored


**Parameters:**

:index: into nums[]
:num: stored in nums[`index`]
:timestamp: block time when nums was updated



________________________________________

NumsDivided(uint256,uint256,uint256,uint256,uint256)
----------------------------------------------------
:Purpose:  Emitted when nums[] are divided


**Parameters:**

:divisor: value used to divide nums[]
:num0: value in nums[0] after dividing
:num1: value in nums[1] after dividing
:num2: value in nums[2] after dividing
:timestamp: block time when nums divided



________________________________________

NumsStored(uint256,uint256,uint256,uint256)
-------------------------------------------
:Purpose:  Emitted when new nums are stored


**Parameters:**

:num0: stored in nums[0]
:num1: stored in nums[1]
:num2: stored in nums[2]
:timestamp: block time when nums were updated



________________________________________

NumsStoredAndDivided(uint256)
-----------------------------
:Purpose:  Emitted when nums were stored and then divided


**Parameters:**

:timestamp: block time after nums[] divided



________________________________________

NumsStoredAndPaid(uint256,uint256,uint256,uint256,uint256,uint256)
------------------------------------------------------------------
:Purpose:  Emitted when new nums are stored along with a value (in wei) sent as a payment.


**Parameters:**

:balance: amount of wei in contract's balance
:num0: stored in nums[0]
:num1: stored in nums[1]
:num2: stored in nums[2]
:paid: amount of wei sent
:timestamp: block time when nums were updated



________________________________________

NumsStoredAndSummed(uint256)
----------------------------
:Purpose:  Emitted when nums were stored and then summed


**Parameters:**

:timestamp: block time after total was stored



________________________________________

NumsSummed(uint256,uint256,uint256,uint256,uint256)
---------------------------------------------------
:Purpose:  Emitted when nums[] total is stored


**Parameters:**

:num0: value in nums[0]
:num1: value in nums[1]
:num2: value in nums[2]
:timestamp: block time when total is stored
:total: sum of the three nums assigned to numsTotal



________________________________________

OwnerSet(uint256,address)
-------------------------
:Purpose:  Emitted when owner is changed


**Parameters:**

:newOwner: address of the new owner
:timestamp: block time when owner was set



________________________________________

Received(uint256,address,uint256)
---------------------------------
:Purpose:  Emitted when contract address is sent ether


**Parameters:**

:amountGwei: of ether received (in gwei)
:sender: address sending the ether
:timestamp: block time when paid



________________________________________

TestConstructed(uint256,address,int256,address)
-----------------------------------------------
:Purpose:  Emitted when the contract is deployed.

:Notes:  Parameters are arbitrary.


**Parameters:**

:Test: address of this contract
:initNum: value assigned with constructor()
:sender: becomes the address of owner
:timestamp: block time, in epoch seconds, when deployed



________________________________________

TwoNumsSummed(uint256,uint256,uint256,uint256)
----------------------------------------------
:Purpose:  Emitted when nums[0] and nums[1] total is stored


**Parameters:**

:num0: value in nums[0]
:num1: value in nums[1]
:timestamp: block time when total is stored
:total: sum of the first two nums assigned to numsTotal



________________________________________

TypesStored(uint256,bool,uint8,uint256,int256,address,string,uint256[3])
------------------------------------------------------------------------
:Purpose:  Emitted when the four different types of variables are stored


**Parameters:**

:testAddr: value given to the address variable
:testArray: values given to the array
:testBool: value given to the boolean variable
:testEnum: value given to the enumerated variable
:testInt: value given to the signed integer variable
:testStr: value given to the string variable
:testUint: value given to the unsigned integer variable
:timestamp: block time when variables were updated


