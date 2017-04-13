from pprint import pprint
from src.contract import Contract

def compatibility(contract_a, contract_b):
    """Returns the LTL expression that should be used to check the compatibility of contracts a and b.
    contract_a and contract_b should both be contract objects"""
    comp = "\tLTLSPEC !( (" + contract_a.assumptions + " & " + contract_b.assumptions + ") | !(" + contract_a.guarantees + " & " + contract_b.guarantees + ") );\n"
    return comp

def consistency(contract_a, contract_b):
    """Returns the LTL expression that should be used to check the consistency of contracts a and b.
    contract_a and contract_b should both be contract objects"""
    cons = "\tLTLSPEC !(" + contract_a.guarantees + " & " + contract_b.guarantees + ");\n"
    return cons

def refinement(contract_a, contract_b):
    """Returns the 2 LTL expression that should be used to check if contract_a refines contract_b
    NOTE: The order of contract_a and contract_b is important as refinement is not always reversible.

    Contract_a is a refinement of contract_b iff the inverse of the below LTL expressions are BOTH unsatisfiable"""
    ltl = []
    ltl.append("( (" + contract_b.assumptions + ") -> (" + contract_a.assumptions+ ") )")
    ltl.append("( (" + contract_a.guarantees + ") -> (" + contract_b.guarantees+ ") )")
    pprint(ltl)
    return ltl

def composition(contract_a, contract_b):
    """Returns a new contract that is the composition of contract_a and contract_b"""
    comp = Contract()
    comp.set_name([contract_a.name + "_comp_" + contract_b.name])
    comp.set_variables(contract_a.variables)
    comp.set_assumptions("(" + contract_a.assumptions + " & " + contract_b.assumptions + ") | !(" + contract_a.guarantees + " & " + contract_b.guarantees + ")")
    comp.set_guarantees("(" + contract_a.guarantees + " & " + contract_b.guarantees + ")")
    print comp
    return comp

def conjunction(contract_a, contract_b):
    """Returns a new contract that is the conjunction of contract_a and contract_b"""
    conj = Contract()
    conj.set_name([contract_a.name + "_conj_" + contract_b.name])
    conj.set_variables(contract_a.variables)
    conj.set_assumptions("(" + contract_a.assumptions + " | " + contract_b.assumptions + ")")
    conj.set_guarantees("(" + contract_a.guarantees + " & " + contract_b.guarantees + ")")
    print conj
    return conj
