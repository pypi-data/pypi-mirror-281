import unittest
from antimalone.context_hashing import context_aware_hash

class TestContextHashing(unittest.TestCase):

    def test_context_aware_hash(self):
        file_path = 'path/to/your/testfile.exe'
        context_hash = context_aware_hash(file_path)
        self.assertIsInstance(context_hash, str)
        self.assertEqual(len(context_hash), 64)

if __name__ == '__main__':
    unittest.main()
