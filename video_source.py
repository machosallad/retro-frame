#!/usr/bin/env python3

# Imports
import time
import cv2
import numpy as np
from PIL import Image
from helpers import ImageHelper
from abstract_source import AbstractSource

class VideoSource(AbstractSource):
    def __init__(self, filename, width=16, height=16):
        super().__init__(width, height)

        self.current_frame = 0
        self.number_of_frames = 0
        self.total_time = 0
        self.video_frames = []
        self.frame_rate = 0
        self.load(filename)

    def load(self, filename):
        print ("Loading video: {0}".format(filename))
        video = cv2.VideoCapture(filename)

        # Find OpenCV version
        (major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')
      
        if int(major_ver)  < 3 :
            self.frame_rate = video.get(cv2.cv.CV_CAP_PROP_FPS)
        else:
            self.frame_rate = video.get(cv2.CAP_PROP_FPS)

        print ("Frames per second : {0}".format(self.frame_rate))

        # Start capturing the video frames
        read_flag, frame = video.read()
        i = 1
        frame_counter = 0

        start_time = time.time()
        while (read_flag):
            # print i
            if i % 1 == 0:
                frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
                frame = cv2.resize(frame, (self.width,self.height), interpolation = cv2.INTER_AREA )
                self.video_frames.append(frame)
                frame_counter += 1          
            read_flag, frame = video.read()
            i += 1
        video.release()
        stop_time = time.time()
        print("Elapsed time to capture video frames:{0}".format(stop_time-start_time))
        
        self.number_of_frames = frame_counter
        print ("Number of frames captures:{0}".format(self.number_of_frames))

    def update(self, dt):
        self.total_time += dt
        if(self.total_time > (1./self.frame_rate)):
            self.current_frame += 1
            self.total_time = 0

        # Restore the frame counter
        if self.current_frame >= self.number_of_frames:
            self.current_frame = 0

        self._buffer = self.video_frames[self.current_frame]
        