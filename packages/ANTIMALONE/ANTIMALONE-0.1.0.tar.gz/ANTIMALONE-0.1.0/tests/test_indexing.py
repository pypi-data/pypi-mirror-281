import unittest
import numpy as np
from antimalone.indexing import train_indexing_model, create_index

class TestIndexing(unittest.TestCase):

    def test_indexing(self):
        data = np.random.rand(100, 10)
        labels = np.random.randint(0, 2, 100)
        model = train_indexing_model(data, labels)
        features = np.random.rand(10)
        index = create_index(model, features)
        self.assertIsInstance(index, np.ndarray)
        self.assertEqual(len(index), 16)

if __name__ == '__main__':
    unittest.main()
