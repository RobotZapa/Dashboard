import pygame
from pygame.locals import *
from dashboard.tools import *
import math


class LiveGraph:
    def __init__(self, window, name, col=None, row=None, domain=(0, 1), **kwargs):
        '''
        TODO: To make this faster the entire frame should be translated one pixel every frame
         and only a single pixel graph should be rendered.

        :param window: the WindowGrid object
        :param name: the name of the gauge
        :param row: the row(s) for the gauge to fill
        :param col: the col(s) for the gauge to fill
        :param kwargs:
        '''
        self.window = window
        self.name = name
        self.domain = domain
        self.surface, self.position, self.size = window.tile(row, col)
        self.colors = {'background': (255, 255, 255), 'line': (0, 0, 0),
                       'label': (255, 0, 0), 'grid': (225, 225, 225), 'name': (0, 0, 0)}
        self.scale_divisor = kwargs['scale_divisor'] if 'scale_divisor' in kwargs else 10
        self.domain_delta = abs(domain[1] - domain[0])
        self.domain_offset = domain[1]
        self.stretch = 1
        self.refresh = 30
        self.center_x = int(self.size[0]/2)
        self.queue = [(i, self.size[1]/2) for i in range(0, int(self.size[0]), self.stretch)]

        font_size = int(self.size[1] / 12)
        font = pygame.font.Font('freesansbold.ttf', font_size)
        self.label_text = font.render(self.name, True, self.colors['name'])
        self.label_text_rect = self.label_text.get_rect()
        self.label_text_rect.center = (self.center_x, font_size / 2)

        self.scale_font_size = int(self.size[1] / 24)

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
        for i in range(self.domain[0], self.domain[1], self.scale_divisor):
            self.label_text = font.render(str(i), True, self.colors['name'])
            self.label_text_rect = self.label_text.get_rect()
            self.label_text_rect.center = (0, 0)
            self.surface.blit(self.label_text, self.label_text_rect)

    def scale_lines(self):
        for i in range(self.domain[0], self.domain[1], self.scale_divisor):
            vert = (self.size[1] / self.domain_delta) * (i + self.domain_offset)
            pygame.draw.line(self.surface, self.colors['grid'], (0, vert), (self.size[0], vert))

    def insert(self, value):
        '''
        Converts a value in domain to a graph point
        :param value: the value to insert
        :return:
        '''
        value -= self.domain_offset
        self.queue.pop(0)
        for i, e in enumerate(self.queue):
            self.queue[i] = (e[0] - self.stretch, e[1])
        self.queue.append((self.size[0], (self.size[1] / self.domain_delta) * value))

    def update(self, x):
        '''
        Adds new data to graph and displays, chucking old data
        :param x:
        :return:
        '''
        self.insert(x)
        self.surface.fill(self.colors['background'])
        #self.draw_text()
        #self.scale_lines()
        pygame.draw.aalines(self.surface, self.colors['line'], False, self.queue)
        self.window.window.blit(self.surface, self.position)

