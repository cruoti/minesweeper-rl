# TODO
# - [x] Flags
# - [x] Win Game
# - [x] Lose Game
# - [x] restart
# - [x] Easy / Med / Hard
# - [ ] Change difficulty interactively in game
# - [x] Scoring
# - [x] API
# - [x] OpenAI Gym Environment
# - [ ] RL Model 
# - ...
# - [ ] Flag counter
# - [ ] Timer
# - [ ] Reset Button
# - [ ] Indent when mouse button down


# Conditions for Winning
# - all unknown cells are mines + all flags are mines (no incorrect flags)
# - all unknown cells are mines + flags are mines
#
# Conditions for Losing
# - click on a mine


import pygame

from backend import Cell
from backend import Game, EasyGame, MedGame, HardGame


# import image files
SPRITE_UNKNWN = pygame.image.load('sprites/Grid.png')
SPRITE_0 = pygame.image.load('sprites/empty.png')
SPRITE_1 = pygame.image.load('sprites/grid1.png')
SPRITE_2 = pygame.image.load('sprites/grid2.png')
SPRITE_3 = pygame.image.load('sprites/grid3.png')
SPRITE_4 = pygame.image.load('sprites/grid4.png')
SPRITE_5 = pygame.image.load('sprites/grid5.png')
SPRITE_6 = pygame.image.load('sprites/grid6.png')
SPRITE_7 = pygame.image.load('sprites/grid7.png')
SPRITE_8 = pygame.image.load('sprites/grid8.png')
SPRITE_FLAG = pygame.image.load('sprites/flag.png')
SPRITE_MINE = pygame.image.load('sprites/mine.png')
SPRITE_MINE_CLICKED = pygame.image.load('sprites/mineClicked.png')
SPRITE_MINE_FALSE = pygame.image.load('sprites/mineFalse.png')


class GameOver(Exception): pass
class Quit(Exception): pass


class ScreenCell(Cell):
    def __init__(self, screen, cell_width, cell_height, value, row, col):
        super().__init__(value)
        self.screen = screen
        self.row = row
        self.col = col
        self.cell_width = cell_width
        self.cell_height = cell_height
        self.rect = pygame.Rect(col*cell_width, row*cell_height, cell_width, cell_height)
        self._sprite = self.get_sprite(value)
        self.is_flagged = False

    @property
    def sprite(self):
        if self.is_known:
            sprite = self._sprite
        elif self.is_flagged:
            sprite = SPRITE_FLAG
        else:
            sprite = SPRITE_UNKNWN
        return pygame.transform.scale(sprite, (self.cell_width, self.cell_height))

    def click(self):
        if not self.is_flagged:
            super().click()
            self.blit()

    def click_flag(self):
        if not self.is_known:
            self.is_flagged = not self.is_flagged
            self.blit()

    def blit(self):
        self.screen.blit(self.sprite, self.rect)
    
    def reveal(self):
        # unknown mines shown
          # flagged
          # not flogged
        # incorrectly flagged mines shown
        sprite = None

        if not self.is_known:
            if self.is_flagged and self.value != -1:  # incorrectly flagged
                sprite = SPRITE_MINE_FALSE
            elif self.value == -1:  # correctly flagged or unknown mines
                sprite = SPRITE_MINE
            
        if sprite is not None:
            self.screen.blit(pygame.transform.scale(sprite, (self.cell_width, self.cell_height)), self.rect)

    @staticmethod
    def get_sprite(value):
        match value:
            case -1: return SPRITE_MINE
            case 0: return SPRITE_0
            case 1: return SPRITE_1
            case 2: return SPRITE_2
            case 3: return SPRITE_3
            case 4: return SPRITE_4
            case 5: return SPRITE_5
            case 6: return SPRITE_6
            case 7: return SPRITE_7
            case 8: return SPRITE_8


class ScreenField(Game):
    def __init__(self, game, screen):
        self.__dict__ = game.__dict__.copy()
        self.screen = screen
        screen_width, screen_height = screen.get_size()
        self.cell_width = screen_width // self.cols
        self.cell_height = screen_height // self.rows

    def setup(self):
        mine_locs, field, __ = super().setup()
        self.screen.fill((255, 255, 255))
        for i in range(self.rows):
            for j in range(self.cols):
                val = self.field[i][j]
                self.mine_field[i][j] = ScreenCell(self.screen, self.cell_width, self.cell_height, val, i, j)
                self.mine_field[i][j].blit()
        return mine_locs, field, self.mine_field
    
    def popup_text(self, txt, font_size, yoff=0):
        screen_text = pygame.font.SysFont("Calibri", font_size, True).render(txt, True, (0, 0, 0), (255, 255, 255))
        screen_text.set_alpha(200)
        rect = screen_text.get_rect()
        screen_width, screen_height = self.screen.get_size()
        rect.center = (screen_width / 2, screen_height / 2 + yoff)
        self.screen.blit(screen_text, rect)

    def find_clicked_cell(self, pos):
        for i in range(self.rows):
            for j in range(self.cols):
                cell = self.mine_field[i][j]
                if cell.rect.collidepoint(pos):
                    return cell
        return None

    def game_loop(self):
        self.setup()

        screen_field = self.mine_field

        # initialize the event loop
        running = True
        is_game_over = False
        while running:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    raise Quit
                if is_game_over:
                    if event.type == pygame.KEYDOWN:
                        if pygame.key.name(event.key) == 'r':
                            self.game_loop()
                            raise Quit
                elif event.type == pygame.MOUSEBUTTONUP:
                    try:
                        clicked_cell = self.find_clicked_cell(event.pos)
                        if event.button == 1:  # LEFT Click
                            is_game_over = self.click_cell(clicked_cell.row, clicked_cell.col)

                            # check if lose - clicked on a mine that isn't flagged
                            if is_game_over and not self.is_won:
                                self.screen.blit(
                                    pygame.transform.scale(SPRITE_MINE_CLICKED, (self.cell_width, self.cell_height)), 
                                    clicked_cell.rect)
                                raise GameOver

                            # check if won
                            # all unknown are mines
                            if is_game_over and self.is_won:
                                raise GameOver

                        elif event.button == 3:  # RIGHT Click
                            clicked_cell.click_flag()

                    except GameOver:
                        # is_game_over = True
                        for i in range(self.rows):
                            for j in range(self.cols):
                                screen_field[i][j].reveal()
                        
                        if self.is_won:
                            self.popup_text('You Win!', 50, -25)
                        else:
                            self.popup_text('You Lose!', 50, -25)
                        self.popup_text("Click 'r' to play again", 50, 25)

            pygame.display.flip()


def main():
    pygame.init()
    
    screen_height = 500
    screen_width = screen_height * 1.2
    screen = pygame.display.set_mode([screen_width, screen_height])

    game = ScreenField(EasyGame(), screen)
    try:
        game.game_loop()
    except Quit:
        pygame.quit()


if __name__ == '__main__':
    main()
