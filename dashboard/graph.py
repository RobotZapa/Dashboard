import pygame
from pygame.locals import *
from dashboard.tools import *
import math


class LiveGraph:
    def __init__(self, window, name, col=None, row=None, domain=(0, 1), **kwargs):
        '''
        :param window: the WindowGrid object
        :param name: the name of the gauge
        :param row: the row(s) for the gauge to fill
        :param col: the col(s) for the gauge to fill
        :param kwargs: zoom (int 1 to 4 is reasonable)
        '''
        self.window = window
        self.name = name
        self.domain = domain
        self.col, self.row = col, row
        self.surface, self.position, self.size = window.tile(row, col)
        self.graph_surface, self.graph_position, self.graph_size = \
            window.tile_fraction(col, row, top=1 / 8, left=1 / 8, bottom=1 / 8)
        self.colors = {'background': (255, 255, 255), 'line': (0, 0, 0),
                       'label': (255, 0, 0), 'grid': (225, 225, 225), 'name': (0, 0, 0)}
        self.scale_divisor = kwargs['scale_divisor'] if 'scale_divisor' in kwargs else 10
        self.domain_delta = abs(domain[1] - domain[0])
        self.domain_offset = domain[1]
        self.refresh = 16
        self.center_x = int(self.size[0]/2)
        self.last = self.graph_size[1]/2
        self.current = self.graph_size[1]/2
        font_size = int(self.size[1] / 12)
        font = pygame.font.Font('freesansbold.ttf', font_size)
        self.label_text = font.render(self.name, True, self.colors['name'])
        self.label_text_rect = self.label_text.get_rect()
        self.label_text_rect.center = (self.center_x, font_size / 2)
        self.scale_font_size = int(self.size[1] / 24)
        self.zoom = 2 if 'zoom' not in kwargs else kwargs['zoom']

        self.first()

    @concurrent
    def test(self):
        x = 0
        while True:
            x += 0.1
            self.update(((self.domain_delta/2)*math.sin(x)-2*self.domain[0]))
            pygame.time.wait(self.refresh)

    def draw_text(self):
        self.surface.blit(self.label_text, self.label_text_rect)

    def label_scale(self):
        font = pygame.font.Font('freesansbold.ttf', self.scale_font_size)
        pos_x = int(self.size[0]/16)
        for i in range(0, self.scale_divisor+1):
            vert = self.graph_position[1] + i * int(self.graph_size[1] / self.scale_divisor)
            value = round(self.domain[1] - (self.domain_delta / self.scale_divisor) * i, 3)
            self.label_text = font.render(str(value), True, self.colors['name'])
            self.label_text_rect = self.label_text.get_rect()
            self.label_text_rect.center = (pos_x, vert)
            self.surface.blit(self.label_text, self.label_text_rect)

    def scale_lines(self):
        for i in range(0, self.scale_divisor+1):
            vert = i * int(self.graph_size[1] / self.scale_divisor)
            pygame.draw.line(self.graph_surface, self.colors['grid'], (0, vert), (self.graph_size[0], vert))

    def insert(self, value):
        '''
        Converts a value in domain to a graph point
        :param value: the value to insert
        :return:
        '''
        value -= self.domain_offset
        self.last = self.current
        self.current = (self.graph_size[1] / self.domain_delta) * value

    def first(self):
        self.surface.fill(self.colors['background'])
        self.graph_surface.fill(self.colors['background'])
        self.draw_text()
        self.scale_lines()
        self.label_scale()
        self.window.window.blit(self.surface, self.position)

    def update(self, x):
        '''
        Adds new data to graph and displays, chucking old data
        :param x:
        :return:
        '''
        pygame.draw.aaline(self.graph_surface, self.colors['line'], (self.graph_size[0] - (2*(1+self.zoom)), self.last),
                           (self.graph_size[0] - (2+self.zoom), self.current))
        self.graph_surface.scroll(-self.zoom)
        self.insert(x)
        self.window.window.blit(self.graph_surface, self.graph_position)

