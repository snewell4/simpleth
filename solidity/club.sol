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
 * test cases. I am not testing for overflow/underflow in math. Beware.
 *
 * @custom:simpleth This should appear in docdev for the Contract
 */
contract Club {
    /// @dev address of the club administrator
    address payable public immutable admin;

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

    struct MemberInfo {
        address addr;         // blockchain address for member account
        MStatus status;       // current status
        bytes32 name;         // name of member
        uint duesBalanceWei;  // membership dues owed, in wei
        uint donationsWei;    // donations to club made, in wei
        uint8 attendance;     // count of meetings attended
    }

    /// @dev member records indexed by account address
    mapping(address => MemberInfo) private member;
    
    /// @dev addresses of all member accounts, includes all who have applied
    address[] private members;

    /// @dev membership dues, in wei
    uint constant DUES_WEI = 10 gwei


    /// @notice Guard function that requires user be the admin.
    ///
    /// @dev Used for admin-only transactions.
    ///
    /// @custom:simpleth Here's a custom tag for Method isAdmin()
    modifier isAdmin() {
        require(msg.sender == admin, "must be admin");
        _;
    }

    /// @notice GUARD function to require member be in good standing.
    ///
    /// @dev Used for transactions where member needs to be APPROVED
    /// and have dues paid in full.
    modifier isInGoodStanding() {
        require(
            member[msg.sender].status == MStatus.APPROVED &&
            member[msg.sender].duesBalanceWei == 0,
            "member not in good standing"
        );
        _;
    }

    /// @notice Guard function to require specific member status.
    ///
    /// @dev Used for transactions where a member's status matters.
    modifier isStatus(address _maddr, MStatus _status) {
        require(
            member[_maddr].status == _status,
           "wrong member status"
        );
        _;
    }   


    event AttendanceMarked(
        uint timestamp,
        address[] list,
        address[] marked
    );
    
    event BalanceTransferred(
        uint timestamp,
        address receiver,
        uint amountWei,
        uint clubBalanceWei
    );

    event ClubConstructed(
        uint timestamp,
        address sender,
        string name,
        address club
    );

    event ClubPaid(
        uint timestamp,
        address payer,
        uint amountWei,
        uint clubBalanceWei
    );

    event DonationPaid(
        uint timestamp,
        address member_address,
        uint amount,
        uint donationWei,
        uint clubBalanceWei
    );

    event DuesPaid(
        uint timestamp,
        address member_address,
        uint amount,
        uint duesBalanceWei,
        uint clubBalanceWei
    );

    event MemberApproved(
        uint timestamp,
        address member_address,
        uint duesBalanceWei
    );

    event MemberBanned(
        uint timestamp,
        address member
    );

    event MemberCreated(
        uint timestamp,
        address member,
        bytes32 name
    );

    event MemberRejected(
        uint timestamp,
        address member
    );

    event Trx1Done(
        uint timestamp,
        uint num,
        uint new_num
    );

    event Trx2Called(
        uint timestamp,
        uint new_num
    );

    event Trx2Done(
        uint timestamp,
        uint num
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

    function approveMember(address _maddr)
    public
    isAdmin()
    isStatus(_maddr, MStatus.APPLIED)
    {
        member[_maddr].status = MStatus.APPROVED;
        member[_maddr].duesBalanceWei = DUES_WEI;
        emit MemberApproved(
            block.timestamp,
            _maddr,
            member[_maddr].duesBalanceWei
        );
    }

    function banMember(address _maddr)
    public
    isAdmin()
    isStatus(_maddr, MStatus.APPROVED)
    {
        member[_maddr].status = MStatus.BANNED;
        emit MemberBanned(
            block.timestamp,
            _maddr
        );
    }

    /**
     * @notice Add admin as a member. Done once by constructor().
     *
     * @dev Admin is automatically added as member[0]. Set the member info for
     * the admin.
     */
    function createAdminMember(address _maddr)
    private
    {
        member[_maddr].addr = _maddr;
        member[_maddr].name = "admin";
        member[_maddr].duesBalanceWei = 0;
        member[_maddr].status = MStatus.APPROVED;
        members.push(_maddr);
    }

    function createMember(bytes32 _name)
    public
    isStatus(msg.sender, MStatus.NEW)
    {
        address maddr_ = msg.sender;
        member[maddr_].addr =  maddr_;
        member[maddr_].status = MStatus.APPLIED;
        member[maddr_].name = _name;
        members.push(maddr_);
        emit MemberCreated(
            block.timestamp,
            maddr_,
            _name
        );
    }

    function doTrx1(uint _num)
    public
    {
        uint new_num_ = _num + 100;
        emit Trx2Called(
            block.timestamp,
            new_num_
        );
        doTrx2(new_num_);
        emit Trx1Done(
            block.timestamp,
            _num,
            new_num_
        );
    }

    function doTrx2(uint _num)
    public
    isAdmin
    {
        require(_num > 110, "must be greater than 110");
        emit Trx2Done(
            block.timestamp,
            _num
        );
    }

    /**
     * @notice Get the addresses of all members.
     *
     * @dev This is for efficiency. One call and the entire array is
     * returned for processing instead of making a series of calls for
     * individual addresses.
     *
     * @return address[] of all member addresses
     */
    function getAllMembers()
    public
    view
    isAdmin
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
     * @return allMemberInfo_ array of MemberInfo structs for each address
     * in members[].
     */
    function getAllMemberInfo()
    public
    view
    isAdmin
    returns (MemberInfo[] memory allMemberInfo_)
    {
        uint count_ = members.length;
        allMemberInfo_ = new MemberInfo[](count_);
        for (uint i = 0; i < count_; i++) {
            allMemberInfo_[i] = member[members[i]];
        }
        return allMemberInfo_;
    }

    /**
     * @notice Get the number of bytes this contract takes up on the
     * blockchain.
     *
     * @dev This is intended primarily for development and testing to check
     * on size of this contract.
     *
     * @param _addr Address of the contract.
     *
     * @return size The size of the deployed code in bytes.
     */
    function getContractSize(address _addr)
        public
        view
        returns(uint size)
    {
        assembly { size := extcodesize(_addr) }
        return size;
    }

    /**
     * @notice Get the MemberInfo for sender.
     *
     * @dev Used by APPROVED members to see only their info.
     *
     * @return MemberInfo with sender's info.
     */
    function getMemberInfo()
    public
    view
    isStatus(msg.sender, MStatus.APPROVED)
    returns (MemberInfo memory)
    {
        return member[msg.sender];
    }

     /**
     * @notice Get the min and max integer values for Status enum.
     *
     * @dev This is to try out the new min and max functions as well
     * as returning multiple values plus multiple returns with Natspec.
     *
     * @return min_ smallest integer used in MStatus enum
     * @return max_ largest integer used in MStatus enum
     */
    function getMStatusRange()
    public
    pure
    returns (uint8, uint8)
    {
        uint8 min_ = uint8(type(MStatus).min);
        uint8 max_ = uint8(type(MStatus).max);
        return (min_, max_);
    }
    
    function markAttendance(address[] memory _attendanceList)
    public
    isAdmin
    returns (address[] memory attendanceListMarked_)
    {
        /// @dev count of members in the attendance list (DOES THIS WORK?)
        uint count_ = _attendanceList.length;
        /// @notice index into attendanceListMarked_ (DOES THIS WORK?)
        uint marked_index_ = 0;
        for (uint8 i_ = 0; i_ < count_; i_++) {
            if (member[_attendanceList[count_]].status == MStatus.APPROVED) {
                member[_attendanceList[count_]].attendance =
                  member[_attendanceList[count_]].attendance + 1;
                attendanceListMarked_[marked_index_] =
                    _attendanceList[count_];
                marked_index_ = marked_index_ + 1;
            }
        }
        emit AttendanceMarked(
            block.timestamp,
            _attendanceList,
            attendanceListMarked_
        );
        return attendanceListMarked_;
    }

    function payDues()
    public
    payable
    {
        member[msg.sender].duesBalanceWei =
            member[msg.sender].duesBalanceWei - msg.value;
        emit DuesPaid(
            block.timestamp,
            msg.sender,
            msg.value,
            member[msg.sender].duesBalanceWei,
            address(this).balance
        );
    }

    function payDonation()
    public
    payable
    isInGoodStanding
    {
        member[msg.sender].donationsWei =
            member[msg.sender].donationsWei + msg.value;
        emit DonationPaid(
            block.timestamp,
            msg.sender,
            msg.value,
            member[msg.sender].donationsWei,
            address(this).balance
        );
    }

    receive()
    external
    payable
    {
        emit ClubPaid(
            block.timestamp,
            msg.sender,
            msg.value,
            address(this).balance
        );
    }

    function rejectMember(address _maddr)
    public
    isAdmin()
    isStatus(_maddr, MStatus.APPLIED)
    {
        member[_maddr].status = MStatus.REJECTED;
        emit MemberRejected(
            block.timestamp,
            _maddr
        );
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
    function transferBalance(address payable _receiver, uint _amountWei)
    public
    isAdmin
    {
        require(
            address(this).balance >= _amountWei,
            "insufficient balance"
        );
        _receiver.transfer(_amountWei);
        emit BalanceTransferred(
            block.timestamp,
            _receiver,
            _amountWei,
            address(this).balance
        );
    }
}