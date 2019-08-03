#!/usr/bin/env python3

# Imports
import time
import numpy as np
from PIL import Image
from helpers import ImageHelper
from source.abstract_source import AbstractSource, SourceType

class ImageSource(AbstractSource):
    def __init__(self, filename, width=16, height=16):
        super().__init__(width, height)
        self._type = SourceType.image
        self.load(filename)

    def load(self, filename):
        im = Image.open(filename)

        im = ImageHelper.convert_any_to_rgb(im)
        im = ImageHelper.resize_image(im, (self.width, self.height))

        self._buffer = np.array(im)

    def update(self, dt):
        pass