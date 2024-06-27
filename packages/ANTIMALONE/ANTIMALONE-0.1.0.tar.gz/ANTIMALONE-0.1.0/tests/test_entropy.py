import unittest
from antimalone.entropy import calculate_enhanced_entropy

class TestEntropyCalculation(unittest.TestCase):

    def test_calculate_enhanced_entropy(self):
        file_path = 'path/to/your/testfile.exe'
        results = calculate_enhanced_entropy(file_path)
        self.assertIn('global_entropy', results)
        self.assertIn('section_entropies', results)
        self.assertIn('sliding_window_entropies', results)

if __name__ == '__main__':
    unittest.main()
