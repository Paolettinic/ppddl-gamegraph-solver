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
from predicate import Predicate
from term import Term
import matplotlib.pyplot as plt


def parse():
    usage = 'python3 main.py <DOMAIN> <INSTANCE>'
    description = 'pypddl-parser is a PDDL parser built on top of ply.'
    parser = argparse.ArgumentParser(usage=usage, description=description)

    parser.add_argument('domain',  type=str, help='path to PDDL domain file')
    parser.add_argument('problem', type=str, help='path to PDDL problem file')

    return parser.parse_args()

def find_all(element, array):
    return [i for i, x in enumerate(array) if x == element]

def is_sub_dictionary(dictionary1, dictionary2):
    matching = True
    assert len(dictionary1) <= len(dictionary2)
    for key in dictionary1:
        if matching:
            if key in dictionary2:
                matching = dictionary1[key] == dictionary2[key]
            else:
                return False
    return matching

def same_dictionary_different_values(dictionary1,dictionary2):
    if not len(dictionary1) == len(dictionary2): return False
    for key in dictionary1:
        if not key in dictionary2:
            return False
        else:
            if dictionary1[key] == dictionary2[key]:
                return False
    return True
        

def has_no_common_keys(dictionary1, dictionary2):
    for key in dictionary1:
        if key in dictionary2:
            return False
    return True

def apply_effects(current_state,effect):
    arguments = []
    new_state = current_state.copy()

    for p in effect.predicate.args:
        arguments.append(Term.constant(p.value))

    if effect.is_positive():
        new_state.add(Predicate(effect.predicate.name, arguments))
    else:
        new_state.remove(Predicate(effect.predicate.name, arguments))
    
    return new_state


def get_possible_paths(init, actions): 

    possible_path = {} #{action -> Action : stato_finale -> list(Predicates)}

    for a in actions:

        print(f"_______{a.name}_________")
        params = {}
        for par in a.params:
            params[par.name] = []

        sorted_preconditions = sorted(a.preconditions, key=lambda x: x.predicate.arity)
        actuable = True
        has_singular_term = False
        #s = {precondizione1: {arg1: [valori],arg2[valori]},precondizione2: {arg1: [valori],arg2[valori]}}  
        s = {}

        for p in sorted_preconditions: #TODO: put this into a function and return immediately if not actuable
            if actuable:
                if p.predicate.arity == 0:
                    has_singular_term = True
                    actuable = p.predicate.name in map(str,init)
                    s[p.predicate.name] = {}
                    
                else:
                    
                    s[p.predicate.name] = []

                    for pred in init:
                        if p.predicate.name == pred.name:

                            s[p.predicate.name] += [dict(zip(p.predicate.args,pred.args))]
       
        possible_parameters = []

        if actuable:
            for prec in s: #v-at road
                if len(s[prec]) > 0: # not-flattire 
                    if len(possible_parameters) > 0:
                        if not has_no_common_keys(s[prec][0],possible_parameters[0]):
                            to_remove = []
                            to_add = []
                            for prec_params in s[prec]: #{?from: value ?to: value}
                                for item in possible_parameters:   
                                    if is_sub_dictionary(item,prec_params):
                                        if not item in to_remove:
                                            to_remove.append(item) 
                                        if not prec_params in to_add:
                                            to_add.append(prec_params)
                                    else:
                                        if same_dictionary_different_values(item,prec_params):
                                            if not item in to_remove:
                                                to_remove.append(item)
                            for i in to_remove:
                                possible_parameters.remove(i)
                            for i in to_add:
                                possible_parameters.append(i)
                        else: # add all possible values to each dictionary in possible parameters
                            for item in possible_parameters:
                                for new_items in s[prec]:
                                    item.update(new_items)
                    else:
                        possible_parameters += [x for x in s[prec]]
                        
            ## UNCOMMENT THESE LINES TO SEE FORMATTED POSSIBLE PARAMS.
            # for p in possible_parameters:
            #     for arg in p:
            #         print(arg,"\t",str(p[arg]))
            
            if len(possible_parameters) > 0:
                for p_p in possible_parameters:
                #     # print(p_p) -> {"from": val, "to": val}
                    new_states = []

                    for probability, effect in a.effects:
                        new_state = init.copy()
                        for e in effect:
                            arguments = []

                            for p in e.predicate.args:
                                arguments.append(Term.constant(p_p[p].value))

                            if e.is_positive():
                                new_state.add(Predicate(e.predicate.name, arguments))
                            else:
                                new_state.remove(Predicate(e.predicate.name, arguments))

                        new_states.append({"p":probability, "s":new_state})

                    possible_path[f"{a.name}({str({k : v.value for k,v in p_p.items()})})"] = new_states
            else:
                if len(a.params) == 0 and has_singular_term and actuable:
                    new_states = []

                    for probability, effect in a.effects:
                        new_state = init.copy()
                        for e in effect:
                            if e.is_positive():
                                new_state.add(Predicate(e.predicate.name))
                            else:
                                new_state.remove(Predicate(e.predicate.name))

                        new_states.append({"p":probability, "s":new_state})

                    possible_path[f"{a.name}()"] = new_states       

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


