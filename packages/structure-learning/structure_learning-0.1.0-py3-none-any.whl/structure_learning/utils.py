from typing import Union

import numpy as np


def seed_to_generator(seed) -> Union[np.random.Generator, np.random.RandomState]:
    """
    Return a generator from a seed, if the seed is already a generator, return it.

    Parameters:
    -----------
    seed: int or np.random.Generator or np.random.RandomState or None
        The seed to use for the generator.

    Returns:
    --------
    np.random.Generator or np.random.RandomState
        The generator to use for random number generation.
    """
    if isinstance(seed, np.random.Generator) or isinstance(seed, np.random.RandomState):
        return seed
    return np.random.default_rng(seed)


def shift_seed(seed, shift=1) -> Union[int, np.random.Generator, np.random.RandomState, None]:
    """
    Shift the seed by one if it is an integer.

    Parameters:
    -----------
    seed: int or np.random.Generator or np.random.RandomState or None
        The seed to shift.

    Returns:
    --------
    int or np.random.Generator or np.random.RandomState or None
        The shifted seed or the original generator/state/None.
    """
    if isinstance(seed, int):
        return seed + shift
    return seed
