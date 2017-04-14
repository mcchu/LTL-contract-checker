#!/usr/bin/env python
"""Operations module provides LTL operations to test contracts"""

from src.contract import Contract

def compatibility(acontract, bcontract):
    """Checks if acontract and bcontract are compatible

    Args:
        acontract: a contract object
        bcontract: a contract object

    Returns:
        A string LTL expression that checks the compatibility of the inputs
    """
    return _ltl(composition(acontract, bcontract).get_assumptions())

def consistency(acontract, bcontract):
    """Checks if acontract and bcontract are consistent

    Args:
        acontract: a contract object
        bcontract: a contract object

    Returns:
        A string LTL expression that checks the consistency of the inputs
    """
    return _ltl(composition(acontract, bcontract).get_guarantees())

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

def composition(acontract, bcontract):
    """Takes the composition of two contracts

    Args:
        acontract: a contract object
        bcontract: a contract object

    Returns:
        A contract object that is the composition of the two inputs
    """
    comp = Contract()
    comp.set_name(acontract.name + '_comp_' + bcontract.name)
    comp.set_variables(_merge(acontract.variables, bcontract.variables))
    comp.set_assumptions(_or(_and(acontract.get_assumptions(), bcontract.get_assumptions()),
                             _inv(_and(acontract.get_guarantees(), bcontract.get_guarantees()))))
    comp.set_guarantees(_and(acontract.get_guarantees(), bcontract.get_guarantees()))
    return comp

def conjunction(acontract, bcontract):
    """Takes the conjunction of two contracts

    Args:
        acontract: a contract object
        bcontract: a contract object

    Returns:
        A contract object that is the conjunction of the two inputs
    """
    conj = Contract()
    conj.set_name(acontract.name + "_conj_" + bcontract.name)
    conj.set_variables(_merge(acontract.variables, bcontract.variables))
    conj.set_assumptions(_or(acontract.get_assumptions(), bcontract.get_assumptions()))
    conj.set_guarantees(_and(acontract.get_guarantees(), bcontract.get_guarantees()))
    return conj

def _merge(alist, blist):
    """Merges input lists and removes duplicates"""
    return list(set(alist) | set(blist))

def _ltl(astr):
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
