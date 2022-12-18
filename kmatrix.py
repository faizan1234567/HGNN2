import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import argparse

def read_args():
    '''command line args'''
    parser = argparse.ArgumentParser(description = "Commnad line args for genearting K matrix")
    parser.add_argument('--nodes_csv', type= str, help = "nodes csv file path")
    parser.add_argument('--edges_csv', type = str, help= "edges csv file path")
    parser.add_argument('--k', type = int, help= "set k value, user defined")
    return parser.parse_args()

def df_tolist(df):
  ''' convert to list from dataframe function
  df: data frame 
  return:
  source_nodes, target_nodes: list of two dataframes
  '''
  # list of soruce nodes
  source_nodes = df.iloc[:, 0].tolist()

  # target nodes --> list
  target_nodes = df.iloc[:, 1].tolist()

  return source_nodes, target_nodes

def calculateLength(a, b, spl):
  '''function to calculate nodes length or distance
  args:
  a : node a source
  b : node b target
  nodes_list: list of nodes in a graph
  edges_data: edges information
  return length between a and b'''
  try:
    return spl[a][b]
  except KeyError:
    return 0
  return spl[a][b]

def save_data_csv(K, nodes_list):
  '''convert to graph data to a csv file for graph generation
  Args: K (numpy array of graph relations) 2708x2708
        nodes_list: (list) of nodes
  '''
  Kmatrix = {}
  for i, cols in enumerate(nodes_list):
    Kmatrix[f"{cols}"] = K[:, i].tolist()
  
  graph_data = pd.DataFrame(Kmatrix, index = nodes_list)
  graph_data.to_csv("grah_data.csv", sep='\t')
  

def main():
    '''function responsible for running other functions in 
    a modular way'''
    args = read_args()
    edges_data = pd.read_csv(args.edges_csv)
    nodes_data = pd.read_csv(args.nodes_csv)
    nodes_list = nodes_data.iloc[:, 0].tolist()
    num_nodes = len(nodes_list)
    source_nodes, target_nodes = df_tolist(edges_data)
    source_nodes_length = len(source_nodes)
    # K matrix with all zeros entries
    
    K = np.zeros((num_nodes, num_nodes), dtype = np.int32)
    # create a graph G using network x library
    G = nx.Graph()
    G.add_nodes_from(nodes_list)
    edgeInfo = list(zip(edges_data.Source, edges_data.Target))
    G.add_edges_from(edgeInfo)
    #shortest path
    sp = dict(nx.all_pairs_shortest_path(G))
    #sp[a][b]
    #shortest path length
    spl = dict(nx.all_pairs_shortest_path_length(G))
    if args.k:
        k = args.k
        for i, row in enumerate(nodes_list):
            for j, col in enumerate(nodes_list):
                length = calculateLength(row, col, spl)
                if length <= k and length !=0:
                    K[i, j] = 1
                else:
                    K[i, j] = 0
    print(f'K matrix for {args.k} hops: {K}')
    print(f"K matrix has a shape of {K.shape}")

    print("now saving to csv file...")
    save_data_csv(K, nodes_list)
    print("finished!!!")

    return K

if __name__ == "__main__":
    K = main()


                