from math import ceil, floor
class Queue:
    def __init__(self, nodes=None):
        try:
            self.nodes = list(nodes)
        except:
            self.nodes = []
    def __iter__(self):
        return iter(self.nodes)
    def __len__(self):
        return len(self.nodes)
    def __str__(self):
        return str(list(self))
    def add(self, node):
        self.nodes.append(node); return node
    def get(self):
        return self.nodes[0]
    def pop(self):
        return self.nodes.pop(0)
    def has(self, node):
        return node in self.nodes
    
class noPathError(Exception):
    def __init__(self, graph, node1, node2, message = ""):
        self.message = message
        self.graph = graph
        self.node1 = node1
        self.node2 = node2
        super().__init__(self.message)
    def __str__(self):
        return f"No path between {self.node1} and {self.node2} in the following graph:\n{str(self.graph)} ({self.message})"

def strWidth(str):
    output = 0
    for line in str.strip().split("\n"):
        if(len(line.strip()) > output): output = len(line.strip())
    return output

def indent_multi_line_str(str, indentation="    ", end=""):
    if(type(indentation) == int):
        indentation = ' '*indentation
    output = ""
    for line in str.strip().split("\n"):
        output = output + indentation + line.strip() + end + "\n"
    return output

def box(str):
    output = f"┌{'-'*strWidth(str)}┐\n"
    for line in str.strip().split("\n"):
        output = f"{output}|{line}{' '*(strWidth(str)-len(line))}|\n"
    output = output + f"└{'-'*strWidth(str)}┘"
    return output

def table_to_str(table):
    output = ""
    colKeys = []
    colKeyWidth = 0
    valueWidth = 0
    for i in table:
        if(len(str(i).strip()) > valueWidth): valueWidth = len(str(i).strip())
        for j in table[i]:
            if type(table[i][j]) and table[i][j].is_integer():
                table[i][j] = int(table[i][j])
            if not j in colKeys: colKeys.append(j)
            if(len(str(j).strip()) > colKeyWidth): colKeyWidth = len(str(j).strip())
            if(len(str(table[i][j]).strip()) > valueWidth): valueWidth = len(str(table[i][j]).strip())


    for rowKey in table:
        output = f"{output}{rowKey}|"
        for key in table[rowKey]:
            value = table[rowKey][key]
            if not key in colKeys: colKeys.append(key)
            output = f"{output}{' '*floor((valueWidth-len(str(value)))/2)}{value}{' '*ceil((valueWidth-len(str(value)))/2)}|"
        output = f"{output}\n"
    topRow = ""
    for key in table:
        topRow = f"{topRow}{' '*floor((valueWidth-len(str(key)))/2)}{key}{' '*ceil((valueWidth-len(str(key)))/2)} "
    output = f"{' '*colKeyWidth} {topRow}\n{output}"

    return output

def two_value_table_to_str(table):
    output = ""
    keyWidth = 0
    valueWidth = 0
    for key in table:
        if(len(str(key).strip()) > keyWidth): keyWidth = len(str(key).strip())
        if(len(str(table[key]).strip()) > valueWidth): valueWidth = len(str(table[key]).strip())
        output = f"{output}{key}|{table[key]}\n"
    return output

