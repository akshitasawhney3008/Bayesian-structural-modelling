import math
import networkx as nx
import numpy as np
import random
from collections import OrderedDict
import pandas as pd
import matplotlib.pyplot as plt


def p_x(m, val1, protein_data1):
    count_mx = 0
    for i in range(len(protein_data1)):
        if protein_data1[i] == val1:
            count_mx = count_mx + 1
    return count_mx / m


def p_y(m, val2, protein_data2):
    count_my = 0
    for i in range(len(protein_data2)):
        if protein_data2[i] == val2:
            count_my = count_my + 1
    return count_my / m


def p_x_y(m, val1, val2, protein_data1, protein_data2):
    count_mxy = 0
    for i in range(len(protein_data1)):
        if protein_data1[i] == val1 and protein_data2[i] == val2:
            count_mxy = count_mxy + 1
    return count_mxy/m


def i_x_y(m, protein_data1, protein_data2):
    summation = 0
    list_of_arity = [[1,1], [1,2], [2,1], [2,2]]
    for lst in list_of_arity:
        pxy = p_x_y(m, lst[0],lst[1], protein_data1, protein_data2)
        px = p_x(m, lst[0], protein_data1)
        py = p_y(m, lst[1], protein_data2)
        if px == 0 or py == 0 or pxy == 0:
            ixy = 0
        else:
            ixy = pxy * math.log(pxy/(px*py))
        summation = summation + ixy
    return summation


def h_x_y(m, protein_data1):
    summation = 0
    for i in range(1, 3):
        summation = summation + (p_x(m, i, protein_data1) * math.log(p_x(m, i, protein_data1)))
    return summation


def connected_nodes(graphob):
    list_of_edges = graphob.edges
    list_of_edges = list(set(sum(list_of_edges, ())))
    return len(list_of_edges)



def bic_score(graphob, protein_data1, protein_data2):
    print('Calculating BIC Score..')
    m = len(protein_data1)
    #bic = m * i_x_y(m, protein_data1, protein_data2) - m * h_x_y(m, protein_data1) - ((math.log(m)/2)*(nodes-connected_nodes(graphob)))
    bic = m * i_x_y(m, protein_data1, protein_data2) - m * h_x_y(m, protein_data1) - ((math.log(m)/2)*connected_nodes(graphob))
    return bic


def select_action(random_no):
    if random_no >= 0 and random_no < 0.33:
        return 1
    elif random_no >= 0.33 and random_no < 0.66:
        return 2
    elif random_no >= 0.66 and random_no <= 1:
        return 3


def add_edge(node1, node2, graphob, protein1data, protein2data, bic):
    print('Add edge..')
    if graphob.has_edge(node1, node2) or graphob.has_edge(node2, node1):
        return bic
    else:
        graphob.add_edge(node1, node2)
        list_of_edges = list(nx.simple_cycles(graphob))
        if not list_of_edges:
            bic1 = bic_score(graphob, protein1data, protein2data)
            bic1 = bic + bic1
            if bic1 < bic:
                graphob.remove_edge(node1, node2)
                return bic
            else:
                return bic1

        else:
            graphob.remove_edge(node1, node2)
            return bic


def delete_edge(node1, node2, graphob, protein1data, protein2data, bic):
    print('Delete edge..')
    if graphob.has_edge(node1, node2):
        graphob.remove_edge(node1, node2)
        bic1 = bic_score(graphob, protein1data, protein2data)
        bic1 = bic - bic1
        if bic1 < bic:
            graphob.add_edge(node1, node2)
            return bic
        else:
            return bic1
    elif graphob.has_edge(node2, node1):
        graphob.remove_edge(node2, node1)
        bic1 = bic_score(graphob, protein1data, protein2data)
        bic1 = bic - bic1
        if bic1 < bic:
            graphob.add_edge(node1, node2)
            return bic
        else:
            return bic1
    else:
        return bic


