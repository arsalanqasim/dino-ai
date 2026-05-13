from dino_ai.neural import NeuralNetwork


def test_predict_output_shape() -> None:
    model = NeuralNetwork(in_nodes=11, hid_nodes=10, out_nodes=2)
    output = model.predict([0.0] * 11)

    assert len(output) == 2
    assert all(0.0 <= value <= 1.0 for value in output)


def test_clone_preserves_structure() -> None:
    model = NeuralNetwork(in_nodes=11, hid_nodes=10, out_nodes=2)
    clone = model.clone()

    assert clone.in_nodes == model.in_nodes
    assert clone.hid_nodes == model.hid_nodes
    assert clone.out_nodes == model.out_nodes
    assert clone.weights_ih == model.weights_ih
    assert clone.weights_ho == model.weights_ho
