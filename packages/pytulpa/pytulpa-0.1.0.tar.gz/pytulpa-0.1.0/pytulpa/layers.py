import numpy as np
from .activations import tanh

class Layer:
    def __init__(self):
        self.input = None
        self.output = None

    def forward(self, input):
        pass

    def backward(self, output_error):
        pass

class DenseLayer(Layer):
    def __init__(self, input_size, output_size):
        super().__init__()
        self.weights = np.random.randn(output_size, input_size) * 0.1
        self.bias = np.zeros((output_size, 1))

    def forward(self, input):
        self.input = input
        self.output = np.dot(sel        return self.output

    def backward(self, output_error):
        input_error = np.dot(self.weights.T, output_error)
        self.gradients = {
            'weights': np.dot(output_error, self.input.T),
            'bias': np.sum(output_error, axis=1, keepdims=True)
        }
        return input_error

class LiquidLayer(Layer):
    def __init__(self, input_size, hidden_size, dt=0.1, tau=1.0):
        super().__init__()
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.dt = dt
        self.tau = tau
        self.W_in = np.random.randn(hidden_size, input_size) * 0.1
        self.W_rec = np.random.randn(hidden_size, hidden_size) * 0.1
        self.h = np.zeros((hidden_size, 1))
        self.dh_history = []

    def forward(self, input):
        self.input = input
        self.z = np.dot(self.W_in, input) + np.dot(self.W_rec, self.h)
        dh = (-self.h + tanh(self.z)) / self.tau
        self.h += self.dt * dh
        self.dh_history.append(dh)
        self.output = self.h
        return self.output

    def backward(self, output_error, truncation=10):
        dh = output_error
        dW_in = np.zeros_like(self.W_in)
        dW_rec = np.zeros_like(self.W_rec)
        input_error = np.zeros_like(self.input)

        for t in reversed(range(max(0, len(self.dh_history) - truncation), len(self.dh_history))):
            dh = dh + self.dt * (-dh / self.tau + np.dot(self.W_rec.T, dh * (1 - np.tanh(self.z)**2) / self.tau))
            
            dW_in += np.dot(dh * (1 - np.tanh(self.z)**2) / self.tau, self.input.T)
            
            dW_rec += np.dot(dh * (1 - np.tanh(self.z)**2) / self.tau, self.h.T)
            
            input_error += np.dot(self.W_in.T, dh * (1 - np.tanh(self.z)**2) / self.tau)

        dW_in *= self.dt
        dW_rec *= self.dt
        input_error *= self.dt

        self.gradients = {
            'W_in': dW_in,
            'W_rec': dW_rec
        }

        self.dh_history = []

        return input_error