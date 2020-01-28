#!/user/bin/env python3
"""
Main entry point of the retro-frame project.
Runs the main game-loop.
"""

# Imports
import os
import platform
import sys
import abc
import numpy as np
import time
import requests
import pafy
import youtube_dl
import threading
import random
import pygame
from io import BytesIO
from enum import Enum
from random import seed
from random import randint
from PIL import Image
from pathlib import Path
from helpers import ImageHelper
from source.animation import AnimationSource
from source.image import ImageSource
from source.sprite import SpriteSource
from source.video import VideoSource
from source.abstract import SourceType

# Global variables
DISPLAY_WIDTH = 16
DISPLAY_HEIGTH = 16
FPS = 25
SPRITE_DIRECTORY    =   "sources/sprites/"
IMAGE_DIRECTORY     =   "sources/images/"
ANIMATION_DIRECTORY =   "sources/animations/"
VIDEO_DIRECTORY     =   "sources/videos/"
WAIT_ANIMATION      =   "resources/loading.gif"
CACHE_DIRECTORY     =   "cache/"
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
                self.sources.append(AnimationSource(filename=BytesIO(resp.content),type=SourceType.giphy))
            except:
                pass

    def load_images(self,dirpath):
        """ Load images from given directory"""
        if os.path.exists(dirpath):
            with os.scandir(dirpath) as entries:
                for entry in entries:
                    if entry.is_file():
                        self.sources.append(ImageSource(os.path.join(dirpath,entry.name), DISPLAY_WIDTH, DISPLAY_HEIGTH))
        else:
            print("Warning. Non-existing directory:",dirpath)

    def load_animations(self, dirpath):
        """ Load animations (gifs) from given directory"""
        if os.path.exists(dirpath):
            with os.scandir(dirpath) as entries:
                for entry in entries:
                    if entry.is_file():
                        self.sources.append(AnimationSource(os.path.join(dirpath,entry.name), DISPLAY_WIDTH, DISPLAY_HEIGTH))
        else:
            print("Warning. Non-existing directory:",dirpath)

    def load_sprites(self, dirpath):
        """ Load sprites from given directory"""
        self.sprite = SpriteSource(os.path.join(dirpath,"sprite_mario.png"), 233, 99, 16, 16, 5, 0.2, 1, 1)
        self.sources.append(self.sprite)

        self.goomba = SpriteSource(os.path.join(dirpath,"characters.gif"), 296, 187, 16, 16, 2, 0.2, 3, 3)
        self.sources.append(self.goomba)

    def load_videos(self,dirpath):
        """ Load videos from given directory"""
        if os.path.exists(dirpath):
            with os.scandir(dirpath) as entries:
                for entry in entries:
                    if entry.is_file():
                        self.sources.append(VideoSource(os.path.join(dirpath,entry.name), DISPLAY_WIDTH, DISPLAY_HEIGTH))
        else:
            print("Warning. Non-existing directory:",dirpath)

    def load_youtube_videos(self, urls):
        """ Load YouTube videos from the given array of urls"""
        for url in urls:
            vPafy = pafy.new(url)
            play = vPafy.getbest(preftype="webm")
            if play is not None:
                self.sources.append(VideoSource(play.url,DISPLAY_WIDTH, DISPLAY_HEIGTH))

    def rest_add_youtube_video_worker(self,url,videoid):
        cache_file = self.check_video_cache(CACHE_DIRECTORY,videoid)
        
        if cache_file != "":
            url = cache_file

        self.sources.append(VideoSource(filename=url,width=DISPLAY_WIDTH, height=DISPLAY_HEIGTH,type=SourceType.youtube,videoid=videoid))

    def rest_refresh_sources(self,source):
        if source == "all":
            self.sources.clear()
            self.load_default_resources()
            return True
        else:
            self.clear_source(source)
            if self.reload_source(source):
                return True
            else:
                return False

    def clear_source(self,source):
        for i in range(self.sources.__len__()-1,-1,-1):        
            if source == "images":
                if self.sources[i].type == SourceType.image:
                    self.sources.pop(i)
            elif source == "animations":
                if self.sources[i].type == SourceType.animation:
                    self.sources.pop(i)
            elif source == "sprites":
                if self.sources[i].type == SourceType.sprite:
                    self.sources.pop(i)
            elif source == "videos":
                if self.sources[i].type == SourceType.video:
                    self.sources.pop(i)
            elif source == "giphy":
                if self.sources[i].type == SourceType.giphy:
                    self.sources.pop(i)
            elif source == "youtube":
                if self.sources[i].type == SourceType.youtube:
                    self.sources.pop(i)

    def reload_source(self,source):
        result = True
        if source == "images":
            self.load_images(IMAGE_DIRECTORY)
        elif source == "animations":
            self.load_animations(ANIMATION_DIRECTORY)
        elif source == "sprites":
            self.load_sprites(SPRITE_DIRECTORY)
        elif source == "videos":
            self.load_videos(VIDEO_DIRECTORY)
        else:
            result = False
        
        return result

    def check_video_cache(self,directory,videoid):
        if os.path.isdir(directory):
            with os.scandir(directory) as entries:
                for entry in entries:
                    filename, file_extension = os.path.splitext(entry)
                    if file_extension == ".bin":
                        if videoid in filename:
                            return  filename+file_extension
        return ""  

    def rest_add_youtube_video(self,url):
            vPafy = pafy.new(url)
            play = vPafy.getbest(preftype="webm")
            if play is None:
                return False
            else:
                worker_thread = threading.Thread(target=self.rest_add_youtube_video_worker,args=(play.url,vPafy.videoid,))
                worker_thread.start()
                return True

    def rest_add_giphy_video(self,tag, count):
        worker_thread = threading.Thread(target=self.load_giphy_animations,args=(count,tag,))
        worker_thread.start()
        return True

    def rest_set_slideshow_control(self,command):
        if command == "next":
            self.slideshow_request_next = True
            return True
        elif command == "previous":
            self.slideshow_request_previous = True
            return True
        elif command == "pause":
            self.slideshow_request_pause = True
            return True
        elif command == "play":
            self.slideshow_request_pause = False
            return True

        return False

    def __init__(self):
        # Change working directory
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        
        if platform.system() == "Linux":
            if os.uname()[1] == 'raspberrypi':
                from display.ws2812b import WS2812B
                self.display = WS2812B(DISPLAY_WIDTH,DISPLAY_HEIGTH)

                from usb_sync import USBDetector
                self.usb_sync = USBDetector("sources/")
        else:
            from display.computer import Computer
            self.display = Computer(DISPLAY_WIDTH, DISPLAY_HEIGTH)

        self.source_index = 0
        self.sources = []
        self.load_threads = []
        self.view_length = 15
        self.mode = ViewMode.random
        self.allowed_content_dict = {SourceType.image:True, SourceType.video:True, SourceType.sprite:False, SourceType.animation:True, SourceType.giphy:True, SourceType.youtube:True}
        self.slideshow_request_pause = False
        self.slideshow_request_next = False
        self.slideshow_request_previous = False

        from server.http_server import RetroFrameHttpServer
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
        self.load_threads.append(threading.Thread(target=self.load_videos,args=(VIDEO_DIRECTORY,)))

        # Start all the threads in one go
        for thread in self.load_threads:
            thread.start()

    def mainloop(self):
        # Setup local variables
        wait_animation = AnimationSource(WAIT_ANIMATION)

        # Prepare and start loading resources
        lastSourceChange = time.time()
        clock = pygame.time.Clock()
        self.load_default_resources()
        dt = 0
        requested_fps = 0
       
        while True:
            # Verify if any resources are loaded
            if self.sources.__len__() > 0:
                # Update game logic, objects and data structures here using dt
                for source in self.sources:
                    source.update(dt)
                
                # Check if new source should be selected
                if (time.time() - lastSourceChange > self.view_length) or self.slideshow_request_next or self.slideshow_request_previous:
                    lastSourceChange = time.time()
                    self.source_index = self.get_next_source_index()

                # Update the display buffer
                self.display.buffer = self.sources[self.source_index].buffer
                requested_fps = self.sources[self.source_index].fps
            else:
                # Show waiting animation
                wait_animation.update(dt)
                self.display.buffer = wait_animation.buffer
            
            # Render the frame
            self.display.show()

            # Limit CPU usage do not go faster than FPS
            #print("FPS:", clock.get_fps(), "DT:", dt) # FPS = 1 / time to process loop
            if requested_fps > 0:
                dt = clock.tick(requested_fps)
            else:
                dt = clock.tick(FPS)
        return

    def get_next_source_index(self):
        # Check if any slideshow control commands are active
        next_index = self.source_index + 1
        if self.slideshow_request_previous:
            next_index = self.source_index - 1
            self.slideshow_request_previous = False
        elif self.slideshow_request_next:
            next_index = self.source_index + 1
            self.slideshow_request_next = False
        elif self.slideshow_request_pause:
            return self.source_index

        # First check if we are beyond the list or not
        if next_index >= self.sources.__len__():
            next_index = 0
        elif next_index < 0:
            next_index = self.sources.__len__() - 1

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
        if type_as_string == "images":
            self.allowed_content_dict[SourceType.image] = status
            return True
        elif type_as_string == "animations":
            self.allowed_content_dict[SourceType.animation] = status
            return True
        elif type_as_string == "sprites":
            self.allowed_content_dict[SourceType.sprite] = status
            return True
        elif type_as_string == "videos":
            self.allowed_content_dict[SourceType.video] = status
            return True
        elif type_as_string == "giphy":
            self.allowed_content_dict[SourceType.giphy] = status
            return True
        elif type_as_string == "youtube":
            self.allowed_content_dict[SourceType.youtube] = status
            return True
        else:
            return False

    def get_content_allowance(self,type_as_string):
        if type_as_string == "images":
            return self.allowed_content_dict[SourceType.image]
        elif type_as_string == "animations":
            return self.allowed_content_dict[SourceType.animation]
        elif type_as_string == "sprites":
            return self.allowed_content_dict[SourceType.sprite]
        elif type_as_string == "videos":
            return self.allowed_content_dict[SourceType.video]
        elif type_as_string == "giphy":
            return self.allowed_content_dict[SourceType.giphy]
        elif type_as_string == "youtube":
            return self.allowed_content_dict[SourceType.youtube]
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
