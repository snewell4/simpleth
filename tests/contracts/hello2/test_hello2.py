"""Test HelloWorld2 smart contract"""
import pytest

from simpleth import Blockchain, Contract, Results


def test_HelloWorld2():
    """Deploy HelloWorld2.sol, check for good deploy, call function to get
    the greeting and test it is the expected greeting"""
    c = Contract('HelloWorld2')
    receipt = c.deploy(Blockchain().address(0))
    results = Results(receipt, c)
    greeting = c.call_fcn('getGreeting')
    assert greeting == 'Hello World!' and results.trx_name == 'deploy'
