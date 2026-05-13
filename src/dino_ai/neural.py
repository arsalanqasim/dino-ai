"""Minimal feed-forward neural network used by agents."""

from __future__ import annotations

import math
import random


class NeuralNetwork:
    def __init__(self, in_nodes: int, hid_nodes: int, out_nodes: int) -> None:
        self.in_nodes = in_nodes
        self.hid_nodes = hid_nodes
        self.out_nodes = out_nodes

        self.weights_ih = [
            [random.uniform(-1, 1) for _ in range(in_nodes)] for _ in range(hid_nodes)
        ]
        self.weights_ho = [
            [random.uniform(-1, 1) for _ in range(hid_nodes)] for _ in range(out_nodes)
        ]
        self.bias_h = [random.uniform(-1, 1) for _ in range(hid_nodes)]
        self.bias_o = [random.uniform(-1, 1) for _ in range(out_nodes)]

    def predict(self, inputs: list[float]) -> list[float]:
        hidden: list[float] = []
        for i in range(self.hid_nodes):
            sum_val = self.bias_h[i]
            for j in range(self.in_nodes):
                sum_val += inputs[j] * self.weights_ih[i][j]
            hidden.append(max(0, sum_val))

        outputs: list[float] = []
        for i in range(self.out_nodes):
            sum_val = self.bias_o[i]
            for j in range(self.hid_nodes):
                sum_val += hidden[j] * self.weights_ho[i][j]
            clamped = max(-50, min(50, sum_val))
            outputs.append(1 / (1 + math.exp(-clamped)))

        return outputs

    def clone(self) -> "NeuralNetwork":
        cloned = NeuralNetwork(self.in_nodes, self.hid_nodes, self.out_nodes)
        cloned.weights_ih = [row[:] for row in self.weights_ih]
        cloned.weights_ho = [row[:] for row in self.weights_ho]
        cloned.bias_h = self.bias_h[:]
        cloned.bias_o = self.bias_o[:]
        return cloned

    def mutate(self, rate: float) -> None:
        def mutate_val(val: float) -> float:
            if random.random() < rate:
                return val + random.gauss(0, 0.5)
            return val

        self.weights_ih = [[mutate_val(w) for w in row] for row in self.weights_ih]
        self.weights_ho = [[mutate_val(w) for w in row] for row in self.weights_ho]
        self.bias_h = [mutate_val(b) for b in self.bias_h]
        self.bias_o = [mutate_val(b) for b in self.bias_o]

    def crossover(self, partner: "NeuralNetwork") -> "NeuralNetwork":
        child = NeuralNetwork(self.in_nodes, self.hid_nodes, self.out_nodes)

        for i in range(self.hid_nodes):
            for j in range(self.in_nodes):
                child.weights_ih[i][j] = (
                    self.weights_ih[i][j]
                    if random.random() < 0.5
                    else partner.weights_ih[i][j]
                )

        for i in range(self.out_nodes):
            for j in range(self.hid_nodes):
                child.weights_ho[i][j] = (
                    self.weights_ho[i][j]
                    if random.random() < 0.5
                    else partner.weights_ho[i][j]
                )

        for i in range(self.hid_nodes):
            child.bias_h[i] = (
                self.bias_h[i] if random.random() < 0.5 else partner.bias_h[i]
            )

        for i in range(self.out_nodes):
            child.bias_o[i] = (
                self.bias_o[i] if random.random() < 0.5 else partner.bias_o[i]
            )

        return child
