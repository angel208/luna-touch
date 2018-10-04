from luna_touch import touch_detect, calibration, _const
from luna_touch.RedisQueue import RedisQueue
import queue

if __name__ == '__main__':
    print("hi")
    surface_model = calibration.run_calibration_process()
    event_queue = RedisQueue( _const.QUEUE_NAME )
    touch_detect.start_detection_service(surface_model, event_queue)