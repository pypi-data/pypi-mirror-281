# iros/network.py
import numpy as np
from .layers import Layer
import pickle

class NeuralNetwork:
    def __init__(self):
        self.layers = []

    def add_layer(self, layer):
        self.layers.append(layer)

    def forward(self, input_data):
        output = input_data
        for layer in self.layers:
            output = layer.forward(output)
        return output

    def backward(self, loss_gradient, learning_rate):
        for layer in reversed(self.layers):
            loss_gradient = layer.backward(loss_gradient, learning_rate)

    def train(self, x_train, y_train, epochs, learning_rate):
        for epoch in range(epochs):
            # Forward pass
            output = self.forward(x_train)
            # Compute loss gradient
            loss_gradient = output - y_train
            # Backward pass
            self.backward(loss_gradient, learning_rate)
            # Compute loss (for monitoring)
            loss = np.mean(loss_gradient**2)
            print(f'Epoch {epoch+1}/{epochs}, Loss: {loss}')

    def save(self, file_path):
        with open(file_path, 'wb') as f:
            pickle.dump([(layer.weights, layer.biases) for layer in self.layers], f)

    def load(self, file_path):
        with open(file_path, 'rb') as f:
            data = pickle.load(f)
            for layer, (weights, biases) in zip(self.layers, data):
                layer.weights, layer.biases = weights, biases
