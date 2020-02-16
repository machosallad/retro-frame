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
        self._type = SourceType.clock
        self.fps = 2

        self.zero = [   [0,1,1,1,0],
                        [1,0,0,0,1],
                        [1,0,0,1,1],
                        [1,0,1,0,1],
                        [1,1,0,0,1],
                        [1,0,0,0,1],
                        [0,1,1,1,0]]
        
        self.one = [    [0,0,1,0,0],
                        [0,1,1,0,0],
                        [0,0,1,0,0],
                        [0,0,1,0,0],
                        [0,0,1,0,0],
                        [0,0,1,0,0],
                        [1,1,1,1,1]]

        self.two = [    [0,1,1,1,0],
                        [1,0,0,0,1],
                        [0,0,0,0,1],
                        [0,0,0,1,0],
                        [0,0,1,0,0],
                        [0,1,0,0,0],
                        [1,1,1,1,1]]

        self.three = [  [0,1,1,1,0],
                        [1,0,0,0,1],
                        [0,0,0,0,1],
                        [0,1,1,1,0],
                        [0,0,0,0,1],
                        [1,0,0,0,1],
                        [0,1,1,1,0]]

        self.four = [   [0,1,0,0,1],
                        [0,1,0,0,1],
                        [1,0,0,0,1],
                        [1,1,1,1,1],
                        [0,0,0,0,1],
                        [0,0,0,0,1],
                        [0,0,0,0,1]]
        
        self.five = [   [1,1,1,1,1],
                        [1,0,0,0,0],
                        [1,0,0,0,0],
                        [1,1,1,1,0],
                        [0,0,0,0,1],
                        [1,0,0,0,1],
                        [0,1,1,1,0]]
        
        self.six = [    [0,1,1,1,0],
                        [1,0,0,0,0],
                        [1,0,0,0,0],
                        [1,1,1,1,0],
                        [1,0,0,0,1],
                        [1,0,0,0,1],
                        [0,1,1,1,0]]
        
        self.seven = [  [1,1,1,1,1],
                        [0,0,0,0,1],
                        [0,0,0,0,1],
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
                        [1,0,0,0,1],
                        [0,1,1,1,0]]

    def load(self, filename):
        pass

    def update(self, dt):

        now = datetime.datetime.now().time()
        time_array = now.strftime("%H:%M:%S").split(":")

        upper_h = int(time_array[0][0])
        lower_h = int(time_array[0][1])

        upper_m = int(time_array[1][0])
        lower_m = int(time_array[1][1])

        self._buffer = self.__construct_buffer(upper_h,lower_h,upper_m,lower_m)
        
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

    def __construct_buffer(self, upper_h,lower_h,upper_m,lower_m):
        tmp_buffer = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        number = None
        rgb = (255, 255, 255)
        column_origin = 5
        row_origin = 0
        margin = 1

        for position in range(4):
            if position == 0:
                number = self.__get_number_array(upper_h)
                column_offset = column_origin + 0
                row_offset = row_origin + 0
            if position == 1:
                number = self.__get_number_array(lower_h)
                column_offset = column_origin + len(number[0]) + margin
                row_offset = row_origin + 0
            if position == 2:
                number = self.__get_number_array(upper_m)
                column_offset = column_origin + 0
                row_offset = row_origin + 9
            if position == 3:
                number = self.__get_number_array(lower_m)
                column_offset = column_origin + len(number[0]) + margin
                row_offset = row_origin + len(number) + 2
        
            for column in range(len(number[0])):
                for row in range(len(number)):
                    if number[row][column] == 1:
                        tmp_buffer[row + row_offset, column + column_offset] = rgb

        return tmp_buffer