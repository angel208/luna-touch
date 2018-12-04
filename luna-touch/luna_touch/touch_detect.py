import numpy as np
from collections import OrderedDict
import copy

import cv2 as cv
from primesense import openni2
from primesense import _openni2 as c_api
from scipy.spatial import distance
import json

from luna_touch import _const, calibration, helpers, touch_tracking
from luna_touch.Touch import Touch


from timeit import default_timer as timer


def start_detection_service( surface_model, event_queue ):
    # can also accept the path of the OpenNI dll path
    openni2.initialize("../lib")  

    dev = helpers.open_kinect_device()

    depth_stream = dev.create_depth_stream()
    depth_stream.start()
    depth_stream.set_video_mode(c_api.OniVideoMode(pixelFormat = c_api.OniPixelFormat.ONI_PIXEL_FORMAT_DEPTH_1_MM, resolutionX = 640, resolutionY = 480, fps = 30))

    color_stream = dev.create_color_stream()
    color_stream.start()
    color_stream.set_video_mode(c_api.OniVideoMode(pixelFormat = c_api.OniPixelFormat.ONI_PIXEL_FORMAT_RGB888, resolutionX = 640, resolutionY = 480, fps = 30))

    with open('bracelets.json') as f:
        bracelets = json.load(f)
        print(bracelets)

    previous_frame_touches = OrderedDict()
    current_frame_touches = OrderedDict() 

    #this transform matrix will be used in the process of mapping the touches to screen coordinates
    #screen_resolution = helpers.get_display_resolution()
    screen_resolution = ( 1366, 768)
    transform_matrix = get_transform_matrix( surface_model['touch_area_limits'], screen_resolution[0], screen_resolution[1])

    #repeat for every frame
    while True :
        start = timer()
        previous_frame_touches = touch_tracking.not_ended_touches( current_frame_touches )

        depth_frame = depth_stream.read_frame()
        depth_image = helpers.raw_depth_frame_to_img( depth_frame )

        min_threshold = ( surface_model["min_touch_distance"], surface_model["min_touch_distance"], surface_model["min_touch_distance"] )
        max_threshold = ( surface_model["max_touch_distance"], surface_model["max_touch_distance"], surface_model["max_touch_distance"] )
        
        blurred_img = cv.medianBlur(depth_image,5)

        thresholded_image = cv.inRange(blurred_img, min_threshold , max_threshold)

        filtered_img = helpers.morph_opening( thresholded_image )

        detected_touches = raw_touches(thresholded_image, touch_area_limits = surface_model["touch_area_limits"])

    
        current_frame_touches = touch_tracking.track_touches_changes( previous_frame_touches, detected_touches )
        
        #color_frame = color_stream.read_frame()
        #img_bgr = helpers.raw_color_frame_to_BGR( color_frame )
        #img_hsv = helpers.raw_color_frame_to_HSV( color_frame )
        #img_bgr = recog_users( bracelets, img_hsv, img_bgr, current_frame_touches )

        ############## DISPLAY ###########
        color_img = cv.cvtColor(filtered_img, cv.COLOR_GRAY2BGR )

        for index, touch in current_frame_touches.items():
            if touch.state == 1:
                color_img = cv.circle(color_img, touch.position , touch.radius , (0,255,0), 2)
                color_img = cv.putText(color_img, str(touch.id) , (touch.position[0] - 10, touch.position[1] - 10), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            elif touch.state == 2:
                color_img = cv.circle(color_img, touch.position , touch.radius , (0,0,255), 2)
                color_img = cv.putText(color_img, str(touch.id) , (touch.position[0] - 10, touch.position[1] - 10), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            else:
                color_img = cv.circle(color_img, touch.position , touch.radius , (255,0,0), 2)
                color_img = cv.putText(color_img, str(touch.id) , (touch.position[0] - 10, touch.position[1] - 10), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)


        color_img = cv.drawContours(color_img, [surface_model["touch_area_limits"]], 0, (0,0, 255), 3)
        ###################################################


        maped_touches = map_touches_to_screen_coordinates(current_frame_touches.copy(), transform_matrix)
        
        
        enqueue( event_queue , maped_touches)

       #cv.imshow("color", img_bgr)
        cv.imshow("threshold", color_img)
        cv.waitKey(34)

        end = timer()
        #print(end - start) 


    depth_stream.stop()
    openni2.unload()

def map_touches_to_screen_coordinates(current_frame_touches, transform_matrix):

    maped_touches = OrderedDict()

    for key, touch in current_frame_touches.items():
        maped_touches[key] = copy.copy(touch)
        maped_touches[key].position =  map_touch_position_to_screen_coordinate( touch.position , transform_matrix )

    return maped_touches


def enqueue( event_queue , event ):

    if event_queue.qsize() > _const.MAX_QUEUE_SIZE:
        
        event_queue.get()

    
    touch = [ touch.__dict__ for touch in  list(event.values())  ]
    print(event)
    event_queue.put( touch )
    
def recog_users( bracelets, hsv_image, bgr_img, touches):

    for bracelet in bracelets:
    
        lower = np.array(bracelet["lower_threshold"])
        upper = np.array(bracelet["upper_threshold"])

        filtered = cv.inRange(hsv_image, lower , upper)
        filtered = cv.medianBlur(filtered,5)
        filtered = helpers.morph_opening( filtered )

        im2, contours, hierarchy = cv.findContours(filtered,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)

        #filter by shape TODO
        if(len(contours)):

            max_contour = max(contours, key = cv.contourArea)

            M = cv.moments(max_contour)

            if ( M["m00"] > 0):
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                print( "center: " + str(cX) + "," + str(cY))
                bgr_img = cv.drawContours(bgr_img, max_contour, 0, (255,0,0), 3)
            else:
                continue;
        else:
            continue;

        bracelet["current_pos"] = [ cX , cY ]
    
    #print(bracelets)

    
    touches_pos = [ list(touch.position) for touch in  list(touches.values()) ]
    bracelets_pos = [ x["current_pos"] for x in bracelets ]

    if( len(touches_pos) > 0 ):

        print(touches_pos)
        print(bracelets_pos)

        print("Asd")
        print(touches)

        # the result of this operation is the index of the first array that are closer to the second = [ 0 0 1 1 1]
        closest_distance_indexes = np.argmin(distance.cdist(bracelets_pos,touches_pos,'sqeuclidean'),axis=0)
        
        for index, touch in list(touches.values()):
            print(touch)
            bracelet_index = closest_distance_indexes[index]
            touch.user = bracelets[bracelet_index]["id"]

        print(touches)

    return bgr_img

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


# the list of points will be ordered
# such that the first entry in the list is the bottom-left,
# the second entry is the bottom-right, the third is the
# top-right, and the fourth is the top-left
def order_rect_points(pts):

    #print("ords")
    #print(type(pts))
    
    rect = np.zeros((4, 2), dtype = "float32")
 
    # the top-left point will have the smallest sum, whereas
    # the bottom-right point will have the largest sum
    s = pts.sum(axis = 1)
    rect[3] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]
 
    # now, compute the difference between the points, the
    # top-right point will have the smallest difference,
    # whereas the bottom-left will have the largest difference
    diff = np.diff(pts, axis = 1)
    rect[1    ] = pts[np.argmin(diff)]
    rect[0] = pts[np.argmax(diff)]
 
    # return the ordered coordinates
    return rect

def get_transform_matrix(original_points, resolution_max_width, resolution_max_heigth):
    
    ordered_original_rectangle = order_rect_points(original_points)
    ( bl, br, tr, tl) = ordered_original_rectangle
 
    final_map_width = resolution_max_width
    final_map_heigth = resolution_max_heigth
    
    destination_matrix = np.array([
        
        [0, final_map_heigth - 1],
        [final_map_width - 1, 0],
        [final_map_width - 1, final_map_heigth - 1],

        [0, 0]
        ],
         dtype = "float32")
 
    transform_matrix = cv.getPerspectiveTransform( ordered_original_rectangle, destination_matrix )

    return transform_matrix


def map_touch_position_to_screen_coordinate( touch_position , transform_matrix ):

    point =  np.array([[list(touch_position)]], dtype=np.float32)

    maped_point = cv.perspectiveTransform( src = point , m = transform_matrix);
    result_point = list(map(int,maped_point[0][0]))

    if result_point[0] < 0:
        result_point[0] = 0 
    elif result_point[1] < 0:
        result_point[1] = 0 


    return  tuple(result_point)

