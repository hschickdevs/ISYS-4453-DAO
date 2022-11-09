// SPDX-License-Identifier: MIT
pragma solidity ^0.8.9;

import "@openzeppelin/contracts/governance/Governor.sol";
import "@openzeppelin/contracts/governance/extensions/GovernorCountingSimple.sol";
import "@openzeppelin/contracts/governance/extensions/GovernorVotes.sol";

contract ClassGovernor is Governor, GovernorCountingSimple, GovernorVotes {
    constructor(IVotes _token) Governor("ClassGovernor") GovernorVotes(_token) {}

    function votingDelay() public pure override returns (uint256) {
        return 1; // 1 block
    }

    function votingPeriod() public pure override returns (uint256) {
        return 50400; // 1 week
    }

    function quorum(uint256 blockNumber) public pure override returns (uint256) {
        return 1e18;
    }
}
