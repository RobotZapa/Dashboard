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

        self.sleep = pygame.time.wait

    @concurrent
    def loop(self, framerate):
        framerate = int(1000/framerate)
        while True:
            self.update()
            pygame.time.wait(framerate)

    def update(self):
        '''
        For use on Windows or Mac OS
        A coroutine to update the screen (must be done on main thread)
        :return:
        '''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)
        pygame.display.flip()

    def tile(self, col, row):
        '''
        Returns the (size_x, size_y, pos_x, pos_y) dimensions of the surface for a given tile
        :param col: position in grid [int or (start, stop)]
        :param row: position in grid [int or (start, stop)]
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

    def tile_fraction(self, col, row, top=0, right=0, left=0, bottom=0):
        '''
        A relative fraction of a tile
        :param col: position in grid [int or (start, stop)]
        :param row: position in grid [int or (start, stop)]
        :param top: a fraction of distance in y until the northern face of the tile_fraction
        :param right: a fraction of distance in x until the eastern face of the tile_fraction
        :param left: a fraction of distance in y until the southern face of the tile_fraction
        :param bottom: a fraction of distance in x until the western face of the tile_fraction
        :return:
        '''
        row_count = 1 if type(row) == int else row[1] - row[0] + 1
        col_count = 1 if type(col) == int else col[1] - col[0] + 1
        row_start = row if type(row) == int else row[0]
        col_start = col if type(col) == int else col[0]
        tile_size_x = self.tile_size[0] * col_count
        tile_size_y = self.tile_size[1] * row_count
        size_x = int(tile_size_x - (bottom + right) * tile_size_x)
        size_y = int(tile_size_y - (top + left) * tile_size_y)
        tile_pos_x = self.tile_size[0] * col_start
        tile_pos_y = self.tile_size[1] * row_start
        pos_x = tile_pos_x + top * tile_size_x
        pos_y = tile_pos_y + bottom * tile_size_y
        TileSurface = pygame.Surface((size_x, size_y), SRCALPHA)
        TileSurface.fill(self.background_color)
        return TileSurface, (pos_x, pos_y), (size_x, size_y)

    def tile_portion(self, col, row, size_x=None, size_y=None, offset_x=0, offset_y=0):
        '''
        (Recommended to use tile_fraction for non moving surfaces)
        Returns a subsurface for a tile (in the center of a tile without offset)
        :param col: position in grid [int or (start, stop)]
        :param row: position in grid [int or (start, stop)]
        :param size_x: the size of the subsurface in x
        :param size_y: the size of the subsurface in y
        :param offset_x: the offset from the center of the tile in x
        :param offset_y: the offset from the center of the tile in y
        :return: a surface, (x, y) position of the surface, (x, y) size of the surface
        '''
        row_count = 1 if type(row) == int else row[1] - row[0] + 1
        col_count = 1 if type(col) == int else col[1] - col[0] + 1
        row_start = row if type(row) == int else row[0]
        col_start = col if type(col) == int else col[0]
        half_x = int(self.tile_size[0] * row_count) / 2
        half_y = int(self.tile_size[1] * col_count) / 2
        posx = self.tile_size[0] * row_count \
            if size_x is None else (self.tile_size[0] * row_start) + (half_x - size_x/2) + offset_x
        posy = self.tile_size[1] * col_start \
            if size_y is None else (self.tile_size[1] * col_start) + (half_y - size_y/2) + offset_y
        TileSurface = pygame.Surface((size_x, size_y), SRCALPHA)
        TileSurface.fill(self.background_color)
        return TileSurface, (posx, posy), (size_x, size_y)
