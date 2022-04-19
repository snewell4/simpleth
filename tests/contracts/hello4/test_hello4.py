"""Test HelloWorld4 smart contract"""
import pytest

from simpleth import Blockchain, Contract, Results, Filter


def test_HelloWorld4_deploy():
    """Deploy HelloWorld4.sol with a greeting string in constructor arg,
    check for good deploy, call function to get that greeting and test
    it is the expected greeting."""
    c = Contract('HelloWorld4')
    u = Blockchain().address(0)
    f = Filter(c)
    hello_str = 'Hello World!'
    receipt = c.deploy(u, hello_str)
    results = Results(receipt, c)
    greeting = c.call_fcn('getGreeting')
    assert greeting == hello_str and results.trx_name == 'deploy'


def test_HelloWorld4_setGreeting():
    """Continue with the deployed contract. Run trx to set a new
    greeting, get that greeting, test it is the expected string,
    and check event emitted with the greeting."""
    c = Contract('HelloWorld4')
    u = Blockchain().address(0)
    c.connect()
    f = Filter(c)
    hello_str = 'Hello Again!'
    n_blocks = 1       # look at last block mined for constructor event
    receipt = c.run_trx(u, 'setGreeting', hello_str)
    results = Results(receipt, c)
    greeting = c.call_fcn('getGreeting')
    event = f.get_old_events('GreetingSet', n_blocks)
    assert greeting == hello_str and \
        results.trx_name == 'setGreeting' and \
        event[0]['args']['greeting'] == hello_str

