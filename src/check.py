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
        self.check_contracts = []
        self.contract_names = []

    def set_type(self, check_type):
        """Assigns the check type"""
        self.check_type = [x for x in check_types if x == check_type][0]

    def set_contracts(self, contracts):
        """Assigns the contracts associated with the check"""
        self.check_contracts = contracts
        for contract in contracts:
            self.contract_names.append(contract.name)

    def __str__(self):
        """Override the print behavior"""
        astr = ('\'' + self.contract_names[0] + '\'' + ' ' + self.check_type + ' with ' + '\'' + self.contract_names[1] + '\'' + '\n')
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

    def add_check(self, check):
        self.checks.append(check)

    def __str__(self):
        """Override the print behavior"""        
        astr = '\nCheck the following items:\n'
        for check in self.checks:
            astr += ('\'' + check.contract_names[0] + '\'' + ' ' + check.check_type + ' with ' + '\'' + check.contract_names[1] + '\'' + '\n')
        return astr

    def compile(self, contracts):
        outfile = open('nusmv.smv', 'w')
        outfile.write("MODULE main\n")

        # Iterate through the contracts dictionary, breaking after printing the variables from the first contract
        # (because for now, all contracts have the same variables)
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

        outfile.write("\n")

        # Cleanup the Contracts to concatenate assumptions and guarantees and put into saturated form
        for k,v in contracts.items():
            v.cleanup_contract()
            # print "\n", v

        # Iterate through all checks and run the corresponding function for that test (for now, only works with 2 contracts)
        for check in self.checks:
            if check.check_type == 'compatibility': 
                comp = self.compatibility(contracts[check.contract_names[0]],contracts[check.contract_names[1]])
                outfile.write(comp)
            elif check.check_type == 'consistency': 
                const = self.consistency(contracts[check.contract_names[0]],contracts[check.contract_names[1]])
                outfile.write(const)

        # Return the name of the generated .smv file so the calling function can run NuSMV
        return 'nusmv.smv'

    def compatibility(self, contract_a, contract_b):
        """Returns the LTL expression that should be used to check the compatibility of contracts a and b.
        contract_a and contract_b should both be contract objects"""
        comp = "\tLTLSPEC !( (" + contract_a.assumptions + " & " + contract_b.assumptions + ") | !(" + contract_a.guarantees + " & " + contract_b.guarantees + ") );\n"
        return comp

    def consistency(self, contract_a, contract_b):
        """Returns the LTL expression that should be used to check the consistency of contracts a and b.
        contract_a and contract_b should both be contract objects"""
        cons = "\tLTLSPEC !(" + contract_a.guarantees + " & " + contract_b.guarantees + ");\n"
        return cons
        
    def run(self, contracts):
        """runs the set of contracts and checks through NuSMV and parses the results to return to the user"""

        # Use compile() to get the name of the .smv file to run in terminal
        file = self.compile(contracts)

        # Initialize an array to hold the results of the checks
        self.results = []

        # create the command and run in terminal
        self.output = subprocess.check_output(['NuSMV', file]).splitlines()

        # Get rid of all initial notes, warnings and blank lines
        self.output = [x for x in self.output if not (x[:3] == '***' or x[:7] == 'WARNING' or x == '')]
        # pprint(self.output)

        # Iterate through all remaining lines of output, stopping at each "-- specification line to parse it"
        result_num = -1      # Counter to keep track of what result you're looking at
        in_result = False   # Flag to track if you're in a counterexample output
        temp_counterexample = []
        counterexamples = {}

        for line in self.output:
            # If this line is going to indicate whether or not a LTL spec is true/false
            if line[:16] == '-- specification':
                if in_result == True:
                    in_result = False
                    # pprint(temp_counterexample)
                    counterexamples[result_num] = temp_counterexample
                    temp_counterexample = []
                if 'is false' in line:
                    self.results.append(True)
                    result_num += 1
                elif 'is true' in line:
                    self.results.append(False)
                    result_num += 1

            # If you are currently in a counterexample
            if in_result:
                temp_counterexample.append(line)

            # If the next line is going to be the start of a counterexample, set the in_result flag
            if line == 'Trace Type: Counterexample ':
                in_result = True

        if in_result == True:
                    in_result = False
                    counterexamples[result_num] = temp_counterexample
                    temp_counterexample = []

        for x in range(result_num + 1):
            print "Result of checking:", self.checks[x]
            print 'Statement is', self.results[x]
            print 'Example:'
            for y in counterexamples[x]:
                print y
            print ''

        # pprint(self.results)
        # retain only the lines that return whether or not a specification is true/false
        # self.output = [x for x in self.output if x[:16] == '-- specification']

        # Iterate throught the results and parse whether or not a statement is valid
        # for i in range(len(self.output)):
        #     if 'is false' in self.output[i]:
        #         self.results.append(True)
        #     elif 'is true' in output[i]:
        #         self.results.append(False)

        # # print output to console
        # pprint(self.output)
        # pprint(self.results)



