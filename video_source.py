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

        self.video_frames = []
        self.load_videos(filename)
        self.current_frame = 0
        self.number_of_frames = 0

    def load_videos(self,video_file):
        # print "load_videos"
        vid_frames = []
        capture = cv2.VideoCapture(video_file)

        read_flag, frame = capture.read()
        i = 1

        while (read_flag):
            # print i
            if i % 10 == 0:
                self.video_frames.append(frame)
                vid_frames.append(frame)
            
            read_flag, frame = capture.read()
            i += 1
        vid_frames = np.asarray(vid_frames, dtype='uint8')[:-1]
        capture.release()
        self.number_of_frames = i
        print (i)

    def load(self, filename):
        pass

    def update(self, dt):
        self._buffer = self.video_frames[5]
        self.current_frame += 1
        print(self.current_frame)