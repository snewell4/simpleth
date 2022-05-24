.. image:: ../images/contract_separator.png


club
****
:Description: Club Contract

:Purpose:  This is a contrived example of a club and members used to exercise basic functionality of Solidity smart contracts. It is used for integration testing of Python code with simpleth classes.

:Notes:  Be careful in making any changes. Do not break the simpleth test cases. I am not testing for overflow/underflow in math. Beware.

:Author:  Stephen Newell
:simpleth: This should appear in docdev for the Contract


.. image:: ../images/section_separator.png

STATE VARIABLES
^^^^^^^^^^^^^^^

:DUES\_WEI: membership dues, in wei

:admin: address of the club administrator

:member: member records indexed by account address

:members: addresses of all member accounts, includes all who have applied

:name: name of the club



.. image:: ../images/section_separator.png

METHODS
^^^^^^^
getAllMemberInfo()
------------------
:Purpose:  Get the MemberInfo for all members.

:Notes:  This is for efficiency. One call and all info about all members is returned for processing instead of making a series of calls for individual addresses.

**Returns:**

:allMemberInfo\_: array of MemberInfo structs for each address in members[].



________________________________________

getAllMembers()
---------------
:Purpose:  Get the addresses of all members.

:Notes:  This is for efficiency. One call and the entire array is returned for processing instead of making a series of calls for individual addresses.

**Returns:**

:\_0: address[] of all member addresses



________________________________________

getContractSize(address)
------------------------
:Purpose:  Get the number of bytes this contract takes up on the blockchain.

:Notes:  This is intended primarily for development and testing to check on size of this contract.

**Parameters:**

:\_addr: Address of the contract.


**Returns:**

:size: The size of the deployed code in bytes.



________________________________________

getMStatusRange()
-----------------
:Purpose:  Get the min and max integer values for Status enum.

:Notes:  This is to try out the new min and max functions as well as returning multiple values plus multiple returns with Natspec.

**Returns:**

:\_0: min\_ smallest integer used in MStatus enum
:\_1: max\_ largest integer used in MStatus enum



________________________________________

getMemberInfo()
---------------
:Purpose:  Get the MemberInfo for sender.

:Notes:  Used by APPROVED members to see only their info.

**Returns:**

:\_0: MemberInfo with sender's info.



________________________________________

transferBalance(address,uint256)
--------------------------------
:Purpose:  Transfer all Ether out of the contract account and into the drainBalance() sender account.

:Notes:  Use this method to pull Ether out of the contract. It only transfers out all Ether; there is no parameter to specify the amount to withdraw. Guard modifier only allows admin to execute. The Ether withdrawn is transferred into the admin account. A require() will cause drainBalance() to revert if the balance is zero. Emits BalanceDrained().


.. image:: ../images/section_separator.png

EVENTS
^^^^^^
None
