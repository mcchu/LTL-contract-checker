#!/usr/bin/env python
"""Check module defines a check class that links contracts to a pre-defined check type"""

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
        self.contracts = []

    def set_type(self, check_type):
        """Assigns the check type"""
        self.check_type = [x for x in check_types if x == check_type][0]

    def set_contracts(self, contracts):
        """Assigns the contracts associated with the check"""
        self.contracts = contracts

    def __str__(self):
        """Override the print behavior"""
        astr = 'Check: ' + self.check_type + '\n'
        astr += 'Contracts:\n'
        for contract in self.contracts:
            astr += ('  ' + contract.name + '\n')
        return astr

    def __eq__(self, other):
        """Override the default Equals behavior"""
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return False

    def __ne__(self, other):
        """Define a non-equality test"""
        return not self.__eq__(other)
