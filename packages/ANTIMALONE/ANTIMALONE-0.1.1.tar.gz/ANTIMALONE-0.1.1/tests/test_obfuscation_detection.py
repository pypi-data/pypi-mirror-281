import unittest
from antimalone.obfuscation_detection import create_code_graph, detect_obfuscation

class TestObfuscationDetection(unittest.TestCase):

    def test_obfuscation_detection(self):
        # Mock file content representing a simple code structure
        file_content = b'function1 function2 function3'
        code_graph = create_code_graph(file_content)
        is_obfuscated = detect_obfuscation(code_graph)
        self.assertIsInstance(is_obfuscated, bool)

if __name__ == '__main__':
    unittest.main()
