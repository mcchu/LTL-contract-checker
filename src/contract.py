#!/usr/bin/env python
"""Contract module defines a contract class to store contract data attributes and a contracts class
to store all system contracts and overall system alphabet"""

from collections import OrderedDict

class Contract(object):
    """Contract class stores data attributes of a contract

    Attributes:
        name: a string name for the contract
        variables: a list of tuples containing string variables and initial values
        assumptions: a list of string relations assumed by contract
        guarantees: a list of string relations guaranteed by contract
    """
    def __init__(self):
        """Initialize a contract object"""
        self.name = ''
        self.variables = []
        self.assumptions = []
        self.guarantees = []

    def add_name(self, name):
        """Assigns the contract a name

        Args:
            name: a string name for the contract
        """
        self.name = name

    def add_variable(self, variable):
        """Adds a variable to the contract variables

        Args:
            variable: a tuple containing a variable and initial value
        """
        self.variables.append(variable)

    def add_variables(self, variables):
        """Adds a list of variables to the contract variables

        Args:
            variables: a list of tuples containing variables and initial values
        """
        for variable in variables:
            self.variables.append(variable)

    def add_assumption(self, assumption):
        """Adds an assumption to the contract assumptions

        Args:
            assumption: a string assumption
        """
        self.assumptions.append(assumption)

    def add_guarantee(self, guarantee):
        """Adds a guarantee to the contract guarantees

        Args:
            guarantee: a string guarantee
        """
        self.guarantees.append(guarantee)

    def get_assumptions(self):
        """Get a concatenated string of all assumptions

        Returns:
            A parenthesized, concatenated string of assumptions
        """
        assumptions = [assumption + ' & ' for assumption in self.assumptions]
        return '(' + ''.join(assumptions)[:-3] + ')'

    def get_guarantees(self):
        """Get a concatenated string of all guarantees

        Returns:
            A parenthesized, concatenated string of guarantees
        """
        guarantees = [guarantee + ' & ' for guarantee in self.guarantees]
        return '(' + ''.join(guarantees)[:-3] + ')'

    def saturate_guarantees(self):
        """Helper function that saturates each guarantee with contract assumptions"""
        assumptions = self.get_assumptions()
        self.guarantees = ['(' + assumptions + ' -> ' +
                           guarantee + ')' for guarantee in self.guarantees]

    def __str__(self):
        """Override the print behavior"""
        astr = '[\n  name: [ ' + self.name + ' ]\n'
        astr += '  variables: [ '
        for var, init in self.variables:
            astr += '(' + var + ' := ' + init + '), '
        astr = astr[:-2] + ' ]\n  assumptions: [ '
        for assumption in self.assumptions:
            astr += assumption + ', '
        astr = astr[:-2] + ' ]\n  guarantees: [ '
        for guarantee in self.guarantees:
            astr += guarantee + ', '
        return astr[:-2] + ' ]\n]'

    def __eq__(self, other):
        """Override the default Equals behavior"""
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return False

    def __ne__(self, other):
        """Define a non-equality test"""
        return not self.__eq__(other)

class Contracts(object):
    """Contracts class stores all contracts for a system and the shared alphabet

    Attributes:
        contracts: a list of contract objects
        alphabet: a list of tuples containing the shared alphabet among all contracts
    """
    def __init__(self):
        """Initialize a contracts object"""
        self.contracts = OrderedDict()
        self.alphabet = []

    def add_contract(self, contract):
        """Add a contract to the contracts object and update the alphabet

        Args:
            contract: a contract object
        """
        self.contracts[contract.name] = contract
        self.alphabet = list(set(self.alphabet) | set(contract.variables))

    def get_contract(self, name):
        """Get the contract with the specified name

        Args:
            name: a string name associated with a contract

        Returns:
            A contract object with the specified name"""
        return self.contracts[name]

    def get_contracts(self):
        """Get all contracts in the contracts object

        Returns:
            A list of contract objects
        """
        return self.contracts

    def get_alphabet(self):
        """Get the shared contract alphabet

        Returns:
            A list of tuples containing the shared alphabet and their initial values
        """
        return self.alphabet

    def __str__(self):
        """Override the print behavior"""
        astr = '{\n'
        for (name, _) in self.contracts.iteritems():
            astr += '  ' + name + ',\n'
        return astr + '}'

    def __eq__(self, other):
        """Override the default Equals behavior"""
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return False

    def __ne__(self, other):
        """Define a non-equality test"""
        return not self.__eq__(other)
