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
from ast import Index
from os import stat
from pddlparser import PDDLParser
import networkx as nx
import itertools
from predicate import Predicate
from literal import Literal
from term import Term

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

def get_possible_paths(state, actions, predicates): 
    #TODO: add multiple actions: move(x1,x2), move(x1,x3) are both valid!
    init = state.init

    possible_path = {} #{action -> Action : stato_finale -> list(Predicates)}

    for a in actions:

        # print(f"_______{a.name}_________")
        params = {}
        for par in a.params:
            params[par.name] = None

        sorted_preconditions = sorted(a.preconditions, key=lambda x: x.predicate.arity)
        actuable = True
        #s = {precondizione1: {arg1: [valori],arg2[valori]},precondizione2: {arg1: [valori],arg2[valori]}}  
        s = {}
        preconditions_dic = {}
        index = 0
        for p in sorted_preconditions: #TODO: put this into a function and return immediatly if not actuable
            if actuable:
                if p.predicate.arity == 0:
                    actuable = p.predicate.name in map(str,init)
                    s[p.predicate.name] = {}
                    preconditions_dic[index] = p.predicate.name
                    index += 1
                else:
                    preconditions_dic[index] = p.predicate.name
                    index+=1
                    s[p.predicate.name] = {}
                    for arg in p.predicate.args:
                        s[p.predicate.name][arg] = []
                    
                    for pred in init:
                        if p.predicate.name == pred.name:

                            for j, term in enumerate(p.predicate.args):
                                s[p.predicate.name][term].append(pred.args[j])
        idx_row_prec = 0
        if len(preconditions_dic) - 1 > 0 : #TODO: add actuable check
            for idx in range(len(preconditions_dic) - 1):
                idx_row_next = 0
                not_found = True
                if not_found: #commentare
                    for arg in s[preconditions_dic[idx]]:
                        if not_found:
                            for i in range(idx_row_next,len(s[preconditions_dic[idx]][arg])):
                                if s[preconditions_dic[idx]][arg][i].value in map(lambda x : x.value,s[preconditions_dic[idx + 1]][arg]):
                                    not_found = False
                                    idx_row_next = list(map(
                                        lambda x : x.value,
                                        s[preconditions_dic[idx + 1]][arg])
                                        ).index(
                                            s[preconditions_dic[idx]][arg][i].value
                                        )
                                    idx_row_prec = i
                                    #
                                    if len(s[preconditions_dic[idx]]) < len(s[preconditions_dic[idx + 1]]):
                                        for matched_arg in s[preconditions_dic[idx + 1]]:
                                            params[matched_arg] = s[preconditions_dic[idx + 1]][matched_arg][idx_row_next].value
                                    else:
                                        params[arg] = s[preconditions_dic[idx]][arg][i].value
                        else:       
                            if s[preconditions_dic[idx]][arg][idx_row_prec] == s[preconditions_dic[idx+1]][arg][idx_row_next]:
                                params[par.name] = s[preconditions_dic[idx]][arg][idx_row_prec].value
                            else:
                                for par in a.params:
                                    params[par.name] = None
                                not_found = True
        #TODO: check for actions with parameters not used in preconditions (if it's a correctly defined FOND problem)
        if len(params) > 0:
            valid_action = True
            for p in params:
                if not params[p]: valid_action = False
            if not not_found and valid_action:
                new_state = init.copy()
                for e in a.effects:
                    # print(type(e[1])) #TODO: actions execution
                    # Vedere se l'effetto è positivo o negativo
                    # rimuovere i neg. e aggiungere i positivi
                    # init.add(list(Predicates))
                    if e[0] == 1.0: # non probabilistico
                        args = []
                        for p in e[1].predicate.args:
                            args.append(Term.constant(params[p]))
                        # print(e[1].is_positive())
                        if e[1].is_positive():
                            # print(f"added {e[1].predicate.name} -> {list(map(str,args))}")
                            new_state.add(Predicate(e[1].predicate.name, args))
                            # print(list(map(str,new_state)))
                        else:
                            # print(f"removed {e[1].predicate.name} -> {list(map(str,args))}")
                           
                            new_state.remove(Predicate(e[1].predicate.name, args))
                possible_path[a] = new_state


        # else:
        #     if actuable:
        #         for e in a.effects:
        #             print(e) #TODO: actions execution

        # print(list(map(str,new_state))) #stato corrente
        # print(params)

        
        

    return possible_path

            
           
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
            return False
    #check goal predicates: name and airty
    for g in problem.goal:
        if not g.name in domain_predicates:
            print(f"Error: predicate {g.name} of goal state not defined in domain")
            return False
        elif not g.arity == domain_predicates[g.name]:
            print(f"Mismatch airty of predicate {g.name} in goal")
            return False

    #TODO: check if init args are defined in object
    return True
# class State:

if __name__ == '__main__':

    args = parse()

    domain  = PDDLParser.parse(args.domain)         # Vedi classe Domain
    problem = PDDLParser.parse(args.problem)        # Vedi classe Problem  

    if semantic_check(domain, problem):
        print("semantic check passed!")
        #problem.init -> stato iniziale -> a1, a2, a3 
        s = get_possible_paths(problem, domain.operators, domain.predicates) # {action: [stato = set()]}
        node_idx = 0
        G = nx.Graph()
        G.add_node(1, state = problem.init)
        # node_idx += 1
        # for a in s:
        #     G.add_node(f"tuple(s[a]) {a.name}")
        #     node_idx += 1

        # print(G.number_of_nodes())
        # for i in G.nodes.items():
        #     print(i)
        G.add_node(2, state = "bello")
        # G.add_edge("ciao","bello")
        print(list(map(str,G.nodes[1]['state'])))
        

#move-to(a,b) -> stato1
#move-to(a-c) -> stato2