pragma solidity ^0.8;
// SPDX-FileCopyrightText: Copyright 2021 Stephen R. Newell
// SPDX-License-Identifier: MIT

/**
 * @title TestNeverDeployed
 *
 * @author Stephen Newell
 *
 * @notice Used with PyTest test cases that attempt to use a contract
 * without doing a connect().  This contract should never be deployed.
 *
 * @dev For test use, this contract should be compiled but should not
 * have a address file (`.addr`) in the `artifacts` directory.
 */
contract TestNeverDeployed {
    string public text = "I should never get deployed";

    function setText(string memory _text) public {
        text = _text;
    }
}