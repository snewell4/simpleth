"""Test HelloWorld2 smart contract"""
from simpleth import Blockchain, Contract, Results


def test_HelloWorld2():
    """Deploy HelloWorld2.sol, check for good deploy, call function to get
    the greeting and test it is the expected greeting"""
    c = Contract('HelloWorld2')
    receipt = c.deploy(Blockchain().address(0))
    results = Results(c, receipt)
    greeting = c.call_fcn('getGreeting')
    assert greeting == 'Hello World!' and results.trx_name == 'deploy'
