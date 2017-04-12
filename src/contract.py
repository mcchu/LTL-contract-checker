#!/usr/bin/env python
"""Contract module defines a contract class to store contract data attributes"""

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
        self.name = name[0]

    def set_variables(self, variables):
        """Assigns the contract variables"""
        self.variables = variables

    def set_assumptions(self, assumptions):
        """Assigns the contract assumptions"""
        self.assumptions = assumptions

    def set_guarantees(self, guarantees):
        """Assigns the contract guarantees"""
        self.guarantees = guarantees

    def cleanup_contract(self):
        """Concatenates all assumptions and guarantees and puts the contract
        into saturated form"""
        self.concatenate_assumptions()
        self.concatenate_guarantees()
        self.saturate()

    def concatenate_assumptions(self):
        """Takes in a contract with a list of assumptions and concatenates them all"""
        st = ""
        for assumption in self.assumptions:
            st += (assumption + " & ")
        self.assumptions = st[:-3]

    def concatenate_guarantees(self):
        """Takes in a contract with a list of guaranteesa and concatenates them all"""
        st = ""
        for guarantee in self.guarantees:
            st += (guarantee + " & ")
        self.guarantees = st[:-3]

    def saturate(self):
        """Takes in a contract and modifies its guarantees to be in saturated form"""
        self.guarantees = "( (" + self.assumptions + ") -> (" + self.guarantees + ") )"

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
