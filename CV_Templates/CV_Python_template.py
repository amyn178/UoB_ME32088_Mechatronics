"""
This script captures camera frames, displays color and grayscale images, and reports the frame rate.

@author: ioannisgeorgilas
"""

# This is the vision library OpenCV
import cv2
import logging
# This is a library for mathematical functions for python (used later)
import numpy as np
# This is a library to get access to time-related functionalities
import time


logging.basicConfig(level=logging.INFO)

# Select the first camera (0) that is connected to the machine
# in Laptops should be the built-in camera
cap = cv2.VideoCapture(1)
if not cap.isOpened():
    logging.error("Could not open camera 1")
    raise SystemExit(1)
logging.info("Camera 1 opened")

# Set the width and height of the camera to 1920x1080
cap.set(3,1920)
cap.set(4,1080)
logging.info(
    "Camera resolution: %dx%d",
    int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
    int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
)

#Create two opencv named windows
cv2.namedWindow("frame-image", cv2.WINDOW_AUTOSIZE)
cv2.namedWindow("gray-image", cv2.WINDOW_AUTOSIZE)
cv2.namedWindow("canny-image", cv2.WINDOW_AUTOSIZE)
cv2.namedWindow("gausian-image", cv2.WINDOW_AUTOSIZE)

#Position the windows next to each other
cv2.moveWindow("frame-image",0,100)
cv2.moveWindow("gray-image",100,100)
cv2.moveWindow("canny-image",200,100)
cv2.moveWindow("gausian-image",300,100)

# Execute this continuously
last_fps_log = time.perf_counter()
while(True):
    
    # Start the performance clock
    start = time.perf_counter()
    
    # Capture current frame from the camera
    ret, frame = cap.read()
    if not ret:
        logging.error("Could not read a frame from camera 1")
        break
    
    # Convert the image from the camera to Gray scale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    #display the gausian blur image in another window
    gausian = cv2.GaussianBlur(gray, (9, 9), 0)

    #canny edge detection
    #change the thresholds to see the effect on the output
    canny = cv2.Canny(gausian, 40, 100)

    # Display the original frame in a window
    cv2.imshow('frame-image',frame)
    
    # Display the grey image in another window
    cv2.imshow('gray-image',gray)

    # Display the canny image in another window
    cv2.imshow('canny-image',canny)

    # Display the gausian image in another window
    cv2.imshow('gausian-image',gausian)

    # Stop the performance counter
    end = time.perf_counter()
    
    # Report the frame rate once per second rather than on every frame
    if end - last_fps_log >= 1.0:
        logging.info("Camera FPS: %.2f", 1 / (end - start))
        last_fps_log = end

    # If the button q is pressed in one of the windows 
    if cv2.waitKey(20) & 0xFF == ord('q'):
        # Exit the While loop
        break
    

# When everything done, release the capture
cap.release()
# close all windows
cv2.destroyAllWindows()
logging.info("Camera capture stopped")
# exit the kernel
exit(0)