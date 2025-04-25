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
