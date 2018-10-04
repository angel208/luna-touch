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
    prev_touches = []

    return prev_touches

@pytest.fixture
def curr_touches():
    curr_touches = [      
                    Touch((600,600), 20)
               ]

    curr_touches[0].state = _const.TOUCH_STATE_BEGAN

    curr_touches[0].id = 0

    return  curr_touches

@pytest.fixture
def missing_touches():
    missing_touches = []

   
    return  missing_touches

@pytest.fixture
def final_touches():
    final_touches=OrderedDict()

    final_touches[0] = Touch((600,600),   20)
    

    final_touches[0].state = _const.TOUCH_STATE_BEGAN

    final_touches[0].id = 0
    

    return final_touches

def test_touch_tracking_for_new_touches(prev_touches, curr_touches, final_touches):

    calculated_final_touches = touch_tracking.track_touches_changes( prev_touches, curr_touches )

    set_de_id_en_final_touch = set( (touch.id) for touch in list(final_touches.values()) )

    difference = [ touch for touch in list(calculated_final_touches.values()) if (touch.id) not in set_de_id_en_final_touch ]

    assert difference == []
