import pygame
from dashboard.tools import *


class Toggle:
    def __init__(self, window, col, row):
        pass

class Button:
    def __init__(self, window, col, row):
        pass


class Keyboard:
    def __init__(self, window, col, row):
        pass


class Indicator:
    def __init__(self, window, col, row, name=None, off=None, on=None, text_on=None, text_off=None):
        '''
        An indicator tile
        :param window: WindowGrid/TileGrid object
        :param row: the row(s) for the indicator to fill
        :param col: the col(s) for the indicator to fill
        :param name: text on top of the indicator
        :param off: color or image
        :param on: color or image
        :param text_on: the color of text with on (if text)
        :param text_off: the color of text when off (if text)
        '''
        self.window = window
        self.name = name
        self.col, self.row = col, row
        self.surface, self.position, self.size = window.tile(col, row)
        self.center = [int(self.size[0] / 2), int(self.size[1] / 2)]
        self.radius = int(min(self.size) / 2)
        self.img_pos = (self.position[0]+((self.size[0]/2)-self.radius),
                        self.position[1]+((self.size[1]/2)-self.radius))
        self.off = off
        self.on = on

        if name:
            font = pygame.font.Font('freesansbold.ttf', int((self.radius*(1.6+.17*len(name)))/len(name)))
            self.text = {True: font.render(self.name, True, text_on), False: font.render(self.name, True, text_off)}
            self.label_text_rect = self.text[True].get_rect()
            self.label_text_rect.center = (self.center[0], self.center[1])

        self.update(False)

    @concurrent
    def test(self):
        status = False
        while True:
            status = not status
            self.update(status)
            pygame.time.wait(1000)

    def update(self, bool):
        if bool:
            if is_color(self.on):
                self.surface.fill(self.window.background_color)
                pygame.draw.circle(self.surface, self.on, self.center, self.radius)
            else:
                self.surface.fill(self.window.background_color)
                img = pygame.transform.scale(pygame.image.load(self.on), (self.radius * 2, self.radius * 2))
                self.surface.blit(img, self.img_pos)
        else:
            if is_color(self.off):
                self.surface.fill(self.window.background_color)
                pygame.draw.circle(self.surface, self.off, self.center, self.radius)
            else:
                self.surface.fill(self.window.background_color)
                img = pygame.transform.scale(pygame.image.load(self.off), (self.radius * 2, self.radius * 2))
                self.surface.blit(img, self.img_pos)
        if self.name:
            self.surface.blit(self.text[bool], self.label_text_rect)
        self.window.window.blit(self.surface, self.position)

