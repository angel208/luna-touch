from luna_touch import touch_detect, calibration, _const
from luna_touch.RedisQueue import RedisQueue
import queue

from subprocess import call

if __name__ == '__main__':
    print("hi")
    surface_model = calibration.run_calibration_process()

    #call(["node", "./luna_touch_web_server/luna_touch_web_server.js"]) 
    
    event_queue = RedisQueue( _const.QUEUE_NAME )
    touch_detect.start_detection_service(surface_model, event_queue)