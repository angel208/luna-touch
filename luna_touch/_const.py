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
    MIN_TOUCH_DISTANCE_CONST = -50
    MAX_TOUCH_DISTANCE_CONST = +10
    CALIBRATION_DISTANCE_ITERATIONS = 10




    ##===================================

import sys
sys.modules[__name__] = _const(  )

