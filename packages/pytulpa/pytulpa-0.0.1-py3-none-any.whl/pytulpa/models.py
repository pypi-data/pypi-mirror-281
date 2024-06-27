import numpy as np
from .layers import LiquidLayer

class Model:
    def __init__(self):
        self.layers = []

    def add(self, layer):
        self.layers.append(layer)

    def forward(self, X):
        for layer in self.layers:
            X = layer.forward(X)
        return X

    def backward(self, y_true):
        gradients = []
        error = y_true - self.layers[-1].output
        for layer in reversed(self.layers):
            error = layer.backward(error)
            gradients.append(layer.gradients)
        return list(reversed(gradients))

    def parameters(self):
        return [layer.parameters for layer in self.layers if hasattr(layer, 'parameters')]

class LNN(Model):
    def __init__(self, input_size, hidden_size, output_size, dt=0.1, tau=1.0):
        super().__init__()
        self.add(LiquidLayer(input_size, hidden_size, dt, tau))
        self.add(DenseLayer(hidden_size, output_size))