#!/usr/bin/env python3

import numpy as np
import pygame
import sys

from display.abstract_display import AbstractDisplay


class Computer(AbstractDisplay):
    def __init__(self, width=16, height=16, margin=5, size=30):
        super().__init__(width, height)

        self.margin = margin
        self.size = size

        self.window_size = (width * size + (width + 1) *
                            margin, height * size + (height + 1) * margin)

        pygame.init()
        self.surface = pygame.display.set_mode(self.window_size)
        pygame.display.set_caption("retro-frame {}x{}".format(width, height))
        self.show()

    def show(self, gamma=False):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
       
        for j in range (self.width):
            for i in range(self.height):
                color = self.buffer[i][j] * self.brightness
                pygame.draw.rect(self.surface, color,[(self.margin + self.size) * j + self.margin,
                            (self.margin + self.size) * i + self.margin,
                            self.size,
                            self.size])
        pygame.display.update()

        return

if __name__ == "__main__":
    display = Computer()
    # display.run_benchmark()
    display.create_test_pattern()
    display.show()
    import time
    time.sleep(5)
