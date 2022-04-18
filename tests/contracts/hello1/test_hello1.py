"""Test HelloWorld1 smart contract"""
import pytest

from simpleth import Blockchain, Contract, Results

    
def test_HelloWorld1():
    """Deploy HelloWorld1.sol"""
    c = Contract('HelloWorld1')
    receipt = c.deploy(Blockchain().address(0))
    results = Results(receipt, c)
    greeting = c.get_var('greeting')
    assert greeting == 'Hello World!' and results.trx_name == 'deploy'
