#!/usr/bin/env python
"""Check module defines a check class that links contracts to a pre-defined check type"""
from collections import OrderedDict
import src.operations as ops

class Check(object):
    """Check class is a base class for predefined check types

    Attributes:
        check_type: a string type associated with a check
        contracts: an ordered dictionary of contracts associated with a check
    """
    def __init__(self, contracts=None):
        """Initialize a check object"""
        self.check_type = ''
        if isinstance(contracts, list):
            self.contracts = OrderedDict([(contract.name, contract) for contract in contracts])
        else:
            self.contracts = OrderedDict()

    def set_contracts(self, contracts):
        """Replaces all contracts in the check contracts attribute

        Args:
            contracts: an array of contract objects
        """
        self.contracts.clear()
        for contract in contracts:
            self.add_contract(contract)

    def add_contract(self, contract):
        """Adds a contract to the check contracts attribute

        Args:
            contract: a contract object
        """
        self.contracts[contract.name] = contract

    def get_contract(self, name):
        """Get a specific contract associated with the check

        Args:
            name: a string name of a contract

        Returns:
            A contract object with the specified name
        """
        return self.contracts[name]

    def __str__(self):
        """Override the print behavior"""
        astr = self.check_type + ': [ '
        for contract in self.contracts.values():
            astr += contract.name + ', '
        return astr[:-2] + ' ]'

    def __eq__(self, other):
        """Override the default Equals behavior"""
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return False

    def __ne__(self, other):
        """Define a non-equality test"""
        return not self.__eq__(other)

class Compatibility(Check):
    """Compatibility is a subclass of check for the compatibility check type

    Attributes:
        check_type: a string containing the compatibility check type
        comp_type: a string containing the type of compatibility check
        contracts (inherited): an ordered dictionary of contracts associated with a check
    """
    def __init__(self, comp_type='', contracts=None):
        """Initialize a compatibility check object"""
        super(Compatibility, self).__init__(contracts)
        self.check_type = 'compatibility'
        self.comp_type = comp_type

    def get_ltl(self):
        """Returns the LTL statement for the compatibility of two contracts"""
        # (TODO) remove hard-coded contract parameters
        if self.comp_type == 'composition':
            contract = ops.composition(self.contracts.values()[0], self.contracts.values()[1])
        else:
            contract = ops.conjunction(self.contracts.values()[0], self.contracts.values()[1])
        return ops.compatibility(contract)

    def __str__(self):
        """Override the print behavior"""
        astr = self.check_type + ': {\n'
        astr += '  type : ' + self.comp_type + '\n'
        astr += '  contracts: ['
        for contract in self.contracts.values():
            astr += contract.name + ', '
        return astr[:-2] + ']\n}'

class Consistency(Check):
    """Consistency is a subclass of check for the consistency check type

    Attributes:
        check_type: a string containing the consistency check type
        contracts (inherited): an ordered dictionary of contracts associated with a check
    """
    def __init__(self, cons_type='', contracts=None):
        """Initialize a consistency check object"""
        super(Consistency, self).__init__(contracts)
        self.check_type = 'consistency'
        self.cons_type = cons_type

    def get_ltl(self):
        """Returns the LTL statement for the consistency of two contracts"""
        # (TODO) remove hard-coded contract parameters
        if self.cons_type == 'composition':
            contract = ops.composition(self.contracts.values()[0], self.contracts.values()[1])
        else:
            contract = ops.conjunction(self.contracts.values()[0], self.contracts.values()[1])
        return ops.consistency(contract)

    def __str__(self):
        """Override the print behavior"""
        astr = self.check_type + ': {\n'
        astr += '  type : ' + self.cons_type + '\n'
        astr += '  contracts: ['
        for contract in self.contracts.values():
            astr += contract.name + ', '
        return astr[:-2] + ']\n}'

class Refinement(Check):
    """Refinement is a subclass of check for the refinement check type

    """
    def __init__(self, contracts=None):
        """Initialize a refinement check object"""
        super(Refinement, self).__init__(contracts)
        self.check_type = 'refinement'

    def get_ltl(self):
        """Returns the LTL statement to check if contract_a refines contract_b"""
        # (TODO) remove hard-coded contract parameters
        return ops.refinement(self.contracts.values()[0], self.contracts.values()[1])

    def __str__(self):
        """Override the print behavior"""
        astr = self.check_type + ': {\n'
        astr += '  contracts: ['
        for contract in self.contracts.values():
            astr += contract.name + ', '
        return astr[:-2] + ']\n}'

class Checks(object):
    """Checks is a class that stores all the check objects associated with a system

    Attributes:
        checks: a list of check objects
    """
    def __init__(self):
        """Initialize a checks object"""
        self.checks = []

    def add_check(self, check):
        """Add a check to the checks object

        Args:
            check: a check object
        """
        self.checks.append(check)

    def __str__(self):
        """Override the print behavior"""
        astr = '[\n'
        for check in self.checks:
            astr += '  ' + (check.check_type + ': [ ')
            for contract in check.contracts.values():
                astr += contract.name + ', '
            astr = astr[:-2] + ' ],\n'
        return astr[:-2] + '\n]'

    def __eq__(self, other):
        """Override the default Equals behavior"""
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return False

    def __ne__(self, other):
        """Define a non-equality test"""
        return not self.__eq__(other)
