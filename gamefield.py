import numpy as np
import draw
import constants


class GameField:
    def __init__(self):
        self.playing = False
        self.bomb_field = np.array([])
        self.user_field = np.array([])
        self.game_field = np.array([])
        self.height = 0
        self.width = 0
        self.bombs = 0
        self.opened_cells = 0
        self.picture = draw.PicField()

    def delete_data(self):
        self.playing = False
        self.bomb_field = np.array([])
        self.user_field = np.array([])
        self.game_field = np.array([])
        self.height = 0
        self.width = 0
        self.bombs = 0
        self.opened_cells = 0

    def init_game_field(self, user_arguments, chat_id):
        self.playing = True
        self.bomb_field = np.zeros((user_arguments.height, user_arguments.width))
        self.game_field = np.zeros((user_arguments.height, user_arguments.width))
        self.user_field = np.array([constants.EMPTY] * (user_arguments.width * user_arguments.height))
        self.user_field = np.resize(self.user_field, (user_arguments.height, user_arguments.width))
        self.height = user_arguments.height
        self.width = user_arguments.width
        self.bombs = user_arguments.bombs
        self.opened_cells = 0
        self.plant_bombs_()
        self.init_bomb_field_()
        self.picture.new_field('{}.jpg'.format(chat_id), user_arguments.height, user_arguments.width)

    def plant_bombs_(self):
        self.bomb_field = np.hstack(self.bomb_field)
        for i in range(0, self.bombs):
            self.bomb_field[i] = 1
        np.random.shuffle(self.bomb_field)
        self.bomb_field = np.resize(self.bomb_field, (self.height, self.width))

    def init_bomb_field_(self):
        for i in range(0, self.height):
            for j in range(0, self.width):
                self.game_field[i][j] = self.init_cell_(i, j)

    def init_cell_(self, index_i, index_j):
        if self.bomb_field[index_i][index_j] == 1:
            return 0
        sum_ = 0
        for i in (-1, 0, 1):
            for j in (-1, 0, 1):
                if 0 <= index_j + j < self.width and 0 <= index_i + i < self.height:
                   sum_ += self.bomb_field[index_i + i][index_j + j]
        return sum_

    def draw_lose_field(self, x, y):
        for i in range(0, self.height):
            for j in range(0, self.width):
                if not(x == i and y == j) and self.bomb_field[i][j] == 1:
                    self.picture.draw_bomb(i, j)
        self.picture.draw_exploded_bomb(x, y)

    def draw_win_field(self):
        for i in range(0, self.height):
            for j in range(0, self.width):
                if self.bomb_field[i][j] == 1:
                    self.picture.draw_bomb(i, j)

    def open_cell(self, x, y):
        if self.user_field[x][y] == constants.FLAGGED:
            self.remove_flag_cell(x, y)
            return
        if self.bomb_field[x][y] == 1:
            self.draw_lose_field(x, y)
            self.playing = False
            return constants.LOSER
        elif self.game_field[x][y] != 0:
            self.user_field[x][y] = self.game_field[x][y]
            self.picture.draw_number(x, y, self.user_field[x][y])
            self.opened_cells += 1
        else:
            self.open_zero_cells(x, y)
        if self.opened_cells == self.height * self.width - self.bombs:
            self.draw_win_field()
            self.playing = False
            return constants.WINNER
        else:
            return constants.INPROGRESS

    def open_zero_cells(self, x, y):
        if self.user_field[x][y] != constants.EMPTY:
            return
        self.user_field[x][y] = self.game_field[x][y]
        self.opened_cells += 1
        self.picture.draw_number(x, y, self.user_field[x][y])
        if self.game_field[x][y] != 0:
            return
        if x > 0:
            self.open_zero_cells(x - 1, y)
        if y > 0:
            self.open_zero_cells(x, y - 1)
        if x < self.height - 1:
            self.open_zero_cells(x + 1, y)
        if y < self.width - 1:
            self.open_zero_cells(x, y + 1)

    def flag_cell(self, x, y):
        if self.user_field[x][y] == constants.FLAGGED:
            return False
        self.user_field[x][y] = constants.FLAGGED
        self.picture.draw_flag(x, y)
        return True

    def remove_flag_cell(self, x, y):
        if self.user_field[x][y] == constants.FLAGGED:
            self.user_field[x][y] = constants.EMPTY
            self.picture.remove_flag(x, y)
            return True
        return False

    def __str__(self):
        return str(self.user_field)
