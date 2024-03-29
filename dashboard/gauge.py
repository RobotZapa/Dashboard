import pygame
import pygame.gfxdraw
from pygame.locals import *
from dashboard.tools import *
import math


class Gauge:
    def __init__(self, window, name, col=None, row=None, domain=(0, 1),
                 inlay=0, unit_ticks=True, tick_divisor=10, **kwargs):
        '''
        :param window: the WindowGrid object
        :param name: the name of the gauge
        :param row: the row(s) for the gauge to fill
        :param col: the col(s) for the gauge to fill
        :param domain: (minimum_value, maximum_value)
        :param kwargs:
                    | inlay=0 : lowers the gauge into the tile
                    | unit_ticks=true : every unit has a tick mark
                    | tick_divisor=10 : how many units is there a big tick and label
                    | img_file=None : an image to replace the automatic gauge generator
        '''
        #TODO image file
        self.window = window
        self.name = name
        self.surface, self.position, self.size = window.tile(col, row)
        self.needle_surface, self.needle_pos, self.needle_size = window.tile_fraction(col, row)
        self.unit_ticks = unit_ticks
        self.tick_divisor = tick_divisor
        self.inlay = inlay
        self.center = [int(self.size[0] / 2), int(self.size[1] / 2) + self.inlay]
        self.radius = int(min(self.size) / 2) + self.inlay
        self.domain = domain
        self.unit_delta = domain[1] - domain[0]
        normal = 2.0 / self.radius
        theta = math.pi / 2 - math.asin(1 - self.inlay * normal)
        self.gauge_units = (2.0 * math.pi - 2 * theta) / self.unit_delta
        self.gauge_start = 2.0 * math.pi - (math.pi / 2 + theta)
        self.needle_center = int(min(self.size) / 64)
        self.colors = {'dial': (240, 240, 240), 'needle': (255, 0, 0), 'tick': (0, 0, 0),
                       'text': (0, 255, 0), 'name': (0, 0, 0)}

        self.update(self.domain[0])
        self.first()

    @concurrent
    def test(self):
        while True:
            for i in range(self.domain[0], self.domain[1]):
                self.update(i)
                pygame.time.wait(10)
            for i in range(self.domain[1], self.domain[0], -1):
                self.update(i)
                pygame.time.wait(10)

    def value_to_cords(self, val, radius=None):
        if not radius:
            radius = self.radius
        val = self.gauge_units * val
        val = val - self.gauge_start
        x = math.cos(val) * radius + self.center[0]
        y = math.sin(val) * radius + self.center[1]
        return x, y

    def ticks(self, length=None):
        '''
        The number of ticks to make over the entire range
        :param length: length of ticks as root(2) * a number of pixels
        :return:
        '''
        if length is None:
            length = self.radius / 12
        for tick in range(self.domain[0], self.domain[1]):
            if self.unit_ticks:
                multipler = 3 if tick % self.tick_divisor == 0 else 2
                start = self.value_to_cords(tick, radius=self.radius - length * multipler)
                stop = self.value_to_cords(tick, radius=self.radius - length)
                pygame.draw.aaline(self.surface, self.colors['tick'], start, stop)
            elif tick % self.tick_divisor == 0:
                start = self.value_to_cords(tick, radius=self.radius - length * 2)
                stop = self.value_to_cords(tick, radius=self.radius - length)
                pygame.draw.aaline(self.surface, self.colors['tick'], start, stop)

    def labels(self):
        font_size = int(self.radius / 12)
        name_font = pygame.font.Font('freesansbold.ttf', font_size * 2)
        font = pygame.font.Font('freesansbold.ttf', font_size)

        text = name_font.render(self.name, True, self.colors['name'])
        textRect = text.get_rect()
        textRect.center = (self.center[0], self.center[1] - (self.radius / 12))
        self.surface.blit(text, textRect)
        # Numbers
        length = 4 * (self.radius / 12)
        for tick in range(self.domain[0], self.domain[1], self.tick_divisor):
            # font = pygame.font.Font('freesansbold.ttf', font_size)
            text = font.render(str(tick), True, self.colors['text'])
            textRect = text.get_rect()
            textRect.center = self.value_to_cords(tick, radius=self.radius - length)
            self.surface.blit(text, textRect)

    def needle(self, x):
        self.needle_surface.fill((0, 0, 0, 0))
        self.needle_surface.set_alpha(0)
        pygame.draw.line(self.needle_surface, self.colors['needle'], self.center, self.value_to_cords(x), 5)
        pygame.draw.circle(self.needle_surface, self.colors['tick'], self.center, self.needle_center)

    def first(self):
        pygame.draw.circle(self.surface, self.colors['dial'], self.center, self.radius + 1)
        self.ticks()
        self.labels()

    def update(self, x):
        self.needle(x)
        self.window.window.blit(self.surface, self.position)
        self.window.window.blit(self.needle_surface, self.position)


