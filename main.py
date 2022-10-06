import networkx as nx
import numpy.random as rnd
import itertools as it
# import pygraphviz as pgv
import matplotlib.pyplot as plt
from networkx.algorithms import bipartite
import json

from networkx.drawing.nx_pydot import graphviz_layout

edgeColor = "black"
nodeColor = "green"


def addNoorientedEdge(f_item, s_item, graph=None):
    graph.add_edge(f_item, s_item)
    graph.add_edge(s_item, f_item)


def addOrientedEdge(from_dot, to_dot, G):
    G.add_edge(from_dot, to_dot)


def createNode(G, name_of_dot):
    G.add_node(name_of_dot)


def deleteNode(G, name):
    G.remove_node(name)


def deleteEdge(G, dot1, dot2):
    G.remove_edge(dot1, dot2)


def info(G):
    dots = G.nodes()
    print('Nodes of graph - ', dots)
    edgs = G.edges()
    print('Edges of graph - ', edgs)
    if nx.is_planar(G):
        print('Graph is planar!')
        nx.draw(G, pos=nx.planar_layout(G), with_labels=True, node_size=1000, arrows=True, node_color='green')
        plt.show()
    else:
        print('Graph is not planar!')
        nx.draw(G, pos=nx.planar_layout(G), with_labels=True, node_size=1000, arrows=True, node_color='green')
    print("Amount of dots - " + str(len(dots)))
    print("Amount of edges - " + str(len(edgs)))
    print('')
    for dot in dots:
        info_dot(G, dot)
    print('Adjacency matrix: ')
    showMatrix(G)



def convertToTree(G):
    pos = graphviz_layout(G, prog="twopi")
    nx.draw(G, pos)
    plt.show()


def info_dot(G, name_dot):
    edges = G.edges()
    counter = 0
    for edge in edges:
        if name_dot in edge:
            counter += 1
    print(str(name_dot) + " dot have a " + str(counter) + " edges")


def getMatrix(G):
    matrix = []
    horizontalNodes = G.nodes()
    verticalNodes = G.nodes()
    edges = G.edges()
    counter = -1
    for node1 in horizontalNodes:
        counter += 1
        tempList = []
        for node2 in verticalNodes:
            check = (node1, node2)
            if check in edges:
                tempList.append(1)
            else:
                tempList.append(0)
        matrix.append(tempList)
    return matrix


def showMatrix(G):
    matrix = getMatrix(G)
    for pr in matrix:
        print(pr)


def getHamiltonCycles(G, curr, visited, path):
    matrix = getMatrix(G)
    path.append(curr)
    if len(path) == len(matrix):
        if matrix[path[0]][path[-1]] == 1:
            return True
        else:
            path.pop()
            return False
    visited[curr] = True
    for next in range(len(matrix)):
        if matrix[curr][next] == 1 and not visited[next]:
            if (getHamiltonCycles(G, next, visited, path)):
                return True
    visited[curr] = False
    path.pop()
    return False


def download(G, namefile):
    data = {'nodes': [], 'edges': []}
    name = namefile + '.json'
    dots = G.nodes
    edg = G.edges
    for dt in dots:
        data['nodes'].append(dt)
    for ed in edg:
        data['edges'].append(ed)
    with open(name, 'w') as outfile:
        json.dump(data, outfile)


def upload(G, namefile):
    name = namefile + '.json'
    with open(name) as json_file:
        data = json.load(json_file)
    nodes = data['nodes']
    edges = data['edges']
    for it in nodes:
        G.add_node(it)
    for it2 in edges:
        G.add_edge(it2[0], it2[1])
    nx.draw(G,
            node_color='green',
            node_size=1000,
            with_labels=True, arrows=True)
    plt.show()


