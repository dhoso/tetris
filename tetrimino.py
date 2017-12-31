from tetrimino_pattern import TetriminoPattern

class Tetrimino:
    FIELD_WIDTH = 10
    FIELD_HEIGHT = 20
    ROTATE_NUM = 4
    patterns = TetriminoPattern()

    def __init__(self, tetrimino_type):
        self.tetrimino_type = tetrimino_type
        self.rotation = 0
        self.base = (3, 0)

    def generate_blocks_as_coodinate_array(self):
        pattern = Tetrimino.patterns.get_pattern(self.tetrimino_type, self.rotation)
        pattern = self.__convert_one_into_position(pattern)
        pattern = self.__flatten(pattern)
        pattern = self.__eliminate_none(pattern)
        block_positoins = self.__add_position_array(pattern, self.base)

        return block_positoins

    def generate_blocks_as_field_format(self):
        block_positions = self.generate_blocks_as_coodinate_array()

        blocks_field = [[None for i in range(self.FIELD_WIDTH)] for j in range(self.FIELD_HEIGHT)]
        for block in block_positions:
            blocks_field[block[1]][block[0]] = self.tetrimino_type

        return blocks_field

    def rotate(self):
        self.rotation = (self.rotation + 1) % 4

    def set_base(self, base):
        self.base = base

    # Converts one into its position in 2d list
    # Example: [[0, 1], [1, 0]] -> [[None, (0, 1)], [(1, 0), None]]
    def __convert_one_into_position(self, li):
        return [[(j, i) if val == 1 else None for j, val in enumerate(row)] for i, row in enumerate(li)]

    # Flattens a 2d list into 1d
    # Example: [[0, 1], [2, 3]] -> [0, 1, 2, 3]
    def __flatten(self, li):
        return [y for x in li for y in x]

    # Eliminate None in a list
    # Example: [0, 1, None, 2, None] -> [0, 1, 2]
    def __eliminate_none(self, li):
        return [i for i in li if i is not None]

    # Add a position into all positional elements in an array
    # Example: li: [(0, 1), (2, 3)], additional_pos: (10, 10) -> [(10, 11), (12, 13)]
    def __add_position_array(self, li, additional_pos):
        return [(i[0] + additional_pos[0], i[1] + additional_pos[1]) for i in li]
