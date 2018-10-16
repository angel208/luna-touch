##This class contains al the constants needed in the module.
##it doesnt allow the rebinding of the constants

class _const:

    class ConstError(TypeError): pass

    def __setattr__(self, name, value):       
            raise self.ConstError("Can't rebind const")

    def __delattr__(self, name):
            raise self.ConstError("Can't unbind const")
    
    ##============CONSTANTS==============

    DEPTH_WHITE = 65536
    MIN_TOUCH_DISTANCE_CONST = -4
    MAX_TOUCH_DISTANCE_CONST = -2
    CALIBRATION_DISTANCE_ITERATIONS = 2
    CALIBRATION_AREA_ITERATIONS = 50

    MIN_THRESH_WHITE = (-15, -15, 168)
    MAX_THRESH_WHITE = (15, 15, 295)
    OPENING_KERNEL_SIZE = 5
    GAUSSIAN_BLUR_SIZE = (5, 5)

    DEPTH_OPENING_KERNEL_SIZE = 4
    DEPTH_EROTION_KERNEL_SIZE = 2
    DEPTH_DILATION_KERNEL_SIZE = 6
    DEPTH_GAUSSIAN_BLUR_SIZE = (5, 5)
    DEPTH_MEDIAN_BLUR_SIZE = 3

    OUTSIDE_ROI_DEPTH_VALUE = 6000
    UNDEFINED_PIXEL_DEPTH = 0

    POINT_OUTSIDE_POLY = -1
    POINT_OUTSIDE_SCREEN = -1
    POINT_INSIDE_POLY = 1
    POINT_AT_POLY_VERTEX = 0

    MAX_TOUCH_CONTOUR_AREA = 500
    MIN_TOUCH_CONTOUR_AREA = 10


    TOUCH_STATE_BEGAN = 1
    TOUCH_STATE_ENDED = 2
    TOUCH_STATE_STILL = 3
    TOUCH_STATE_MOVED = 4
    TOUCH_STATE_MISSED = 5
    TOUCH_TRACKING_MAX_RATIO = 70   
    TOUCH_TRACKING_MAX_MISSED_FRAMES = 2
    DEFAULT_TOUCH_AREA = MIN_TOUCH_CONTOUR_AREA+10

    MAX_QUEUE_SIZE = 30
    QUEUE_NAME = "luna-touch-queue"


    PY_AXIS_ROW = 1

    ##===================================

import sys
sys.modules[__name__] = _const(  )

