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
 * @title CLS title1           - DOCDEV
 * @title CLS title2           - DOCDEV
 * @author CLS author1         - DOCDEV
 * @author CLS author2         - DOCDEV
 * @notice CLS notice1         - DOCUSER
 * @notice CLS notice2         - DOCUSER
 * @custom:testa  CLS test1 #1 - DOCDEV
 * @custom:testa  CLS test1 #2 - DOCDEV
 * @custom:testb  CLS test2   - DOCDEV
 * @dev CLS dev1               - DOCDEV
 * @dev CLS dev2               - DOCDEV
 */
contract TestNatspec {
    /**
     * @dev VAR dev1           - DOCDEV
     * @dev VAR dev2           - DOCDEV
     */
    uint[3] public nums;

    /// @dev VAR dev          - DOCDEV
    /// @custom:testa  VAR test1 - DOCDEV
    int public specialNum;

    /**
     * @notice EVT notice     - DOCUSER
     * @dev EVT dev           - DOCDEV
     * @custom:testa  EVT test1 - DOCDEV
     * @param num0 EVT param  - DOCDEV
     * @param num1 EVT param  - DOCDEV
     * @param num2 EVT param  - DOCDEV
     */
    event NumsStored(
        uint num0,
        uint num1,
        uint num2
    );

    /**
     * @notice TRX notice1     - DOCUSER
     * @notice TRX notice2     - DOCUSER
     * @dev TRX dev1           - DOCDEV
     * @dev TRX dev2           - DOCDEV
     * @custom:testa  TRX test1 #1 - DOCDEV
     * @custom:testa  TRX test1 #2 - DOCDEV
     * @custom:testb  TRX test2 #1 - DOCDEV
     * @param _num0 TRX param - DOCDEV
     * @param _num1 TRX param - DOCDEV
     * @param _num2 TRX param - DOCDEV
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
