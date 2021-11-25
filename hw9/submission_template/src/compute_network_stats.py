import argparse
import networkx as nx
import json

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input')
    parser.add_argument('-o', '--output')
    args = parser.parse_args()
    
    G = nx.Graph()
    
    result = {
        'most_connected_by_num': [],
        'most_connected_by_weight': [],
        'most_central_by_betweenness': []
    }

    with open(args.input) as f:
        net = json.load(f)

    for n in net:
        for e in net[n]:
            G.add_edge(n,e, weight=net[n][e])
    
    result['most_connected_by_num'] = [k for k,_ in sorted(G.degree(), key=lambda x: x[1], reverse=True)[:3]]

    result['most_connected_by_weight'] = [k for k,_ in sorted(G.degree(weight='weight'), key=lambda x: x[1], reverse=True)[:3]]

    result['most_central_by_betweenness'] = [k for k,_ in sorted(nx.algorithms.betweenness_centrality(G).items(), key=lambda x: x[1], reverse=True)[:3]]

    with open(args.output, 'w') as f:
        json.dump(result, f)

if __name__ == '__main__':
    main()
