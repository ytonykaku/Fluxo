import networkx as nx
import matplotlib.pyplot as plt

def main():
    graph = open("graph.txt")
    G = nx.DiGraph()

    for line in graph.readlines():
        node_a, node_b, weight = line.split()
        G.add_weighted_edges_from([(node_a, node_b, int(weight))])
    graph.close()

    flow = algorithmFordFulkerson(G, "S", "T")
    print(f'Max Flow for given graph: {flow}')
    drawGraph(G)

def makeGraph(G):
    AuxG = nx.DiGraph()

    for i in G:
        for j in G[i]:
            AuxG.add_node(i)
            AuxG.add_node(j)
            AuxG.add_edge(i, j, weight=G[i][j]["weight"])

    return AuxG

def maxFlowPath(G, path):
    flow = float('inf')
    for i in range(len(path)-1):
        lowestFlow = G[path[i]][path[i+1]]['weight']

        if lowestFlow < flow:
            flow = lowestFlow

    return flow


def algorithmFordFulkerson(G, source, target):
    Graph = makeGraph(G)
    flow = 0

    if(nx.has_path(Graph, source, target)):
        path = nx.shortest_path(G, source, target)
    else:
        print("No valid paths between the nodes")
        return

    while(nx.has_path(Graph, source, target)):
        maxpathFlow = maxFlowPath(Graph, path)

        for i in range(len(path)-1):
            Graph[path[i]][path[i+1]]["weight"] -= maxpathFlow

            if (Graph[path[i]][path[i+1]]["weight"] == 0):
                Graph.remove_edge(path[i], path[i+1])
                flow += G[path[i]][path[i+1]]["weight"]

            Graph.add_edge(path[i+1], path[i], weight=maxpathFlow)

        if(nx.has_path(Graph, source, target)):
            path = nx.shortest_path(Graph, source, target)

    return flow

def drawGraph(G):
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True)
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    plt.show()

main()