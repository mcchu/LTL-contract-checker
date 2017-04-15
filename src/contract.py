#!/usr/bin/env python
"""Contract module defines a contract class to store contract data attributes and a contracts class
to store all system contracts and overall system alphabet"""

class Contract(object):
    """Contract class stores data attributes of a contract

    Attributes:
        name: a string name for the contract
        variables: a list of string variables from assumptions and guarantees
        assumptions: a list of string relations assumed by contract
        guarantees: a list of string relations guaranteed by contract
    """

    def __init__(self):
        """Initialize a contract object"""
        self.name = ''
        self.variables = []
        self.assumptions = []
        self.guarantees = []

    def set_name(self, name):
        """Assigns the contract a name"""
        if isinstance(name, list):
            name = name[0]
        self.name = name

    def set_variables(self, variables):
        """Assigns the contract variables"""
        self.variables = variables

    def set_assumptions(self, assumptions):
        """Assigns the contract assumptions"""
        if isinstance(assumptions, str):
            assumptions = [assumptions]
        self.assumptions = assumptions

    def set_guarantees(self, guarantees):
        """Assigns the contract guarantees"""
        if isinstance(guarantees, str):
            guarantees = [guarantees]
        self.guarantees = guarantees

    def get_assumptions(self):
        """Returns concatenated string of all assumptions"""
        assumptions = [assumption + ' & ' for assumption in self.assumptions]
        return '(' + ''.join(assumptions)[:-3] + ')'

    def get_unsat_guarantees(self):
        """Returns concatenated string of all guarantees in unsaturated form"""
        guarantees = [guarantee + ' & ' for guarantee in self.guarantees]
        return '(' + ''.join(guarantees)[:-3] + ')'

    def get_guarantees(self):
        """Returns concatenated string of all guarantees in saturated form"""
        assumptions = self.get_assumptions()
        guarantees = self.get_unsat_guarantees()
        return  '(' + assumptions + ' -> ' + guarantees + ')'

    def __str__(self):
        """Override the print behavior"""
        astr = 'Name: ' + self.name + '\n'
        astr += 'Variables:\n'
        for variable in self.variables:
            astr += ('  ' + variable + '\n')
        astr += 'Assumptions:' + self.assumptions + '\n'
        # for assumption in self.assumptions:
        #     astr += ('  ' + assumption + '\n')
        astr += 'Guarantees:' + self.guarantees + '\n'
        # for guarantee in self.guarantees:
        #     astr += ('  ' + guarantee + '\n')
        return astr

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
        self.contracts = []
        self.alphabet = []

    def add_contract(self, contract):
        """Add a contract to the contracts object and update the alphabet

        Args:
            contract: a contract object
        """
        self.contracts.append(contract)
        self.alphabet = list(set(self.alphabet) | set(contract.variables))

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

    def __eq__(self, other):
        """Override the default Equals behavior"""
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return False

    def __ne__(self, other):
        """Define a non-equality test"""
        return not self.__eq__(other)
