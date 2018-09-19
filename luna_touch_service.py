from luna_touch import touch_detect, calibration
from flask import Flask, jsonify
import queue
import threading
from collections import OrderedDict

from luna_touch.Touch import Touch

app = Flask(__name__)

surface_model = calibration.run_calibration_process()

#this should go in a thread
#touch_detect.start_detection_service( surface_model )
event_queue = queue.Queue( maxsize = 30 )

threading.Thread(target=touch_detect.start_detection_service, args=(surface_model , event_queue ,) ).start()

#API DEFINITIONS:   


@app.route('/touches')
def get_touches():

    
    if ( event_queue.qsize() > 1 ):
        touches = event_queue.get_nowait()
        touches_list = [ touch.__dict__ for touch in list(touches.values()) ]
        response_data = jsonify({ 'count' : len(touches), 'touches' : touches_list })
        return  response_data, 200
    elif  (event_queue.qsize() == 1 ):
        touches = event_queue.queue[0]
        touches_list = [ touch.__dict__ for touch in list(touches.values()) ]
        response_data = jsonify({ 'count' : len(touches), 'touches' : touches_list })
        return  response_data, 200
    else:
        touches = []
        response_data = jsonify({ 'count' : len(touches), 'touches' : touches })
        return response_data , 200

    return "unexpected error", 500

@app.route('/touches/<touch_id>')
def get_touch(touch_id):
    
    

    return "unexpected error", 500


#RUN WEB SERVER
if __name__ == '__main__':
    app.run(threaded=True,port=5001)