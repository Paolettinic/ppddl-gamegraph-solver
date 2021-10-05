
import argparse
import networkx as nx
import matplotlib.pyplot as plt
from parser.pddlparser import PDDLParser
from parser.predicate import Predicate
from parser.term import Term
from solver.solver import solve


def parse():
    usage = 'python3 main.py <DOMAIN> <INSTANCE>'
    description = 'ppddl-gamegraph-solver is a PPDDL to game graph converter, based on ply and solved with simplex method.'
    parser = argparse.ArgumentParser(usage=usage, description=description)

    parser.add_argument('domain',  type=str, help='path to PPDDL domain file')
    parser.add_argument('problem', type=str, help='path to PPDDL problem file')

    return parser.parse_args()


            
           
def semantic_check(domain, problem) :
    # check if predicates match with types
    domain_predicates = {}

    for p in domain.predicates:
        domain_predicates[p.name] = p.arity
        for t in p.args:
            if not t.type in domain.types:
                print(f"Error: {t.type} not defined in domain types")
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
    

def get_possible_paths(init, actions): 

    def apply_effects(current_state : set ,effects : list, possible_parameter: list):
        
        new_state = current_state.copy()

        for e in effects:
            arguments = []

            for p in e.predicate.args:
                arguments.append(Term.constant(possible_parameter[p].value))

            if e.is_positive():
                new_state.add(Predicate(e.predicate.name, arguments))
            else:
                predicate = Predicate(e.predicate.name, arguments)
                if predicate in new_state:
                    new_state.remove(predicate)
        
        return new_state

    def preconditions_natural_join(preconditions1, preconditions2):

        def match(dict1, dict2, join_on):
            return all(dict1[j] == dict2[j] for j in join_on)

        t1_set = set(preconditions1[0]) if len(preconditions1) > 0 else set()
        t2_set = set(preconditions2[0]) if len(preconditions2) > 0 else set()

        join_on = t1_set & t2_set #Common keys
        diff = t2_set - join_on #Difference

        results = []
        for prec1 in preconditions1:
            for prec2 in preconditions2:
                if match(prec1, prec2,join_on):
                    row = prec1.copy()
                    for d in diff:
                        row.update({d : prec2[d]})
                    results.append(row)
        return results


    possible_path = {} #{action -> str : stato_finale -> list(Predicates)}
    for a in actions:
        # print(f"________{a.name}__________")
        actuable = True
        #preconditions_dic = {precondizione1: {arg1: [valori],arg2[valori]},precondizione2: {arg1: [valori],arg2[valori]}}  
        preconditions_dic = {}

        for p in a.preconditions:
            if actuable:
                if p.predicate.arity == 0:
                    actuable = p.predicate.name in map(str,init)
                    # preconditions_dic[p.predicate.name] = []
                    
                else:
                    preconditions_dic[p.predicate.name] = []

                    for pred in init:
                        if p.predicate.name == pred.name:
                            preconditions_dic[p.predicate.name] += [dict(zip(p.predicate.args,pred.args))]
        possible_parameters = [{}]
        if actuable:
            for name in preconditions_dic:
                possible_parameters = preconditions_natural_join(possible_parameters,preconditions_dic[name])
                # print(possible_parameters)
                if possible_parameters == []:
                    break


            
            if len(possible_parameters) > 0:
                for possible_parameter in possible_parameters:
                    new_states = []

                    for probability, effect in a.effects:
                        new_state = apply_effects(init,effect,possible_parameter)

                        new_states.append({"p":probability, "s":new_state})
                        func_args_str = str({k : v.value for k,v in possible_parameter.items()}) if len(possible_parameter.items()) > 0 else ""
                    possible_path[f"{a.name}({func_args_str})"] = new_states
    for p in possible_path:
        print(p)
    return possible_path


