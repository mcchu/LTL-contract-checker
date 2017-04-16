#!/usr/bin/env python
"""Parse module defines a parse class and defines contract and check file specifications"""

import subprocess
from src.contract import Contract, Contracts
from src.check import Compatibility, Consistency, Checks

# contract file attributes
TAB_WIDTH = 2
COMMENT_CHAR = '##'
ASSIGNMENT_CHAR = ':='
CONTRACT_HEADER = 'CONTRACT'
CONTRACT_NAME_HEADER = 'NAME'
CONTRACT_VARIABLES_HEADER = 'VARIABLES'
CONTRACT_ASSUMPTIONS_HEADER = 'ASSUMPTIONS'
CONTRACT_GUARANTEES_HEADER = 'GUARANTEES'
CHECKS_HEADER = 'CHECKS'
COMPATIBILITY_CHECK = 'compatibility'
CONSISTENCY_CHECK = 'consistency'

def parse(specfile):
    """Parses the system specification file and returns the contracts and checks

    Args:
        specfile: a string input file name for the system specification file

    Returns:
        A tuple containing a contracts object and a checks object
    """
    # init return variables
    contracts, checks = Contracts(), None

    with open(specfile, 'r') as ifile:

        for line in ifile:
            line = _clean_line(line)

            # skip empty lines
            if not line.strip():
                continue

            # parse contract
            if CONTRACT_HEADER in line:
                tab_lim = _line_indentation(line)
                contract = _parse_contract(tab_lim, ifile)
                contracts.add_contract(contract)

            # parse checks
            if CHECKS_HEADER in line:
                tab_lim = _line_indentation(line)
                checks = _parse_checks(tab_lim, ifile, contracts)

    return contracts, checks

def generate(contracts, checks, smvfile):
    """Generates a NuSMV file with configured variable declarations and LTL checks

    Args:
        contracts: a contracts object containing all the contracts in a system
        checks: a checks object containing all the desired checks on the system
        smvfile: a string name for the generated NuSMV file
    """
    with open(smvfile, 'w') as ofile:

        # write module heading declaration
        ofile.write('MODULE main\n')

        # write variable type declarations
        ofile.write('VAR\n')
        for (var, _) in contracts.get_alphabet():
            ofile.write('\t' + var + ': boolean;\n')

        # write variable assignment declarations
        ofile.write('ASSIGN\n')
        for (var, init) in contracts.get_alphabet():
            ofile.write('\tinit(' + var + ') := ' + init + ';\n')
        ofile.write('\n')

        # write LTL specifications declarations for each check
        for check in checks.checks:
            ofile.write(check.get_ltl())

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
    header = '' # init header variable

    # parse contract
    for line in afile:
        line = _clean_line(line)
        tab_len = _line_indentation(line)

        # end parse when number of indents is lower than or equal to tab limit
        if tab_len <= tab_lim:
            break

        # when number of indents is one more than limit, parce header
        elif tab_len == tab_lim + 1:
            header = line

        # when number of indents is more than header, parce data
        elif tab_len == tab_lim + 2:

            if CONTRACT_NAME_HEADER in header:
                contract.add_name(line.strip())

            elif CONTRACT_VARIABLES_HEADER in header:
                var, init = line.split(ASSIGNMENT_CHAR, 1)
                contract.add_variable((var.strip(), init.strip()))

            elif CONTRACT_ASSUMPTIONS_HEADER in header:
                contract.add_assumption(line.strip())

            elif CONTRACT_GUARANTEES_HEADER in header:
                contract.add_guarantee(line.strip())

            # (TODO) add error - unexpected contract heading
            else:
                continue

        # (TODO) add error - unexpected number of indentations
        else:
            continue

    # saturate contract guarantees
    contract.saturate_guarantees()

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
            check_contracts = [contracts.get_contract(x.strip()) for x in check_contracts]

            # construct compatibility check
            if check_type.strip() == COMPATIBILITY_CHECK:
                check = Compatibility()

            # construct consistency check
            elif check_type.strip() == CONSISTENCY_CHECK:
                check = Consistency()

            # (TODO) add error - unrecognized check
            else:
                continue

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
