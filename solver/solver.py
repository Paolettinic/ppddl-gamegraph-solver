import numpy as np
import networkx as nx
from scipy.optimize import linprog

# TODO: check for None 
def generate_matrices(graph : nx.Graph):
    A_ub = []
    b_ub = []
    A_eq = []
    b_eq = []
    for node in graph:
        # v(i) >= v(j) ----> v(j) - v(i) <= 0
        if graph.nodes[node]["type"] == "max":
            for j in graph.neighbors(node):
                Ai = np.zeros(len(graph))
                Ai[node] = -1.0
                Ai[j] = 1.0
                A_ub.append(Ai.copy()) 
                b_ub.append(0.0)
        # sum(Pj*v(j),Pk*v(k),...) - v(i) <= 0
        elif graph.nodes[node]["type"] == "avg": 
            Ai = np.zeros(len(graph))
            Ai[node] = -1.0 
            prob = 0
            for j in graph.neighbors(node):
                
                for e in graph[node][j]:
                    prob += graph[node][j][e]["weight"]
                if len(graph[node][j]) > 1:
                    print(prob)
                Ai[j] = prob

            A_ub.append(Ai.copy())
            b_ub.append(0.0)
        #v(i) = 0
        elif graph.nodes[node]["type"] == "sink":
            Ai = np.zeros(len(graph))
            Ai[node] = 1.0
            A_eq.append(Ai.copy())
            b_eq.append(0.0)
        #v(i) = 1
        elif graph.nodes[node]["type"] == "goal":
            Ai = np.zeros(len(graph))
            Ai[node] = 1.0
            A_eq.append(Ai.copy())
            b_eq.append(1.0)

    return A_ub, b_ub, A_eq, b_eq

def solve(graph):
    c = np.ones(len(graph))
    A_ub, b_ub, A_eq, b_eq = generate_matrices(graph)
    return linprog(c = c, A_ub = A_ub, b_ub=b_ub, A_eq = A_eq, b_eq = b_eq,bounds=(0,1))
    

if __name__ == "__main__":
    c = [1.0,1.0]
    A_ub = [[-2.0,-3.0],[-3.0,-2.0]]
    b_ub = [0.0,0.0]
    x = linprog(c=c,A_ub = A_ub, b_ub = b_ub, bounds=(0,1), method="simplex")
    print(x)