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
    string public greeting;

    event HelloWorld4Constructed(
        uint timestamp,
        address sender,
        string initGreeting,
        address HelloWorld4
    );

    event GreetingSet(
        uint timestamp,
        address sender,
        string greeting
    );

    constructor(string memory _initGreeting) {
        greeting = _initGreeting;
        emit HelloWorld4Constructed(
            block.timestamp,
            msg.sender,
            greeting,
            address(this)
        );
    }

    function setGreeting(string memory _greeting) public {
        greeting = _greeting;
        emit GreetingSet(
            block.timestamp,
            msg.sender,
            greeting
        );
    }

    function getGreeting() public view returns (string memory) {
        return greeting;
    }
}
