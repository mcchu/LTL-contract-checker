#!/usr/bin/env python
"""Check module defines a check class that links contracts to a pre-defined check type"""
from pprint import pprint
from contract import Contract

check_types = ['compatibility', 'consistency']

class Check(object):
    """Check class provides methods for pre-defined check types

    Attributes:
        check: a string type associated with a check
        contracts: a list of contracts associated with a check

    """
    def __init__(self):
        """Initialize a check object"""
        self.check_type = ''
        self.check_contracts = []
        self.contract_names = []

    def set_type(self, check_type):
        """Assigns the check type"""
        self.check_type = [x for x in check_types if x == check_type][0]

    def set_contracts(self, contracts):
        """Assigns the contracts associated with the check"""
        self.check_contracts = contracts
        for contract in contracts:
            self.contract_names.append(contract.name)

    def __str__(self):
        """Override the print behavior"""
        astr = ('\'' + self.contract_names[0] + '\'' + ' ' + self.check_type + ' with ' + '\'' + self.contract_names[1] + '\'' + '\n')
        return astr

    def __eq__(self, other):
        """Override the default Equals behavior"""
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return False

    def __ne__(self, other):
        """Define a non-equality test"""
        return not self.__eq__(other)

class Checks(object):

    def __init__(self):
        self.checks = []

    def add_check(self, check):
        self.checks.append(check)

    def __str__(self):
        """Override the print behavior"""
        astr = '\nCheck the following items:\n'
        for check in self.checks:
            astr += ('\'' + check.contract_names[0] + '\'' + ' ' + check.check_type + ' with ' + '\'' + check.contract_names[1] + '\'' + '\n')
        return astr

    def __eq__(self, other):
        """Override the default Equals behavior"""
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return False

    def __ne__(self, other):
        """Define a non-equality test"""
        return not self.__eq__(other)

