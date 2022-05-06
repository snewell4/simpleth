"""Test HelloWorld4 smart contract"""
from simpleth import Blockchain, Contract, Results, EventSearch


def test_HelloWorld4_deploy():
    """Deploy and check constructor arg becomes the greeting"""
    c = Contract('HelloWorld4')
    u = Blockchain().address(0)
    hello_str = 'Hello World 4!'
    receipt = c.deploy(u, hello_str)
    results = Results(c, receipt)
    greeting = c.call_fcn('getGreeting')
    assert greeting == hello_str and results.trx_name == 'deploy'


def test_HelloWorld4_deploy_event():
    """Get the constructor event and check the greeting"""
    c = Contract('HelloWorld4')
    c.connect()
    e = EventSearch(c, 'HelloWorld4Constructed')
    hello_str = 'Hello World 4!'
    events = e.get_old()
    assert events[0]['args']['initGreeting'] == hello_str


def test_HelloWorld4_setGreeting():
    """Run trx to change greeting and check the change was made"""
    c = Contract('HelloWorld4')
    c.connect()
    u = Blockchain().address(0)
    hello_str = 'Hello Again!'
    receipt = c.run_trx(u, 'setGreeting', hello_str)
    results = Results(c, receipt)
    greeting = c.call_fcn('getGreeting')
    assert greeting == hello_str and results.trx_name == 'setGreeting'


def test_HelloWorld4_setGreeting_event():
    """Check for the event with the new greeting"""
    c = Contract('HelloWorld4')
    c.connect()
    e = EventSearch(c, 'GreetingSet')
    hello_str = 'Hello Again!'
    events = e.get_old()
    assert events[0]['args']['greeting'] == hello_str
