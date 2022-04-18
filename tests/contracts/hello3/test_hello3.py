"""Test HelloWorld3 smart contract"""
import pytest

from simpleth import Blockchain, Contract, Results


def test_HelloWorld3():
    """Deploy HelloWorld3.sol, check for good deploy, call function to set
    the greeting, call function to get that greeting and test it is the
    expected greeting plus check on expected trx names"""
    c = Contract('HelloWorld3')
    u = Blockchain().address(0)
    receipt1 = c.deploy(u)
    results1 = Results(receipt1, c)
    hello_str = 'Hello World!!'
    receipt2 = c.run_trx(u, 'setGreeting', hello_str)
    results2 = Results(receipt2, c)
    greeting = c.call_fcn('getGreeting')
    assert greeting == hello_str and \
        results1.trx_name == 'deploy' and \
        results2.trx_name == 'setGreeting'
