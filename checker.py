# LTL_contract_checker.py
# New main incorporating all pieces of the software tool
# EE599 Final Project
# Spring 2017
import sys
import getopt

from src.fileio import parse, compile, run


def main(argv):
    # parse command line inputs specifing the contract .txt file using -i (-o is not used right now but could be in the future)
    inputfile = ''
    outputfile = ''
    try:
        opts, _ = getopt.getopt(argv, "hi:o:", ["ifile=", "ofile="])
    except getopt.GetoptError:
        print 'test.py -i <inputfile> -o <outputfile>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'test.py -i <inputfile> -o <outputfile>'
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg

    # parse system specification file
    contracts, checks = parse(inputfile)

    # compile NuSMV file
    smvfile = compile(contracts, checks)

    print checks

    run(smvfile, checks)

if __name__ == "__main__":
    main(sys.argv[1:])