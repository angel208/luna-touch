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
    MIN_TOUCH_DISTANCE_CONST = -5
    MAX_TOUCH_DISTANCE_CONST = -2
    CALIBRATION_DISTANCE_ITERATIONS = 2
    CALIBRATION_AREA_ITERATIONS = 50

    MIN_THRESH_WHITE = (-15, -15, 168)
    MAX_THRESH_WHITE = (15, 15, 295)
    OPENING_KERNEL_SIZE = 5
    GAUSSIAN_BLUR_SIZE = (5, 5)

    DEPTH_OPENING_KERNEL_SIZE = 2
    DEPTH_GAUSSIAN_BLUR_SIZE = (4, 4)

    OUTSIDE_ROI_DEPTH_VALUE = 6000
    UNDEFINED_PIXEL_DEPTH = 0

    POINT_OUTSIDE_POLY = -1
    POINT_OUTSIDE_SCREEN = -1
    POINT_INSIDE_POLY = 1
    POINT_AT_POLY_VERTEX = 0

    MAX_TOUCH_CONTOUR_AREA = 50
    MIN_TOUCH_CONTOUR_AREA = 5


    ##===================================

import sys
sys.modules[__name__] = _const(  )

