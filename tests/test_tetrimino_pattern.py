import sys, os
path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(path)

import unittest
from tetrimino_pattern import TetriminoPattern

class TestTetriminoPattern(unittest.TestCase):
    def test_get_pattern(self):
        patterns = TetriminoPattern()
        self.assertEqual(patterns.get_pattern(0, 0), [[0, 1, 0, 0], [0, 1, 0, 0], [0, 1, 0, 0], [0, 1, 0, 0]])
        self.assertEqual(patterns.get_pattern(6, 3), [[0, 1, 0, 0], [1, 1, 1, 0], [0, 0, 0, 0], [0, 0, 0, 0]])

if __name__ == '__main__':
    unittest.main()
