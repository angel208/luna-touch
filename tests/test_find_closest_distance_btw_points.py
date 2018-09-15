import pytest
import numpy as np
from collections import OrderedDict
from scipy.spatial import distance

from luna_touch import touch_tracking
from luna_touch.Touch import Touch
from luna_touch import _const


@pytest.fixture
def curr_touches():
    touches = OrderedDict()
    touches[0] = Touch((1,1), 0)
    touches[1] = Touch((1,1), 1)
    touches[2] = Touch((1,1), 2)
    touches[3] = Touch((1,1), 3)
    touches[4] = Touch((1,1), 4)
 
    
    touches[1].state = _const.TOUCH_STATE_ENDED
    touches[3].state = _const.TOUCH_STATE_ENDED

    return touches

@pytest.fixture
def not_ended_touches():

    not_ended_touches = OrderedDict()
    not_ended_touches[0] = Touch((1,1), 0)
    not_ended_touches[2] = Touch((1,1), 2)
    not_ended_touches[4] = Touch((1,1), 4)

    return  not_ended_touches

def test_not_ended_touches(curr_touches, not_ended_touches):

    set_de_radio_en_lista_final = set( (touch.area) for touch in list(not_ended_touches.values()) )

    not_ended_touches = touch_tracking.not_ended_touches( curr_touches )

    difference = [ touch for touch in  list(not_ended_touches.values()) if (touch.area) not in set_de_radio_en_lista_final ]
 
    assert difference == []


#########################################################33

@pytest.fixture
def touches():
    touches = OrderedDict()
    touches[0] = Touch((1,1),20)
    touches[1] = Touch((2,2),20)
    touches[3] = Touch ((2,2), 20)
    touches[5] = Touch ((2,2), 20)

    return touches


def test_get_next_available_id(touches):

   
    assert touch_tracking.get_next_available_id(touches) == 2


############################################################

@pytest.fixture
def prev_touches_dist_test():
    previous_frame_touches=OrderedDict()

    previous_frame_touches[0] = Touch((1,1), 30)
    previous_frame_touches[1] = Touch((20,20), 20)
    previous_frame_touches[2] = Touch((50,50), 67)
    previous_frame_touches[3] = Touch((200,200), 30)


    previous_frame_touches[0].id = 0
    previous_frame_touches[1].id = 1
    previous_frame_touches[2].id = 2
    previous_frame_touches[3].id = 3

    return previous_frame_touches

@pytest.fixture
def curr_touches_dist_test():
    curr_touches = [
                    Touch((3,3), 20),
                    Touch((20,20), 67),
                    Touch((2,2), 30)                    
               ]

    return  curr_touches

@pytest.fixture
def result_matrix_dist_test():
    result_matrix = [
                        {'id': 1,  'prev_pos': (20, 20), 'curr_pos': (20, 20), 'distance': 0},
                        {'id': 0,  'prev_pos': (1, 1),'curr_pos': (2, 2), 'distance': 1},
                        {'id': 2,  'prev_pos': (50, 50),'curr_pos': None, 'distance': None},
                        {'id': 3,  'prev_pos': (200, 200),'curr_pos': None, 'distance': None},
                        {'id': None,  'prev_pos': None,'curr_pos': (3,3), 'distance': None, 'prev_index': 0}
                    ]

    return  result_matrix

def test_find_closest_distance_btw_points(prev_touches_dist_test, curr_touches_dist_test, result_matrix_dist_test ):

    distance_matrix = touch_tracking.find_min_distance_btw_points( prev_touches_dist_test, curr_touches_dist_test)



    np.testing.assert_array_equal(distance_matrix, result_matrix_dist_test)
