.. image:: ../images/contract_separator.png


TestNeverDeployed
*****************
:Description: TestNeverDeployed

:Purpose:  Used with PyTest test cases that attempt to use a contract without doing a connect().  This contract should never be deployed.

:Notes:  For test use, this contract should be compiled but should not have a address file (`.addr`) in the `artifacts` directory.

:Author:  Stephen Newell

.. image:: ../images/section_separator.png

STATE VARIABLES
^^^^^^^^^^^^^^^

:text: state variable to use with a Contract().get\_var()



.. image:: ../images/section_separator.png

METHODS
^^^^^^^
setText(string)
---------------
:Purpose:  Update contract text variable

:Notes:  Should never be called since contract does not deploy.

**Parameters:**

:\_text: becomes the contract text value.



.. image:: ../images/section_separator.png

EVENTS
^^^^^^
None