class Graph:
    def __init__(self):
        self.nodes = set()
        self.adjacency_list = {}
        self.neighbor_matrix = {}
        #Basic algorithm safety precautions (joke)
        self._cost_of_becoming_skynet = 9999999.9
        self._cost_of_harming_humans = 9999999.9
        self._cost_of_destroying_world = float('inf')
        self._cost_of_changing_self = 999999.9
        

    def __str__(self):
        return f"""Nodes:
{self.nodes}
Adjacency list:
{two_value_table_to_str(self.adjacency_list)}
Adjacency matrix:
{table_to_str(self.neighbor_matrix)}"""

    def add_node(self, new_node):
        self.nodes.add(new_node)
        self.adjacency_list.update({new_node:[]})
        self.neighbor_matrix.update({new_node:{}})
        for existing_node in self.neighbor_matrix:
            self.neighbor_matrix[existing_node].update({new_node:0})
            self.neighbor_matrix[new_node].update({existing_node:0})

    def remove_node(self, node):
        self.nodes.remove(node)
        for n in self.get_neighbors(node): self.remove_edge(node, n)
        self.adjacency_list.pop(node, None)
        self.neighbor_matrix.pop(node, None)
        for existing_node in self.neighbor_matrix:
            self.neighbor_matrix[existing_node].pop(node, None)

    def add_edge(self, node1, node2, weight=1.0, directional=False):
        self.adjacency_list[node1].append(node2)
        self.adjacency_list[node2].append(node1)
        self.neighbor_matrix[node1][node2] = weight
        if not directional:
            self.neighbor_matrix[node2][node1] = weight

    def remove_edge(self, node1, node2):
        self.adjacency_list[node1].remove(node2)
        self.adjacency_list[node2].remove(node1)
        self.neighbor_matrix[node1][node2] = 0
        self.neighbor_matrix[node2][node1] = 0

    def get_neighbors(self, node, use_adjacency_list=True):
        if use_adjacency_list: 
            return self.adjacency_list[node]
        return [other for other in self.neighbor_matrix if self.neighbor_matrix[node][other] != 0]
        
    def has_edge(self, node1, node2, use_adjacency_list=True):
        if use_adjacency_list:
            return node2 in self.adjacency_list[node1]
        return self.neighbor_matrix[node1][node2] != 0

    def get_edge_weight(self, node1, node2):
        return self.neighbor_matrix[node1][node2] if self.neighbor_matrix[node1][node2] != 0 else None

    def get_path_cost(self, path):
        path_cost = 0
        cost_of_becoming_skynet = 9999999.9
        if(type(path) == Queue): path = list(path)
        for i in range(len(path)-1):
            node = path[i]
            next = path[i+1]
            try:
                path_cost += self.get_edge_weight(node, next)
            except TypeError:
                raise noPathError(self, path[0], path[-1])
        return path_cost

    def bfs(self, start_node, end_node = None, use_adjacency_list=True):
        #Basic algorithm safety precautions (joke)
        cost_of_becoming_skynet = 9999999.9
        cost_of_harming_humans = 9999999.9
        cost_of_destroying_world = float('inf')
        frontier = Queue([start_node])
        explored = Queue()
        failures = []
        while not end_node in list(explored) and len(frontier) > 0:
            explored.add(frontier.get())
            #Add new nodes and store them in one line via list comprehension!
            new=[frontier.add(neighbor) for neighbor in self.get_neighbors(frontier.get(),use_adjacency_list) if not explored.has(neighbor)]
            #Keep track of failed paths
            if(len(new) == 0 and not end_node in explored):
                failures.append(frontier.get())
            #Remove the node
            frontier.pop()
        #If no goal provided, return everything explored
        if not end_node:
            return explored
        if len(frontier) == 0:
            raise noPathError(self, start_node, end_node)
        
        #Take the explored and find the path to the goal (NYI)
        raise NotImplementedError("Cannot return the path yet lol")


    def connected_components(self):
        output = []
        for node in self.nodes:
            if not(True in [node in group for group in output]):
                output.append(list(self.bfs(node)))
        return output
    
    
if __name__ == "__main__":
    g = Graph()
    g.add_node("a")
    g.add_node("b")
    g.add_node("c")
    g.add_node("d")
    g.add_node("e")
    g.add_node(1)
    g.add_node("1")
    print(g.adjacency_list)
    print(g.neighbor_matrix)
    g.add_edge("a", "b")
    g.add_edge("b", "c")
    g.add_edge("e", "d")
    print(g.adjacency_list)
    print(table_to_str(g.neighbor_matrix))
    print(g.connected_components())
    print(g.bfs("e", "a"))
    

