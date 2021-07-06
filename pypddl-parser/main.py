# This file is part of pypddl-PDDLParser.

# pypddl-parser is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# pypddl-parser is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with pypddl-parser.  If not, see <http://www.gnu.org/licenses/>.


import argparse
from pddlparser import PDDLParser
import networkx as nx



class Stato:
    def __init__(self,tipo, set) -> None:
        self._type = tipo
        self._set = set
        self._value = 0
    
    @property
    def type(self):
        return self._type
    @property
    def set(self):
        return self._set
    @property
    def value(self):
        return self._value
    
    def __str__(self):
        str = f"Tipo:\t\t{self._type}\n"
        str += f"Set:\t\t{self._set}"
        return str

def parse():
    usage = 'python3 main.py <DOMAIN> <INSTANCE>'
    description = 'pypddl-parser is a PDDL parser built on top of ply.'
    parser = argparse.ArgumentParser(usage=usage, description=description)

    parser.add_argument('domain',  type=str, help='path to PDDL domain file')
    parser.add_argument('problem', type=str, help='path to PDDL problem file')

    return parser.parse_args()

def execute_actions(state, actions):
    for a in actions:
        check = 0
        for prec in a.preconditions:
            p = str(prec)
            if not p in state:
                check = 1
        if check == 0:
            '''all conditions verified'''
            print("verified")
        else:
            print("not verified")
            check=0

def semantic_check(domain, problem) :
    # check if predicates match with types
    domain_predicates = {}

        
    for p in domain.predicates:
        domain_predicates[p.name] = p.arity
        for t in p.args:
            if not t.type in domain.types:
                print(f"Error: {t.type} not defined in domain types")
                return False
    # check if functions matches predicates:
    for f in domain.functions:
        if not f.predicate in domain_predicates:
            print(f"Error: predicate {f.predicate} of function {f.name} not defined in domain")
            return False
    for a in domain.operators:
        for p in a.params:
            if not p.type in domain.types:
                print(f"Error: {t.type} not defined in domain types")
                return False
    #check domain-problem match
    if not problem.domain == domain.name:
        print("Problem's domain doesn't match domain file!")
        return False
    for o in problem.objects:
        if not o in domain.types:
            print(f"Error: object has type: {t.type}, not defined in domain types")
            return False
    #check init predicates: name and arity
    for i in problem.init:
        if not i.name in domain_predicates:
            print(f"Error: predicate {i.name} of init state not defined in domain")
            return False
        elif not i.arity == domain_predicates[i.name]:
            print(f"Mismatch airty of predicate {i.name} in init")
    #check goal predicates: name and airty
    for g in problem.goal:
        if not g.name in domain_predicates:
            print(f"Error: predicate {g.name} of goal state not defined in domain")
            return False
        elif not g.arity == domain_predicates[g.name]:
            print(f"Mismatch airty of predicate {g.name} in goal")
            return False
    return True

if __name__ == '__main__':

    args = parse()

    domain  = PDDLParser.parse(args.domain)         # Vedi classe Domain
    problem = PDDLParser.parse(args.problem)        # Vedi classe Problem  
    
    if semantic_check(domain, problem):
        print("semantic check passed!")



    