import sys, os
path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
sys.path.append(path)

import unittest
from tetrimino import Tetrimino

class TestTetrimino(unittest.TestCase):
    def test_generate_blocks_as_coodinate_array(self):
        tetrimino = Tetrimino(0)
        tetrimino.set_base((3, 0))
        blocks = tetrimino.generate_blocks_as_coodinate_array()
        self.assertEqual(blocks, [(4, 0), (4, 1), (4, 2), (4, 3)])

        tetrimino = Tetrimino(6)
        tetrimino.set_base((3, 0))
        blocks = tetrimino.generate_blocks_as_coodinate_array()
        self.assertEqual(blocks, [(4, 0), (4, 1), (5, 1), (4, 2)])

    def test_generate_blocks_as_field_format(self):
        def check_blocks_by_position(field, pos, block_type):
            self.assertEqual(field[pos[1]][pos[0]], block_type)

        block_type = 0
        tetrimino = Tetrimino(block_type)
        tetrimino.set_base((3, 0))
        blocks = tetrimino.generate_blocks_as_field_format()
        check_blocks_by_position(blocks, (0, 0), None)
        check_blocks_by_position(blocks, (4, 0), block_type)
        check_blocks_by_position(blocks, (4, 1), block_type)
        check_blocks_by_position(blocks, (4, 2), block_type)
        check_blocks_by_position(blocks, (4, 3), block_type)
        check_blocks_by_position(blocks, (4, 4), None)

    def test_rotate(self):
        tetrimino = Tetrimino(0)

        tetrimino.rotate()
        tetrimino.rotate()
        tetrimino.rotate()
        self.assertEqual(tetrimino.rotation, 3)

        tetrimino.rotate()
        self.assertEqual(tetrimino.rotation, 0)

if __name__ == '__main__':
    unittest.main()
