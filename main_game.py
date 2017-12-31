import random

class MainGame:
    STATUS_INITIALIZING = 0
    STATUS_GENERATING_TETRIMINO = 1
    STATUS_CONTROLLING_TETRIMINO = 2
    STATUS_DELETING_BLOCKS = 3
    STATUS_GAMEOVER = 4

    def __init__(self, screen, assets):
        self.status = MainGame.STATUS_INITIALIZING
        self.screen = screen
        self.next_tetrimino_type = random.randint(6)
        self.assets = assets

    def run(self):
        if self.status == MainGame.STATUS_INITIALIZING:
            self.__initialize()
            self.__generate_tetrimino()
            self.__control_tetrimino()

        elif self.status == MainGame.STATUS_GENERATING_TETRIMINO:
            self.__generate_tetrimino()
            self.__control_tetrimino()

        elif self.status == MainGame.STATUS_CONTROLLING_TETRIMINO:
            self.__control_tetrimino()

        elif self.status == MainGame.STATUS_DELETING_BLOCKS:
            self.__delete_blocks()

    def __initialize(self):
        self.next_tetrimino

        self.screen.fill((255,255,255))

    def __generate_tetrimino(self):
        self.tetrimino = Tetrimino(self.next_tetrimino_type)
        self.next_tetrimino_type = random.randint(0, 6)
        is_generatable = self.determine_generatability(self.field, self.tetrimino)
        if not is_generatable:
            self.status = MainGame.STATUS_GAMEOVER
            return

    def __control_tetrimino(self):
        pass

    def __delete_blocks(self):
        pass
