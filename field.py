class Field:
    WIDTH = 10
    HEIGHT = 20

    def __init__(self):
        self.blocks = [[None for i in range(Field.WIDTH)] for j in range(Field.HEIGHT)]

    def get_block(self, x, y):
        return self.blocks[y][x]

    def set_block(self, x, y, value):
        self.blocks[y][x] = value
