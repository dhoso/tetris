class TetriminoPattern:
    TETRIMINO_PATTERNS_FILE = 'assets/patterns.csv'
    PATTERN_WIDTH = 4
    PATTERN_HEIGHT = 4
    ROTATION_NUM = 4

    def __init__(self):
        with open(TetriminoPattern.TETRIMINO_PATTERNS_FILE) as f:
                data_raw = f.read().strip()

        data = self.__convert_csv_to_matrix(data_raw)
        data = self.__convert_str_to_int_in_matrix(data)

        self.data = self.__group_matrix(data)

    def get_pattern(self, tetrimino_type, rotation):
        return self.data[tetrimino_type][rotation]

    def __convert_csv_to_matrix(self, data):
        return list(map(lambda line: line.split(','), data.split('\n')))

    def __convert_str_to_int_in_matrix(self, data):
        return list(map(lambda x: list(map(lambda y: int(y) if y.isdigit() else None, x)), data))

    def __group_matrix(self, data):
        data = self.__group_list(data, TetriminoPattern.PATTERN_HEIGHT)
        return list(map(lambda row: self.__group_matrix_vertically(row, TetriminoPattern.PATTERN_WIDTH), data))

    # Groups list at a regular intervals.
    # Example: data: [0, 1, 2, 3, 4, 5], group_size: 2 -> [[0, 1], [2, 3], [4, 5]]]
    def __group_list(self, data, group_size):
        assert len(data) % group_size == 0, 'group_size is not a multiple of data length'
        return [[data[i * group_size + j] for j in range(group_size)] for i in range(int(len(data) / group_size))]

    # Groups matrix vertically at a regular intervals.
    # Example: data; [[0, 1, 2, 3], [4, 5, 6, 7]], group_size: 2 -> [[[0, 1], [4, 5]], [[2, 3], [6, 7]]]
    def __group_matrix_vertically(self, data, group_size):
        assert len(data[0]) % group_size == 0, 'group_size is not a multiple of data width'
        return [
                    [data[j][i*group_size:((i + 1) * group_size)] for j in range(len(data))]
                                                                  for i in range(int(len(data[0]) / group_size))
               ]
