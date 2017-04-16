#!/usr/bin/env python
"""Core module defines the core workflow functions of the LTL contract checker tool"""

import subprocess
from src.contract import Contract, Contracts
from src.check import Compatibility, Consistency, Checks

# contract file attributes
TAB_WIDTH = 2
FILE_HEADER_INDENT = 0
CONTRACT_HEADER_INDENT = 1
CONTRACT_DATA_INDENT = 2
CHECK_DATA_INDENT = 1
COMMENT_CHAR = '##'
ASSIGNMENT_CHAR = ':='
CHECKS_HEADER = 'CHECKS'
CONTRACT_HEADER = 'CONTRACT'
CONTRACT_NAME_HEADER = 'NAME'
CONTRACT_VARIABLES_HEADER = 'VARIABLES'
CONTRACT_ASSUMPTIONS_HEADER = 'ASSUMPTIONS'
CONTRACT_GUARANTEES_HEADER = 'GUARANTEES'
COMPATIBILITY_CHECK = 'COMPATIBILITY'
CONSISTENCY_CHECK = 'CONSISTENCY'

def parse(specfile):
    """Parses the system specification file and returns the contracts and checks

    Args:
        specfile: a string input file name for the system specification file

    Returns:
        A tuple containing a contracts object and a checks object
    """
    contracts, checks = Contracts(), Checks() # returned contracts and checks
    contract = Contract() # contract and check holders
    file_header = '' # file header line contents
    contract_header = '' # contract header line contents

    with open(specfile, 'r') as ifile:
        for line in ifile:
            line, ntabs = _clean_line(line)

            # skip empty lines
            if not line:
                continue

            # parse file header line
            elif ntabs == FILE_HEADER_INDENT:
                # store previously parsed contract
                if CONTRACT_HEADER in file_header:
                    if contract.is_full():
                        contract.saturate_guarantees()
                        contracts.add_contract(contract)
                    else: # (TODO) add error - contract params incomplete
                        pass
                # parse file headers
                if CONTRACT_HEADER in line:
                    if file_header:
                        contract = Contract()
                    file_header = line
                elif CHECKS_HEADER in line:
                    file_header = line
                else: # (TODO) add error - unexpected file heading
                    pass

            # parse contract and check data
            else:
                if CONTRACT_HEADER in file_header:
                    if ntabs == CONTRACT_HEADER_INDENT:
                        contract_header = line
                    elif ntabs == CONTRACT_DATA_INDENT:
                        if CONTRACT_NAME_HEADER in contract_header:
                            contract.add_name(line.strip())
                        elif CONTRACT_VARIABLES_HEADER in contract_header:
                            var, init = line.split(ASSIGNMENT_CHAR, 1)
                            contract.add_variable((var.strip(), init.strip()))
                        elif CONTRACT_ASSUMPTIONS_HEADER in contract_header:
                            contract.add_assumption(line.strip())
                        elif CONTRACT_GUARANTEES_HEADER in contract_header:
                            contract.add_guarantee(line.strip())
                        else: # (TODO) add error - unexpected contract heading
                            pass
                    else: # (TODO) add error - unexpected indentation
                        pass
                elif CHECKS_HEADER in file_header:
                    if ntabs == CHECK_DATA_INDENT:
                        check_type, check_contracts = line.split(')', 1)[0].split('(', 1)
                        check_contracts = [contracts.get_contract(
                            contract.strip()) for contract in check_contracts.split(',')]
                        if COMPATIBILITY_CHECK in check_type.upper():
                            compatibility = Compatibility()
                            compatibility.set_contracts(check_contracts)
                            checks.add_check(compatibility)
                        elif CONSISTENCY_CHECK in check_type.upper():
                            consistency = Consistency()
                            consistency.set_contracts(check_contracts)
                            checks.add_check(consistency)
                        else: # (TODO) add error - unrecognized check
                            continue
                    else: # (TODO) add error - unexpected indentation
                        pass

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

def _clean_line(line):
    """Returns a comment-free, tab-replaced line with no whitespace and the number of tabs"""
    line = line.split(COMMENT_CHAR, 1)[0] # remove comments
    line = line.replace('\t', ' ' * TAB_WIDTH) # replace tabs with spaces
    return line.strip(), _line_indentation(line)

def _line_indentation(line):
    """Returns the number of indents on a given line"""
    return (len(line) - len(line.lstrip(' '))) / TAB_WIDTH
