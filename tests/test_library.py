#!/usr/bin/env python
"""Test Library module provides a test suite for LTL contract verifier"""

import os
import sys
import unittest
from src.core import parse, generate, run
from src.contract import Contract, Contracts
from src.check import Compatibility, Consistency, Checks

sys.path.append(os.path.join(os.getcwd(), os.path.pardir))

class TestLibrary(unittest.TestCase):
    """TestLibrary class contains method to test LTL contract verifier operations"""

    def test_waiter_customer_model(self):
        """Parse waiter customer model and verify returned contracts and checks objects"""

        # parse waiter customer model
        contracts, checks = parse('tests/waiter_customer.txt')

        # verify waiter contract parsed correctly
        waiter = Contract()
        waiter.add_name('waiter')
        waiter.add_variables([('request', 'FALSE'), ('service', 'FALSE')])
        waiter.add_assumption('TRUE')
        waiter.add_guarantee('((TRUE) -> G(!request -> X !service))')
        waiter.add_guarantee('((TRUE) -> G(request -> X service))')
        self.assertEqual(contracts.get_contract('waiter'), waiter)

        # verify customer contract parsed correctly
        customer = Contract()
        customer.add_name('customer')
        customer.add_variables([('request', 'FALSE'), ('service', 'FALSE')])
        customer.add_assumption('TRUE')
        customer.add_guarantee('((TRUE) -> (F request))')
        customer.add_guarantee('((TRUE) -> G((request & !service) -> X request))')
        customer.add_guarantee('((TRUE) -> G(service -> X !request))')
        self.assertEqual(contracts.get_contract('customer'), customer)

        # verify all contracts have been parsed
        test_contracts = Contracts()
        test_contracts.add_contract(waiter)
        test_contracts.add_contract(customer)
        self.assertEqual(test_contracts, contracts)

        # verify compatibility check
        compatibility = Compatibility('composition')
        compatibility.set_contracts([waiter, customer])
        self.assertEqual(compatibility, checks.checks[0])

        # verify consistency check
        consistency = Consistency('composition')
        consistency.set_contracts([waiter, customer])
        self.assertEqual(consistency, checks.checks[1])

        # verify all checks have been parsed correctly
        test_checks = Checks()
        test_checks.add_check(compatibility)
        test_checks.add_check(consistency)
        self.assertEqual(test_checks, checks)

    def test_checks(self):
        """Runs the program and outputs status of the LTL statements"""

        # parse waiter customer model
        contracts, checks = parse('tests/waiter_customer.txt')
        #run(cont)
