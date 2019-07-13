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
import requests
import pafy
import youtube_dl
from io import BytesIO
from enum import Enum
from random import seed
from random import randint
from PIL import Image
from pathlib import Path
from helpers import ImageHelper
from animation_source import AnimationSource
from image_source import ImageSource
from sprite_source import SpriteSource
from video_source import VideoSource

# Global variables
#HARDWARE = "WS2812B"
HARDWARE = "COMPUTER"
DISPLAY_WIDTH = 16
DISPLAY_HEIGTH = 16
FPS = 60
SPRITE_DIRECTORY    =   '/retroframe/sprites/'
IMAGE_DIRECTORY     =   '/retroframe/images/'
ANIMATION_DIRECTORY =   '/retroframe/animations/'
VIDEO_DIRECTORY     =   '/retroframe/videos/'
GIPHY_API_KEY = "dc6zaTOxFJmzC" # Giphy public beta API key

# Class declarations
class Source(Enum):
    animation = 1
    image = 2
    sprite = 3
    clock = 4

class RetroFrame():

    def load_giphy_animations(self,count,tag):
        """Requests a random gif"""
        for x in range(count):
            r = requests.get("http://api.giphy.com/v1/gifs/random?api_key={0}&tag={1}".format(GIPHY_API_KEY,tag))
            try:
                random_gif_url = r.json()["data"]["images"]["fixed_height_small"]["url"]
                print(random_gif_url)
                resp = requests.get(random_gif_url)
                self.sources.append(AnimationSource(BytesIO(resp.content)))
            except:
                pass

    def load_images(self,dirpath):
        with os.scandir(dirpath) as entries:
            for entry in entries:
                if entry.is_file():
                    self.sources.append(ImageSource(os.path.join(dirpath,entry.name), DISPLAY_WIDTH, DISPLAY_HEIGTH))

    def load_animations(self, dirpath):
        with os.scandir(dirpath) as entries:
            for entry in entries:
                if entry.is_file():
                    self.sources.append(AnimationSource(os.path.join(dirpath,entry.name), DISPLAY_WIDTH, DISPLAY_HEIGTH))

    def load_sprites(self, dirpath):
        self.sprite = SpriteSource(os.path.join(dirpath,"sprite_mario.png"), 233, 99, 16, 16, 5, 0.2, 1, 1)
        self.sources.append(self.sprite)

        self.goomba = SpriteSource(os.path.join(dirpath,"characters.gif"), 296, 187, 16, 16, 2, 0.2, 3, 3)
        self.sources.append(self.goomba)

    def load_videos(self,dirpath):
        with os.scandir(dirpath) as entries:
            for entry in entries:
                if entry.is_file():
                    self.sources.append(VideoSource(os.path.join(dirpath,entry.name), DISPLAY_WIDTH, DISPLAY_HEIGTH))    

    def load_youtube_videos(self):
        urls = ["https://www.youtube.com/watch?v=7yeA7a0uS3A",
        "https://www.youtube.com/watch?v=AxuvUAjHYWQ", 
        "https://www.youtube.com/watch?v=Ae-Pl-Q34ng"]

        for url in urls:
            vPafy = pafy.new(url)
            play = vPafy.getbest(preftype="webm")
            self.sources.append(VideoSource(play.url))

    def __init__(self):

        # Create surface of (width, height), and its window.
        if HARDWARE == 'WS2812B':
            pass
        elif HARDWARE == 'COMPUTER':
            from computer import Computer
            self.display = Computer(DISPLAY_WIDTH, DISPLAY_HEIGTH)
        else:
            raise RuntimeError(
                "Display hardware \"{}\" not known.".format(HARDWARE))

        self.sources = []

        # Working directories
        sprite_dir = os.path.join(os.path.dirname(__file__),SPRITE_DIRECTORY)
        image_dir = os.path.join(os.path.dirname(__file__),IMAGE_DIRECTORY)
        animation_dir = os.path.join(os.path.dirname(__file__),ANIMATION_DIRECTORY)
        video_dir = os.path.join(os.path.dirname(__file__),VIDEO_DIRECTORY)
                
        # Set up some data
        #self.load_giphy_animations(10,"pixelart")
        #self.load_images(image_dir)
        #self.load_animations(animation_dir)
        #self.load_sprites(sprite_dir)
        #self.load_videos(video_dir)
        self.load_youtube_videos()


    def mainloop(self):
        lastFrameTime = time.time()
        lastSourceChange = time.time()
        sourceCounter = 0
       
        while True:
            # Calculate delta time
            currentTime = time.time()
            dt = currentTime - lastFrameTime
            lastFrameTime = currentTime

            # Update game logic, objects and data structures here using dt
            for source in self.sources:
                source.update(dt)

            # Check if new source should be selected
            if (time.time() - lastSourceChange > 5):
                lastSourceChange = time.time()
                sourceCounter += 1
                if sourceCounter >= self.sources.__len__():
                    sourceCounter = 0
            
            current_source_buffer = self.sources[sourceCounter].buffer

            # Update the display buffer
            self.display.buffer = current_source_buffer

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
