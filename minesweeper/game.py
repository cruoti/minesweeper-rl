import random
import pygame


pygame.init()  # initialize pygame modules


# import image files
sprite_empty = pygame.image.load('sprites/empty.png')
sprite_flag = pygame.image.load('sprites/flag.png')
sprite_unkwn = pygame.image.load('sprites/Grid.png')
sprite_1 = pygame.image.load('sprites/grid1.png')
sprite_2 = pygame.image.load('sprites/grid2.png')
sprite_3 = pygame.image.load('sprites/grid3.png')
sprite_4 = pygame.image.load('sprites/grid4.png')
sprite_5 = pygame.image.load('sprites/grid5.png')
sprite_6 = pygame.image.load('sprites/grid6.png')
sprite_7 = pygame.image.load('sprites/grid7.png')
sprite_8 = pygame.image.load('sprites/grid8.png')
sprite_mine = pygame.image.load('sprites/mine.png')
sprite_mine_clicked = pygame.image.load('sprites/mineClicked.png')
sprite_mine_false = pygame.image.load('sprites/mineFalse.png')


# creating the field
rows = 10
cols = 10
mine_count = 50

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

    # [0] [1] [2]
    # [3] [x] [4]
    # [5] [6] [7]
    
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


print(field)


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
    def __init__(self, value, row, col):
        self.value = value
        self.rect = pygame.Rect(col*cell_width, row*cell_height, cell_width, cell_height)
        self._sprite = self.get_sprite(value)
    
    @property
    def sprite(self):
        return pygame.transform.scale(self._sprite, (cell_width, cell_height))
    
    @staticmethod
    def get_sprite(value):
        match value:
            case -1:
                return sprite_mine
            case 0:
                return sprite_empty
            case 1:
                return sprite_1
            case 2:
                return sprite_2
            case 3:
                return sprite_3
            case 4:
                return sprite_4
            case 5:
                return sprite_5
            case 6:
                return sprite_6
            case 7:
                return sprite_7
            case 8:
                return sprite_8


# initilaize game board
screen.fill((255, 255, 255))

screen_field = [[None] * cols for _ in range(rows)]


# TEST 4
for i in range(rows):
    for j in range(cols):
        val = field[i][j]
        screen_cell = ScreenCell(val, i, j)
        screen_field[i][j] = screen_cell
        screen.blit(screen_cell.sprite, screen_cell.rect)
        # match val:
        #     case -1:
        #         sprite = sprite_mine
        #     case 0:
        #         sprite = sprite_empty
        #     case 1:
        #         sprite = sprite_1
        #     case 2:
        #         sprite = sprite_2
        #     case 3:
        #         sprite = sprite_3
        #     case 4:
        #         sprite = sprite_4
        #     case 5:
        #         sprite = sprite_5
        #     case 6:
        #         sprite = sprite_6
        #     case 7:
        #         sprite = sprite_7
        #     case 8:
        #         sprite = sprite_8

        # rect = pygame.Rect(j*cell_width, i*cell_height, cell_width, cell_height)
        # screen.blit(
        #     pygame.transform.scale(sprite, (cell_width, cell_height)),
        #     rect
        # )

# initialize the event loop
running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONUP:
            print('click')
    
    # screen.fill((255, 255, 255))

    # TEST 1
    # pygame.draw.circle(screen, (0, 0, 255), (250, 250), 75)
    
    # TEST 2
    # surf = pygame.Surface((25, 25))
    # surf.fill((0, 0, 0))
    # screen.blit(surf, (25, 25))

    # TEST 3
    # rect = pygame.Rect(0, 0, cell_width, cell_height)
    # screen.blit(pygame.transform.scale(sprite_unkwn, (cell_width, cell_height)), rect)

    # rect2 = pygame.Rect(cell_width, cell_height, cell_width, cell_height)
    # screen.blit(sprite_unkwn, rect2)

    # # rect3 = pygame.Rect(2*cell_width, 2*cell_height, )

    # # TEST 4
    # for i in range(rows):
    #     for j in range(cols):
    #         val = field[i][j]
    #         match val:
    #             case -1:
    #                 sprite = sprite_mine
    #             case 0:
    #                 sprite = sprite_empty
    #             case 1:
    #                 sprite = sprite_1
    #             case 2:
    #                 sprite = sprite_2
    #             case 3:
    #                 sprite = sprite_3
    #             case 4:
    #                 sprite = sprite_4
    #             case 5:
    #                 sprite = sprite_5
    #             case 6:
    #                 sprite = sprite_6
    #             case 7:
    #                 sprite = sprite_7
    #             case 8:
    #                 sprite = sprite_8

    #         rect = pygame.Rect(j*cell_width, i*cell_height, cell_width, cell_height)
    #         screen.blit(
    #             pygame.transform.scale(sprite, (cell_width, cell_height)),
    #             rect
    #         )


    pygame.display.flip()

pygame.quit()

