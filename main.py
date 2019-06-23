#!/user/bin/env python3
"""
Main entry point of the retro-frame project.
Runs the main game-loop.
"""

# Imports
import sys
import abc
import numpy as np
import time
from random import seed
from random import randint
from PIL import Image
from pathlib import Path

# Global variables


class ImageHelper():
    @staticmethod
    def convert_rgba_to_rgb(image, color=(0, 0, 0)):
        background = Image.new('RGB', image.size, color)
        background.paste(image, mask=image.split()[3])
        return background

    @staticmethod
    def convert_any_to_rgb(image):
        bands = image.getbands()
        if bands == ('R', 'G', 'B', 'A'):
            image = ImageHelper.convert_rgba_to_rgb(image)
        elif bands != ('R', 'G', 'B'):
            image = image.convert('RGB')
        return image

    @staticmethod
    def resize_image(image, size):
        if image.size != size:
            image = image.resize(size)
        return image

# Class declarations
class SpriteViewer():
    def __init__(self, width=16, height=16):
        self.width = width
        self.height = height
        self._buffer = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        self.images_rgb_data = []
        self.number_of_frames = 0
        self.current_frame = 0
        return

    def load_image(self, filename):
        im = Image.open(filename)

        im = ImageHelper.convert_any_to_rgb(im)
        im = ImageHelper.resize_image(im, (self.width, self.height))

        self._buffer = np.array(im)

    def image_as_array(self):
        return self._buffer

    def next_frame(self, frame_number):
        ENGINE_FPS = 60
        GIF_FPS = 25

        if not ( frame_number % (ENGINE_FPS/GIF_FPS)):
            self._buffer = self.images_rgb_data[self.current_frame % self.number_of_frames]
            self.current_frame += 1
        return self._buffer

    def load_gif(self, filename, repetitions=1):
        try:
            im = Image.open(filename)
        except IOError:
            print("{} is not a valid image file".format(filename))

        try:
            # The time to display the current frame of the GIF, in milliseconds
            duration = int(im.info["duration"])
        except KeyError:
            print("{} has no duration meta data!".format(filename))
        except (TypeError, ValueError):
            print("cannot convert info[duration]: {} to integer.".format(
                im.info["duration"]))
        except:
            print("Unknown error while loading {}".format(filename))
            return

        more_frames = True

        while more_frames:
            frame = Image.new("RGBA", im.size)
            frame.paste(im)
            frame = ImageHelper.convert_any_to_rgb(frame)
            frame = ImageHelper.resize_image(frame, (self.width, self.height))
            self.images_rgb_data.append(np.array(frame))
            try:
                im.seek(im.tell() + 1)
            except:
                more_frames = False
            self.number_of_frames += 1


class RetroFrame():
    def __init__(self):
        # Create surface of (width, height), and its window.
        from computer import Computer
        self.display = Computer(16, 16)
        self.sprite = SpriteViewer(16, 16)
        # Set up some data

    def mainloop(self):
        seed(1)
        image_folder = Path("images").absolute()
        file_to_load = (r'F:\PC_BACKUP\Users\Jesper\Documents\GitHub\retro-frame\images\_1.gif') #image_folder / "_1.gif"
        self.sprite.load_gif(file_to_load)
        frame = 0

        while True:
            self.display.buffer = self.sprite.next_frame(frame)
            # Update your game objects and data structures here...
            # for i in range(self.display.number_of_pixels):
            #    self.display.set_pixel_at_index(
            #        i, (randint(0, 255), randint(0, 255), randint(0, 255)))

            # We draw everything from scratch on each frame.

            # Now the surface is ready, tell display to show it!
            self.display.show()

            # to limit CPU usage do not go faster than 60 "fps"
            time.sleep(1/60)
            frame += 1

        return

# Function declarations


# Main body
if __name__ == "__main__":
    retroframe = RetroFrame()
    retroframe.display.show()

    retroframe.mainloop()