def create_graph( graph : nx.Graph, actions, current, current_index, to_be_visited, visited): #graph [0] -> init , to_be_visited [init]
    if len(to_be_visited) > 0:
        neighbors = get_possible_paths(current, actions) #[{action(params)->string : state-> set()}]
        previous = current_index
        new_index = current_index
        for act in neighbors:
            new_state = neighbors[act]
            if not new_state in visited:
                new_index += 1
                graph.add_node(new_index, state = new_state, type = "avg") #TODO add type max. avg 
                graph.add_edges_from( [(previous ,new_index, {"action": act})] )
                to_be_visited.append(new_index)
            else:
                #TODO: nodo = visited[new_state]
                #TODO: add_edges_from([(previous, nodo, {"action": act})]) | add_edge(previous, nodo, action = act)
                pass
        current_index = to_be_visited.pop()
        current = graph.nodes[current_index]['state']
        visited.append({current: current_index})

        return create_graph(graph,actions,current,current_index,to_be_visited,visited)
    else:
        return graph

if __name__ == '__main__':

    args = parse()

    domain  = PDDLParser.parse(args.domain)         # Vedi classe Domain
    problem = PDDLParser.parse(args.problem)        # Vedi classe Problem  
    # for a in domain.operators:
    #     print(a)
    get_possible_paths(problem.init, domain.operators)
    # if semantic_check(domain, problem):
    #     print("semantic check passed!")
    #     #problem.init -> stato iniziale -> a1, a2, a3 
    #     to_be_visited = []

    #     node_idx = 0
    #     G = nx.Graph()
    #     G.add_node(node_idx, state = problem.init)
    #     to_be_visited.append(node_idx)
    #     visited_nodes = []
    #     visited_nodes.append(problem.init)
    #     g = create_graph( G, domain.operators, problem.init, node_idx, to_be_visited, visited_nodes)
        
    #     nx.draw(g, with_labels=True, font_weight='bold')

        # current_node = to_be_visited.pop()
        # s = get_possible_paths(G[current_node]["state"], domain.operators)
        # for action in s:
        #     G.add_node(node_idx, state = s[action])
        #     G.add_edge((current_node,node_idx,{"action": action }))
        #     node_idx += 1
        # while len(to_be_visited) > 0:
            



"""
procedure DFS_iterative(G, v) is
    let S be a stack
    S.push(iterator of G.adjacentEdges(v))
    while S is not empty do
        if S.peek().hasNext() then
            w = S.peek().next()
            if w is not labeled as discovered then
                label w as discovered
                S.push(iterator of G.adjacentEdges(w))
        else
            S.pop() 
"""


