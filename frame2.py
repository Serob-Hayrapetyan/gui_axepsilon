#! /usr/bin/env python

# import the necessary packages
import sys
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
from subprocess import call
from threading import Thread
import PIL.Image, PIL.ImageTk
from Tkinter import *

indexOfPic = 0
indexOfVid = 0

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.framerate = 15
camera.iso = 800
rawCapture = PiRGBArray(camera, size=(450,450)) 

def Preview(root):
    global camera
    global rawCapture
    camera.resolution = (450,450)
    while(True):
    
        for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
            image = frame.array
            b,g,r = cv2.split(image)
            image = cv2.merge((r,g,b))
            # show the frame
            im = PIL.Image.fromarray(image)
            imgtk = PIL.ImageTk.PhotoImage(image=im) 
            Label(root, background = 'black',image=imgtk).place(relx = 0.04,rely = 0.04,relheight = 0.4,relwidth = 0.4)
            rawCapture.truncate(0)

            
def capture():
    global camera
    global indexOfPic
    camera.resolution = (2592,1944)
    name = 'image' + str(indexOfPic) + '.jpg'
    camera.capture('/home/pi/Desktop/pictures/' + name)
    indexOfPic+=1

def video():
    global camera
    global indexOfVid
    camera.resolution = (1280, 720)
    name = 'video' + str(indexOfVid) + '.h264'
    camera.start_preview()
    camera.start_recording('/home/pi/Desktop/pictures/' + name)
    time.sleep(7)
    camera.stop_recording()
    camera.stop_preview()
    indexOfVid+=1
    

def main():
    Preview()
    print("End programm")
    
if __name__ == "__main__":
    main()
