"""Test HelloWorld4 smart contract"""
import pytest

from simpleth import Blockchain, Contract, Results


def test_HelloWorld4_deploy():
    """Deploy HelloWorld4.sol with a greeting string in constructor arg,
    check for good deploy, call function to get that greeting and test
    it is the expected greeting plus check on expected trx names"""
    c = Contract('HelloWorld4')
    u = Blockchain().address(0)
    hello_str = 'Hello World!'
    receipt = c.deploy(u, hello_str)
    results = Results(receipt, c)
    greeting = c.call_fcn('getGreeting')
    assert greeting == hello_str and results.trx_name == 'deploy'


def test_HelloWorld4_setGreeting():
    """Continue with the deployed contract. Run trx to set a new
    greeting, get that greeting, and test it is the expected string"""
    c = Contract('HelloWorld4')
    u = Blockchain().address(0)
    c.connect()
    hello_str = 'Hello Again!'
    receipt = c.run_trx(u, 'setGreeting', hello_str)
    results = Results(receipt, c)
    greeting = c.call_fcn('getGreeting')
    assert greeting == hello_str and results.trx_name == 'setGreeting'