def create_graph( graph : nx.Graph, actions, current : set, current_index, goal_terms, visited = []): #graph [0] -> init , to_be_visited [init]

    visited.append(current)

    path = get_possible_paths(current,actions)

    if len(path) == 0:
        graph.nodes[current_index]["type"] = "sink"
        return

    for actuable_action in path:
        new_index = max(graph) + 1
        if len(path[actuable_action]) > 1: #Probabilistico
            
            avg_index = new_index
            graph.add_node(avg_index, type = "avg") 
            graph.add_edge(current_index ,avg_index,weight=1.0,action = actuable_action)
            to_be_visited = []
            for state in path[actuable_action]:
                
                #Check if is a goal state
                is_goal = True
                for g in goal_terms:
                    if g not in state['s']:
                        is_goal = False

                if is_goal:
                    if min(graph) == 0:
                        graph.add_node(-1, state = goal_terms, type = "goal")
                    graph.add_edge(avg_index, -1, weight=state['p'],action = actuable_action)
 
                else:
                    new_index = max(graph) + 1

                    if state['s'] not in visited:
                    
                        graph.add_node(new_index, state = state['s'], type = "max") 
                        graph.add_edge(avg_index ,new_index,weight=state['p'],action = actuable_action)
                        to_be_visited.append((new_index,state['s']))
                    else:
                        for node in graph: 
                            if "state" in graph.nodes[node]: #Avoids avg nodes
                                if state["s"] == graph.nodes[node]["state"]:
                                    graph.add_edge(avg_index ,int(node) ,weight=state['p'],action = actuable_action)
                                    break
                    for new_index, new_state in to_be_visited:
                        create_graph( graph, actions, new_state, new_index, goal_terms, visited)
                    to_be_visited = [] #Not needed, but just in case...

        else: #Deterministico
            #Check if is a goal state
            state = path[actuable_action][0]
            is_goal = True
            for g in goal_terms:
                if g not in state['s']:
                    is_goal = False

            if is_goal:
                if min(graph) == 0:
                    graph.add_node(-1, state = goal_terms, type = "goal")
                graph.add_edge(current_index ,-1,weight=1.0,action = actuable_action)
            else:
                new_state = state['s']
                if new_state not in visited:
                    graph.add_node(new_index, state = new_state , type = "max") 
                    graph.add_edge(current_index ,new_index, weight=1.0,action = actuable_action)
                    
                    create_graph( graph, actions, new_state, new_index, goal_terms, visited)
                else:
                    for node in graph: #TODO: cambiare in while
                        if "state" in graph.nodes[node]:
                            if new_state == graph.nodes[node]["state"]:
                                graph.add_edge(current_index ,int(node) , weight=1.0,action = actuable_action)
                                break


if __name__ == '__main__':

    args = parse()

    domain  = PDDLParser.parse(args.domain)         # Vedi classe Domain
    problem = PDDLParser.parse(args.problem)        # Vedi classe Problem  

    # print(get_possible_paths(problem.init, domain.operators))
    if semantic_check(domain, problem):
        print("semantic check passed!")
        #problem.init -> stato iniziale -> a1, a2, a3 
        node_idx = 0
        G = nx.MultiDiGraph()
        G.add_node(node_idx, state = problem.init,type="max")

        create_graph( G, domain.operators, problem.init, node_idx, problem.goal)

        nodes_avg = []
        nodes_max = []
        nodes_goal = []
        nodes_start = [0]
        nodes_sink = []
        for x,y in G.nodes(data=True):
            if y['type']=='avg': nodes_avg.append(x)
            if y['type']=='max': nodes_max.append(x)
            if y['type']=='sink': nodes_sink.append(x)
            if y['type']=='goal': nodes_goal.append(x)
        pos = nx.kamada_kawai_layout(G)
        nx.draw_networkx_nodes(G,pos,nodelist=nodes_max,node_color='#00facc')
        nx.draw_networkx_nodes(G,pos,nodelist=nodes_avg,node_color='#bbff00')
        nx.draw_networkx_nodes(G,pos,nodelist=nodes_goal,node_color='#ff00aa')
        nx.draw_networkx_nodes(G,pos,nodelist=nodes_start,node_color='#ff0000')
        nx.draw_networkx_nodes(G,pos,nodelist=nodes_sink,node_color='#000000')
        nx.draw_networkx_edges(G,pos)
        plt.show()
        solution = solve(G)["x"]
        print(solution)
        strategy = {}
        for x in nodes_max:

            next_state = -1
            max_val = -1
            for n in G.neighbors(x):
                if solution[n] > max_val:
                    max_val = solution[n]
                    next_state = n 
            action = G[x][next_state][0]["action"]
            strategy[x] = action
        for s in strategy:
            print(f"{s} : strategy: {strategy[s]}")
