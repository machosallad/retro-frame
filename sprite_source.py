#!/usr/bin/env python3

# Imports
import time
import numpy as np
from PIL import Image
from helpers import ImageHelper
from abstract_source import AbstractSource

class SpriteSource(AbstractSource):
    def __init__(self, filename, x, y, dx, dy, count, duration, dx_offset=0, dy_offset=0, width=16, height=16):
        super().__init__(width, height)
        self.duration = duration
        self.count = count
        self.images_rgb_data = []
        self.number_of_frames = count
        self.current_frame = 0

        self.load(filename, x, y, dx, dy, count, dx_offset, dy_offset)

    def load(self, filename, x, y, dx, dy, count, duration, dx_offset=0, dy_offset=0):
        im = Image.open(filename)
        im = ImageHelper.convert_any_to_rgb(im)
        
        for i in range(self.count):
            sprite = im.crop((x, y, x + dx, y + dy))
            sprite.load()
            sprite = ImageHelper.resize_image(sprite, (self.width, self.height))

            self.images_rgb_data.append(np.array(sprite))
            x += dx + dx_offset

    def update(self, dt):
        self.totalTime += dt
        if(self.totalTime > self.duration):
            self.current_frame += 1
            self.totalTime = 0
        
        self._buffer = self.images_rgb_data[self.current_frame % self.number_of_frames]