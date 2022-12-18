import argparse
import matplotlib.pyplot as plt
import networkx as nx
import hypernetx as hnx
import pandas as pd

def read_args():
    ''' read commandline args'''
    parser = argparse.ArgumentParser()
    parser.add_argument("--graph", type = str, help= "graph data in csv file")
    parser.add_argument("--draw_detail", action= "store_true", help="draw hypergraph and show details")
    return parser.parse_args()

def graph_data(grah_data):
    """strore graph data into a dict
    Args: graph_csv(csv file) storing graph data
    return: graph connnection dictionary
    """
    graph_connection = {} 
    rows = grah_data.iloc[:, 0].tolist()
    cols = grah_data.columns.tolist()
    del cols[0]
    # interate over rows
    for i, row in enumerate(rows):
        record = []
        record.append(row)
        for j, col in enumerate(cols):
            if grah_data.iloc[i, j] == 1:
                record.append(int(col))
            else:
                pass
        graph_connection[f"E{i}"] = record

    #processing to delete some unwanted nodes
    keys = list(graph_connection.keys())
    for key in keys:
        len_ = len(graph_connection[key])
        if len_ == 1:
            del graph_connection[key]
    return graph_connection


def main():
    '''rest of the code goes here'''
    args = read_args()
    if args.graph:
        g_data = pd.read_csv(args.graph)
        print("generating graph connection dictionary!!")
        graph_connection = graph_data(g_data)
        print('done!!!\n')

        print("generating hypergraph now...")
        H = hnx.Hypergraph(graph_connection)
        print("done!!!")
        if args.draw_detail:
            # hnx.draw(H)
            print(f"number of nodes: {len(H.nodes)}")
            print(f"number of edges: {len(H.edges)}")
        print('finished.!!')
if __name__ == "__main__":
    main()