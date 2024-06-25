# iros/layers.py
import numpy as np
from .activations import sigmoid, sigmoid_derivative, relu, relu_derivative
import pickle

class Layer:
    def __init__(self, input_size, output_size, activation):
        self.weights = np.random.randn(input_size, output_size) * 0.1
        self.biases = np.zeros((1, output_size))
        self.activation = activation
        self.activation_function = self.get_activation_function(activation)
        self.activation_derivative = self.get_activation_derivative(activation)

    def get_activation_function(self, activation):
        if activation == 'sigmoid':
            return sigmoid
        elif activation == 'relu':
            return relu
        else:
            raise ValueError('Unsupported activation function')

    def get_activation_derivative(self, activation):
        if activation == 'sigmoid':
            return sigmoid_derivative
        elif activation == 'relu':
            return relu_derivative
        else:
            raise ValueError('Unsupported activation function')

    def forward(self, input_data):
        self.input = input_data
        self.z = np.dot(input_data, self.weights) + self.biases
        self.output = self.activation_function(self.z)
        return self.output

    def backward(self, output_error, learning_rate):
        # Calculate activation error
        activation_error = output_error * self.activation_derivative(self.z)
        # Calculate input error for the next layer
        input_error = np.dot(activation_error, self.weights.T)
        # Calculate the gradient for weights and biases
        weights_error = np.dot(self.input.T, activation_error)

        # Update weights and biases
        self.weights -= learning_rate * weights_error
        self.biases -= learning_rate * activation_error.mean(axis=0, keepdims=True)
        return input_error

    def save(self, file_path):
        with open(file_path, 'wb') as f:
            pickle.dump((self.weights, self.biases), f)

    def load(self, file_path):
        with open(file_path, 'rb') as f:
            self.weights, self.biases = pickle.load(f)
