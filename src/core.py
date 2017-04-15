#!/usr/bin/env python
"""Parse module defines a parse class and defines contract and check file specifications"""

import subprocess
from src.operations import compatibility, consistency
from src.contract import Contract
from src.check import Check
from src.check import Checks


# contract file attributes
TAB_WIDTH = 2
COMMENT_CHAR = '##'
CONTRACT_HEADER = 'CONTRACT:'
CONTRACT_NAME_HEADER = 'NAME:'
CONTRACT_VARIABLES_HEADER = 'VARIABLES:'
CONTRACT_ASSUMPTIONS_HEADER = 'ASSUMPTIONS:'
CONTRACT_GUARANTEES_HEADER = 'GUARANTEES:'
CHECKS_HEADER = 'CHECKS:'

def parse(infile):
    """Parses input text file

    Returns:
        A tuple of a list of contracts and a list of checks

    """
    # init return variables
    contracts, checks = {}, None

    with open(infile, 'r') as in_file:

        for line in in_file:
            line = _clean_line(line)

            # skip empty lines
            if not line.strip():
                continue

            # parse contract
            if CONTRACT_HEADER in line:
                tab_lim = _line_indentation(line)
                contract = _parse_contract(tab_lim, in_file)
                contracts[contract.name] = contract

            # parse checks
            if CHECKS_HEADER in line:
                tab_lim = _line_indentation(line)
                checks = _parse_checks(tab_lim, in_file, contracts)

    return contracts, checks

def generate(contracts, checks):

    # generate output file
    outfile = open('nusmv.smv', 'w')
    outfile.write("MODULE main\n")

    # Iterate through the contracts dictionary, breaking after printing the variables from the first contract
    # (because for now, all contracts have the same variables)
    # TEMP -> Change for alphabet projection
    outfile.write("VAR\n")
    for k, v in contracts.items():
        for var in v.variables:
            var_char = var[:(var.find(":="))]
            outfile.write("\t" + var_char + ": boolean;\n")
        break

    # Iterate through the contracts dictionary, breaking after initializing the values of the variables
    # from the first contract
    outfile.write("ASSIGN\n")
    for k, v in contracts.items():
        for var in v.variables:
            idx = var.find(" :=")
            var_char = var[:idx]
            outfile.write("\tinit(" + var_char + ")" + var[idx:] + ";\n")
        break

    # -- END TEMP --

    outfile.write("\n")

    # Iterate through all checks and run the corresponding function for that test (for now, only works with 2 contracts)
    for check in checks.checks:
        if check.check_type == 'compatibility':
            comp = compatibility(contracts[check.contract_names[0]],contracts[check.contract_names[1]])
            outfile.write(comp)

                # Uncomment the line below if you want to test the correctness of the composition function)
                # composition(contracts[check.contract_names[0]],contracts[check.contract_names[1]])

                # Uncomment the line below if you want to test the correctness of the conjunction function)
                # conjunction(contracts[check.contract_names[0]],contracts[check.contract_names[1]])
        elif check.check_type == 'consistency':
            const = consistency(contracts[check.contract_names[0]],contracts[check.contract_names[1]])
            outfile.write(const)

    # Return the name of the generated .smv file so the calling function can run NuSMV
    return 'nusmv.smv'


def run(smvfile, checks):
    """runs the set of contracts and checks through NuSMV and parses the results to return to the user"""

    # Initialize an array to hold the results of the checks
    results = []

    # create the command and run in terminal
    output = subprocess.check_output(['NuSMV', smvfile]).splitlines()

    # Get rid of all initial notes, warnings and blank lines
    output = [x for x in output if not (x[:3] == '***' or x[:7] == 'WARNING' or x == '')]
    # pprint(self.output)

    # Iterate through all remaining lines of output, stopping at each "-- specification line to parse it"
    result_num = -1      # Counter to keep track of what result you're looking at
    in_result = False   # Flag to track if you're in a counterexample output
    temp_counterexample = []
    counterexamples = {}

    for line in output:
        # If this line is going to indicate whether or not a LTL spec is true/false
        if line[:16] == '-- specification':
            if in_result == True:
                in_result = False
                # pprint(temp_counterexample)
                counterexamples[result_num] = temp_counterexample
                temp_counterexample = []
            if 'is false' in line:
                results.append(True)
                result_num += 1
            elif 'is true' in line:
                results.append(False)
                result_num += 1

        # If you are currently in a counterexample
        if in_result:
            temp_counterexample.append(line)

        # If the next line is going to be the start of a counterexample, set the in_result flag
        if line == 'Trace Type: Counterexample ':
            in_result = True

    if in_result:
        in_result = False
        counterexamples[result_num] = temp_counterexample
        temp_counterexample = []

    for x in range(result_num + 1):
        print "Result of checking:", checks.checks[x]
        print 'Statement is', results[x]
        print 'Example:'
        for y in counterexamples[x]:
            print y
        print ''

def _parse_contract(tab_lim, afile):
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
        line = _clean_line(line)
        tab_len = _line_indentation(line)

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

def _parse_checks(tab_lim, afile, contracts):
    """Parses the checks block within the input text file"""
    checks = Checks()

    # parse checks
    for line in afile:
        line = _clean_line(line)
        tab_len = _line_indentation(line)

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
            checks.add_check(check)

    return checks

def _clean_line(line):
    """Returns a comment-free, tab-replaced line with no ending whitespace"""
    line = line.split(COMMENT_CHAR, 1)[0] # remove comments
    line = line.replace('\t', ' ' * TAB_WIDTH) # replace tabs with spaces
    return line.rstrip() # remove ending whitespace

def _line_indentation(line):
    """Returns the number of indents on a given line"""
    return (len(line) - len(line.lstrip(' '))) / TAB_WIDTH
