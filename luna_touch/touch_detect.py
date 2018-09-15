import numpy as np
from collections import OrderedDict
 
import cv2 as cv
from primesense import openni2
from primesense import _openni2 as c_api

from luna_touch import _const, calibration, helpers, touch_tracking
from luna_touch.Touch import Touch

#from timeit import default_timer as timer


def start_detection_service( surface_model ):
    # can also accept the path of the OpenNI dll path
    openni2.initialize("../lib")  

    dev = helpers.open_kinect_device()

    depth_stream = dev.create_depth_stream()
    depth_stream.start()
    depth_stream.set_video_mode(c_api.OniVideoMode(pixelFormat = c_api.OniPixelFormat.ONI_PIXEL_FORMAT_DEPTH_1_MM, resolutionX = 640, resolutionY = 480, fps = 30))

    previous_frame_touches = OrderedDict()
    current_frame_touches = OrderedDict() 

    #repeat for every frame
    while True :
        #start = timer()
        previous_frame_touches = touch_tracking.not_ended_touches( current_frame_touches )

        depth_frame = depth_stream.read_frame()
        depth_image = helpers.raw_depth_frame_to_img( depth_frame )

        min_threshold = ( surface_model["min_touch_distance"], surface_model["min_touch_distance"], surface_model["min_touch_distance"] )
        max_threshold = ( surface_model["max_touch_distance"], surface_model["max_touch_distance"], surface_model["max_touch_distance"] )
        
        blurred_img = cv.medianBlur(depth_image,5)

        #return an image with the objects inside the touching area
        thresholded_image = cv.inRange(blurred_img, min_threshold , max_threshold)

        filtered_img = helpers.morph_opening( thresholded_image, _const.DEPTH_OPENING_KERNEL_SIZE )

        detected_touches = raw_touches(thresholded_image, touch_area_limits = surface_model["touch_area_limits"])

        #if(len(detected_touches) > 0):
        #    print(detected_touches)
        #else:
        #    print("no touch")
    
        current_frame_touches = touch_tracking.track_touches_changes( previous_frame_touches, detected_touches )

        ############## DISPLAY ###########
        color_img = cv.cvtColor(filtered_img, cv.COLOR_GRAY2BGR )

        for index, touch in current_frame_touches.items():
            color_img = cv.circle(color_img, touch.position , touch.radius , (0,255,0), 2)
            color_img = cv.putText(color_img, str(touch.id) , (touch.position[0] - 10, touch.position[1] - 10), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        color_img = cv.drawContours(color_img, [surface_model["touch_area_limits"]], 0, (0,0, 255), 3)


        cv.imshow("threshold", color_img)
        cv.waitKey(34)

        #end = timer()
        #print(end - start)


    depth_stream.stop()
    openni2.unload()


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

             raw_touches.append( Touch(center_of_mass = contours_in_screen[i]["center_of_mass"], area = contours_in_screen[i]["area"]) )

    return raw_touches


def not_ended_touches( current_frame_touches ):

    not_ended_touches = [ touch for touch in current_frame_touches if touch.state != _const.TOUCH_STATE_ENDED  ]

    return not_ended_touches

