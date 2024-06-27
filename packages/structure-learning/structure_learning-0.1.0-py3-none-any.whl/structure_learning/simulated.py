import scipy.stats as st

from structure_learning.causal_model import CausalModel
from structure_learning.conditional_functions import LinearFunction
from structure_learning.distributions import ConditionalDistribution, Distribution
from structure_learning.graph import random_dag
from structure_learning.utils import shift_seed


def _get_number_of_edges(d, n_edges_per_d, n_edges_total, n_edges_density):
    """
    Get the number of edges from the input parameters.

    Parameters
    ----------
    d: int
        The number of variables.
    n_edges_per_d: int or None
        The number of edges per variable. Results in n_edges = n_edges_per_d * d.
    n_edges_total: int or None
        The total number of edges. Results in n_edges = n_edges_total.
    n_edges_density: float or None
        The edge density. Results in n_edges = n_edges_density * d * (d - 1) / 2.

    Returns
    -------
    int
        The number of edges.

    Raises
    ------
    ValueError
        If not exactly one of n_edges_per_d, n_edges_total, or n_edges_density is provided.
    """
    if sum(x is not None for x in [n_edges_per_d, n_edges_total, n_edges_density]) != 1:
        raise ValueError(
            "Exactly one of n_edges_per_d, n_edges_total, or n_edges_density must be provided."
        )

    n_edges = None
    if n_edges_per_d is not None:
        n_edges = n_edges_per_d * d
    elif n_edges_total is not None:
        n_edges = n_edges_total
    elif n_edges_density is not None:
        n_edges = int(n_edges_density * d * (d - 1) / 2)
    return n_edges


def gaussian_linear_mean_model(
    d,
    n_edges_per_d=None,
    n_edges_total=None,
    n_edges_density=None,
    std=1.0,
    weights_init_type="avoid_zero_positive",
    seed: int | None = None,
) -> CausalModel:
    """
    Generate a random linear Gaussian model.


    """
    n_edges = _get_number_of_edges(d, n_edges_per_d, n_edges_total, n_edges_density)

    # Step 1) Get graph
    graph = random_dag(d, n_edges, seed=seed)

    # Step 2) Generate distributions
    distributions = {}
    for i in graph.nodes:
        parents = list(graph.predecessors(i))
        if len(parents) == 0:
            distributions[i] = Distribution(st.norm, loc=0, scale=std)
        else:
            parents_to_child = LinearFunction(
                input_names=parents,
                output_names=["loc"],
                seed=shift_seed(seed, i),
                init_type=weights_init_type,
            )
            distributions[i] = ConditionalDistribution(
                st.norm, parents=parents, function=parents_to_child, scale=std
            )

    return CausalModel(graph, distributions)
