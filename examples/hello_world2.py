from simpleth import Blockchain, Contract

sender = Blockchain().get_address(0)

c = Contract('HelloWorld2')
c.deploy(sender)
greeting = c.call_fcn('getGreeting')

print(greeting)
