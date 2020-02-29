import pygame
from pygame.locals import *
from dashboard.tools import *


class WindowGrid:
    def __init__(self, cols, rows, size, name="Dashboard"):
        '''
        Creates a Dashboard Window
        :param cols: number of grid cols (units of width)
        :param rows: number of grid rows (units of height)
        :param size: "600x800" or "fullscreen" or "resizable"
        :param name: the name of the window
        '''
        self.rows = rows
        self.cols = cols
        self.frame_delay = 30  # milliseconds per frame
        self.background_color = (0, 0, 0)

        pygame.init()
        pygame.display.set_caption(name)
        # TODO pygame.display.set_icon(pygame.image.load("Icon.png"))

        # SELF.WINDOW CONSTRUCTION
        x, y = (800, 600)
        if "x" in size:
            x, y = size.split('x')
            if ' ' in x:
                x = x.split(' ')[-1]
            if ' ' in y:
                y = y.split(' ')[0]
            x, y = int(x), int(y)
        if "fullscreen" in size.lower():
            self.window = pygame.display.set_mode([x, y], flags=FULLSCREEN)
        elif "resizable" in size.lower():
            self.window = pygame.display.set_mode([x, y], flags=RESIZABLE)
        else:
            self.window = pygame.display.set_mode([x, y])

        # CALCULATED VARIABLES
        self.size = (x, y)
        self.tile_size = (self.size[0] / self.rows, self.size[1] / self.cols)

        self.__window_thread()

    @concurrent
    def __window_thread(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    running=False
            pygame.display.update()
            pygame.time.wait(self.frame_delay)

    def tile(self, row, col):
        '''
        Returns the (size_x, size_y, pos_x, pos_y) dimensions of the surface for a given tile
        :param row: position in grid [int or (start, stop)]
        :param col: position in grid [int or (start, stop)]
        :return: a surface, (x,y) position of the surface, (x,y) size of the surface
        '''
        row_count = 1 if type(row) == int else row[1] - row[0] + 1
        col_count = 1 if type(col) == int else col[1] - col[0] + 1
        row_start = row if type(row) == int else row[0]
        col_start = col if type(col) == int else col[0]
        sizex = self.tile_size[0] * row_count
        sizey = self.tile_size[1] * col_count
        posx = self.tile_size[0] * row_start
        posy = self.tile_size[1] * col_start
        TileSurface = pygame.Surface((sizex, sizey), SRCALPHA)
        TileSurface.fill(self.background_color)
        return TileSurface, (posx, posy), (sizex, sizey)

