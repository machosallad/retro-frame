#!/user/bin/env python3
"""
Main entry point of the retro-frame project.
Runs the main game-loop.
"""

# Imports
import os
import sys
import abc
import numpy as np
import time
from random import seed
from random import randint
from PIL import Image
from pathlib import Path
from helpers import ImageHelper

# Global variables
FPS = 60

# Class declarations
class RetroFrame():
    def __init__(self):
        # Create surface of (width, height), and its window.
        from computer import Computer
        from animation_source import AnimationSource
        from image_source import ImageSource
        from sprite_source import SpriteSource
        
        # Working directories
        image_source = os.path.join(os.path.dirname(__file__),'/retroframe/images/')
        gif_to_load = os.path.join(image_source,'_1.gif')
        image_to_load = os.path.join(image_source,'1.png')
        sprite_to_load = os.path.join(image_source,'sprite_mario.png')
        mario_sprite = os.path.join(image_source,'characters.gif')

        self.display = Computer(16, 16)
        self.image = ImageSource(image_to_load, 16, 16)
        self.animation = AnimationSource(gif_to_load, 16, 16)
        self.sprite = SpriteSource(sprite_to_load, 233, 99, 16, 16, 5, 0.2, 1, 1)
        self.goomba = SpriteSource(mario_sprite, 296, 187, 16, 16, 2, 0.2, 3, 3)
        # Set up some data

    def mainloop(self):
        lastFrameTime = time.time()

        while True:
            # Calculate delta time
            currentTime = time.time()
            dt = currentTime - lastFrameTime
            lastFrameTime = currentTime

            # Update game logic, objects and data structures here using dt
            self.sprite.update(dt)
            self.animation.update(dt)
            self.image.update(dt)
            self.goomba.update(dt)
            self.display.buffer = self.goomba.buffer
            
            #for i in range(self.display.number_of_pixels):
            #    self.display.set_pixel_at_index(i, (randint(0, 255), randint(0, 255), randint(0, 255)))

            # Render the frame
            self.display.show()

            # To limit CPU usage do not go faster than 60 "fps"
            sleepTime = 1./FPS - dt
            if sleepTime > 0:
                time.sleep(sleepTime)
        return

# Function declarations


# Main body
if __name__ == "__main__":
    retroframe = RetroFrame()
    retroframe.display.show()

    retroframe.mainloop()
