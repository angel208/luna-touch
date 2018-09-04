import pytest
import numpy as np

from luna_touch import calibration


## PARAMETRIZED
@pytest.mark.parametrize("calibration_frame, result_distance", [

    (np.loadtxt("../tests/distance_test_images/test-frame-1.txt"), 1097),
    (np.loadtxt("../tests/distance_test_images/test-frame-2.txt"), 1097),
    (np.loadtxt("../tests/distance_test_images/test-frame-3.txt"), 1114),
    (np.loadtxt("../tests/distance_test_images/test-frame-4.txt"), 1133),
    
])

def test_distance_calculation_from_calibration_frame(calibration_frame, result_distance):
    assert calibration.find_most_ocurring_pixel_value( calibration_frame ) == result_distance


