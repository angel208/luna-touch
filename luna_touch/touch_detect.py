import numpy as np
 
import cv2 as cv
from primesense import openni2
from primesense import _openni2 as c_api

import _const, calibration, helpers

#==========================Calibration======================

distance_to_surface = calibration.get_surface_distance()
#surface_limit_points = calibration.get_surface_limit_points()

touch_area = {
               "min_touch_distance" : int(distance_to_surface + _const.MIN_TOUCH_DISTANCE_CONST), 
               "max_touch_distance" : int(distance_to_surface + _const.MAX_TOUCH_DISTANCE_CONST), 
               #include surface limit points
             }

print(touch_area)

#=======================Detection==============================

# can also accept the path of the OpenNI dll path
openni2.initialize("../lib")  

dev = openni2.Device.open_any()

depth_stream = dev.create_depth_stream()
depth_stream.start()
depth_stream.set_video_mode(c_api.OniVideoMode(pixelFormat = c_api.OniPixelFormat.ONI_PIXEL_FORMAT_DEPTH_1_MM, resolutionX = 640, resolutionY = 480, fps = 30))

while True :

    depth_frame = depth_stream.read_frame()
    img = helpers.raw_depth_frame_to_img( depth_frame )

    min_threshold = ( touch_area["min_touch_distance"], touch_area["min_touch_distance"], touch_area["min_touch_distance"] )
    max_threshold = ( touch_area["max_touch_distance"], touch_area["max_touch_distance"], touch_area["max_touch_distance"] )
    
    print(min_threshold)

    #return an image with the objects inside the touching area
    img = cv.inRange(img, min_threshold , max_threshold)

    cv.imshow("threshold", img)
    cv.waitKey(34)


depth_stream.stop()
openni2.unload()

