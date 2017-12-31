import pygame

class Field:
    WIDTH = 10
    HEIGHT = 20

    def __init__(self, assets):
        self.blocks = [[None for i in range(Field.WIDTH)] for j in range(Field.HEIGHT)]
        self.assets = assets

    def get_block(self, x, y):
        return self.blocks[y][x]

    def set_block(self, x, y, value):
        self.blocks[y][x] = value

    def draw(self, screen):
        for y in range(Field.HEIGHT):
            for x in range(Field.WIDTH):
                block_type = self.get_block(x, y)
                if block_type == None:
                    shape = pygame.Rect(x * 10, y * 10, 10, 10)
                    pygame.draw.rect(screen, (0, 0, 0), shape)
                else:
                    image = self.assets['block_imaeg_list'][block_type]
                    screen.blit(image, (x * 10, y * 10))

    def try_delete_blocks(self):
        while True:
            deletable_row_index = []
            for i, row in enumerate(self.blocks):
                if None not in row:
                    deletable_row_index.append(i)

            if len(deletable_row_index) == 0:
                return

            # Sort it by descending order to delete rows correctly
            deletable_row_index = sorted(deletable_row_index, reverse=True)
            deletable_rows_length = len(deletable_row_index)
            for i in deletable_row_index:
                self.blocks.pop(i)
            for i in range(deletable_rows_length):
                self.blocks.insert(0, [None] * Field.WIDTH)
