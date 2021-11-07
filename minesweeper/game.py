# TODO
# - [x] Flags
# - [x] Win Game
# - [x] Lose Game
# - [ ] restart
# - [ ] Easy / Med / Hard
# - [ ] Scoring
# - [ ] API
# - [ ] RL Model 
# - ...
# - [ ] Flag counter
# - [ ] Indent when mouse button down


# Conditions for Winning
# - all unknown cells are mines + all flags are mines (no incorrect flags)
# - all unknown cells are mines + flags are mines




# Conditions for Losing
# - click on a mine


import random
import pygame


pygame.init()  # initialize pygame modules


# import image files
sprite_unkwn = pygame.image.load('sprites/Grid.png')
sprite_0 = pygame.image.load('sprites/empty.png')
sprite_1 = pygame.image.load('sprites/grid1.png')
sprite_2 = pygame.image.load('sprites/grid2.png')
sprite_3 = pygame.image.load('sprites/grid3.png')
sprite_4 = pygame.image.load('sprites/grid4.png')
sprite_5 = pygame.image.load('sprites/grid5.png')
sprite_6 = pygame.image.load('sprites/grid6.png')
sprite_7 = pygame.image.load('sprites/grid7.png')
sprite_8 = pygame.image.load('sprites/grid8.png')
sprite_flag = pygame.image.load('sprites/flag.png')
sprite_mine = pygame.image.load('sprites/mine.png')
sprite_mine_clicked = pygame.image.load('sprites/mineClicked.png')
sprite_mine_false = pygame.image.load('sprites/mineFalse.png')


# creating the field
rows = 10
cols = 10
mine_count = 10

cell_count = rows * cols
mine_locs = random.sample(range(cell_count), mine_count)

field = [[0] * cols for _ in range(rows)]

for loc in mine_locs:
    row = loc // rows
    col = loc % rows
    field[row][col] = -1

for loc in mine_locs:
    row = loc // rows
    col = loc % rows
    
    row_checks = [0]
    if row != 0:
        row_checks.append(-1)
    if row != rows-1:
        row_checks.append(1)
    
    col_checks = [0]
    if col != 0:
        col_checks.append(-1)
    if col != cols-1:
        col_checks.append(1)

    for i in row_checks:
        for j in col_checks:
            val = field[row+i][col+j]
            if val != -1:
                field[row+i][col+j] = val + 1        


class MineField:
    def __init__(self):
        pass


class Cell:
    def __init__(self):
        pass


# initialize screen
screen_width = 500
screen_height = 500
screen = pygame.display.set_mode([screen_width, screen_height])

cell_width = screen_width // rows
cell_height = screen_height // cols

class ScreenCell:
    def __init__(self, screen, value, row, col):
        self.screen = screen
        self.value = value
        self.rect = pygame.Rect(col*cell_width, row*cell_height, cell_width, cell_height)
        self._sprite = self.get_sprite(value)
        self.is_known = False
        self.is_flagged = False

    @property
    def sprite(self):
        if self.is_known:
            sprite = self._sprite
        elif self.is_flagged:
            sprite = sprite_flag
        else:
            sprite = sprite_unkwn
        return pygame.transform.scale(sprite, (cell_width, cell_height))

    def click(self):
        if not self.is_flagged:
            self.is_known = True
            self.blit()

    def click_flag(self):
        if not self.is_known:
            self.is_flagged = not self.is_flagged
            self.blit()

    def blit(self):
        self.screen.blit(self.sprite, self.rect)

    @staticmethod
    def get_sprite(value):
        match value:
            case -1: return sprite_mine
            case 0: return sprite_0
            case 1: return sprite_1
            case 2: return sprite_2
            case 3: return sprite_3
            case 4: return sprite_4
            case 5: return sprite_5
            case 6: return sprite_6
            case 7: return sprite_7
            case 8: return sprite_8


# initilaize game board
screen.fill((255, 255, 255))

screen_field = [[None] * cols for _ in range(rows)]

# display cells
for i in range(rows):
    for j in range(cols):
        val = field[i][j]
        screen_cell = ScreenCell(screen, val, i, j)
        screen_field[i][j] = screen_cell
        screen_cell.blit()


def click_cell(row, col):
    cell = screen_field[row][col]
    cell.click()

    if cell.value == 0:
        row_checks = [0]
        if row != 0:
            row_checks.append(-1)
        if row != rows-1:
            row_checks.append(1)
        
        col_checks = [0]
        if col != 0:
            col_checks.append(-1)
        if col != cols-1:
            col_checks.append(1)
        
        for i in row_checks:
            for j in col_checks:
                if not (i == 0 and j == 0):
                    if not screen_field[row+i][col+j].is_known:
                        click_cell(row+i, col+j)

# initialize the event loop
running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONUP:
            for i in range(rows):
                for j in range(cols):
                    screen_cell = screen_field[i][j]
                    if screen_cell.rect.collidepoint(event.pos):
                        if event.button == 1:  # LEFT Click
                            click_cell(i, j)
                            
                            # check if lose - clicked on a mine that isn't flagged
                            if screen_cell.is_known and screen_cell.value == -1:
                                print('You lose')
                                running = False

                            # check if won
                            # all unknown are mines and all flags are correctly identified as mines
                            won = True
                            for ii in range(rows):
                                for jj in range(rows):
                                    if (not screen_field[ii][jj].is_known) or screen_field[ii][jj].is_flagged:
                                        if screen_field[ii][jj].value != -1:
                                            won = False
                                            break                                    
                            if won:
                                print('You Win!')

                        elif event.button == 3:  # RIGHT Click
                            screen_cell.click_flag()

    pygame.display.flip()

pygame.quit()

