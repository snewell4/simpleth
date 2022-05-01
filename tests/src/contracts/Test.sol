 pragma solidity ^0.8;

// SPDX-FileCopyrightText: Copyright 2021 Stephen R. Newell
// SPDX-License-Identifier: MIT

/**
 *  @title Test Contract
 * 
 *  @author Stephen Newell
 * 
 *  @notice This is used to for testing simpleth methods. It is designed
 *  with very simple transactions, functions, and variables to support
 *  a wide variety of test cases.
 * 
 *  @dev All changes must be made with the Python unit tests in mind. Be
 *  cautious that you do not break anything. See the `tests` directory for
 *  PyTest tests that use this contract.
 */
contract Test {

    /// @dev address that constructed and deployed the contract.
    address public owner;

    /// @dev set by constructor. Has no other purpose.
    int public initNum;

    /// @dev used by the storeNums...() transactions
    uint[3] public nums = [uint(0), 1, 2];

    /// @dev used by sumNums() to hold the sum of nums[].
    uint public numsTotal;

    /// @dev used to store an unsigned integer
    uint public test_uint;

    /// @dev used to store a signed integer
    int public test_int;

    /// @dev used to store an address
    address public test_addr;

    /// @dev used to store a string
    string public test_str;


    /**
     * @notice Emitted when new num1 is stored
     *
     * @param timestamp block time when initNum was updated
     * @param divisor used to divide initNum
     * @param result resulting initNum
     */
    event InitNumDivided(
        uint timestamp,
        int divisor,
        int result
    );

    /**
     * @notice Emitted when num0 is stored
     *
     * @param timestamp block time when nums were updated
     * @param num0 stored in nums[0]
     */
    event Num0Stored(
        uint timestamp,
        uint num0
    );

    /**
     * @notice Emitted when new num1 is stored
     *
     * @param timestamp block time when nums were updated
     * @param num1 stored in nums[1]
     */
    event Num1Stored(
        uint timestamp,
        uint num1
    );

    /**
     * @notice Emitted when new num2 is stored
     *
     * @param timestamp block time when nums were updated
     * @param num2 stored in nums[2]
     */
    event Num2Stored(
        uint timestamp,
        uint num2
    );

    /**
     * @notice Emitted when a selected nums[] is stored
     *
     * @param timestamp block time when nums was updated
     * @param index into nums[]
     * @param num stored in nums[`index`]
     */
    event NumStored(
        uint timestamp,
        uint index,
        uint num
    );

    /**
     * @notice Emitted when new nums are stored
     *
     * @param timestamp block time when nums were updated
     * @param num0 stored in nums[0]
     * @param num1 stored in nums[1]
     * @param num2 stored in nums[2]
     */
    event NumsStored(
        uint timestamp,
        uint num0,
        uint num1,
        uint num2
    );

    /**
     * @notice Emitted when nums were stored and then divided
     *
     * @param timestamp block time after nums[] divided
     */
    event NumsStoredAndDivided(uint timestamp);

    /**
     * @notice Emitted when new nums are stored along with
     * a value (in wei) sent as a payment.
     *
     * @param timestamp block time when nums were updated
     * @param num0 stored in nums[0]
     * @param num1 stored in nums[1]
     * @param num2 stored in nums[2]
     * @param paid amount of wei sent
     * @param balance amount of wei in contract's balance
     */
    event NumsStoredAndPaid(
        uint timestamp,
        uint num0,
        uint num1,
        uint num2,
        uint paid,
        uint balance
    );

    /**
     * @notice Emitted when nums were stored and then summed
     *
     * @param timestamp block time after total was stored
     */
    event NumsStoredAndSummed(uint timestamp);

    /**
     * @notice Emitted when nums[] are divided
     *
     * @param timestamp block time when nums divided
     * @param num0 value in nums[0] after dividing
     * @param num1 value in nums[1] after dividing
     * @param num2 value in nums[2] after dividing
     * @param divisor value used to divide nums[]
     */
    event NumsDivided(
        uint timestamp,
        uint num0,
        uint num1,
        uint num2,
        uint divisor
    );

    /**
     * @notice Emitted when nums[] total is stored
     *
     * @param timestamp block time when total is stored
     * @param num0 value in nums[0]
     * @param num1 value in nums[1]
     * @param num2 value in nums[2]
     * @param total sum of the three nums assigned to numsTotal
     */
    event NumsSummed(
        uint timestamp,
        uint num0,
        uint num1,
        uint num2,
        uint total
    );

    /**
     * @notice Emitted when owner is changed
     *
     * @param timestamp block time when owner was set
     * @param newOwner address of the new owner
     */
    event OwnerSet(
        uint timestamp,
        address newOwner
    );

    /**
     * @notice Emitted when contract address is sent ether
     *
     * @param timestamp block time when paid
     * @param sender address sending the ether
     * @param amount_gwei of ether received (in gwei)
     */
    event Received(
        uint timestamp,
        address sender,
        uint amount_gwei
    );

    /**
     * @notice Emitted when the contract is deployed.
     *
     * @dev Parameters are arbitrary.
     *
     * @param timestamp block time, in epoch seconds, when deployed
     * @param sender becomes the address of owner
     * @param initNum value assigned with constructor()
     * @param Test address of this contract
     */
    event TestConstructed(
        uint timestamp,
        address indexed sender,
        int initNum,
        address Test
    );

    /**
     * @notice Emitted when nums[0] and nums[1] total is stored
     *
     * @param timestamp block time when total is stored
     * @param num0 value in nums[0]
     * @param num1 value in nums[1]
     * @param total sum of the first two nums assigned to numsTotal
     */
    event TwoNumsSummed(
        uint timestamp,
        uint num0,
        uint num1,
        uint total
    );

    /**
     * @notice Emitted when the four different types of variables
     * are stored
     *
     * @param timestamp block time when variables were updated
     * @param test_uint value given to the unsigned integer variable
     * @param test_int value given to the signed integer variable
     * @param test_addr value given to the address variable
     * @param test_str value given to the string variable
     */
    event TypesStored(
        uint timestamp,
        uint test_uint,
        int test_int,
        address test_addr,
        string test_str
    );


    /**
     * @notice Guard function that requires the sender be the Club
     * owner.
     *
     * @dev Used for owner-only transactions.
     */
    modifier isOwner() {
        require(msg.sender == owner, "Must be owner");
        _;
    }


    /**
     * @notice Create a new Test contract on the blockchain.
     *
     * @dev msg.sender becomes contract owner. Emits
     * TestConstructed().
     *
     * @param _initNum value is stored in initNum variable
     */
    constructor(int _initNum) {
        owner = msg.sender;
        initNum = _initNum;
        emit TestConstructed(
            block.timestamp,
            msg.sender,
            initNum,
            address(this)
        );
    }

    /**
     * @notice Divides initNum by a divisor
     *
     * @dev Emits InitNumDivided(). Used to test for divide-by-zero
     * errors by using 0 for divisor and for non-integer results by using
     * 3, or other, for divisor
     *
     * @param _divisor divide initNum by this value
     */
    function divideInitNum(int _divisor)
        public
    {
        initNum = initNum / _divisor;
        emit InitNumDivided(
            block.timestamp,
            _divisor,
            initNum
        );
    }

    /**
     * @notice Divides values in nums[]. There is no test for
     * _divisor being zero. This is used to test a transaction
     * that fails.
     *
     * @dev Emits NumsDivided()
     */
    function divideNums(uint _divisor)
        public
    {
        nums[0] = nums[0] / _divisor;
        nums[1] = nums[1] / _divisor;
        nums[2] = nums[2] / _divisor;
        emit NumsDivided(
            block.timestamp,
            nums[0],
            nums[1],
            nums[2],
            _divisor
        );
    }

    /**
     * @notice Allows current owner to assign a new owner
     *
     * @dev Emits OwnerSet().
     *
     * @param _newOwner address of the account to be the new owner
     */
    function setOwner(address _newOwner)
        public
        isOwner
    {
        owner = _newOwner;
        emit OwnerSet(
            block.timestamp,
            _newOwner
        );
    }

    /**
     * @notice Stores one of the nums[]
     *
     * @dev Emits NumStored(). Used to test for out of bounds
     * errors by giving bad value to `_index`.
     *
     * @param _index selects which nums[]
     * @param _num value to store in nums[`index`]
     */
    function storeNum(uint _index, uint _num)
        public
    {
        nums[_index] = _num;
        emit NumStored(
            block.timestamp,
            _index,
            nums[_index]
        );
    }

    /**
     * @notice Stores the three args in nums[]
     *
     * @dev Emits NumsStored()
     *
     * @param _num0 value to store in nums[0]
     * @param _num1 value to store in nums[1]
     * @param _num2 value to store in nums[2]
     */
    function storeNums(uint _num0, uint _num1, uint _num2)
        public
    {
        nums[0] = _num0;
        nums[1] = _num1;
        nums[2] = _num2;
        emit NumsStored(
            block.timestamp,
            nums[0],
            nums[1],
            nums[2]
        );
    }

    /**
     * @notice Stores the three args in nums[] and call
     * sumNums() to divide nums
     *
     * @dev Used to test calling a function that fails
     *
     * @param _num0 value to store in nums[0]
     * @param _num1 value to store in nums[1]
     * @param _num2 value to store in nums[2]
     * @param _divisor pass to divideNums() to divide
     * the three nums
     */
    function storeNumsAndDivide(
            uint _num0,
            uint _num1,
            uint _num2,
            uint _divisor
        )
        public
    {
        nums[0] = _num0;
        nums[1] = _num1;
        nums[2] = _num2;
        emit NumsStored(
            block.timestamp,
            nums[0],
            nums[1],
            nums[2]
        );
        divideNums(_divisor);
        emit NumsStoredAndDivided(block.timestamp);
    }

    /**
     * @notice Stores the three args in nums[] and accepts a payment.
     *
     * @dev Emits NumsStored()
     *
     * @param _num0 value to store in nums[0]
     * @param _num1 value to store in nums[1]
     * @param _num2 value to store in nums[2]
     */
    function storeNumsAndPay(uint _num0, uint _num1, uint _num2)
        public
        payable
    {
        nums[0] = _num0;
        nums[1] = _num1;
        nums[2] = _num2;
        emit NumsStoredAndPaid(
            block.timestamp,
            nums[0],
            nums[1],
            nums[2],
            msg.value,
            address(this).balance
        );
    }

    /**
     * @notice Stores the three args in nums[] and call
     * sumNums() to sum the nums
     *
     * @dev Emits NumsStored() and NumsStoredAndSummed()
     *
     * @param _num0 value to store in nums[0]
     * @param _num1 value to store in nums[1]
     * @param _num2 value to store in nums[2]
     */
    function storeNumsAndSum(uint _num0, uint _num1, uint _num2)
        public
    {
        nums[0] = _num0;
        nums[1] = _num1;
        nums[2] = _num2;
        emit NumsStored(
            block.timestamp,
            nums[0],
            nums[1],
            nums[2]
        );
        sumNums();
        emit NumsStoredAndSummed(block.timestamp);
    }

    /**
     * @notice Stores the three args in nums[] but does
     * not emit an event.
     *
     * @dev Same as NumsStored() but this transaction
     * does not emit NumsStored()
     *
     * @param _num0 value to store in nums[0]
     * @param _num1 value to store in nums[1]
     * @param _num2 value to store in nums[2]
     */
    function storeNumsWithNoEvent(
        uint _num0,
        uint _num1,
        uint _num2
    )
        public
    {
        nums[0] = _num0;
        nums[1] = _num1;
        nums[2] = _num2;
    }

    /**
     * @notice Stores the three args in nums[] and emits
     * three different events.
     *
     * @dev Same as NumsStored() but this transaction
     * emits Num0Stored(), Num1Stored(), Num2Stored()
     * instead of NumsStored().
     *
     * @param _num0 value to store in nums[0]
     * @param _num1 value to store in nums[1]
     * @param _num2 value to store in nums[2]
     */
    function storeNumsWithThreeEvents(
        uint _num0,
        uint _num1,
        uint _num2
    )
        public
    {
        nums[0] = _num0;
        nums[1] = _num1;
        nums[2] = _num2;
        emit Num0Stored(block.timestamp, nums[0]);
        emit Num1Stored(block.timestamp, nums[1]);
        emit Num2Stored(block.timestamp, nums[2]);
    }

    /**
     * @notice Sums values in nums[] and stores in numsTotal
     *
     * @dev Emits NumsSummed()
     */
    function sumNums()
        public
    {
        numsTotal = nums[0] + nums[1] + nums[2];
        emit NumsSummed(
            block.timestamp,
            nums[0],
            nums[1],
            nums[2],
            numsTotal
        );
    }

    /**
     * @notice Sums values in nums[0] and nums[1] and stores in
     * numsTotal. Required to be owner to call
     *
     * @dev Emits TwoNumsSummed()
     */
    function sumTwoNums()
        public
    {
        require(msg.sender == owner, "must be owner to sum two nums");
        numsTotal = nums[0] + nums[1];
        emit TwoNumsSummed(
            block.timestamp,
            nums[0],
            nums[1],
            numsTotal
        );
    }

    /**
     * @notice Stores a variety of data types into public state
     * variables
     *
     * @dev Emits TypesStored()
     *
     * @param _uint unsigned integer to store in test_uint
     * @param _int signed integer to store into test_int
     * @param _addr address to store into test_addr
     * @param _str string to store into test_str
     */
    function storeTypes(
        uint _uint,
        int _int,
        address _addr,
        string memory _str
    )
        public
    {
        test_uint = _uint;
        test_int = _int;
        test_addr = _addr;
        test_str = _str;
        emit TypesStored(
            block.timestamp,
            test_uint,
            test_int,
            test_addr,
            test_str
        );
    }

    /**
     * @notice Function to return nums[0]
     */
    function getNum0() public view returns(uint num) {
        return nums[0];
    }

    /**
     * @notice Function to return nums[index]
     *
     8 @param index specifies the nums[] entry to return
     */
    function getNum(uint8 index) public view returns(uint num) {
        return nums[index];
    }

    /**
     * @notice Function to return all values in nums[]
     *
     * @dev Returns the three values in a list
     */
    function getNums() public view returns(uint[3] memory) {
        return nums;
    }

    /**
     * @notice Fallback function to make contract payable
     *
     * @dev Adds value sent to contract balance
     */
    receive() external payable {
        emit Received(
            block.timestamp,
            msg.sender,
            msg.value
        );
    }
}
