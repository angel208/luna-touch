import numpy as np
import cv2 as cv
import time
import ctypes

from primesense import utils
from primesense import openni2

from luna_touch import _const


def raw_depth_frame_to_img( frame ):

    frame_data = frame.get_buffer_as_uint16()
    img = np.frombuffer(frame_data, dtype=np.uint16) 
    img.shape = (1, 480, 640)
    img = np.concatenate((img, img, img), axis=0)
    img = np.swapaxes(img, 0, 2)
    img = np.swapaxes(img, 0, 1)

    return img

def raw_color_frame_to_HSV ( color_frame ):
    frame_data = color_frame.get_buffer_as_uint8()
    img = np.frombuffer(frame_data, dtype=np.uint8) 
    img.shape = (480, 640, 3)
    img = cv.cvtColor(img, cv.COLOR_RGB2HSV )
    return img

def raw_color_frame_to_BGR ( color_frame ):
    frame_data = color_frame.get_buffer_as_uint8()
    img = np.frombuffer(frame_data, dtype=np.uint8) 
    img.shape = (480, 640, 3)
    img = cv.cvtColor(img, cv.COLOR_RGB2BGR )
    return img

def raw_color_frame_to_LAB ( color_frame ):
    frame_data = color_frame.get_buffer_as_uint8()
    img = np.frombuffer(frame_data, dtype=np.uint8) 
    img.shape = (480, 640, 3)
    img = cv.cvtColor(img, cv.COLOR_RGB2LAB )
    return img

def morph_opening( img ):

    erotion_kernel = np.ones(( _const.DEPTH_EROTION_KERNEL_SIZE, _const.DEPTH_EROTION_KERNEL_SIZE ),np.uint8)
    dilation_kernel = np.ones(( _const.DEPTH_DILATION_KERNEL_SIZE, _const.DEPTH_DILATION_KERNEL_SIZE ),np.uint8)

    eroded_img = cv.erode(img,erotion_kernel,iterations = 1)
    open_img = cv.dilate(eroded_img,dilation_kernel,iterations = 1)
 
    return open_img

def get_circle_radius( area ):

    radius = np.sqrt( area / np.pi )
    
    return radius

def timestamp_in_milliseconds():
   return int(round(time.time() * 1000))

def open_kinect_device():
    print("Buscando Dispositivo Kinect...")

    while True:
        try:
            device = openni2.Device.open_any()
            break
        except utils.OpenNIError:
            print("no")

    return device

def get_display_resolution():
    user32 = ctypes.windll.user32
    screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    return screensize