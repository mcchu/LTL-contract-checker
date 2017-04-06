#!/usr/bin/env python
"""Parse module defines a parse class and defines contract and check file specifications"""

from src.contract import Contract
from src.check import Check

# contract file attributes
TAB_WIDTH = 2
COMMENT_CHAR = '##'
CONTRACT_HEADER = 'CONTRACT:'
CONTRACT_NAME_HEADER = 'NAME:'
CONTRACT_VARIABLES_HEADER = 'VARIABLES:'
CONTRACT_ASSUMPTIONS_HEADER = 'ASSUMPTIONS:'
CONTRACT_GUARANTEES_HEADER = 'GUARANTEES:'
CHECKS_HEADER = 'CHECKS:'

class Parser(object):
	"""Parser class provides parse method for contract and check text file specification

	Arguments:
		afile: a string location of the text file to be parsed

	"""
	def __init__(self, afile=''):
		self.afile = afile

	def parse(self):
		"""Parses input text file

		Returns:
			A tuple of a list of contracts and a list of checks

		"""
		# init return variables
		contracts, checks = {}, None

		with open(self.afile, 'r') as in_file:

			for line in in_file:
				line = self.__clean_line(line)

				# skip empty lines
				if not line.strip():
					continue

				# parse contract
				if CONTRACT_HEADER in line:
					tab_lim = self.__line_indentation(line)
					contract = self.__parse_contract(tab_lim, in_file)
					contracts[contract.name] = contract

				# parse checks
				if CHECKS_HEADER in line:
					tab_lim = self.__line_indentation(line)
					checks = self.__parse_checks(tab_lim, in_file, contracts)

		return contracts, checks

	def __parse_contract(self, tab_lim, afile):
		"""Parses a contract block within the input text file"""
		contract = Contract() # init contract object
		group = None # init group variable

		# init array for contract data and contract data adder utility functions
		data = [
			('name', CONTRACT_NAME_HEADER, contract.set_name, []),
			('variables', CONTRACT_VARIABLES_HEADER, contract.set_variables, []),
			('assumptions', CONTRACT_ASSUMPTIONS_HEADER, contract.set_assumptions, []),
			('guarantees', CONTRACT_GUARANTEES_HEADER, contract.set_guarantees, [])
		]

		# parse contract
		for line in afile:
			line = self.__clean_line(line)
			tab_len = self.__line_indentation(line)

			# end parse when number of indents is lower than or equal to tab limit
			if tab_len <= tab_lim:
				break

			# when number of indents is one more than limit, parce header
			elif tab_len == tab_lim + 1:
				group = [x for x in data if x[1] in line][0]

			# when number of indents is more than header, parce data
			else:
				group[3].append(line.strip())

		# add contract elements to contract object
		data = [x[2](x[3]) for x in data]

		return contract

	def __parse_checks(self, tab_lim, afile, contracts):
		"""Parses the checks block within the input text file"""
		checks = {}

		# parse checks
		for line in afile:
			line = self.__clean_line(line)
			tab_len = self.__line_indentation(line)

			# end parse when number of indents is lower than or equal to tab limit
			if tab_len <= tab_lim:
				break

			# when number of indents is greater than tab limit
			else:
				# parse check
				check_type, check_contracts = line.split('(', 1)

				# find contracts associated with check
				check_contracts = check_contracts[:-1].split(',')
				check_contracts = [contracts[x.strip()] for x in check_contracts]

				# construct and store check
				check = Check()
				check.set_type(check_type.strip())
				check.set_contracts(check_contracts)
				checks[check.check_type] = check

		return checks

	@classmethod
	def __clean_line(cls, line):
		"""Returns a comment-free, tab-replaced line with no ending whitespace"""
		line = line.split(COMMENT_CHAR, 1)[0] # remove comments
		line = line.replace('\t', ' ' * TAB_WIDTH) # replace tabs with spaces
		return line.rstrip() # remove ending whitespace

	@classmethod
	def __line_indentation(cls, line):
		"""Returns the number of indents on a given line"""
		return (len(line) - len(line.lstrip(' '))) / TAB_WIDTH
