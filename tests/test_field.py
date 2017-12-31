import sys, os
path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(path)

import unittest
from field import Field

class TestField(unittest.TestCase):
    def test_init(self):
        field = Field()
        self.assertEqual(len(field.blocks), 20)
        self.assertEqual(len(field.blocks[0]), 10)

    def test_set_and_get_block(self):
        field = Field()
        field.set_block(0, 0, 0)
        field.set_block(9, 19, 6)
        self.assertEqual(field.get_block(0, 0), 0)
        self.assertEqual(field.get_block(9, 19), 6)
        self.assertEqual(field.get_block(3, 3), None)

if __name__ == '__main__':
    unittest.main()
