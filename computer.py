#!/usr/bin/env python3

import numpy as np
import pygame
import sys

from abstract_display import AbstractDisplay


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

        self.surface.fill((0, 0, 0))

        it = np.nditer([self.buffer[:, :, 0],
                        self.buffer[:, :, 1],
                        self.buffer[:, :, 2]], flags=['multi_index'])
        while not it.finished:
            color = (it[0] * self.brightness, it[1] *
                     self.brightness, it[2] * self.brightness)
            (row, column) = it.multi_index
            pygame.draw.rect(self.surface, color,
                             [(self.margin + self.size) * column + self.margin,
                              (self.margin + self.size) * row + self.margin,
                              self.size,
                              self.size])
            it.iternext()

        pygame.display.update()
        return


if __name__ == "__main__":
    display = Computer()
    # display.run_benchmark()
    display.create_test_pattern()
    display.show()
    import time
    time.sleep(5)
