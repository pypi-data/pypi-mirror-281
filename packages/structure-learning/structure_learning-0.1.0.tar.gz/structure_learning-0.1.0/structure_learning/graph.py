import networkx as nx

from structure_learning.utils import seed_to_generator


def chain_graph(n_variables: int = 20) -> nx.DiGraph:
    """
    Return a chain graph: 1 -> 2 -> ... -> n_variables.

    Parameters
    ----------
    n_variables: int
        Number of variables in the chain graph.

    Returns
    -------
    nx.DiGraph
        The chain graph with `n_variables` nodes: 0, 1, ..., `n_variables` - 1.
    """
    graph = nx.DiGraph()
    nodes = list(range(n_variables))
    graph.add_nodes_from(nodes)
    for a, b in zip(nodes[:-1], nodes[1:]):
        graph.add_edge(a, b)

    return graph


def random_dag_from_undirected_graph(
    graph: nx.Graph,
    seed=None,
) -> nx.DiGraph:
    """
    Transform an undirected graph into a random DAG by arbitrarily orienting the edges.

    The nodes are randomly shuffled and the edges are oriented from a node with a lower index to
    a node with a higher index.

    Parameters
    ----------
    graph: nx.Graph
        The undirected graph.
    seed: int or np.random.RandomState or np.random.Generator (optional)
        The random state to use for sampling the edge directions.

    Returns
    -------
    nx.DiGraph
        The directed acyclic graph (DAG) created from the input graph.
    """
    seed = seed_to_generator(seed)

    nodes = list(graph.nodes)
    nodes_original = nodes.copy()
    seed.shuffle(nodes)
    edges = []
    for edge in graph.edges:
        if nodes.index(edge[0]) < nodes.index(edge[1]):
            edges.append(edge)
        else:
            edges.append((edge[1], edge[0]))
    dag = nx.DiGraph()
    dag.add_nodes_from(nodes_original)
    dag.add_edges_from(edges)

    return dag


def random_dag(
    n_nodes: int = 20, n_edges: int = 20, distribution: str = "erdos_renyi", seed=None
) -> nx.DiGraph:
    """
    Generate a random directed acyclic graph (DAG) with a given number of nodes, edges and
    distribution.

    Parameters
    ----------
    n_nodes: int
        Number of nodes in the graph.
    n_edges: int
        Number of edges in the graph.
    distribution: str
        The distribution of the graph. Either "erdos_renyi" or "scale_free".
    seed: int or np.random.RandomState or np.random.Generator (optional)
        The random state to use for generating the graph.

    Returns
    -------
    nx.DiGraph
        The generated DAG.

    Raises
    ------
    ValueError
        If the distribution is not "erdos_renyi" or "scale_free".
    """
    if distribution == "erdos_renyi":
        graph = nx.gnm_random_graph(n_nodes, n_edges, directed=False, seed=seed)
    elif distribution == "scale_free":
        graph = nx.scale_free_graph(n_nodes, seed=seed)
    else:
        raise ValueError(f"Unknown distribution {distribution}.")

    return random_dag_from_undirected_graph(graph, seed=seed)
