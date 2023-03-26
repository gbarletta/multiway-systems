import networkx as nx
from networkx.drawing.nx_pydot import write_dot

def replace_nth(s, sub, repl, n):
    find = s.find(sub)
    i = find != -1
    while find != -1 and i != n:
        find = s.find(sub, find + 1)
        i += 1
    if i == n:
        return s[:find] + repl + s[find+len(sub):]
    return s

def occurrences(string, sub):
    count = start = 0
    while True:
        start = string.find(sub, start) + 1
        if start > 0:
            count+=1
        else:
            return count
        
def get_nodes_at_depth(g, depth, from_node):
    path_lengths = nx.shortest_path_length(g, source=from_node)
    return [node for node, d in path_lengths.items() if d == depth]
        
def generate_graph(**kwargs):
    g = nx.DiGraph()
    for level in range(kwargs["max_level"]):
        if level == 0:
            g.add_node(kwargs["initial_state"])
            continue
        for state in get_nodes_at_depth(g, level-1, kwargs["initial_state"]):
            for rule in kwargs["rules"]:
                for i in range(occurrences(state, rule[0])):
                    new_state = replace_nth(state, rule[0], rule[1], i+1)
                    g.add_edge(state, new_state)
    return g

g = generate_graph(initial_state="A", rules=[("A", "BBB"), ("BB", "A")], max_level=10)
write_dot(g, "graph.dot")