import copy
from typing import Optional, Union

import networkx as nx
import numpy as np

from structure_learning.distributions import ConditionalDistribution, Distribution
from structure_learning.utils import seed_to_generator

NodeType = Union[str, int]
DistributionType = Union[Distribution, ConditionalDistribution]


class CausalModel:
    """
    A causal model consists of three components:
    - a directed acyclic graph (DAG) where nodes represent variables and edges represent a direct
       causal effect from one variable to another.
    - a set of distributions, one for each variable, describing variables conditionally on their
       parents.
    - (optional) a set of interventions, each of which is a set of distributions that overwrite
      some variables' conditional distribution.

    Parameters
    ----------
    graph : nx.DiGraph
        The causal graph.
    distributions : dict[NodeType, DistributionType]
        A dictionary where each key is a node of the graph and its value is the distribution (or
        conditional distributions) of the node. The dictionary must contain a key for each node of
        the graph.
    interventions_distributions : dict[str, dict[NodeType, DistributionType]], optional
        A dictionary where each key is the name of an intervention and its value is a dictionary
        where each key is a node of the graph and its value is the distribution (or conditional
        distributions) of the node under the intervention. Interventions can overwrite only a
        subset of the nodes' distributions. Default is None.
    """

    def __init__(
        self,
        graph: nx.DiGraph,
        distributions: dict[NodeType, DistributionType],
        interventions_distributions: Optional[dict[str, dict[NodeType, DistributionType]]] = None,
    ):
        _check_acyclic(graph)
        self.graph = graph
        self.distributions = copy.deepcopy(distributions)
        self.interventions_distributions = (
            copy.deepcopy(interventions_distributions)
            if interventions_distributions is not None
            else {}
        )
        self.interventions = list(self.interventions_distributions.keys())

    @property
    def n_interventions(self):
        """Number of interventions in the causal model."""
        return len(self.interventions_distributions)

    @property
    def nodes(self) -> list:
        """Number of nodes/variables in the causal model."""
        return list(self.graph.nodes)

    def get_parents(self, node):
        """Return the parents of a variable."""
        return sorted(self.graph.predecessors(node))

    def sample(self, n_samples, intervention_name=None, seed=None):
        if intervention_name is not None and intervention_name not in self.interventions:
            raise ValueError(f"Intervention does not exist, {intervention_name}")
        if intervention_name is not None:
            intervened_distributions = self.interventions_distributions[intervention_name]
        else:
            intervened_distributions = {}

        seed = seed_to_generator(seed)

        samples_per_node = {}
        for node in nx.topological_sort(self.graph):
            parents = list(self.graph.predecessors(node))
            parents_values = {parent: samples_per_node[parent] for parent in parents}
            if node in intervened_distributions:
                distribution = intervened_distributions[node]
            else:
                distribution = self.distributions[node]
            samples_per_node[node] = distribution.sample(
                parents_values=parents_values, n_samples=n_samples, seed=seed
            )

        concatenated = np.array([samples_per_node[node] for node in self.nodes]).T
        return concatenated

    def sample_observational(self, n_samples, seed=None):
        """Sample from the observational distribution of the causal model."""
        return self.sample(n_samples, seed=seed)

    def sample_interventional(self, n_samples, intervention_name, seed=None):
        """Sample from the interventional distribution of the causal model."""
        return self.sample(n_samples, intervention_name=intervention_name, seed=seed)


def _check_acyclic(graph: nx.DiGraph):
    if not nx.is_directed_acyclic_graph(graph):
        raise ValueError("Graph is not acyclic.")
