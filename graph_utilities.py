import networkx as nx

def add_edge_to_graph(g, node1, node2, weight = 1, nodeNotFoundMode = None):
    match nodeNotFoundMode:
        case "error":
            if not(g.has_node(node1) and g.has_node(node2)):
                raise nx.NodeNotFound
            g.add_edge(node1, node2)
            g[node1][node2]["weight"] = weight
        case "add":
            if not g.has_node(node1): g.add_node(node1)
            if not g.has_node(node2): g.add_node(node2)
            g.add_edge(node1, node2)
            g[node1][node2]["weight"] = weight
        case _:
            if(g.has_node(node1) and g.has_node(node2)):
                g.add_edge(node1, node2)
                g[node1][node2]["weight"] = weight

def contains_duplicates(thelist):
  seen = set()
  for x in thelist:
    if x in seen: return True
    seen.add(x)
  return False

def without(l, e):
    try:
        l.remove(e)
    except:
        return l
    return l

def pos_range_without_all(w, h, ignore = []):
    output = []
    [[output.append((i, j)) for i in range(w) if (i, j) not in ignore] for j in range(h)]
    return output

def add_edges_to_graph_from(g, edges, weights=None, nodeNotFoundMode = None):
    if not weights or len(weights) == 0:
        for edge in edges:
            add_edge_to_graph(g, edge[0], edge[1], nodeNotFoundMode)
    elif type(weights) == dict:
        for edge in edges:
            try:
                add_edge_to_graph(g, edge[0], edge[1], weights[edge], nodeNotFoundMode)
            except KeyError:
                add_edge_to_graph(g, edge[0], edge[1], 1, nodeNotFoundMode)
    else:
        for i in range(len(edges)):
            try:
                add_edge_to_graph(g, edges[i][0], edges[i][1], weights[i], nodeNotFoundMode)
            except IndexError:
                add_edge_to_graph(g, edges[i][0], edges[i][1], 1, nodeNotFoundMode)