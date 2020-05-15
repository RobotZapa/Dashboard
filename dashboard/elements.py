import pygame
from pygame.locals import *
from dashboard.tools import *
import time


class Toggle:
    def __init__(self, window, col, row):
        pass#TODO toggle button

class Button:
    def __init__(self, window, col, row, name=None, off=None, on=None, text_on=None, text_off=None, **kwargs):
        '''
        Tile acts like a button (it is however, clear)
        :param window: WindowGrid/TileGrid object
        :param row: the row(s) for the indicator to fill
        :param col: the col(s) for the indicator to fill
        :param name: text on top of the indicator
        :param off: color or image
        :param on: color or image
        :param text_on: the color of text with on (if text)
        :param text_off: the color of text when off (if text)
        :param callback: a quick function when the button is pressed
        :param args: a tuple of arguments for the callback
        :param debounce_time: the time between registering clicks (100ms default)
        :param hover: color or image TODO
        '''
        self.callback = kwargs['callback'] if 'callback' in kwargs else None
        self.indicator = Indicator(window, col, row, name, off, on, text_on, text_off)
        self.button = Press(window, col, row, **kwargs)
        window.eventloop.add(self.event_check)

    def event_check(self):
        pass


class Textbox:
    def __init__(self):
        pass#TODO textbox area

class Keyboard:
    def __init__(self, window, col, row):
        pass#TODO keyboard area


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
                img = pygame.transform.smoothscale(pygame.image.load(self.on), (self.radius * 2, self.radius * 2))
                self.surface.blit(img, self.img_pos)
        else:
            if is_color(self.off):
                self.surface.fill(self.window.background_color)
                pygame.draw.circle(self.surface, self.off, self.center, self.radius)
            else:
                self.surface.fill(self.window.background_color)
                img = pygame.transform.smoothscale(pygame.image.load(self.off), (self.radius * 2, self.radius * 2))
                self.surface.blit(img, self.img_pos)
        if self.name:
            self.surface.blit(self.text[bool], self.label_text_rect)
        self.window.window.blit(self.surface, self.position)

    def draw(self, color_img):
        if is_color(color_img):
            self.surface.fill(self.window.background_color)
            pygame.draw.circle(self.surface, color_img, self.center, self.radius)
        else:
            self.surface.fill(self.window.background_color)
            img = pygame.transform.smoothscale(pygame.image.load(color_img), (self.radius * 2, self.radius * 2))
            self.surface.blit(img, self.img_pos)
        if self.name:#TODO
            self.surface.blit(self.text[bool], self.label_text_rect)
        self.window.window.blit(self.surface, self.position)


class Label:
    def __init__(self, window, col, row, text_color, background_color=None, text=None):
        '''
        A text box with passive or active text
        :param window:
        :param col(s):
        :param row(s):
        :param text_color:
        :param background_color:
        :param text:
        '''
        #TODO

    def text(self, new_text):
        pass


class Hover:
    def __init__(self, window, col, row, **kwargs):
        '''
        Mouse hovering over
        :param window: WindowGrid/TileGrid object
        :param row: the row(s) for the indicator to fill
        :param col: the col(s) for the indicator to fill
        :param debounce_time: the time between registering clicks (100ms default)
        :param in_callback: a quick function when the button is pressed
        :param in_args: None or a tuple of arguments
        :param out_callback: a quick function when the button is pressed
        :param out_args: None or a tuple of arguments
        '''
        self.surface, self.position, self.size = window.tile(col, row)
        self.in_callback = kwargs['in_callback'] if 'in_callback' in kwargs else None
        self.in_args = kwargs['in_args'] if 'in_args' in kwargs else None
        self.out_callback = kwargs['out_callback'] if 'out_callback' in kwargs else None
        self.out_args = kwargs['out_args'] if 'out_args' in kwargs else None
        self.debounce = kwargs['debounce']/1000 if 'debounce' in kwargs else 0.1
        self.pos_max = self.position[0] + self.size[0], self.position[1] + self.size[1]
        window.eventloop.add(self.event_check)
        self.inside = False

    def event_check(self):
        pos = pygame.mouse.get_pos()
        if self.pos_max[0] > pos[0] > self.position[0] and self.pos_max[1] > pos[1] > self.position[1]:
            if not self.inside and self.in_callback:
                if self.in_args:
                    self.in_callback(*self.in_args)
                else:
                    self.in_callback()
                self.inside = True
        else:
            if self.inside and self.out_callback:
                if self.out_args:
                    self.out_callback(*self.out_args)
                else:
                    self.out_callback()
                self.inside = False


class Press:
    def __init__(self, window, col, row, **kwargs):
        '''
        Tile click
        :param window: WindowGrid/TileGrid object
        :param row: the row(s) for the indicator to fill
        :param col: the col(s) for the indicator to fill
        :param debounce_time: the time between registering clicks (100ms default)
        :param callback: a quick function when the button is pressed
        :param args: None or a tuple of arguments
        '''
        self.surface, self.position, self.size = window.tile(col, row)
        self.callback = kwargs['callback'] if 'callback' in kwargs else None
        self.args = kwargs['args'] if 'args' in kwargs else None
        self.debounce = kwargs['debounce']/1000 if 'debounce' in kwargs else 0.1
        self.pos_max = self.position[0] + self.size[0], self.position[1] + self.size[1]
        window.eventloop.add(self.event_check)
        self.last_event = 0

    def event_check(self):
        if pygame.mouse.get_pressed()[0] and self.debounce < (time.time() - self.last_event):
            self.last_event = time.time()
            pos = pygame.mouse.get_pos()
            if self.pos_max[0] > pos[0] > self.position[0] and self.pos_max[1] > pos[1] > self.position[1]:
                if self.callback:
                    if self.args:
                        self.callback(*self.args)
                    else:
                        self.callback()
