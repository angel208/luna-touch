import numpy as np

import cv2 as cv
from primesense import openni2
from primesense import _openni2 as c_api

import _const, helpers
#from . import _const


def get_surface_information():

    touch_area_limits = get_surface_area_limits()
    print(touch_area_limits)
    surface_distance = get_surface_distance(touch_area_limits)
    print(surface_distance)

    touch_area = {
                    "min_touch_distance" : int(surface_distance + _const.MIN_TOUCH_DISTANCE_CONST), 
                    "max_touch_distance" : int(surface_distance + _const.MAX_TOUCH_DISTANCE_CONST), 
                    "touch_area_limits"  : touch_area_limits,
                 }

    return touch_area

def get_surface_area_limits():
    # can also accept the path of the OpenNI redistribution
    openni2.initialize("../lib")     
    dev = openni2.Device.open_any()
    color_stream = dev.create_color_stream()
    color_stream.start()
    color_stream.set_video_mode(c_api.OniVideoMode(pixelFormat = c_api.OniPixelFormat.ONI_PIXEL_FORMAT_RGB888, resolutionX = 640, resolutionY = 480, fps = 30))

    counter = 0
    avg_points = np.array([ [0,0] , [0,0] , [0,0] , [0,0] ])

    while counter < _const.CALIBRATION_AREA_ITERATIONS :

        color_frame = color_stream.read_frame()
        img_hsv = helpers.raw_color_frame_to_HSV( color_frame )
        img_bgr = helpers.raw_color_frame_to_BGR( color_frame )

        blurred = cv.GaussianBlur(img_hsv, _const.GAUSSIAN_BLUR_SIZE , 0)

        thresholded_img = cv.inRange(blurred,  _const.MIN_THRESH_WHITE , _const.MAX_THRESH_WHITE )

        filtered_img = helpers.morph_opening( thresholded_img, _const.OPENING_KERNEL_SIZE  )

        _ , contours, _ = cv.findContours( filtered_img, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

        if len(contours) > 0:
            #find the biggest contour
            biggest_contour = max(contours, key = cv.contourArea)
            
            min_rectangle = cv.minAreaRect(biggest_contour)
            rec_points = cv.boxPoints(min_rectangle)
            rec_points = np.int0(rec_points)

            cv.drawContours(img_bgr, [rec_points], 0, (0,0, 255), 3)

            avg_points = avg_points + np.array(rec_points)

            counter += 1
                
        cv.imshow("image", img_bgr )
        cv.waitKey(34)    

    avg_points = avg_points // counter    

    cv.drawContours(img_bgr, [avg_points], 0, (0,255, 0), 3)

    #while True:
    #    cv.imshow("image", img_bgr )
    #    cv.waitKey(34)  

    color_stream.stop()
    openni2.unload()

    return avg_points


def get_surface_distance( touch_area_limits ):

    return 713

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

        calibration_frame = get_ROI( img , touch_area_limits )

        curr_surface_distance = find_most_ocurring_pixel_value( calibration_frame , touch_area_limits)
        
        if ( curr_surface_distance > _const.UNDEFINED_PIXEL_DEPTH ) and ( curr_surface_distance < _const.OUTSIDE_ROI_DEPTH_VALUE ) :
            print(curr_surface_distance)
            distances_array.append(curr_surface_distance)
            counter = counter + 1
        else: 
            print(curr_surface_distance)

    surface_distance = mode(distances_array)

    depth_stream.stop()
    openni2.unload()

    return surface_distance




def find_most_ocurring_pixel_value( calibration_frame, limits ):

    # Sort the array to traverse it, looking for the most occurring pixel value in the image
    calibration_frame = calibration_frame.flatten()
    calibration_frame.sort()

    max_count = 0
    mode_value = 0

    curr_count = 0
    curr_pixel_value = 0

    for pixel in calibration_frame :

        if (pixel != _const.UNDEFINED_PIXEL_DEPTH) and (pixel != _const.OUTSIDE_ROI_DEPTH_VALUE):

            if pixel == curr_pixel_value : 
                curr_count = curr_count + 1
            else:
                if curr_count >= max_count :
                    max_count = curr_count
                    mode_value = curr_pixel_value
                    
                curr_count = 0 
                curr_pixel_value = pixel

    return mode_value


def get_ROI(calibration_frame, limits):
    
    filtered_frame = calibration_frame

    for i, row in enumerate(filtered_frame) :
        for j, pixel in enumerate(row):

            is_inside_roi = cv.pointPolygonTest(limits, (j,i), False)

            if( is_inside_roi == _const.POINT_OUTSIDE_POLY   ):

                filtered_frame[i][j] = _const.OUTSIDE_ROI_DEPTH_VALUE

    return filtered_frame



def mode( array ):

    array.sort()
    print(array)
    max_count = 0
    mode_value = 0

    curr_count = 0
    curr_value = 0

    for distance in array:
         
         if distance == curr_value : 
             curr_count = curr_count + 1
         else:
             if curr_count >= max_count :
                max_count = curr_count
                mode_value = curr_value
                
             curr_count = 0 
             curr_value = distance

    return mode_value


