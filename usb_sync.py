#!/usr/bin/env python3

# Imports
import threading
import pyudev
import os
from dirsync import sync
import time

class USBDetector():
    ''' Monitor udev to detect connected USB flash drives '''

    def __init__(self, directory):
        self.directory = directory
        thread = threading.Thread(target=self._work)
        thread.daemon = True
        thread.start()

    def _work(self):
        ''' Runs the detection loop '''
        self.context = pyudev.Context()
        self.monitor = pyudev.Monitor.from_netlink(self.context)
        self.monitor.filter_by(subsystem='usb')
        self.monitor.start()
        for device in iter(self.monitor.poll,None):
            print('{0.action} on {0.device_path}'.format(device))
            if device.action == 'add':
                self.on_created()

    def on_created(self):
        print("USB attached to the system. Sync directories!")
        time.sleep(1)
        with os.scandir("/media/pi/") as entries:
            print(entries)
            for entry in entries:
                print(entry)
                if entry.is_dir():
                    self.create_default_directories(entry.path)
                    self.sync_files(entry.path+"/sources/",self.directory)

    def create_default_directories(self, path):
        self.create_directory(path+"/sources/images")
        self.create_directory(path+"/sources/animations")
        self.create_directory(path+"/sources/videos")
        self.create_directory(path+"/sources/sprites")
    
    def create_directory(self,directory):
        if not os.path.exists(directory):
            os.makedirs(directory)

    def sync_files(self,source,destination):
        print("before sync")
        sync(source,destination,'sync',purge=False)
        print("after sync")

if __name__ == "__main__":
    usb_sync = USBDetector("/home/pi/")

    while(True):
        pass
