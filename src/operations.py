#!/usr/bin/env python
"""Operations module provides LTL operations to test contracts"""

import contract

def compatibility(contract):
    """Checks the compatibility of a contract object

    Args:
        contract: a contract object

    Returns:
        A string LTL expression that checks the compatibility of the input
    """
    return _ltl_inv(contract.get_assumptions())

def consistency(contract):
    """Checks the consistency of a contract object

    Args:
        contract: a contract object

    Returns:
        A string LTL expression that checks the consistency of the input
    """
    return _ltl_inv(contract.get_guarantees())

def refinement(acontract, bcontract):
    """Checks if acontract refines bcontract

    Args:
        acontract: a contract object
        bcontract: a contract object

    Returns:
        A string LTL expression that checks if acontract refines bcontract
    """
    return _ltl(_and(_imply(bcontract.get_assumptions(), acontract.get_assumptions()),
                     _imply(acontract.get_guarantees(), bcontract.get_guarantees())))

def saturation(contract):
    """Perform a saturation operation on a contract

    Args:
        contract: an unsaturated contract object
    """
    contract.guarantees = [_imply(contract.get_assumptions(), g) for g in contract.guarantees]

def composition(contracts):
    """Perform a composition operation on a list of contracts

    Args:
        contracts: a list of contract objects

    Returns:
        A contract object that is the composition of whole list
    """
    if len(contracts) == 1:
        return contracts[0]
    else:
        comp = contract.Contract()
        comp.add_name(contracts[0].name + '_comp_' + contracts[1].name)
        comp.add_variables(_merge(contracts[0].variables, contracts[1].variables))
        comp.add_assumption(_or(_and(contracts[0].get_assumptions(), contracts[1].get_assumptions()),
                            _inv(_and(contracts[0].get_guarantees(), contracts[1].get_guarantees()))))
        comp.add_guarantee(_and(contracts[0].get_guarantees(), contracts[1].get_guarantees()))
        contracts.pop(0) #remove first element in list
        contracts[0] = comp #replace "new" first element with conj
        return composition(contracts)

def conjunction(contracts):
    """Takes the conjunction of a list of contracts

    Args:
        contracts: a list of contract objects

    Returns:
        A contract object that is the conjunction of whole list
    """
    if len(contracts) == 1:
        return contracts[0]
    else:
        conj = contract.Contract()
        conj.add_name(contracts[0].name + "_conj_" + contracts[1].name)
        conj.add_variables(_merge(contracts[0].variables, contracts[1].variables))
        conj.add_assumption(_or(contracts[0].get_assumptions(), contracts[1].get_assumptions()))
        conj.add_guarantee(_and(contracts[0].get_guarantees(), contracts[1].get_guarantees()))
        contracts.pop(0) #remove first element in list
        contracts[0] = conj #replace "new" first element with conj
        return conjunction(contracts)

def _merge(alist, blist):
    """Merges input lists and removes duplicates"""
    return list(set(alist) | set(blist))

def _ltl(astr):
    """Applies an inverted LTLSPEC wrapper to the input string"""
    return '\tLTLSPEC ' + astr + ';\n'

def _ltl_inv(astr):
    """Applies an inverted LTLSPEC wrapper to the input string"""
    return '\tLTLSPEC !' + astr + ';\n'

def _and(astr, bstr):
    """Returns logical and of astr and bstr"""
    return '(' + astr + ' & ' + bstr + ')'

def _or(astr, bstr):
    """Returns logical or of astr and bstr"""
    return '(' + astr + ' | ' + bstr + ')'

def _imply(astr, bstr):
    """Returns logical implication of bstr by astr"""
    return '(' + astr + ' -> ' + bstr + ')'

def _inv(astr):
    """Returns logical not of input"""
    return '!' + astr
