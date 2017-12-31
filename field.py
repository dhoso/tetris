class Field:
    WIDTH = 10
    HEIGHT = 20

    def __init__(self):
        # FIXME: たぶんこの初期化方法ではまともに動かない。
        self.blocks = [[None] * Field.WIDTH] * Field.HEGIHT

    def get_block(self, x, y):
        return self.blocks[x][y]

    def set_block(self, x, y, value):
        self.blocks[x][y] = value
