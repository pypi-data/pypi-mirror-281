# tests/test_network.py
import unittest
import numpy as np
from my_neural_network.network import NeuralNetwork
from my_neural_network.layers import Layer

class TestNeuralNetwork(unittest.TestCase):
    def test_network(self):
        nn = NeuralNetwork()
        nn.add_layer(Layer(2, 3, 'relu'))
        nn.add_layer(Layer(3, 1, 'sigmoid'))
        x = np.array([[1, 2]])
        y = nn.forward(x)
        self.assertEqual(y.shape, (1, 1))

if __name__ == '__main__':
    unittest.main()
