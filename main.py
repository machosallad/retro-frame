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
import threading
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
SPRITE_DIRECTORY    =   "sources/sprites/"
IMAGE_DIRECTORY     =   "sources/images/"
ANIMATION_DIRECTORY =   "sources/animations/"
VIDEO_DIRECTORY     =   "sources/videos/"
WAIT_ANIMATION      =   "resources/loading.gif"
GIPHY_API_KEY = "dc6zaTOxFJmzC" # Giphy public beta API key

# Class declarations
class Source(Enum):
    random = 0
    animation = 1
    image = 2
    sprite = 3
    video = 4
    clock = 5

class RetroFrame():

    def load_giphy_animations(self,count,tag):
        """Requests a number of random gifs from Giphy"""
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
        """ Load images from given directory"""
        with os.scandir(dirpath) as entries:
            for entry in entries:
                if entry.is_file():
                    self.sources.append(ImageSource(os.path.join(dirpath,entry.name), DISPLAY_WIDTH, DISPLAY_HEIGTH))

    def load_animations(self, dirpath):
        """ Load animations (gifs) from given directory"""
        with os.scandir(dirpath) as entries:
            for entry in entries:
                if entry.is_file():
                    self.sources.append(AnimationSource(os.path.join(dirpath,entry.name), DISPLAY_WIDTH, DISPLAY_HEIGTH))

    def load_sprites(self, dirpath):
        """ Load sprites from given directory"""
        self.sprite = SpriteSource(os.path.join(dirpath,"sprite_mario.png"), 233, 99, 16, 16, 5, 0.2, 1, 1)
        self.sources.append(self.sprite)

        self.goomba = SpriteSource(os.path.join(dirpath,"characters.gif"), 296, 187, 16, 16, 2, 0.2, 3, 3)
        self.sources.append(self.goomba)

    def load_videos(self,dirpath):
        """ Load videos from given directory"""
        with os.scandir(dirpath) as entries:
            for entry in entries:
                if entry.is_file():
                    self.sources.append(VideoSource(os.path.join(dirpath,entry.name), DISPLAY_WIDTH, DISPLAY_HEIGTH))    

    def load_youtube_videos(self, urls):
        """ Load YouTube videos from the given array of urls"""
        for url in urls:
            vPafy = pafy.new(url)
            play = vPafy.getbest(preftype="webm")
            self.sources.append(VideoSource(play.url,DISPLAY_WIDTH, DISPLAY_WIDTH))

    def __init__(self):
        # Change working directory
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        
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
        self.load_threads = []

    def load_default_resources(self):
        """ Load all resources which should always be used by the application."""
        # Set up some data
        self.load_images(IMAGE_DIRECTORY)
        self.load_animations(ANIMATION_DIRECTORY)
        self.load_sprites(SPRITE_DIRECTORY)
        
        # Create loader threads the heavier resources
        urls = ["https://www.youtube.com/watch?v=AxuvUAjHYWQ", "https://www.youtube.com/watch?v=Ae-Pl-Q34ng"]
        self.load_threads.append(threading.Thread(target=self.load_youtube_videos,args=(urls,)))
        self.load_threads.append(threading.Thread(target=self.load_videos,args=(VIDEO_DIRECTORY,)))
        self.load_threads.append(threading.Thread(target=self.load_giphy_animations,args=(10,"pixelart")))

        # Start all the threads in one go
        for thread in self.load_threads:
            thread.start()

    def mainloop(self):
        # Setup local variables
        sourceCounter = 0
        wait_animation = AnimationSource(WAIT_ANIMATION)

        # Prepare and start loading resources
        lastFrameTime = time.time()
        lastSourceChange = time.time()
        self.load_default_resources()
       
        while True:
            # Calculate delta time
            currentTime = time.time()
            dt = currentTime - lastFrameTime
            lastFrameTime = currentTime

            # Verify if resources are fully loaded
            if self.all_resources_loaded():
                # Update game logic, objects and data structures here using dt
                for source in self.sources:
                    source.update(dt)
                
                # Check if new source should be selected
                if (time.time() - lastSourceChange > 5):
                    lastSourceChange = time.time()
                    sourceCounter += 1
                    if sourceCounter >= self.sources.__len__():
                        sourceCounter = 0

                # Update the display buffer
                self.display.buffer = self.sources[sourceCounter].buffer
            else:
                # Show waiting animation
                wait_animation.update(dt)
                self.display.buffer = wait_animation.buffer
            
           # Render the frame
            self.display.show()

            # To limit CPU usage do not go faster than 60 "fps"
            sleepTime = 1./FPS - dt
            if sleepTime > 0:
                time.sleep(sleepTime)
        return

    def all_resources_loaded(self):
        """ Verify if all resources are fully loaded"""
        all_sources_ready = True
        for thread in self.load_threads:
            if thread.is_alive():
                all_sources_ready = False
            else:
                thread.join()
        return all_sources_ready

# Function declarations

# Main body
if __name__ == "__main__":
    retroframe = RetroFrame()
    retroframe.display.show()

    retroframe.mainloop()