def reverse_edge(node1, node2, graphob, protein1data, protein2data, bic):
    print('Reverse edge..')
    if graphob.has_edge(node1, node2):
        graphob.remove_edge(node1, node2)
        graphob.add_edge(node2, node1)
        list_of_edges = list(nx.simple_cycles(graphob))
        if not list_of_edges:
            bic1 = bic_score(graphob, protein1data, protein2data)
            bic1 = bic + bic1
            if bic1 < bic:
                graphob.remove_edge(node2, node1)
                graphob.add_edge(node1, node2)
                return bic
            else:
                return bic1
        else:
            graphob.remove_edge(node2, node1)
            graphob.add_edge(node1, node2)
            return bic
    elif graphob.has_edge(node2, node1):
        graphob.remove_edge(node2, node1)
        graphob.add_edge(node1, node2)
        list_of_edges = list(nx.simple_cycles(graphob))
        if not list_of_edges:
            bic1 = bic_score(graphob, protein1data, protein2data)
            bic1 = bic + bic1
            if bic1 < bic:
                graphob.remove_edge(node1, node2)
                graphob.add_edge(node2, node1)
                return bic
            else:
                return bic1
        else:
            graphob.remove_edge(node1, node2)
            graphob.add_edge(node2, node1)
            return bic
    else:
        return bic


file_read = np.loadtxt('final1.txt', delimiter=',',  skiprows=1)
file_read = file_read.transpose()
list_of_final_graphs = []
for i in range(100):
    # file_read = np.array([[1, 1, 2, 1], [1, 2, 2, 1], [1, 1, 1, 1], [1, 2, 2, 2], [2, 2, 1, 1]])
    # file_read = file_read.transpose()
    # nodes = len(file_read)
    # graphob = nx.fast_gnp_random_graph(nodes, 0.5, directed=True)
    # while (len(list(nx.simple_cycles(graphob))) != 0):
    #     graphob = nx.fast_gnp_random_graph(nodes, 0.5, directed=True)
    # list_of_edges = graphob.edges

    prob_of_edge = 0.25
    nodes = len(file_read)
    graphob = nx.fast_gnp_random_graph(nodes, prob_of_edge, directed=True)
    print('Before while')
    while(len(list(nx.simple_cycles(graphob))) != 0):
        graphob = nx.fast_gnp_random_graph(nodes, prob_of_edge, directed=True)
    print('After while')
    list_of_edges = graphob.edges
    # graphob = nx.Graph()
    # graphob.add_edges_from([(1, 4), (3, 4), (4, 2)])
    # list_of_edges = [[1, 4], [3, 4], [4, 2]]
    bic = 0
    for edge in list_of_edges:
       bic = bic + bic_score(graphob, file_read[edge[0]-1], file_read[edge[1]-1])


    for j in range(10000):
        print('Performing random operations..')
        random_no = random.random()
        case = select_action(random_no)
        if case == 1:
            protein1 = random.randint(0, nodes-1)
            protein2 = random.randint(0, nodes-1)
            while(protein1 == protein2):
                protein2 = random.randint(1,nodes)
            bic = add_edge(protein1, protein2, graphob, file_read[protein1-1], file_read[protein2-1], bic)
        if case == 2:
            protein1 = random.randint(0, nodes-1)
            protein2 = random.randint(0, nodes-1)
            while (protein1 == protein2):
                protein2 = random.randint(0, nodes-1)
            bic = delete_edge(protein1, protein2, graphob, file_read[protein1-1], file_read[protein2-1], bic)
        if case == 3:
            protein1 = random.randint(0, nodes-1)
            protein2 = random.randint(0, nodes-1)
            while (protein1 == protein2):
                protein2 = random.randint(0, nodes-1)
            bic = reverse_edge(protein1, protein2, graphob, file_read[protein1-1], file_read[protein2-1], bic)
    final_graph = []
    for (u, v) in graphob.edges():
        edge1 = []
        edge1.append(u)
        edge1.append(v)
        final_graph.append(edge1)
    list_of_final_graphs.append(list(graphob.edges))


print('Generating concensus among results..')
dict_of_edges = {}
probability_threshold = 0.10
list_of_final_graphs = list((sum(list_of_final_graphs, [])))
distinct_edges = list(set(list_of_final_graphs))
for edge in distinct_edges:
    dict_of_edges[edge] = list_of_final_graphs.count(edge)
dict_of_edges = OrderedDict(sorted(dict_of_edges.items(), key=lambda t: t[1], reverse=True))

list_of_edge_thresh = {}
edge_list = []
G=nx.DiGraph()
for key,value in dict_of_edges.items():
    if value/100 >= probability_threshold:
        if len(list(nx.simple_cycles(G))) == 0:
            list_of_edge_thresh[key] = value
            G.add_edge(*key)

print(G.edges)
print(list_of_edge_thresh)