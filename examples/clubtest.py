from simpleth import Blockchain, Contract
b = Blockchain()
admin = b.accounts[0]
user1 = b.accounts[1]
user2 = b.accounts[2]
c = Contract('Club')
r = c.deploy(admin, 'Club Boffo', constructor_event_name='ClubConstructed')
r=c.run_trx(user1, 'createMember', 'User1', 2004, event_name='MemberCreated')
r=c.run_trx(user2, 'createMember', 'User2', 1970, event_name='MemberCreated')
r = c.run_trx(admin, 'approveMember', user1, event_name='MemberApproved')
r = c.run_trx(admin, 'approveMember', user2, event_name='MemberApproved')
member_infos = c.call_fcn('getAllMemberInfos')
print(f'1) member_infos = {member_infos}')
r = c.run_trx(
    user1,
    'payDues',
    event_name='DuesPaid',
    value_wei=member_infos[1][4]
    )
print(r)
r = c.run_trx(
    user2,
    'payDues',
    event_name='DuesPaid',
    value_wei=member_infos[2][4]
    )
print(r)
member_infos = c.call_fcn('getAllMemberInfos')
print(f'2) member_infos = {member_infos}')
print(f'balance of Club = {b.balance(c.address)}')
print(f'balance of admin = {b.balance(admin)}')
r = c.run_trx(admin, 'drainBalance', event_name='BalanceDrained')
print(r)
print(f'balance of Club = {b.balance(c.address)}')
print(f'balance of admin = {b.balance(admin)}')