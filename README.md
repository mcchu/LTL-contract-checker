# README for LTL Python Contract Checker

Authors: Nikhil Narang, Jack Kellner, Michael Chu

This is a README file describing the required format of the contract operations input.txt 
file, as well as instructions for how to execute the program


## Format of contract specification .txt file


The input.txt file requires following a very specific format in order for the program 
correctly. If you are running into issues with the program, please double check the format 
of your input file for correctness.

The input file requires the following headers for each contract: “CONTRACT:”, “NAME:”, 
“VARIABLES:”, “ASSUMPTIONS:”, and “GUARANTEES:”

“CONTRACTS:” must be specified at the beginning of a new line, and the other four headers 
must be specified on their own lines, with one tab indentation. On a new line after each 
of the headers, increase indentation to two tabs, and then specify the content that 
belongs to that header. Under assumptions and guarantees, all lines are logically ANDed 
together to generate the final assumptions/guarantees for that contract.

After all contracts have been specified, then you must specify the “CHECKS:” header, to 
tell the tool which contract operations should be performed on which contracts. The 
following options can be specified:

	“COMPATIBILITY_COMP(contract1, contract2, …)”
	Checks the compatibility of the composition of a list of contracts, where 
        “contract1, contract2, …” are the names of the contracts that you want to run the 
        check on exactly as the name is specified under the “NAME:” header in the contract 
        declaration

	“COMPATIBILITY_CONJ(contract1, contract2, …)”
	Checks the compatibility of the conjunction of a list of contracts, where 
        “contract1, contract2, …” are the names of the contracts that you want to run the 
        check on exactly as the name is specified under the “NAME:” header in the contract 
        declaration

	“CONSISTENCY_COMP(contract1, contract2, …)”
	Checks the consistency of the composition of a list of contracts, where 
        “contract1, contract2, …” are the names of the contracts that you want to run the 
        check on exactly as the name is specified under the “NAME:” header in the contract 
        declaration

	“CONSISTENCY_CONJ(contract1, contract2, …)“
	Checks the consistency of the conjunction of a list of contracts, where 
        “contract1, contract2, …” are the names of the contracts that you want to run the 
        check on exactly as the name is specified under the “NAME:” header in the contract 
        declaration

	NOTE: If you want to check the compatibility or consistency of one contract, you 
        can do so using either the _CONJ or _COMP version of the command and passing in 
        only one contract. When either the _CONJ or _COMP internal methods are called on a 
        list of only one contract, no modifications will be made to the contract.
	
Some example input .txt files have been included in the top level directory 
(‘waiter_customer.txt’)

## Command Line Execution

To run the tool, first ensure that your contract specification .txt file is in the same 
directory as “checker.py” (the top level directory). For the sake of these instructions, 
we will refer to that file as ‘input.txt’

Open a terminal window, and navigate to the folder where ‘checker.py’ and 
‘input.txt’ (this should be your contract specification .txt file), and run the following 
command

$ cd LTLCHECK/src
$ python checker.py --i <specfile-name> --o <smvfile-name>

Where the argument following -i is the path to your contract specification file. 
Optionally, you can use the -o flag to specify where the generated .smv file will be 
output.

The report references two case studies: the waiter-customer model and the train model. 
These models can be run with the following

$ python checker.py -i ../tests/spec/waiter_customer.txt -o ../tests/smv/nusmv.smv
$ python checker.py -i ../tests/spec/train_door.txt -o ../tests/smv/nusmv.smv
