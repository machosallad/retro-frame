#!/usr/bin/env python3

# Imports
import time
import cv2
import numpy as np
from PIL import Image
from helpers import ImageHelper
from source.abstract import AbstractSource, SourceType
import pickle
import os
import math

class VideoSource(AbstractSource):
    def __init__(self, filename, width=16, height=16,type=SourceType.video, videoid=""):
        super().__init__(width, height)

        self.videoid = videoid
        self.current_frame = 0
        self.number_of_frames = 0
        self.total_time = 0
        self.video_frames = []
        self.frame_rate = 0
        self.frame_time = 0.0
        self._type = type
        self.load(filename)

    def load_binary(self,data):
        file = open(data,"rb")
        object_file = pickle.load(file)
        deserialised = object_file
        file.close()

        self.video_frames = deserialised
        self.number_of_frames = self.video_frames.__len__()

        parts = data.split("_")
        self.frame_rate = float(parts[1].split(".")[0])
        self.fps = self.frame_rate
        self._type = SourceType.youtube
        
    def dump_buffer(self, directory):
        if not os.path.isdir(directory):
            os.mkdir(directory)
        
        frame_rate = str(int(math.ceil(self.frame_rate)))
        dump = "{}{}_{}.bin".format(directory,self.videoid,frame_rate) # directory/videoid_fps.bin
        with open(dump,"wb") as handle:
            pickle.dump(self.video_frames,handle,protocol=pickle.HIGHEST_PROTOCOL)

    def load(self, filename):
        # Check if filename is binary
        if(filename.endswith(".bin")):
            self.load_binary(filename)
        else:
            print ("Loading video: {0}".format(filename))
            video = cv2.VideoCapture(filename)

            # Find OpenCV version
            (major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')
        
            if int(major_ver)  < 3 :
                self.frame_rate = video.get(cv2.cv.CV_CAP_PROP_FPS)
            else:
                self.frame_rate = video.get(cv2.CAP_PROP_FPS)

            print ("Frames per second : {0}".format(self.frame_rate))
            self.frame_time = 1./self.frame_rate
            self.fps = self.frame_rate

            frame_counter = 0

            start_time = time.time()
            while (True):
                # Start capturing the video frames
                ret, frame = video.read()

                if not ret:
                    break       

                frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
                frame = cv2.resize(frame, (self.width,self.height), interpolation = cv2.INTER_AREA )
                self.video_frames.append(frame)
                frame_counter += 1
                            
            video.release()
            stop_time = time.time()
            print("Elapsed time to capture video frames:{0}".format(stop_time-start_time))
            
            self.number_of_frames = frame_counter
            print ("Number of frames captures:{0}".format(self.number_of_frames))

            if self.videoid != "":
                self.dump_buffer("cache/")

    def update(self, dt):
        if self.fps > 0:
            # Grab the next frame directly
            self.current_frame += 1
        else:
            # Calculate if a new frame should be selected
            self.total_time += dt
            if(self.total_time > self.frame_time):
                self.current_frame += 1
                self.total_time = 0

        # Restore the frame counter
        if self.current_frame >= self.number_of_frames:
            self.current_frame = 0

        self._buffer = self.video_frames[self.current_frame]
        