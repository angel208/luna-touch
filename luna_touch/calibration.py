import numpy as np

import cv2 as cv
from primesense import openni2
from primesense import _openni2 as c_api

import _const, helpers
#from . import _const


def get_surface_distance():

    # can also accept the path of the OpenNI redistribution
    openni2.initialize("../lib")     

    dev = openni2.Device.open_any()
    depth_stream = dev.create_depth_stream()
    depth_stream.start()
    depth_stream.set_video_mode(c_api.OniVideoMode(pixelFormat = c_api.OniPixelFormat.ONI_PIXEL_FORMAT_DEPTH_1_MM, resolutionX = 640, resolutionY = 480, fps = 30))

    counter = 1
    distances_array = []

    while counter <= _const.CALIBRATION_DISTANCE_ITERATIONS :

        print("calibrating...")

        depth_frame = depth_stream.read_frame()

        img = helpers.raw_depth_frame_to_img( depth_frame )

        curr_surface_distance = find_most_ocurring_pixel_value( img )

        distances_array.append(curr_surface_distance)

        counter = counter + 1

    surface_distance = mode(distances_array)

    depth_stream.stop()
    openni2.unload()

    return surface_distance




def find_most_ocurring_pixel_value( calibration_frame ):

    # Sort the array to traverse it, looking for the most occurring pixel value in the image
    calibration_frame = calibration_frame.flatten()
    calibration_frame.sort()

    max_count = 0
    mode_value = 0

    curr_count = 0
    curr_pixel_value = 0

    for pixel in calibration_frame :
         
         if pixel == curr_pixel_value : 
             curr_count = curr_count + 1
         else:
             if curr_count > max_count :
                max_count = curr_count
                mode_value = curr_pixel_value
                
             curr_count = 0 
             curr_pixel_value = pixel

    return mode_value


def mode( array ):

    array.sort()

    max_count = 0
    mode_value = 0

    curr_count = 0
    curr_value = 0

    for distance in array:
         
         if distance == curr_value : 
             curr_count = curr_count + 1
         else:
             if curr_count > max_count :
                max_count = curr_count
                mode_value = curr_value
                
             curr_count = 0 
             curr_value = distance

    return mode_value