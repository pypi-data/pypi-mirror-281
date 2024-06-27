import pytest
from structure_learning.simulated import gaussian_linear_mean_model


@pytest.mark.parametrize("d", [1, 2, 3, 4, 5])
def test_gaussian_linear_mean_model_simple(d):
    # n = 100
    # seed = 0
    # X, B_true = gaussian_linear_mean_model(n, d, seed=seed)
    # assert X.shape == (n, d)
    # assert B_true.shape == (d, d)
    # assert (B_true == 0).all()
    model = gaussian_linear_mean_model(d, 1)
    samples = model.sample_observational(100)
    assert samples.shape == (100, d)


def test_gaussian_linear_mean_model():
    model = gaussian_linear_mean_model(10, n_edges_per_d=2)
    assert model.graph.number_of_edges() == 20

    model = gaussian_linear_mean_model(10, n_edges_total=3)
    assert model.graph.number_of_edges() == 3

    model = gaussian_linear_mean_model(10, n_edges_density=0.1)
    assert model.graph.number_of_edges() == int(10 * 9 / 2 * 0.1)

    with pytest.raises(ValueError, match="Exactly one of"):
        gaussian_linear_mean_model(10, n_edges_per_d=2, n_edges_total=3)

    with pytest.raises(ValueError, match="Exactly one of"):
        gaussian_linear_mean_model(10, n_edges_per_d=2, n_edges_density=0.1)
