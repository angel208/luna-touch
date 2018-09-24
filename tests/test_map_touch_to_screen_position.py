import pytest
import numpy as np

from luna_touch import touch_detect
from luna_touch.Touch import Touch
from luna_touch import _const


@pytest.fixture
def points_from_camera_perspective():
    
    points_from_camera_perspective = np.array([[294, 400],[261, 155],[92, 178],[125, 425] ], np.int32)
    return points_from_camera_perspective


@pytest.fixture
def touch_position():

    touch_position = ( 125 , 425 )
    return  touch_position

@pytest.mark.parametrize("test_points, maped_points", [

    (( 125 , 425 ), ( 0 , 0 )),
    (( 92  , 178 ), ( 0 , 767 )),
    (( 261 , 155 ), ( 1365, 767 )),
    (( 294 , 400 ), ( 1365, 0 )),
    (( 72  , 178 ), ( 0 , 775)),
    (( 294 , 420 ), ( 1343 , 0 )),
    
])

def test_touch_mapping_to_screen_coordinates(points_from_camera_perspective, test_points, maped_points):

    transform_matrix = touch_detect.get_transform_matrix( original_points = points_from_camera_perspective, resolution_max_width = 1366, resolution_max_heigth = 768)
   
    mapped_point = touch_detect.map_touch_position_to_screen_coordinate( test_points , transform_matrix )    
    
    assert mapped_point == maped_points

