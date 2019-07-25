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
import random
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
from abstract_source import SourceType

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
class ViewMode(Enum):
    order = 0
    random = 1
    static = 2
    shuffle = 3

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
            if play is not None:
                self.sources.append(VideoSource(play.url,DISPLAY_WIDTH, DISPLAY_WIDTH))

    def rest_add_youtube_video_worker(self,url):
        vPafy = pafy.new(url)
        play = vPafy.getbest(preftype="webm")
        if play is not None:
            self.sources.append(VideoSource(play.url,DISPLAY_WIDTH, DISPLAY_WIDTH))

    def rest_add_youtube_video(self,url):
            vPafy = pafy.new(url)
            play = vPafy.getbest(preftype="webm")
            if play is None:
                return False
            else:
                worker_thread = threading.Thread(target=self.rest_add_youtube_video_worker,args=(url,))
                worker_thread.start()
                return True

    def __init__(self):
        # Change working directory
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        
        # Create surface of (width, height), and its window.
        if HARDWARE == 'WS2812B':
            from ws2812b import WS2812B
            self.display = WS2812B(DISPLAY_WIDTH,DISPLAY_HEIGTH)
            pass
        elif HARDWARE == 'COMPUTER':
            from computer import Computer
            self.display = Computer(DISPLAY_WIDTH, DISPLAY_HEIGTH)
        else:
            raise RuntimeError(
                "Display hardware \"{}\" not known.".format(HARDWARE))

        self.source_index = 0
        self.sources = []
        self.load_threads = []
        self.view_length = 5
        self.mode = ViewMode.random
        self.allowed_content_dict = {SourceType.image:False, SourceType.video:True, SourceType.sprite:False, SourceType.animation:False}

        from http_server import RetroFrameHttpServer
        self.http_server = RetroFrameHttpServer(self,500)
        self.http_server.setDaemon(True)
        self.http_server.start()


    def load_default_resources(self):
        """ Load all resources which should always be used by the application."""
        # Set up some data
        self.load_images(IMAGE_DIRECTORY)
        self.load_animations(ANIMATION_DIRECTORY)
        #self.load_sprites(SPRITE_DIRECTORY)
        
        # Create loader threads the heavier resources
        urls = ["https://www.youtube.com/watch?v=AxuvUAjHYWQ", "https://www.youtube.com/watch?v=Ae-Pl-Q34ng"]
        #self.load_threads.append(threading.Thread(target=self.load_youtube_videos,args=(urls,)))
        #self.load_threads.append(threading.Thread(target=self.load_videos,args=(VIDEO_DIRECTORY,)))
        #self.load_threads.append(threading.Thread(target=self.load_giphy_animations,args=(10,"nes")))

        # Start all the threads in one go
        for thread in self.load_threads:
            thread.start()

    def mainloop(self):
        # Setup local variables
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
                if (time.time() - lastSourceChange > self.view_length):
                    lastSourceChange = time.time()
                    self.source_index = self.get_next_source_index()

                # Update the display buffer
                self.display.buffer = self.sources[self.source_index].buffer
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

    def get_next_source_index(self):
        next_index = self.source_index + 1
        # First check if we are beyond the list or not
        if next_index >= self.sources.__len__():
            next_index = 0

        # Check if next is allowed
        while True:
            if self.source_index == next_index:
                break 
            elif self.allowed_content_dict[self.sources[next_index].type]:
                return next_index
            else:
                next_index += 1
                if next_index >= self.sources.__len__():
                    next_index = 0

        return self.source_index


    def set_content_allowence(self,type_as_string,status):
        if type_as_string == "image":
            self.allowed_content_dict[SourceType.image] = status
        elif type_as_string == "animation":
            self.allowed_content_dict[SourceType.animation] = status
        elif type_as_string == "sprite":
            self.allowed_content_dict[SourceType.sprite] = status
        elif type_as_string == "video":
            self.allowed_content_dict[SourceType.video] = status
        else:
            pass

    def get_content_allowance(self,type_as_string):
        if type_as_string == "image":
            return self.allowed_content_dict[SourceType.image]
        elif type_as_string == "animation":
            return self.allowed_content_dict[SourceType.animation]
        elif type_as_string == "sprite":
            return self.allowed_content_dict[SourceType.sprite]
        elif type_as_string == "video":
            return self.allowed_content_dict[SourceType.video]
        else:
            return False
 
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
