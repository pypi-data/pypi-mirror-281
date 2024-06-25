# tests/test_layers.py
import unittest
import numpy as np
from my_neural_network.layers import Layer

class TestLayers(unittest.TestCase):
    def test_layer_forward(self):
        layer = Layer(2, 2, 'sigmoid')
        x = np.array([[1, 2]])
        y = layer.forward(x)
        self.assertEqual(y.shape, (1, 2))

if __name__ == '__main__':
    unittest.main()
