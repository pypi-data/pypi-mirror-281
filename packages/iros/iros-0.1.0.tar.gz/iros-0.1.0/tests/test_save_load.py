# tests/test_save_load.py
import unittest
import numpy as np
import os
from my_neural_network.network import NeuralNetwork
from my_neural_network.layers import Layer

class TestSaveLoad(unittest.TestCase):
    def test_save_load(self):
        nn = NeuralNetwork()
        nn.add_layer(Layer(2, 3, 'relu'))
        nn.add_layer(Layer(3, 1, 'sigmoid'))
        x = np.array([[1, 2]])
        y = nn.forward(x)

        nn.save('test_model.pkl')
        nn2 = NeuralNetwork()
        nn2.add_layer(Layer(2, 3, 'relu'))
        nn2.add_layer(Layer(3, 1, 'sigmoid'))
        nn2.load('test_model.pkl')
        y2 = nn2.forward(x)

        self.assertTrue(np.array_equal(y, y2))
        os.remove('test_model.pkl')

if __name__ == '__main__':
    unittest.main()