class ArcGauge:
    def __init__(self, window, name, col=None, row=None, domain=(0, 1),
                 inlay=0, unit_ticks=True, tick_divisor=10, **kwargs):
        '''
        :param window: the WindowGrid object
        :param name: the name of the gauge
        :param row: the row(s) for the gauge to fill
        :param col: the col(s) for the gauge to fill
        :param domain: (minimum_value, maximum_value)
        :param kwargs: inlay=0 | unit_ticks=false | tick_divisor=10 |
        '''
        self.window = window
        self.name = name
        self.surface, self.position, self.size = window.tile(col, row)
        self.needle_surface, self.needle_pos, self.needle_size = window.tile_fraction(col, row)
        self.unit_ticks = unit_ticks
        self.tick_divisor = tick_divisor
        self.inlay = inlay
        self.center = [int(self.size[0] / 2), int(self.size[1] / 2) + self.inlay]
        self.radius = int(min(self.size) / 2) + self.inlay
        self.domain = domain
        self.unit_delta = domain[1] - domain[0]
        normal = 2.0 / self.radius
        theta = math.pi / 2 - math.asin(1 - self.inlay * normal)
        self.gauge_units = (2.0 * math.pi - 2 * theta) / self.unit_delta
        self.gauge_start = 2.0 * math.pi - (math.pi / 2 + theta)
        self.needle_center = int(min(self.size) / 2)
        self.needle_rect = pygame.Rect(self.center[0]-int(min(self.size)/2), self.center[1]-int(min(self.size)/2),
                                       min(self.size), min(self.size))
        self.colors = {'dial': (0, 0, 0), 'needle': (255, 0, 0), 'tick': (255, 255, 255),
                       'text': (0, 255, 0), 'name': (255, 255, 255), 'clear': (0, 0, 0, 0)}

        self.update(self.domain[0])
        self.first()

    @concurrent
    def test(self):
        while True:
            for i in range(self.domain[0], self.domain[1]):
                self.update(i)
                pygame.time.wait(10)
            for i in range(self.domain[1], self.domain[0], -1):
                self.update(i)
                pygame.time.wait(10)

    def value_to_cords(self, val, radius=None):
        if not radius:
            radius = self.radius
        val = self.gauge_units * val
        val = val - self.gauge_start
        x = math.cos(val) * radius + self.center[0]
        y = math.sin(val) * radius + self.center[1]
        return x, y

    def value_to_radians(self, val):
        val = self.gauge_units * val
        val = self.gauge_start - val
        return val

    def ticks(self, length=None):
        '''
        The number of ticks to make over the entire range
        :param length: length of ticks as root(2) * a number of pixels
        :return:
        '''
        if length is None:
            length = self.radius / 12
        for tick in range(self.domain[0], self.domain[1]):
            if self.unit_ticks:
                multipler = 3 if tick % self.tick_divisor == 0 else 2
                start = self.value_to_cords(tick, radius=self.radius - length * multipler)
                stop = self.value_to_cords(tick, radius=self.radius - length)
                pygame.draw.aaline(self.surface, self.colors['tick'], start, stop)
            elif tick % self.tick_divisor == 0:
                start = self.value_to_cords(tick, radius=self.radius - length * 2)
                stop = self.value_to_cords(tick, radius=self.radius - length)
                pygame.draw.aaline(self.surface, self.colors['tick'], start, stop)

    def labels(self):
        font_size = int(self.radius / 12)
        name_font = pygame.font.Font('freesansbold.ttf', font_size * 2)
        font = pygame.font.Font('freesansbold.ttf', font_size)

        text = name_font.render(self.name, True, self.colors['name'])
        textRect = text.get_rect()
        textRect.center = (self.center[0], self.center[1] - (self.radius / 12))
        self.surface.blit(text, textRect)
        # Numbers
        length = 4 * (self.radius / 12)
        for tick in range(self.domain[0], self.domain[1], self.tick_divisor):
            # font = pygame.font.Font('freesansbold.ttf', font_size)
            text = font.render(str(tick), True, self.colors['text'])
            textRect = text.get_rect()
            textRect.center = self.value_to_cords(tick, radius=self.radius - length)
            self.surface.blit(text, textRect)

    def needle(self, x):
        pygame.draw.arc(self.surface, self.colors['needle'], self.needle_rect, self.value_to_radians(x), self.value_to_radians(0), int(min(self.size)/16))
        #pygame.draw.line(self.surface, self.colors['needle'], self.center, self.value_to_cords(x), 5)

    def first(self):
        pygame.draw.circle(self.surface, self.colors['dial'], self.center, self.radius + 1)
        self.ticks()
        self.labels()

    def update(self, x):
        self.first()
        self.needle(x)
        self.window.window.blit(self.surface, self.position)