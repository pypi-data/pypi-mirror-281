import numpy as np

class Optimizer:
    def update(self, parameters, gradients):
        pass

class SGD(Optimizer):
    def __init__(self, learning_rate=0.01):
        self.learning_rate = learning_rate

    def update(self, parameters, gradients):
        for param, grad in zip(parameters, gradients):
            for key in param:
                param[key] -= self.learning_rate * grad[key]

class Adam(Optimizer):
    def __init__(self, learning_rate=0.001, beta1=0.9, beta2=0.999, epsilon=1e-8):
        self.learning_rate = learning_rate
        self.beta1 = beta1
        self.beta2 = beta2
        self.epsilon = epsilon
        self.m = None
        self.v = None
        self.t = 0

    def update(self, parameters, gradients):
        if self.m is None:
            self.m = [dict((k, np.zeros_like(v)) for k, v in param.items()) for param in parameters]
            self.v = [dict((k, np.zeros_like(v)) for k, v in param.items()) for param in parameters]

        self.t += 1
        lr_t = self.learning_rate * np.sqrt(1 - self.beta2**self.t) / (1 - self.beta1**self.t)

        for param, grad, m, v in zip(parameters, gradients, self.m, self.v):
            for key in param:
                m[key] = self.beta1 * m[key] + (1 - self.beta1) * grad[key]
                v[key] = self.beta2 * v[key] + (1 - self.beta2) * (grad[key]**2)
                param[key] -= lr_t * m[key] / (np.sqrt(v[key]) + self.epsilon)
