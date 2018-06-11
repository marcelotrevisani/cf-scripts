"""
Functions to find the longest paths between nodes in a graph.

"""
from copy import deepcopy
from collections import defaultdict

import networkx as nx


def cyclic_topological_sort(graph, source):
    """Return a list of nodes in a graph with cycles in topological order.

    Performs a topological sort of `graph` starting from the node `source`.
    This is not a true topological sort if `graph` contains cycles, but
    any nodes that are not part of a cycle are given in correct topological
    order.

    Parameters
    ----------
    graph : networkx.classes.digraph.DiGraph
        A directed graph.
    source : str
        The name of the source node.

    Returns
    -------
    list
        The nodes of `graph` in topological sort order.

    """

    order = []
    _visit(graph, source, order)
    return reversed(order)


def _visit(graph, node, order):
    if graph.node[node].get('visited', False):
        return
    graph.node[node]['visited'] = True
    for n in graph.neighbors(node):
        _visit(graph, n, order)
    order.append(node)


def get_longest_paths(graph, source):
    """Get the length of the longest path to each node from a source node.

    Parameters
    ----------
    graph : networkx.classes.digraph.DiGraph
        A directed graph.
    source : str
        The name of the source node.

    Returns
    -------
    dict
        A dictionary where keys are the names of the nodes in `graph` and
        values are the lengths of the longest path from `source`.

    """

    dist = {node: -float('inf') for node in graph}
    dist[source] = 0
    visited = []
    for u in cyclic_topological_sort(graph, source):
        visited.append(u)
        for v in graph.neighbors(u):
            if v in visited:
                continue
            if dist[v] < dist[u] + 1:
                dist[v] = dist[u] + 1

    return dist


def get_levels(graph, source):
    """Get the nodes in each level of a topological sort of a graph starting
    from a specified source node.

    Parameters
    ----------
    graph : networkx.classes.digraph.DiGraph
        A directed graph.
    source : str
        The name of the source node.

    Returns
    -------
    dict
        A dictionary where keys are integers and values are the names of the
        nodes in `graph` with longest path length equal to the key.

    """

    g2 = deepcopy(graph)
    desc = nx.algorithms.descendants(graph, source)
    for node in graph.node:
        if (node not in desc and node != source):
            g2.remove_node(node)

    dist = get_longest_paths(g2, source)
    levels = defaultdict(set)
    for k, v in dist.items():
        levels[v].add(k)
    return levels