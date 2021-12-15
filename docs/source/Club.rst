**Description:** Club Contract

**Purpose:**  This is a contrived example of a club and members used to exercise basic functionality of Solidity smart contracts. It is used for integration testing of Python code with simpleth classes.

**Notes:**  Be careful in making any changes. Do not break the simpleth test cases.I am not testing for overflow/underflow in math. Beware.

**Author:**  Stephen Newell

________________________________________________________________________________

State Variables
---------------

+------------+--------------------------------------------------------------------------------------------------------------------+
|  Name      |  Comment                                                                                                           |
+------------+--------------------------------------------------------------------------------------------------------------------+
|  DUES_WEI  |  membership dues, in wei                                                                                           |
+------------+--------------------------------------------------------------------------------------------------------------------+
|  admin     |  address of the club administrator                                                                                 |
+------------+--------------------------------------------------------------------------------------------------------------------+
|  member    |  member records indexed by account address                                                                         |
+------------+--------------------------------------------------------------------------------------------------------------------+
|  members   |  addresses of all member accounts, includes all who have applied                                                   |
+------------+--------------------------------------------------------------------------------------------------------------------+
|  name      |  name of the club string can not be immutable (I could change to bytes32) DOES THIS WORK AND SHOW UP AS A NOTICE?  |
+------------+--------------------------------------------------------------------------------------------------------------------+


________________________________________________________________________________

Methods
-------


getAllMemberInfo()
^^^^^^^^^^^^^^^^^^
**Purpose:**  Get the MemberInfo for all members.

**Notes:**  This is for efficiency. One call and all info about all members is returned for processing instead of making a series of calls for individual addresses.


**Returns:**

+------------------+--------------------------------------------------------------+
|  Name            |  Description                                                 |
+------------------+--------------------------------------------------------------+
|  allMemberInfo_  |  array of MemberInfo structs for each address in members[].  |
+------------------+--------------------------------------------------------------+


getAllMembers()
^^^^^^^^^^^^^^^
**Purpose:**  Get the addresses of all members.

**Notes:**  This is for efficiency. One call and the entire array is returned for processing instead of making a series of calls for individual addresses.


**Returns:**

+--------+-------------------------------------+
|  Name  |  Description                        |
+--------+-------------------------------------+
|  _0    |  address[] of all member addresses  |
+--------+-------------------------------------+


getContractSize(address)
^^^^^^^^^^^^^^^^^^^^^^^^
**Purpose:**  Get the number of bytes this contract takes up on the blockchain.

**Notes:**  This is intended primarily for development and testing to check on size of this contract.


**Parameters:**

+---------+----------------------------+
|  Name   |  Description               |
+---------+----------------------------+
|  _addr  |  Address of the contract.  |
+---------+----------------------------+



**Returns:**

+--------+-------------------------------------------+
|  Name  |  Description                              |
+--------+-------------------------------------------+
|  size  |  The size of the deployed code in bytes.  |
+--------+-------------------------------------------+


getMStatusRange()
^^^^^^^^^^^^^^^^^
**Purpose:**  Get the min and max integer values for Status enum.

**Notes:**  This is to try out the new min and max functions as well


**Returns:**

+--------+-----------------------------------------------------------------+
|  Name  |  Description                                                    |
+--------+-----------------------------------------------------------------+
|  _0    |  Natspec.                                                       |
+--------+-----------------------------------------------------------------+
|  _1    |  min_, max_ smallest and largest integers used in MStatus enum  |
+--------+-----------------------------------------------------------------+


getMemberInfo()
^^^^^^^^^^^^^^^
**Purpose:**  Get the MemberInfo for sender.

**Notes:**  Used by APPROVED members to see only their info.


**Returns:**

+--------+----------------------------------+
|  Name  |  Description                     |
+--------+----------------------------------+
|  _0    |  MemberInfo with sender's info.  |
+--------+----------------------------------+


transferBalance(address,uint256)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
**Purpose:**  Transfer all Ether out of the contract account and into the drainBalance() sender account.

**Notes:**  Use this method to pull Ether out of the contract. It only transfers out all Ether; there is no parameter to specify the amount to withdraw. Guard modifier only allows admin to execute. The Ether withdrawn is transferred into the admin account. A require() will cause drainBalance() to revert if the balance is zero. Emits BalanceDrained().


________________________________________________________________________________

