pragma solidity ^0.8;
// SPDX-FileCopyrightText: Copyright 2021 Stephen R. Newell
// SPDX-License-Identifier: MIT

/// @title HelloWorld3
///
/// @author Stephen Newell
///
/// @notice A more complex contract to say hello to the world.
///
/// @dev Uses a transaction to set the greeting and a function to return
/// the greeting.
contract HelloWorld3 {
    string public greeting;

    function setGreeting(string memory _greeting) public {
        greeting = _greeting;
    }

    function getGreeting() public view returns (string memory) {
        return greeting;
    }
}
