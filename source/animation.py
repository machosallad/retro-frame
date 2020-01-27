#!/usr/bin/env python3

# Imports
import time
import numpy as np
from PIL import Image
from helpers import ImageHelper
from source.abstract import AbstractSource, SourceType

class AnimationSource(AbstractSource):
    def __init__(self,filename, width=16, height=16,type=SourceType.animation):
        super().__init__(width, height)
        self.images_rgb_data = []
        self.number_of_frames = 0
        self.current_frame = 0
        self.duration = []
        self._type = type

        self.load(filename)

    def update(self, dt):

        self.totalTime += dt
        if(self.totalTime > self.duration[self.current_frame % self.number_of_frames]):
            self.current_frame += 1
            self.totalTime = 0
        
        self._buffer = self.images_rgb_data[self.current_frame % self.number_of_frames]

    def load(self, filename, repetitions=1):
        try:
            im = Image.open(filename)
        except IOError:
            print("{} is not a valid image file".format(filename))

        more_frames = True
        while more_frames:
            frame = Image.new("RGBA", im.size)
            frame.paste(im)
            frame = ImageHelper.convert_any_to_rgb(frame)
            frame = ImageHelper.resize_image(frame, (self.width, self.height))
            self.images_rgb_data.append(np.array(frame))

            try:
                # The time to display the current frame of the GIF, in milliseconds and store
                self.duration.append(float(im.info["duration"]))
                im.seek(im.tell() + 1)
            except KeyError:
                print("{} has no duration meta data!".format(filename))
            except (TypeError, ValueError):
                print("cannot convert info[duration]: {} to integer.".format(im.info["duration"]))
            except:
                more_frames = False

            self.number_of_frames += 1        