def menu():
    global nodeColor, edgeColor
    G = nx.Graph()
    Grafs = []
    choice = 1

    node1 = ''
    node2 = ''
    while choice:
        print()
        print("1 - create node")
        print("2 - delete node")
        print("3 - create edge between nodes")
        print("4 - delete edge between nodes")
        print("5 - show hamilton cycles")
        print("6 - show diameter of the graf")
        print("7 - show radius of the graf")
        print("8 - show center of the graf")
        print("9 - show information about graph")
        print("10 - download graph")
        print("11 - upload graph")
        print("12 - change node color")
        print("13 - change edge color")
        print("14 - show Cartesian Product")
        print("15 - show Composition")
        print("16 - exit")
        print()
        choice = int(input("Enter choice "))
        if choice == 1:
            node1 = str(input('Enter name of node: '))
            G.add_node(node1)
            nx.draw(G,
                    node_color=nodeColor,
                    edge_color=edgeColor,
                    node_size=1000,
                    with_labels=True, arrows=True)
            plt.show()
        elif choice == 2:
            name = str(input('Enter name of node: '))
            if name in G.nodes:
                deleteNode(G, name)
                nx.draw(G, node_color=nodeColor,
                        edge_color=edgeColor, with_labels=True, node_size=1000, arrows=True)
                plt.show()
            else:
                print('Try again')
        elif choice == 3:
            node1 = str(input('Enter name of the first node: '))
            node2 = str(input('Enter name of the second node: '))
            if node1 in G.nodes and node2 in G.nodes:
                addNoorientedEdge(node1, node2, G)
                nx.draw(G,
                        node_color=nodeColor,
                        edge_color=edgeColor,
                        node_size=1000,
                        with_labels=True, arrows=True)
                plt.show()
            else:
                print('Try again! ')
        elif choice == 4:
            node1 = str(input('Enter name of the first node: '))
            node2 = str(input('Enter name of the second node: '))
            if node1 in G.nodes and node2 in G.nodes and (node1, node2) in G.edges:
                deleteEdge(G, node1, node2)
                nx.draw(G,
                        node_color=nodeColor,
                        edge_color=edgeColor,
                        node_size=1000,
                        with_labels=True, arrows=True)
                plt.show()
            else:
                print('Try again! ')
        elif choice == 5:
            matrix = getMatrix(G)
            for i in range(len(matrix)):
                path = []
                visited = [False] * len(matrix)
                getHamiltonCycles(G, i, visited, path)
                print(path)
        elif choice == 6:
            print("Diameter: ", nx.diameter(G))
        elif choice == 7:
            print("Radius: ", nx.radius(G))
        elif choice == 8:
            print("Center: ", list(nx.center(G)))
        elif choice == 9:
            info(G)
        elif choice == 10:
            name = str(input('Enter name of file: '))
            download(G, name)
        elif choice == 11:
            G = nx.Graph()
            name = str(input('Enter name of file: '))
            upload(G, name)
        elif choice == 12:
            nodeColor = input("enter color ")
            nx.draw(G,
                    node_color=nodeColor,
                    edge_color=edgeColor,
                    node_size=1000,
                    with_labels=True, arrows=True)
            plt.show()
        elif choice == 13:
            edgeColor = input("enter color ")
            nx.draw(G,
                    node_color=nodeColor,
                    edge_color=edgeColor,
                    node_size=1000,
                    with_labels=True, arrows=True)
            plt.show()
        elif choice == 14:
            H = nx.Graph()
            tempChoice = 1
            while tempChoice:
                print("1 - create node")
                print("2 - delete node")
                print("3 - create edge between nodes")
                print("4 - delete edge between nodes")
                print("5 - show result")
                tempChoice = int(input("enter temp choice "))
                if tempChoice == 1:
                    node1 = str(input('Enter name of node: '))
                    H.add_node(node1)
                    nx.draw(H,
                            node_color=nodeColor,
                            edge_color=edgeColor,
                            node_size=1000,
                            with_labels=True, arrows=True)
                    plt.show()
                elif tempChoice == 2:
                    name = str(input('Enter name of node: '))
                    if name in H.nodes:
                        deleteNode(H, name)
                        nx.draw(H, node_color=nodeColor,
                                edge_color=edgeColor, with_labels=True, node_size=1000, arrows=True)
                        plt.show()
                    else:
                        print('Try again')
                elif tempChoice == 3:
                    node1 = str(input('Enter name of the first node: '))
                    node2 = str(input('Enter name of the second node: '))
                    if node1 in H.nodes and node2 in H.nodes:
                        addNoorientedEdge(node1, node2, H)
                        nx.draw(H,
                                node_color=nodeColor,
                                edge_color=edgeColor,
                                node_size=1000,
                                with_labels=True, arrows=True)
                        plt.show()
                    else:
                        print('Try again! ')
                elif tempChoice == 4:
                    node1 = str(input('Enter name of the first node: '))
                    node2 = str(input('Enter name of the second node: '))
                    if node1 in H.nodes and node2 in H.nodes and (node1, node2) in H.edges:
                        deleteEdge(H, node1, node2)
                        nx.draw(H,
                                node_color=nodeColor,
                                edge_color=edgeColor,
                                node_size=1000,
                                with_labels=True, arrows=True)
                        plt.show()
                    else:
                        print('Try again! ')
                elif tempChoice == 5:
                    I = nx.cartesian_product(G, H)
                    nx.draw(I,
                            node_color=nodeColor,
                            edge_color=edgeColor,
                            node_size=1000,
                            with_labels=True, arrows=True)
                    plt.show()
                    break
        elif choice == 15:
            H = nx.Graph()
            tempChoice = 1
            while tempChoice:
                print("1 - create node")
                print("2 - delete node")
                print("3 - create edge between nodes")
                print("4 - delete edge between nodes")
                print("5 - show result")
                tempChoice = int(input("enter temp choice "))
                if tempChoice == 1:
                    node1 = str(input('Enter name of node: '))
                    H.add_node(node1)
                    nx.draw(H,
                            node_color=nodeColor,
                            edge_color=edgeColor,
                            node_size=1000,
                            with_labels=True, arrows=True)
                    plt.show()
                elif tempChoice == 2:
                    name = str(input('Enter name of node: '))
                    if name in H.nodes:
                        deleteNode(H, name)
                        nx.draw(H, node_color=nodeColor,
                                edge_color=edgeColor, with_labels=True, node_size=1000, arrows=True)
                        plt.show()
                    else:
                        print('Try again')
                elif tempChoice == 3:
                    node1 = str(input('Enter name of the first node: '))
                    node2 = str(input('Enter name of the second node: '))
                    if node1 in H.nodes and node2 in H.nodes:
                        addNoorientedEdge(node1, node2, H)
                        nx.draw(H,
                                node_color=nodeColor,
                                edge_color=edgeColor,
                                node_size=1000,
                                with_labels=True, arrows=True)
                        plt.show()
                    else:
                        print('Try again! ')
                elif tempChoice == 4:
                    node1 = str(input('Enter name of the first node: '))
                    node2 = str(input('Enter name of the second node: '))
                    if node1 in H.nodes and node2 in H.nodes and (node1, node2) in H.edges:
                        deleteEdge(H, node1, node2)
                        nx.draw(H,
                                node_color=nodeColor,
                                edge_color=edgeColor,
                                node_size=1000,
                                with_labels=True, arrows=True)
                        plt.show()
                    else:
                        print('Try again! ')
                elif tempChoice == 5:
                    I = nx.compose(G, H)
                    nx.draw(I,
                            node_color=nodeColor,
                            edge_color=edgeColor,
                            node_size=1000,
                            with_labels=True, arrows=True)
                    plt.show()
                    break;
        elif choice == 16:
            exit()

        else:
            print("Try again.")


menu()