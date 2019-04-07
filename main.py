import pygame
import random
import colors
import time

BOMBS = 25
WINDOW = [322, 322]
MARGIN = 2
WIDTH = 30

class Main:
    def __init__(self):
        pygame.init()
        self.lost = False
        self.done = False
        self.x = 0  # clicked bomb x cords
        self.y = 0  # y cords
        self.grid = [ [ Field() for x in range(10)] for y in range(10) ]
        self.screen = pygame.display.set_mode(WINDOW)
        self.setbomb()
        self.create_images()
        pygame.display.set_caption("Minesweeper")
        self.mainLoop()

    def mainLoop(self):
    #------- MAIN LOOP -------
        while not self.lost:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        cords = pygame.mouse.get_pos()
                        col = cords[0] // (WIDTH + MARGIN)
                        row = cords[1] // (WIDTH + MARGIN)
                        self.grid[row][col].nearby = self.mask(row, col)
                    elif event.button == 3:
                        cords = pygame.mouse.get_pos()
                        col = cords[0] // (WIDTH + MARGIN)
                        row = cords[1] // (WIDTH + MARGIN)
                        self.grid[row][col].nearby = 69

            self.screen.fill((60,60,60))
            self.draw()
            self.checkwin()
            pygame.display.flip()
        self.lose()

    def create_images(self):
        self.image_empty = pygame.image.load('empty.png')
        self.image_empty = pygame.transform.scale(self.image_empty, (WIDTH, WIDTH))
        self.image_clicked = pygame.image.load('clicked.png')
        self.image_clicked = pygame.transform.scale(self.image_clicked, (WIDTH, WIDTH))
        self.image_bomb = pygame.image.load('bomb.png')
        self.image_bomb = pygame.transform.scale(self.image_bomb, (WIDTH, WIDTH))
        self.image_flag = pygame.image.load('flag.png')
        self.image_flag = pygame.transform.scale(self.image_flag, (WIDTH, WIDTH))
        self.image_bad_flag = pygame.image.load('bad_flag.png')
        self.image_bad_flag = pygame.transform.scale(self.image_bad_flag, (WIDTH, WIDTH))
        self.gameOver_image = pygame.image.load('explode.png')
        self.gameOver_image = pygame.transform.scale(self.gameOver_image, (200, 200))
        self.image_gameOverF = pygame.image.load('gameoverf.png')
        self.image_gameOverF = pygame.transform.scale(self.image_gameOverF, (120, 120))
        self.image_winner = pygame.image.load('winner.png')
        self.image_winner = pygame.transform.scale(self.image_winner, (290, 290))
        self.image_quit = pygame.image.load('quit.png')
        self.image_quit = pygame.transform.scale(self.image_quit, (95, 95))
        self.image_reset = pygame.image.load('reset.png')
        self.image_reset = pygame.transform.scale(self.image_reset, (95, 95))
        self.image_quit_bright = pygame.image.load('quit_bright.png')
        self.image_quit_bright = pygame.transform.scale(self.image_quit_bright, (95, 95))
        self.image_reset_bright = pygame.image.load('reset_bright.png')
        self.image_reset_bright = pygame.transform.scale(self.image_reset_bright, (95, 95))
        self.image_clicked_bomb = pygame.image.load('clicked_bomb.png')
        self.image_clicked_bomb = pygame.transform.scale(self.image_clicked_bomb, (WIDTH, WIDTH))

    def checkwin(self):
        flag_counter = 0
        bomb_counter = 0
        for row in range(10):
            for col in range(10):
                if self.grid[row][col].bomb == 10:
                    bomb_counter +=1
                if self.grid[row][col].bomb == 10 and self.grid[row][col].nearby == 69:
                    flag_counter +=1

        if bomb_counter == flag_counter:
            self.victory()

    def victory(self):
        for row in range(10):
            for col in range(10):
                if self.grid[row][col].bomb == 10:
                    x = ((MARGIN + WIDTH) * col + MARGIN)
                    y = ((MARGIN + WIDTH) * row + MARGIN)
                    self.screen.blit(self.image_flag, (x, y))
                elif self.grid[row][col].bomb == 0 and self.grid[row][col].nearby == 69:
                    x = ((MARGIN + WIDTH) * col + MARGIN)
                    y = ((MARGIN + WIDTH) * row + MARGIN)
                    self.screen.blit(self.image_bad_flag, (x, y))
        time.sleep(0.5)
        pygame.display.flip()
        fill = 0
        dark = pygame.Surface((WINDOW), pygame.SRCALPHA)  # per-pixel alpha
        while fill < 240:
            dark.fill((0, 0, 0, fill))  # alpha
            self.screen.blit(dark, (0, 0))
            pygame.display.flip()
            time.sleep(0.5)
            fill += 60
        self.screen.blit(self.image_winner, (20, 0))
        time.sleep(2)
        pygame.display.flip()
        self.screen.blit(self.image_reset, (34, 225))
        self.screen.blit(self.image_quit, (193, 225))
        pygame.display.flip()
        self.menu()

    def lose(self):
        for row in range(10):
            for col in range(10):
                if self.grid[row][col].bomb == 10:
                    if row == self.x and col == self.y:
                        x = ((MARGIN + WIDTH) * col + MARGIN)
                        y = ((MARGIN + WIDTH) * row + MARGIN)
                        self.screen.blit(self.image_clicked_bomb, (x, y))
                    else:
                        x = ((MARGIN + WIDTH) * col + MARGIN)
                        y = ((MARGIN + WIDTH) * row + MARGIN)
                        self.screen.blit(self.image_bomb, (x, y))
                elif self.grid[row][col].bomb == 0 and self.grid[row][col].nearby == 69:
                    x = ((MARGIN + WIDTH) * col + MARGIN)
                    y = ((MARGIN + WIDTH) * row + MARGIN)
                    self.screen.blit(self.image_bad_flag, (x, y))

        self.screen.blit(self.gameOver_image, (55, 65))
        time.sleep(1.5)
        pygame.display.flip()
        fill = 0
        dark = pygame.Surface((WINDOW), pygame.SRCALPHA)  # per-pixel alpha
        while fill < 240:
            dark.fill((0, 0, 0, fill))  # alpha
            self.screen.blit(dark, (0, 0))
            pygame.display.flip()
            time.sleep(0.5)
            fill += 60
        self.screen.blit(self.image_gameOverF, (95, 100))
        time.sleep(2)
        pygame.display.flip()
        self.screen.blit(self.image_reset, (34, 225))
        self.screen.blit(self.image_quit, (193, 225))
        pygame.display.flip()
        self.menu()

    def menu(self):
        choice = False
        while not choice:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    choice = True
                else:
                    mouse = pygame.mouse.get_pos()
                    if 120 > mouse[0] > 34 and 290 > mouse[1] > 250:
                        self.screen.blit(self.image_reset_bright, (35, 225))
                        pygame.display.flip()
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            Main()
                    else:
                        self.screen.blit(self.image_reset, (34, 225))
                        pygame.display.flip()

                    if 290 > mouse[0] > 200 and 290 > mouse[1] > 250:
                        self.screen.blit(self.image_quit_bright, (194, 225))
                        pygame.display.flip()
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            pygame.quit()
                    else:
                        self.screen.blit(self.image_quit, (193, 225))
                        pygame.display.flip()


    def setbomb(self):
        for bomb in range(BOMBS):
            while True:
                row = random.randint(0,9)
                col = random.randint(0,9)
                if self.grid[row][col].bomb == 0:
                    self.grid[row][col].bomb = 10
                    break


    def draw(self):

        if not self.lost:
            for row in range(10):
                for col in range(10):

                    color = colors.L_GREY
                    if self.grid[row][col].nearby == 10:
                        color = colors.RED
                    elif self.grid[row][col].nearby < 10 and self.grid[row][col].nearby > 0:
                        color = colors.GREY
                    elif self.grid[row][col].nearby == 69:
                        color = colors.GREEN

                    x = ((MARGIN + WIDTH) * col + MARGIN)
                    y = ((MARGIN + WIDTH) * row + MARGIN)
                    self.screen.blit(self.image_empty, (x, y))

                    if color == colors.RED:
                        x = ((MARGIN + WIDTH) * col + MARGIN)
                        y = ((MARGIN + WIDTH) * row + MARGIN)
                        self.screen.blit(self.image_clicked_bomb, (x, y))
                        self.lost = True
                        cords = pygame.mouse.get_pos()
                        col = cords[0] // (WIDTH + MARGIN)
                        row = cords[1] // (WIDTH + MARGIN)
                        self.x = row
                        self.y = col

                    if color == colors.GREEN:
                        x = ((MARGIN + WIDTH) * col + MARGIN)
                        y = ((MARGIN + WIDTH) * row + MARGIN)
                        self.screen.blit(self.image_flag, (x, y))

                    if color == colors.GREY and color != colors.RED:
                        x = ((MARGIN + WIDTH) * col + MARGIN)
                        y = ((MARGIN + WIDTH) * row + MARGIN)
                        self.screen.blit(self.image_clicked, (x, y))
                        font = pygame.font.SysFont(None, 35)
                        number = font.render(f"{self.grid[row][col].nearby - 1}", True,
                                             (self.color(self.grid[row][col].nearby - 1)))
                        self.screen.blit(number, [((MARGIN + WIDTH) * col + MARGIN) + 9,
                                                  ((MARGIN + WIDTH) * row + MARGIN) + 4.9])



    def color(self, number):
        color = colors.WHITE
        if number == 1:
            color = colors.GRANIT
        elif number == 2:
            color = colors.DEEP
        elif number == 3:
            color = colors.BLOODY
        elif number == 4:
            color = colors.VIOLET
        elif number == 5:
            color = colors.D_ORANGE
        elif number == 6:
            color = colors.D_RED
        elif number == 7:
            color = colors.GREEN
        elif number == 8:
            color = colors.BLACK

        return color

    def isValid(self,row,col):
        return (row >= 0) and (row <= 9) and (col >= 0) and (col <= 9)

    def mask(self,row,col):
        count = 1
        if (self.isValid(row, col) == True):
            if (self.grid[row][col].bomb == 10):
                return 10

        if (self.isValid(row - 1, col) == True):
            if (self.grid[row-1][col].bomb == 10):
                count +=1

        if (self.isValid(row + 1, col) == True):
            if (self.grid[row+1][col].bomb == 10):
                count +=1

        if (self.isValid(row, col+1) == True):
            if (self.grid[row][col+1].bomb == 10):
                count +=1

        if (self.isValid(row, col-1) == True):
            if (self.grid[row][col-1].bomb == 10):
                count +=1

        if (self.isValid(row - 1, col+1) == True):
            if (self.grid[row-1][col+1].bomb == 10):
                count +=1

        if (self.isValid(row - 1, col-1) == True):
            if (self.grid[row-1][col-1].bomb == 10):
                count +=1

        if (self.isValid(row + 1, col+1) == True):
            if (self.grid[row+1][col+1].bomb == 10):
                count +=1

        if (self.isValid(row + 1, col-1) == True):
            if (self.grid[row+1][col-1].bomb == 10):
                count +=1
        return count

class Field:
    def __init__(self):
        self.bomb = 0
        self.nearby = 0



    def getbomb(self):
        return self.bomb

    def getnearby(self):
        return self.nearby

    def setnearby(self, nearby):
        self.nearby = nearby

if __name__ == '__main__':
    game = Main()






