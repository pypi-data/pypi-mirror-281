# tests/test_activations.py
import unittest
import numpy as np
from my_neural_network.activations import sigmoid, relu

class TestActivations(unittest.TestCase):
    def test_sigmoid(self):
        x = np.array([0, 2])
        y = sigmoid(x)
        self.assertTrue(np.all(y >= 0) and np.all(y <= 1))

    def test_relu(self):
        x = np.array([-1, 0, 1])
        y = relu(x)
        self.assertTrue(np.array_equal(y, [0, 0, 1]))

if __name__ == '__main__':
    unittest.main()
