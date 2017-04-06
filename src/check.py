#!/usr/bin/env python
"""Check module defines a check class that links contracts to a pre-defined check type"""
import subprocess
from pprint import pprint

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

class Checks(object):
	def __init__(self):
		self.checks = []

	def add_check(check):
		self.checks.append(check)

	def compile(self):
		# function to compile a .smv file from the list of checks 
		#
		# FOR MICHAEL TO COMPLETE
		# 
		return 'tests/waiter_customer_example.smv'

	def run(self):
		# Return the name of the .smv file to run in terminal
		file = self.compile()

		# Initialize an array to hold the results of the checks
		self.results = []

		# create the command and run in terminal
		self.output = subprocess.check_output(['NuSMV', file]).splitlines()
		# retain only the lines that return whether or not a specification is true/false
		self.output = [x for x in self.output if x[:16] == '-- specification']

		# Iterate throught the results and parse whether or not a statement is valid
		for i in range(len(self.output)):
			if 'is false' in self.output[i]:
				self.results.append(True)
			elif 'is true' in output[i]:
				self.results.append(False)

		# print output to console
		pprint(self.output)
		pprint(self.results)
