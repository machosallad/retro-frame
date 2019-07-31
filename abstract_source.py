#!/usr/bin/env python3

import abc
import numpy as np
import time
from enum import Enum

class SourceType(Enum):
    base = 0
    image = 1
    animation = 2
    sprite = 3
    video = 4
    giphy = 5
    youtube = 6

class AbstractSource(abc.ABC):
    def __init__(self,width=16, height=16):
        self.width = width
        self.height = height
        self.number_of_pixels = self.height * self.width
        self._buffer = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        self.totalTime = 0.
        self._type = SourceType.base
    
    @property
    def buffer(self):
        """The buffer contains the rgb data representation of the source."""
        return self._buffer

    @property
    def type(self):
        """ Source type"""
        return self._type

    def clear_buffer(self):
        self._buffer = np.zeros_like(self._buffer)

    @abc.abstractmethod
    def update(self,dt):
        """Update the source by passing current dt."""
