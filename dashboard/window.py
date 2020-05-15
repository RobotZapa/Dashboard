import pygame
from pygame.locals import *
from dashboard.tools import *


class WindowGrid:
    def __init__(self, cols, rows, size, name="Dashboard", background_color=(0, 0, 0), frame_rate=60):
        '''
        Creates a Dashboard Window
        :param cols: number of grid cols (units of width)
        :param rows: number of grid rows (units of height)
        :param size: "600x800" or "fullscreen" or "resizable"
        :param name: the name of the window
        :param background_color: the color (r,g,b) of the background
        :param frame_rate: frames per second (default 60)
        '''
        self.rows = rows
        self.cols = cols
        self.background_color = background_color

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

        self.eventloop = Loop()
        self.eventloop.add(self.update)
        self.eventloop.add(self.sleep, int(1000 / frame_rate))
        self.framerate = frame_rate

    def loop(self, framerate):
        self.eventloop.loop()

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
        sizex = self.tile_size[0] * col_count
        sizey = self.tile_size[1] * row_count
        posx = self.tile_size[0] * col_start
        posy = self.tile_size[1] * row_start
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
        size_x = int(tile_size_x - (left + right) * tile_size_x)
        size_y = int(tile_size_y - (top + bottom) * tile_size_y)
        tile_pos_x = self.tile_size[0] * col_start
        tile_pos_y = self.tile_size[1] * row_start
        pos_x = tile_pos_x + left * tile_size_x
        pos_y = tile_pos_y + top * tile_size_y
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

class TileGrid:
    def __init__(self, window, col, row, num_cols, num_rows, background_color=None):
        '''
        Creates a Dashboard tile that can be used as a window object for elements
        Use this to split a single tile into it's own grid system
        :param row: the row(s) for the tile to fill
        :param col: the col(s) for the tile to fill
        :param num_cols: number of grid cols (units of width)
        :param num_rows: number of grid rows (units of height)
        :param background_color: the color (r,g,b,a) to be used for the backgrounds
        '''
        self.eventloop = window.eventloop
        self.window = window.window
        self.surface, self.position, self.size = window.tile(col, row)
        self.cols = num_cols
        self.rows = num_rows
        self.tile_size = (self.size[0] / self.rows, self.size[1] / self.cols)
        self.background_color = background_color if background_color is not None else window.background_color

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
        sizex = self.tile_size[0] * col_count
        sizey = self.tile_size[1] * row_count
        posx = self.tile_size[0] * col_start + self.position[0]
        posy = self.tile_size[1] * row_start + self.position[1]
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
        size_x = int(tile_size_x - (left + right) * tile_size_x)
        size_y = int(tile_size_y - (top + bottom) * tile_size_y)
        tile_pos_x = self.tile_size[0] * col_start
        tile_pos_y = self.tile_size[1] * row_start
        pos_x = tile_pos_x + left * tile_size_x
        pos_y = tile_pos_y + top * tile_size_y
        TileSurface = pygame.Surface((size_x, size_y), SRCALPHA)
        TileSurface.fill(self.background_color)
        return TileSurface, (pos_x, pos_y), (size_x, size_y)
