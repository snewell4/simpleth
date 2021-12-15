pragma solidity ^0.8;
// SPDX-FileCopyrightText: Copyright 2021 Stephen R. Newell
// SPDX-License-Identifier: MIT

//
// This contract shows the valid Natspec comments for various types.
// Only the Natspec comments for the following are processed by the
// solc compiler:
//     contract
//     public state variable
//     public function
//
// The solc compiler will place the processed comments in either:
//     <contract>.docdev
//     <contract>.docuser
// Each comment shows the destination file: DOCDEV or DOCUSER
// Each comment shows the destination file: DOCDEV or DOCUSER
//
// Note that modifiers are not processed for Natspec comments.
//
// The printSolDoc.py command will process the .docdev and .docdev
// files to create documentation.
//

/**
 * @title CLS title           - DOCDEV
 * @author CLS author         - DOCDEV
 * @notice CLS notice         - DOCUSER
 * @dev CLS dev               - DOCDEV
 */
contract TestNatspec {
    /**
     * @dev VAR dev           - DOCDEV
     */
    uint[3] public nums;

    /// @dev VAR dev          - DOCDEV
    int public specialNum;

    /**
     * @notice EVT notice     - DOCUSER
     * @dev EVT dev           - DOCDEV
     * @param num0 EVT param  - DOCDEV
     */
    event NumsStored(
        uint num0,
        uint num1,
        uint num2
    );

    /**
     * @notice TRX notice     - DOCUSER
     * @dev TRX dev           - DOCDEV
     * @param _num0 TRX param - DOCDEV
     */
    function storeNums(uint _num0, uint _num1, uint _num2)
    public
    {
        nums[0] = _num0;
        nums[1] = _num1;
        nums[2] = _num2;
        emit NumsStored(nums[0], nums[1], nums[2]);
    }

    /**
     * @notice FCN notice     - DOCUSER
     * @dev FCN dev           - DOCDEV
     * @param index FCN param - DOCDEV
     * @return num FCN return - DOCDEV
     */
    function getNum(uint8 index) public view returns(uint num)
    {
        return nums[index];
    }
}
