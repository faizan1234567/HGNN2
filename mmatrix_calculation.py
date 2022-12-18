"""M Matrix calcualtion script
In each hyperedge node degree will be calculated, based on that avearge node degree
will be determined

M matrix will be obtained by used the following condition.

M = {1 dv >= dvavg
     0 otherwise
M is a vector of node R^n"""

import pandas as pd
import numpy as np
import hypernetx as hnx
from hypergraph_generation import graph_data
from configs import config





def generate_hypergraph(graph_connection_dict = None):
    """generate hypergrah connection based on K value
    
    Args:
    graph_connection: dict
    a connection dictionary between nodes and hyperedegs, default None
    
    Return:
    H: hypergraph object holding a hypergrah"""

    H = hnx.Hypergraph(graph_connection_dict)
    return H

def m_matrix_and_avg_degree_calculation(hypergraph, H):
    """caluclate M matrix and node avearge degree
    
    Args:
    hypergraph: dict
    
    Return:
    data: dict
    H: hnx.gragh
    a dictionary hodling each hyperedge average degree and a M vector"""
    data = {}
    for edge in hypergraph.keys():
        nodes = hypergraph[edge]
        edge_nodes = len(nodes)
        node_degrees =[]
        for node in nodes:
            node_degree = H.degree(node, s=1)
            node_degrees.append(node_degree)
    
    average_degree = sum(node_degrees)/edge_nodes
    m_vector = (np.array(node_degrees) >= average_degree) * 1

    data[edge] = {'Average degree': average_degree, "M vector": m_vector}
    return data





def main():
    hypergraph_data = pd.read_csv(config.graph_data)
    print('creating graph data')
    hypergraph_connections = graph_data(hypergraph_data)
    print('generating hypergraph from the data.')
    H = generate_hypergraph(hypergraph_connections)
    hypergraph = H.incidence_dict
    print('Number of Hyperedges: {}'.format(len(hypergraph)))
    print('-'*40)
    print('Now calculating M matrix and nodes average degrees..')

    data = m_matrix_and_avg_degree_calculation(hypergraph, H)
    print('Inspecting data: showing edge E473 average degree and M vector')
    print(data['E473']['M vector'])
    print(data['E473']['Average degree'])

    print('done!!!')


if __name__ == "__main__":
    main()

