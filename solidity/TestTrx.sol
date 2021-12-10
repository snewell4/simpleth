pragma solidity ^0.8;
// SPDX-FileCopyrightText: Copyright 2021 Stephen R. Newell
// SPDX-License-Identifier: MIT

/// @title TestTrx
///
/// @author Stephen Newell
///
/// @notice This is only used for unit testing the Python Contract() class.
///
/// @dev All changes must be made with the Python unit tests in mind.
contract TestTrx {
    address public owner;
    uint public specialNum = 42;
    int public initNum;
    uint[3] public nums;
    uint public test_uint;
    int public test_int;
    address public test_addr;
    string public test_str;

    event TestTrxConstructed(
        uint timestamp,
        address indexed sender,
        int initNum,
        address TestTrx
    );

    event NumsStored(
        uint num0,
        uint num1,
        uint num2
    );

    event TypesStored(
        uint test_uint,
        int test_int,
        address test_addr,
        string test_str
    );

    constructor(int _initNum) {
        owner = msg.sender;
        initNum = _initNum;
        emit TestTrxConstructed(
            block.timestamp,
            msg.sender,
            initNum,
            address(this)
    );
    }

    function storeNums(uint _num0, uint _num1, uint _num2)
    public
    {
        nums[0] = _num0;
        nums[1] = _num1;
        nums[2] = _num2;
        emit NumsStored(nums[0], nums[1], nums[2]);
    }

    function storeTypes(
        uint _unum,
        int _inum,
        address _addr,
        string memory _str
    )
    public
    {
        test_uint = _unum;
        test_int = _inum;
        test_addr = _addr;
        test_str = _str;
        emit TypesStored(test_uint, test_int, test_addr, test_str);
    }

    function getNum0() public view returns(uint num) {
        return nums[0];
    }

    function getNum(uint8 index) public view returns(uint num) {
        return nums[index];
    }

    function getNums() public view returns(uint[3] memory) {
        return nums;
    }
}
