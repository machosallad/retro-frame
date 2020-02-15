#!/usr/bin/env python3

# Imports
import time
import numpy as np
import datetime
import random
from PIL import Image
from helpers import ImageHelper
from source.abstract import AbstractSource, SourceType

class ClockSource(AbstractSource):
    def __init__(self, width=16, height=16):
        super().__init__(width, height)
        self._type = SourceType.image
        self.fps = 2
        self.rows = 7
        self.columns = 5

        self.zero = [   [0,1,1,1,0],
                        [1,0,0,0,1],
                        [1,0,0,1,1],
                        [1,0,1,0,1],
                        [1,1,0,0,1],
                        [1,0,0,0,1],
                        [0,1,1,1,0]]
        
        self.one = [    [0,1,1,0,0],
                        [0,0,1,0,0],
                        [0,0,1,0,0],
                        [0,0,1,0,0],
                        [0,0,1,0,0],
                        [0,0,1,0,0],
                        [1,1,1,1,1]]

        self.two = [    [1,1,1,1,0],
                        [0,0,0,0,1],
                        [0,0,0,0,1],
                        [0,1,1,1,1],
                        [1,0,0,0,0],
                        [1,0,0,0,0],
                        [1,1,1,1,1]]

        self.three = [  [0,1,1,1,0],
                        [0,0,0,0,1],
                        [0,0,0,0,1],
                        [0,1,1,1,0],
                        [0,0,0,0,1],
                        [0,0,0,0,1],
                        [0,1,1,1,0]]

        self.four = [   [0,0,0,1,1],
                        [0,0,1,0,1],
                        [0,1,0,0,1],
                        [1,0,0,0,1],
                        [1,1,1,1,1],
                        [0,0,0,0,1],
                        [0,0,0,0,1]]
        
        self.five = [   [1,1,1,1,1],
                        [1,0,0,0,0],
                        [1,0,0,0,0],
                        [1,1,1,1,0],
                        [0,0,0,0,1],
                        [0,0,0,0,1],
                        [1,1,1,1,0]]
        
        self.six = [    [0,1,1,1,0],
                        [1,0,0,0,0],
                        [1,0,0,0,0],
                        [1,1,1,1,0],
                        [1,0,0,0,1],
                        [1,0,0,0,1],
                        [0,1,1,1,0]]
        
        self.seven = [  [1,1,1,1,1],
                        [0,0,0,0,1],
                        [0,0,0,1,0],
                        [0,0,0,1,0],
                        [0,0,1,0,0],
                        [0,0,1,0,0],
                        [0,0,1,0,0]]
        
        self.eight = [  [0,1,1,1,0],
                        [1,0,0,0,1],
                        [1,0,0,0,1],
                        [0,1,1,1,0],
                        [1,0,0,0,1],
                        [1,0,0,0,1],
                        [0,1,1,1,0]]
        
        self.nine = [   [0,1,1,1,0],
                        [1,0,0,0,1],
                        [1,0,0,0,1],
                        [0,1,1,1,0],
                        [0,0,0,0,1],
                        [0,0,0,0,1],
                        [0,1,1,1,0]]

    def load(self, filename):
        im = Image.open(filename)

        im = ImageHelper.convert_any_to_rgb(im)
        im = ImageHelper.resize_image(im, (self.width, self.height))

        self._buffer = np.array(im)

    def update(self, dt):

        now = datetime.datetime.now().time()
        time_array = now.strftime("%H:%M:%S").split(":")

        upper_h = int(time_array[0][0])
        lower_h = int(time_array[0][1])

        upper_m = int(time_array[1][0])
        lower_m = int(time_array[1][1])

        self.construct(upper_h,lower_h,upper_m,lower_m)
        
    def __get_number_array(self, number):
        if number == 1:
            return self.one
        if number == 2:
            return self.two
        if number == 3:
            return self.three
        if number == 4:
            return self.four
        if number == 5:
            return self.five
        if number == 6:
            return self.six
        if number == 7:
            return self.seven
        if number == 8:
            return self.eight
        if number == 9:
            return self.nine
        else:
            return self.zero

    def construct(self, upper_h,lower_h,upper_m,lower_m):
        tmp = np.zeros((self.height, self.width, 3), dtype=np.uint8)

        hh = self.__get_number_array(upper_h)
        h = self.__get_number_array(lower_h)
        mm = self.__get_number_array(upper_m)
        m = self.__get_number_array(lower_m)

        r = 255
        g = 255
        b = 255

        x_origin = 5
        y_origin = 0

        x_offset = x_origin + 0
        y_offset = y_origin + 0
        for x in range(self.columns):
            for y in range(self.rows):
                if hh[y][x] == 1:
                    tmp[y + y_offset, x + x_offset] = (r,g,b)

        x_offset = x_origin + self.columns + 1
        y_offset = y_origin + 0
        for x in range(self.columns):
            for y in range(self.rows):
                if h[y][x] == 1:
                    tmp[y + y_offset, x + x_offset] = (r,g,b)
        
        x_offset = x_origin + 0
        y_offset = y_origin + 9
        for x in range(self.columns):
            for y in range(self.rows):
                if mm[y][x] == 1:
                    tmp[y + y_offset, x + x_offset] = (r,g,b)

        x_offset = x_origin + self.columns + 1
        y_offset = y_origin + self.rows + 2
        for x in range(self.columns):
            for y in range(self.rows):
                if m[y][x] == 1:
                    tmp[y + y_offset, x + x_offset] = (r,g,b)

        self._buffer = tmp