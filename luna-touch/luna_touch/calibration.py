import numpy as np
import queue
import threading

import tkinter as tk
from PIL import Image, ImageTk
import cv2 as cv
from primesense import openni2
from primesense import _openni2 as c_api

from luna_touch import _const, helpers
from luna_touch.animatedGif import AnimatedGif

def run_calibration_process():

    root = tk.Tk()
    root.state('zoomed')
    root.resizable(False, False)

    image = Image.open('./luna_touch/res/calibrating.png')
    background_image = ImageTk.PhotoImage(image)

    background = tk.Label( root, image = background_image)
    background.pack()

    player1 = AnimatedGif('./luna_touch/res/calibrating.gif', frames=23, fps=40)

    loading_gif = tk.Label(root)
    loading_gif.configure(image = player1.currentFrame())
    loading_gif.configure(background='white')
    loading_gif.place( relheight = 0.2 , relwidth = 0.2, relx = 0.39 , rely = 0.63)


    q = queue.Queue()
    threading.Thread(target=request_surface_information, args=(q,) ).start()

    while True:

        loading_gif.configure(image = player1.nextFrame())
        root.update()

        if(not q.empty()):
            surface_information = q.get_nowait()
            print(surface_information)
            root.destroy()
            return surface_information
            break



def request_surface_information( surface_information_queue ):

    surface_information = get_surface_information()

    surface_information_queue.put(surface_information)

    return surface_information    

def get_surface_information():

    touch_area_limits = np.array(order_rect_points2(get_surface_area_limits()))
    print(touch_area_limits)
    surface_distance = get_surface_distance(touch_area_limits)
    print(surface_distance)

    touch_area = {
                    "min_touch_distance" : int(surface_distance + _const.MIN_TOUCH_DISTANCE_CONST), 
                    "max_touch_distance" : int(surface_distance + _const.MAX_TOUCH_DISTANCE_CONST), 
                    "touch_area_limits"  : touch_area_limits,
                 }

    return touch_area

# the list of points will be ordered
# such that the first entry in the list is the bottom-left,
# the second entry is the bottom-right, the third is the
# top-right, and the fourth is the top-left
def order_rect_points2(pts):
    print("casl")
    print(pts)

    rect = np.zeros((4, 2), dtype = "float32")
 
    # the top-left point will have the smallest sum, whereas
    # the bottom-right point will have the largest sum
    s = pts.sum(axis = 1)
    rect[3] = pts[np.argmin(s)] #top left
    rect[1] = pts[np.argmax(s)] #bottom_rigth
 
    # now, compute the difference between the points, the
    # top-right point will have the smallest difference,
    # whereas the bottom-left will have the largest difference
    diff = np.diff(pts, axis = 1)
    rect[2] = list(map( int, pts[np.argmin(diff)] ))#top right
    rect[0] = pts[np.argmax(diff)] #bottom left
 
    # return the ordered coordinates
    return list(
                    map(list,
                        [
                            [ int(rect[0][0] - 5), int(rect[0][1] )],
                            [ int(rect[1][0] ) + 10, int(rect[1][1]) - 15] , 
                            [ int(rect[2][0] ), int(rect[2][1] - 22)],
                            [int(rect[3][0] - 20), int(rect[3][1])-  15] 
                        ]
                    )
                )
                
    '''return list(
                    map(list,
                        [
                            [ int(rect[0][0] - 40), int(rect[0][1] )],
                            [ int(rect[1][0] ), int(rect[1][1])], 
                            [ int(rect[2][0]  ), int(rect[2][1] - 40 )],
                            [int(rect[3][0] - 40), int(rect[3][1] - 40)] 
                        ]
                    )
                )'''

def get_surface_area_limits():
    # can also accept the path of the OpenNI redistribution
    openni2.initialize("lib")     
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

        filtered_img = helpers.morph_opening( thresholded_img )

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

    return 650
    #return 720
    
    # can also accept the path of the OpenNI redistribution
    openni2.initialize("../lib")     

    dev = helpers.open_kinect_device()
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


