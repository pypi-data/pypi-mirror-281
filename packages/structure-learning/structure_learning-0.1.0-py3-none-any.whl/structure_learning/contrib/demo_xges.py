from xges import XGES


def compute_metric(predicted_graph, true_graph):
    shd = 0
    for edge in true_graph.edges:
        if edge not in predicted_graph.edges:
            shd += 1
    for edge in predicted_graph.edges:
        if edge not in true_graph.edges and edge[::-1] not in true_graph.edges:
            if edge[::-1] in predicted_graph.edges:
                if edge[0] < edge[1]:
                    shd += 1
            else:
                shd += 1

    return shd


def evaluate_xges_on_data(data, true_graph):
    model = XGES()
    model.fit(data, verbose=1, use_fast_numba=True)

    predicted_graph = model.get_a_dag_networkx()
    shd = compute_metric(predicted_graph, true_graph)
    print(f"SHD: {shd}")


if __name__ == "__main__":
    from structure_learning import gaussian_linear_mean_model

    causal_model = gaussian_linear_mean_model(
        25,
        n_edges_per_d=2,
        seed=2,
        weights_init_type="avoid_zero_positive",
        std=0.5,
    )
    true_graph = causal_model.graph
    data = causal_model.sample_observational(10000, seed=0)
    print(data[0, 0])
    evaluate_xges_on_data(data, true_graph)
