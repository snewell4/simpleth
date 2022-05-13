pragma solidity ^0.8;
// SPDX-FileCopyrightText: Copyright 2021 Stephen R. Newell
// SPDX-License-Identifier: MIT

/// @title HelloWorld4
///
/// @author Stephen Newell
///
/// @notice Adding more functionality to the contract saying hello.
///
/// @dev Uses a transaction to set the greeting and a function to return
/// the greeting. This contract includes emitting an event to the log
/// about setting the greeting.

contract HelloWorld4 {
    /// @dev the greeting to display
    string public greeting;

    /**
     * @notice Emitted when contract is constructed
     *
     * @param timestamp block time when constructed
     * @param sender address sending the constructor
     * @param initGreeting constructor arg with a greeting
     * @param HelloWorld4 address of the newly deployed contract
     */
    event HelloWorld4Constructed(
        uint timestamp,
        address sender,
        string initGreeting,
        address HelloWorld4
    );

    /**
     * @notice Emitted when greeting was changed
     *
     * @param timestamp block time when change was changed
     * @param sender address sending in the change
     * @param greeting new greeting
     */
    event GreetingSet(
        uint timestamp,
        address sender,
        string greeting
    );


    /**
     * @notice Create a new HelloWorld4 contract on the blockchain.
     *
     * @dev Emits HelloWord4().
     *
     * @param _initGreeting set as the greeting string
     */
    constructor(string memory _initGreeting) {
        greeting = _initGreeting;
        emit HelloWorld4Constructed(
            block.timestamp,
            msg.sender,
            greeting,
            address(this)
        );
    }

    /**
     * @notice Sets a new greeting
     *
     * @dev Emits GreetingSet()
     *
     * @param _greeting becomes the contract greeting value
     */
    function setGreeting(string memory _greeting) public {
        greeting = _greeting;
        emit GreetingSet(
            block.timestamp,
            msg.sender,
            greeting
        );
    }

    /**
     * @notice Gets greeting
     *
     * @dev Function; not a transaction
     *
     * @return greeting contract greeting value
     */
    function getGreeting() public view returns (string memory) {
        return greeting;
    }
}
