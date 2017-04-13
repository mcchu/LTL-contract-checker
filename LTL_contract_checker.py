# LTL_contract_checker.py
# New main incorporating all pieces of the software tool
# EE599 Final Project
# Spring 2017
import sys, getopt

from src.parser import Parser
from src.contract import Contract
from src.check import Check
from src.check import Checks


def main(argv):
    # parse command line inputs specifing the contract .txt file using -i (-o is not used right now but could be in the future)
    inputfile = ''
    outputfile = ''
    try:
      opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
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

    # parse the input .txt model, return dictonary of contracts and a 'Checks' object
    parser_obj = Parser(inputfile)
    contracts, checks = parser_obj.parse()
    
    print checks


    checks.run(contracts)



if __name__ == "__main__":
    main(sys.argv[1:])