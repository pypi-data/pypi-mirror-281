from __future__ import annotations

import scipy

from structure_learning.conditional_functions import BaseFunction


class Distribution:
    def __init__(
        self,
        base_distribution: scipy.stats.rv_continuous | scipy.stats.rv_discrete,
        **parameter_values,
    ):
        self.base_distribution = base_distribution
        self.parameter_values = parameter_values

    def sample(self, n_samples=None, parents_values=None, seed=None):
        if parents_values is not None and parents_values != {}:
            raise ValueError(
                "No parent values should be provided for a Distribution object."
                f"Received parents_values={parents_values}."
            )
        return self.base_distribution.rvs(
            size=n_samples, random_state=seed, **self.parameter_values
        )


class ConditionalDistribution:
    def __init__(
        self,
        base_distribution: scipy.stats.rv_continuous | scipy.stats.rv_discrete,
        parents: list,
        function: BaseFunction,
        **parameter_values,
    ):
        self.base_distribution = base_distribution
        self.parents = parents
        self.function = function
        self.parameter_values = parameter_values

    def sample(self, n_samples=None, parents_values=None, seed=None):
        self._check_parents(parents_values)
        parameters = self.function(parents_values)
        return self.base_distribution.rvs(
            size=n_samples, random_state=seed, **parameters, **self.parameter_values
        )

    def _check_parents(self, parents_values):
        if parents_values is None:
            raise ValueError("No parent values provided for a ConditionalDistribution object.")
        for parent in self.parents:
            if parent not in parents_values:
                raise ValueError(f"Parent {parent} not in parents_values.")

        for parent in parents_values:
            if parent not in self.parents:
                raise ValueError(f"Unexpected parent {parent} in parents_values.")
