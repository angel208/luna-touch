import pytest
import numpy as np
from collections import OrderedDict
from scipy.spatial import distance

from luna_touch import touch_tracking
from luna_touch.Touch import Touch
from luna_touch import _const



##########################################################################################

@pytest.fixture
def prev_touches():


    prev_touches=OrderedDict()

    prev_touches[0] = Touch((300,300),   20)
    prev_touches[1] = Touch((400,400), 20)
    prev_touches[2] = Touch((500,500), 20)
    

    prev_touches[0].state = _const.TOUCH_STATE_BEGAN
    prev_touches[1].state = _const.TOUCH_STATE_STILL
    prev_touches[2].state = _const.TOUCH_STATE_MOVED

    prev_touches[0].id = 0
    prev_touches[1].id = 1
    prev_touches[2].id = 2

    return prev_touches

@pytest.fixture
def curr_touches():
    curr_touches = [
                    Touch((320,320), 20),
                    Touch((420,420), 20),
                    Touch((480,480), 20),
               ]

    curr_touches[0].state = _const.TOUCH_STATE_BEGAN
    curr_touches[1].state = _const.TOUCH_STATE_BEGAN
    curr_touches[2].state = _const.TOUCH_STATE_BEGAN
    

    curr_touches[0].id = 0
    curr_touches[1].id = 0
    curr_touches[2].id = 0
    
    
    return  curr_touches

@pytest.fixture
def final_touches():
               
    final_touches=OrderedDict()

    final_touches[0] = Touch((320,320),   20)
    final_touches[1] = Touch((420,420), 20)
    final_touches[2] = Touch((480,480), 20)

    final_touches[0].state = _const.TOUCH_STATE_MOVED
    final_touches[1].state = _const.TOUCH_STATE_MOVED
    final_touches[2].state = _const.TOUCH_STATE_MOVED


    final_touches[0].id = 0
    final_touches[1].id = 1
    final_touches[2].id = 2


    return final_touches

def test_touch_tracking_for_moved_touches(prev_touches, curr_touches, final_touches):

    calculated_final_touches = touch_tracking.track_touches_changes( prev_touches, curr_touches )

    set_de_id_en_final_touch = set( (touch.id) for touch in list(final_touches.values()) )

    difference = [ touch for touch in list(calculated_final_touches.values()) if (touch.id) not in set_de_id_en_final_touch ]

    assert difference == []
