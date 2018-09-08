import numpy as np
 
import cv2 as cv
from primesense import openni2
from primesense import _openni2 as c_api

import _const, calibration, helpers

def raw_touches( thresholded_image, touch_area_limits ):

    _ , contours, _ = cv.findContours( thresholded_image, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    contours_list = get_contours_info( contours )


    #esto va afuera de esta funcion, para poder asi dtectar tambien las figuras
    contours_in_screen = filter_countous_by_position(contours_list, touch_area_limits)

    raw_touches = filter_countous_by_size( contours_in_screen )

    return raw_touches

def get_contours_info( contours ):

    contours_list = []

    for contour in contours:
        
        #gets the moments of the contour, so we can calculate the center of mass and the area with them
        #for more information about contours, refer to https://docs.opencv.org/2.4/modules/imgproc/doc/structural_analysis_and_shape_descriptors.html#moments
        contour_moments = cv.moments(contour)

        center_of_mass = find_center_of_mass( contour_moments )

        #although the area can be calculated with cv.contourArea(contour), this function uses cv.moments that we already used
        #so its better to use the already calculated moments instead of calculing them twice
        area = get_area( contour_moments )

        if center_of_mass != 0 and area != 0 :
            contours_list.append({ "area": area, "center_of_mass": center_of_mass })

    return contours_list
        

def find_center_of_mass( contour_moments ):

    if contour_moments["m00"] != 0:
        center_of_mass = ( contour_moments["m10"] / contour_moments["m00"] , contour_moments["m01"] / contour_moments["m00"] )
    else:
        center_of_mass = (0,0)

    return center_of_mass

def get_area( contour_moments ):

    area = contour_moments["m00"]

    return area


def filter_countous_by_position( contours_list, touch_area_limits):  

    contours_in_screen = []

    for i, contour in enumerate(contours_list) :

        center_of_mass = contour["center_of_mass"]

        contour_position_relative_to_screen = cv.pointPolygonTest( touch_area_limits , center_of_mass , False)

        if contour_position_relative_to_screen != _const.POINT_OUTSIDE_SCREEN :
            
            contours_in_screen.append(contours_list[i])

    return contours_in_screen



def filter_countous_by_size( contours_in_screen ):

    raw_touches = []
    
    for i, contour in enumerate(contours_in_screen) :

        contour_area = contour["area"]

        if  contour_area >= _const.MIN_TOUCH_CONTOUR_AREA and contour_area < _const.MAX_TOUCH_CONTOUR_AREA :

             raw_touches.append(contours_in_screen[i])
        
        else:
            print("toobig")


    return raw_touches

#==========================Calibration======================

surface_model = calibration.get_surface_information()

#=======================Detection==============================

# can also accept the path of the OpenNI dll path
openni2.initialize("../lib")  

dev = openni2.Device.open_any()

depth_stream = dev.create_depth_stream()
depth_stream.start()
depth_stream.set_video_mode(c_api.OniVideoMode(pixelFormat = c_api.OniPixelFormat.ONI_PIXEL_FORMAT_DEPTH_1_MM, resolutionX = 640, resolutionY = 480, fps = 30))


detector = cv.SimpleBlobDetector()

while True :

    depth_frame = depth_stream.read_frame()
    depth_image = helpers.raw_depth_frame_to_img( depth_frame )

    min_threshold = ( surface_model["min_touch_distance"], surface_model["min_touch_distance"], surface_model["min_touch_distance"] )
    max_threshold = ( surface_model["max_touch_distance"], surface_model["max_touch_distance"], surface_model["max_touch_distance"] )
    
    
    #return an image with the objects inside the touching area
    thresholded_image = cv.inRange(depth_image, min_threshold , max_threshold)

    filtered_img = helpers.morph_opening( thresholded_image, _const.DEPTH_OPENING_KERNEL_SIZE )

    touches = raw_touches(thresholded_image, touch_area_limits = surface_model["touch_area_limits"])

    if(len(touches) > 0):
        print(touches)

    ############## DISPLAY ###########
    color_img = cv.cvtColor(filtered_img, cv.COLOR_GRAY2BGR )
    for touch in touches:
        color_img = cv.circle(color_img, tuple(map(int, touch["center_of_mass"])), int(helpers.get_circle_radius( area = touch["area"] )) , (0,0,255), 2)
    
    color_img = cv.drawContours(color_img, [surface_model["touch_area_limits"]], 0, (0,0, 255), 3)


    cv.imshow("threshold", color_img)
    cv.waitKey(34)


depth_stream.stop()
openni2.unload()


