pragma solidity ^0.8;
// SPDX-FileCopyrightText: Copyright 2021 Stephen R. Newell
// SPDX-License-Identifier: MIT

/**
 * @title Club Contract
 *
 * @author Stephen Newell
 *
 * @notice This is a contrived example of a club and members used to
 * exercise basic functionality of Solidity smart contracts. It is used
 * for integration testing of Python code with simpleth classes.
 *
 * @dev Be careful in making any changes. Do not break the simpleth
 * test cases.
 * @dev I am not testing for overflow/underflow in math. Beware.
 */
contract Club {
    /// @dev address of the club administrator
    address payable public admin;

    /// @dev name of the club
    string public name;

    /// @dev club member statuses
    enum MStatus {
        NEW,       // Never applied. Potential applicant.
        APPLIED,   // Has applied for membership
        APPROVED,  // Admin approved. Is a member.
        REJECTED,  // Admin rejected application. Can not apply again.
        BANNED     // Was APPROVED but misbehave. Admin has banned.
    }

    /// @dev club member info record
    struct MemberInfo {
        address addr;          // blockchain address for member account
        MStatus status;        // current status
        string name;           // name of member
        uint16 birth_yr;       // year member was born
        int dues_balance_wei;  // <0 is amount of Ether owed, in wei
                               // >0 is dues credit
    }

    /// @dev member records indexed by account address
    mapping(address => MemberInfo) public member;
    
    /// @dev address[] has the addresses of all users who ever
    /// applied to join.
    address[] public members;

    uint16 private YOUNGEST_AGE = 10;  // minimum age for a member
    uint16 private OLDEST_AGE = 100;   // maximum age for a member
    uint8 private NAME_SIZE = 20;     // maximum number chars in member name
    uint16 private current_year = 2021;  // SN - put in a function

    /// @notice Guard function that requires user be the admin.
    ///
    /// @dev Used for admin-only transactions.
    modifier isAdmin() {
        require(msg.sender == admin, "must be admin");
        _;
    }

    /// @notice Guard function to require specific member status.
    ///
    /// @dev Used for transactions where status value matters.
    modifier isMStatus(address _maddr, MStatus _status) {
        require(isStatus(_maddr, _status), "wrong member status");
        _;
    }   

    event ClubConstructed(
        uint timestamp,
        address indexed sender,
        string name,
        address Club
    );

    event MemberCreated(
        uint timestamp,
        address member,
        string name,
        uint16 birth_yr
    );

    event MemberApproved(
        uint timestamp,
        address member_address,
        int dues_balance_wei
    );

    event MemberRejected(
        uint timestamp,
        address member_address
    );

    event MemberBanned(
        uint timestamp,
        address member_address
    );

    event DuesPaid(
        uint timestamp,
        address member_address,
        uint amount,
        int dues_balance_wei
    );

    event BalanceDrained(
        uint timestamp,
        uint balance
    );

    constructor(string memory _name) {
        admin = payable(msg.sender);
        name = _name;
        createAdminMember(admin);
        emit ClubConstructed(
            block.timestamp,
            msg.sender,
            name,
            address(this)
        );
    }

    /// @notice Use to determine if member has a specific status.
    ///
    /// @dev Intended as a GUARD function for transactions only
    /// permitted to a member with a specific status.
    ///
    /// @param _maddr address of member to check
    /// @param _status status to check
    ///
    /// @return bool True if member has status of _status
    function isStatus(address _maddr, MStatus _status)
    public
    view
    returns (bool)
    {
        return member[_maddr].status == _status;
    }

    /// @notice Use to determine if member is in good standing
    ///
    /// @dev Intended as a GUARD function for transactions only
    /// permitted to active members.
    ///
    /// @dev A member is considered in active when the member is
    /// approved and paid up.  (An active member is also considered
    /// in good standing.)
    ///
    /// @param _maddr address of member to check
    ///
    /// @return bool True if member has status of _status
    function isActive(address _maddr)
    public
    view
    returns (bool)
    {
        return member[_maddr].status == MStatus.APPROVED &&
            member[_maddr].dues_balance_wei > 0;
    }

    function payDues()
    public
    payable
    {
        member[msg.sender].dues_balance_wei =
            member[msg.sender].dues_balance_wei - int256(msg.value);
        emit DuesPaid(
            block.timestamp,
            msg.sender,
            msg.value,
            member[msg.sender].dues_balance_wei
        );
    }

    function createMember(string memory _name, uint16 _birth_yr)
    public
    isMStatus(msg.sender, MStatus.NEW)
    {
        require(getAge(_birth_yr) > YOUNGEST_AGE, "too young");
        require(getAge(_birth_yr) < OLDEST_AGE, "too old");
        require(bytes(_name).length < NAME_SIZE, "too long");
        address maddr_ = msg.sender;
        member[maddr_].addr =  maddr_;
        member[maddr_].status = MStatus.APPLIED;
        member[maddr_].name = _name;
        member[maddr_].birth_yr = _birth_yr;
        members.push(maddr_);
        emit MemberCreated(
            block.timestamp,
            maddr_,
            _name,
            _birth_yr
        );
    }

    function getAge(uint16 _birth_yr)
    private
    view
    returns(uint16 age_)
    {
        age_ = current_year - _birth_yr;
        return age_;
    }

    function setDues(uint16 _birth_yr)
    private
    view
    returns(uint amount)
    {
        if (getAge(_birth_yr) < 18)
            amount = 100000000000;
        else
            amount = 200000000000;
        return amount;
    }

    function approveMember(address _maddr)
    public
    isAdmin()
    isMStatus(_maddr, MStatus.APPLIED)
    {
        member[_maddr].status = MStatus.APPROVED;
        member[_maddr].dues_balance_wei =
            int(setDues(member[_maddr].birth_yr));
        emit MemberApproved(
            block.timestamp,
            _maddr,
            member[_maddr].dues_balance_wei
        );
    }

    function banMember(address _maddr)
    public
    isAdmin()
    isMStatus(_maddr, MStatus.APPROVED)
    {
        member[_maddr].status = MStatus.BANNED;
        emit MemberBanned(
            block.timestamp,
            _maddr
        );
    }

    function rejectMember(address _maddr)
    public
    isAdmin()
    isMStatus(_maddr, MStatus.APPLIED)
    {
        member[_maddr].status = MStatus.REJECTED;
        emit MemberRejected(
            block.timestamp,
            _maddr
        );
    }

    /**
     * @notice Get the addresses of all members.
     *
     * @dev This is for efficiency. One call and the entire array is
     * returned for processing instead of making a series of calls for
     * individual addresses.
     *
     * @return address[] array of all member addresses
     */
    function getAllMembers()
    public
    view
    returns (address[] memory)
    {
        return members;
    }

    /**
     * @notice Get the MemberInfo for all members.
     *
     * @dev This is for efficiency. One call and all info about all members
     * is returned for processing instead of making a series of calls for
     * individual addresses.
     *
     * @return allMemberInfos array of MemberInfo structs for each address
     * in members[].
     */
    function getAllMemberInfos()
    public
    view
    returns (MemberInfo[] memory allMemberInfos)
    {
        uint count = members.length;
        MemberInfo[] memory allMemberInfos_ = new MemberInfo[](count);

        for (uint i = 0; i < count; i++) {
            allMemberInfos_[i] = member[members[i]];
        }

        return allMemberInfos_;
    }

    /**
     * @notice Add admin as a member. Done once by constructor().
     *
     * @dev Admin is automatically added as members[0]. Set the member info for
     * the admin.
     */
    function createAdminMember(address _maddr)
    private
    {
        member[_maddr].addr = _maddr;
        member[_maddr].name = "admin";
        member[_maddr].birth_yr = 0;
        member[_maddr].dues_balance_wei = 0;
        member[_maddr].status = MStatus.APPROVED;
        members.push(_maddr);
    }

    /**
     * @notice Transfer all Ether out of the contract account and into
     * the drainBalance() sender account.
     *
     * @dev Use this method to pull Ether out of the contract. It only
     * transfers out all Ether; there is no parameter to specify the
     * amount to withdraw. Guard modifier only allows admin to execute.
     * The Ether withdrawn is transferred into the admin account. A require()
     * will cause drainBalance() to revert if the balance is zero.
     * Emits BalanceDrained().
     */
    function drainBalance()
    public
    isAdmin
    {
        require(address(this).balance > 0, "can not drain zero balance");
        uint balance_ = address(this).balance;
        admin.transfer(balance_);
        emit BalanceDrained(block.timestamp, balance_);
    }
}