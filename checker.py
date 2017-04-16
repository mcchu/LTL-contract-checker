#!/usr/bin/env python
"""Checker module defines the main function which runs the LTL contract checker tool workflow"""

import sys
import getopt
from src.core import parse, generate, run

def main():
    """Parses command line arguments and runs the LTL contract checker tool"""

    # initialize default command line values
    version = '1.0'
    verbose = False
    spec_file = 'system.spec'
    smv_file = 'nusmv.smv'

    # configure command line short-form and long-form options
    options, _ = getopt.getopt(sys.argv[1:], 'hvi:o:', ['verbose=', 'spec=', 'smv='])

    # parse command line arguments
    for opt, arg in options:
        if opt == '-h':
            print 'test.py -i <specfile> -o <smvfile>'
            sys.exit()
        elif opt in ('-v', '--verbose'):
            verbose = True
        elif opt in ('-i', '--spec'):
            spec_file = arg
        elif opt in ('-o', '--smv'):
            smv_file = arg

    # print tool configurations
    if verbose:
        print 'VERSION    :', version
        print 'VERBOSE    :', verbose
        print 'SPEC_FILE  :', spec_file
        print 'SMV_FILE   :', smv_file

    # parse system specification file
    contracts, checks = parse(spec_file)

    # compile NuSMV file
    generate(contracts, checks, smv_file)

    print checks

    # run NuSMV file
    run(smv_file, checks)

if __name__ == "__main__":
    main()
