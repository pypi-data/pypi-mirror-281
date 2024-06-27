import abc
from typing import Literal

import numpy as np

from structure_learning.utils import seed_to_generator


class BaseFunction(abc.ABC):
    """
    Base class for a function taking a dictionary of inputs (parents) and returning a dictionary
    of outputs, usually parameters of a distribution.
    """

    @abc.abstractmethod
    def compute(self, x: dict) -> dict:
        """
        Compute the function on the input dictionary.

        Parameters
        ----------
        x: dict
            Dictionary of inputs (parents).

        Returns
        -------
        dict
            Dictionary of outputs.
        """

    def initialize_parameters(self, seed=None):
        """
        Initialize the function's parameters.

        Parameters
        ----------
        seed: int or np.random.Generator or np.random.RandomState or None
            The seed to use for random number generation.
        """
        return

    def __call__(self, x: dict):
        return self.compute(x)


class LinearFunction(BaseFunction):
    def __init__(
        self,
        input_names: list,
        output_names: list[str],
        init_type: Literal["kaiming", "normal", "avoid_zero"] = "kaiming",
        seed=None,
    ):
        self.dim_in = len(input_names)
        self.dim_out = len(output_names)
        self.input_names = input_names
        self.output_names = output_names
        self.init_type = init_type
        self.weights = None
        self.bias = None

        self.initialize_parameters(seed, init_type)

    def initialize_parameters(self, seed=None, init_type: str = "kaiming"):
        seed = seed_to_generator(seed)
        if init_type == "kaiming":
            # Initialize weights and bias with Kaiming initialization
            scale = np.sqrt(2 / self.dim_in)
            self.weights = seed.normal(0, scale, (self.dim_out, self.dim_in))
            self.bias = seed.normal(0, scale, self.dim_out)
        elif init_type == "normal":
            self.weights = seed.normal(0, 1, (self.dim_out, self.dim_in))
            self.bias = seed.normal(0, 1, self.dim_out)
        elif init_type in ["avoid_zero_positive", "avoid_zero"]:
            self.weights = seed.uniform(1.0, 3.0, (self.dim_out, self.dim_in))
            self.bias = seed.normal(0, 1, self.dim_out)
            if init_type == "avoid_zero":
                self.weights *= seed.choice([-1, 1], size=self.weights.shape)

    def compute(self, x: dict):
        x = np.array([x[input_name] for input_name in self.input_names])
        res = np.dot(self.weights, x) + self.bias
        return {output_name: res[i] for i, output_name in enumerate(self.output_names)}

    def __repr__(self):
        return f"LinearFunction(dim_in={self.dim_in}, output_names={self.output_names})"


class MLPFunction(BaseFunction):
    def __init__(
        self,
        input_names: list,
        output_names: list[str],
        hidden_sizes: list[int],
        activation: str = "relu",
        seed=None,
    ):
        self.dim_in = len(input_names)
        self.dim_out = len(output_names)
        self.input_names = input_names
        self.output_names = output_names

        self.hidden_sizes = hidden_sizes
        self.weights = []
        self.biases = []
        self.activation = activation

        self.initialize_parameters(seed)

    def initialize_parameters(self, seed=None):
        # Initialize weights and bias with Kaiming initialization
        sizes = [self.dim_in, *self.hidden_sizes, self.dim_out]
        self.weights.clear()
        self.biases.clear()
        for i in range(len(sizes) - 1):
            scale = np.sqrt(2 / sizes[i])
            self.weights.append(seed.normal(0, scale, (sizes[i + 1], sizes[i])))
            self.biases.append(seed.normal(0, scale, sizes[i + 1]))

    def compute(self, x: dict):
        x = np.array([x[input_name] for input_name in self.input_names])
        for i in range(len(self.hidden_sizes)):
            x = np.dot(self.weights[i], x) + self.biases[i]
            if self.activation == "relu":
                x = relu(x)
            elif self.activation == "sigmoid":
                x = sigmoid(x)
            else:
                raise ValueError(
                    f"Unknown activation function {self.activation}. Supported: relu, sigmoid."
                )

        x = np.dot(self.weights[-1], x) + self.biases[-1]
        return {output_name: x[i] for i, output_name in enumerate(self.output_names)}

    def __repr__(self):
        return f"MLPFunction(dim_in={self.dim_in}, output_names={self.output_names})"


def softplus(x):
    return np.logaddexp(0, x)


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


def relu(x):
    return np.maximum(x, 0)
