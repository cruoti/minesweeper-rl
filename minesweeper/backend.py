import random


class Cell:
    def __init__(self, value):#, row, col):
        self.value = value
        self.is_known = False
        self.is_flagged = False

    def click(self):
        self.is_known = True


class Game:
    def __init__(self, rows, cols, mine_count):
        self.rows = rows
        self.cols = cols
        self.mine_count = mine_count

        self.mine_locs = None
        self.field = None
        self.known_field = None

        self.is_game_over = False
        self.is_won = False

    @property
    def cell_count(self):
        return self.rows * self.cols

    @staticmethod
    def create_empty_field(fill_value, rows, cols):
        return [[fill_value] * cols for _ in range(rows)]

    def setup(self):
        self.is_game_over = False
        self.is_won = False

        mine_locs = sorted(random.sample(range(self.cell_count), self.mine_count))
        field = self.create_empty_field(0, self.rows, self.cols)
        # known_field = [[-2] * self.cols for _ in range(self.rows)]

        for loc in mine_locs:
            row = loc // self.cols
            col = loc % self.cols
            field[row][col] = -1

        for loc in mine_locs:
            row = loc // self.cols
            col = loc % self.cols
            
            row_checks = [0]
            if row != 0:
                row_checks.append(-1)
            if row != self.rows-1:
                row_checks.append(1)
            
            col_checks = [0]
            if col != 0:
                col_checks.append(-1)
            if col != self.cols-1:
                col_checks.append(1)

            for i in row_checks:
                for j in col_checks:
                    val = field[row+i][col+j]
                    if val != -1:
                        field[row+i][col+j] = val + 1        

        self.mine_locs = mine_locs
        self.field = field
        self.mine_field = [[None] * self.cols for _ in range(self.rows)]

        for i in range(self.rows):
            for j in range(self.cols):
                val = field[i][j]
                cell = Cell(val)#, i, j)
                self.mine_field[i][j] = cell

        return mine_locs, field, self.mine_field

    def click_cell(self, row, col):
        cell = self.mine_field[row][col]
        cell.click()

        if cell.value == -1:
            self.is_game_over = True
            return True

        if cell.value == 0:
            row_checks = [0]
            if row != 0:
                row_checks.append(-1)
            if row != self.rows-1:
                row_checks.append(1)
            
            col_checks = [0]
            if col != 0:
                col_checks.append(-1)
            if col != self.cols-1:
                col_checks.append(1)
            
            for i in row_checks:
                for j in col_checks:
                    if not (i == 0 and j == 0):
                        if not self.mine_field[row+i][col+j].is_known:
                            self.click_cell(row+i, col+j)

        if self.check_win():
            self.is_game_over = True
            self.is_won = True
            return True
        
        return False
        
    def check_win(self):
        # all unknown or flagged are mines
        for i in range(self.rows):
            for j in range(self.cols):
                if not self.mine_field[i][j].is_known:
                    if self.mine_field[i][j].value != -1:
                        return False
        return True


class EasyGame(Game):
    def __init__(self):
        super().__init__(rows=8, cols=10, mine_count=10)


class MedGame(Game):
    def __init__(self):
        super().__init__(rows=15, cols=18, mine_count=40)


class HardGame(Game):
    def __init__(self):
        super().__init__(rows=20, cols=24, mine_count=99)
