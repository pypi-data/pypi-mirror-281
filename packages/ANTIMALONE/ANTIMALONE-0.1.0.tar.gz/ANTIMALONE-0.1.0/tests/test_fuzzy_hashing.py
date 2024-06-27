import unittest
import numpy as np
from antimalone.fuzzy_hashing import train_fuzzy_hash_model, generate_fuzzy_hash

class TestFuzzyHashing(unittest.TestCase):

    def test_fuzzy_hashing(self):
        data = np.random.rand(100, 4096, 1)
        labels = np.random.randint(0, 2, 100)
        model = train_fuzzy_hash_model(data, labels)
        dummy_byte_array = np.random.randint(0, 256, 4096, dtype=np.uint8)
        fuzzy_hash = generate_fuzzy_hash(model, dummy_byte_array)
        self.assertIsInstance(fuzzy_hash, str)
        self.assertEqual(len(fuzzy_hash), 64)

if __name__ == '__main__':
    unittest.main()
