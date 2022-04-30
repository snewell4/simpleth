from simpleth import Blockchain, Contract, Convert

b = Blockchain()
convert = Convert()

sender = b.address(0)
contract_name = 'HelloWorld4'

c = Contract(contract_name)
deploy_results = c.deploy(sender, 'hello world')
print(f'DETAILS FROM THE TRANSACTION TO DEPLOY {contract_name}')
p.print_trx_results(deploy_results, indent=4)
print()

variable = 'greeting'
print(
    f'GET GREETING FROM THE CONTRACT VARIABLE {variable} '
    f'AS SET BY CONSTRUCTOR.'
    )
greeting = c.get_var(variable)
print(greeting)
print()

trx_name = 'setGreeting'
set_results = c.run_trx(sender, trx_name, 'Hello World!')
print(f'DETAILS FROM THE TRANSACTION {trx_name}.')
p.print_trx_results(set_results, indent=4)
print()

#print(f'DEBUG: trx_results =\n{set_results}')
print(f'CONVERT TIMESTAMP TO LOCAL TIME AND SENDER ADDRESS TO ACCOUNT NUMBER.')
event_args = dict(set_results['event_args'])
timestamp_local = convert.to_local(event_args['timestamp'])
sender_num = convert.to_account_num(event_args['sender'], b.accounts)
print(
    f'    Timestamp converted to local time   = {timestamp_local}\n'
    f'    Account number of sender            = {sender_num}'
    )
print()

fcn_name = 'getGreeting'
greeting = c.call_fcn(fcn_name)
print(f'GET GREETING BY CALLING FUNCTION {fcn_name}.')
print(greeting)
print()

variable = 'greeting'
print(
    f'GET GREETING FROM THE CONTRACT VARIABLE {variable} '
    f'AS SET BY {fcn_name}.'
    )
greeting = c.get_var(variable)
print(greeting)
print()
