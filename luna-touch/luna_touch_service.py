from luna_touch import touch_detect, calibration
from flask import Flask, jsonify, request
import queue
import threading
import multiprocessing as mp
from collections import OrderedDict
import time
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import subprocess, sys


from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

from luna_touch.Touch import Touch

app = Flask(__name__)


#this should go in a thread
#touch_detect.start_detection_service( surface_model )
event_queue = queue.Queue( maxsize = 30 )



#API DEFINITIONS:   

touch_state_dictionary = { 'began' : 1, 'ended': 2, 'still': 3, 'moved' : 4 , 'missed': 5 }


touches = [ Touch( (600,450),23 ), Touch( (23,43),23 ), Touch( (23,43),23 ) , Touch( (23,43),23 )   ]
touches[0].state = 1
touches[1].state = 2
touches[2].state = 2
touches[3].state = 3

@app.route('/touches')
def get_touches():

    state = request.args.get('state')
   
    if ( event_queue.qsize() > 1 ):
        #touches = event_queue.get_nowait()
        touches_list = touches
        response_data = touches_list
    elif  (event_queue.qsize() == 1 ):
        #touches = event_queue.queue[0]
        touches_list = touches
        response_data = touches_list 
    else:
        touches_list = []
        response_data = touches_list 

    if( state ):
        if state in touch_state_dictionary:
            state_code = touch_state_dictionary[state]
            response_data = jsonify([ touch.__dict__ for touch in  response_data if touch.state == state_code ])
            return  response_data, 200
        else:
            response_data = jsonify([])
            return  response_data, 200
    else:
        response_data = jsonify([ touch.__dict__ for touch in response_data ])
        return  response_data, 200


    return "unexpected error", 500

@app.route('/touches/<touch_id>')
def get_touch(touch_id):

    response_data = []
    
    if ( event_queue.qsize() > 0 ):
        touches = event_queue.queue[0]
        touches_list = list(touches.values())  
        response_data = jsonify([ touch.__dict__ for touch in  touches_list if str(touch.id) == touch_id ])
        return  response_data, 200
    else:
        touches_list = []
        response_data = touches_list 
        return  response_data, 200

    return "unexpected error", 500


#RUN WEB SERVER
if __name__ == '__main__':

    #surface_model = calibration.run_calibration_process()

    #t = threading.Thread(target=touch_detect.start_detection_service , args=( surface_model, event_queue, ) )
    #t.start()

    #p = subprocess.Popen([sys.executable, "detection_service.py"])
   
    http_server = HTTPServer(WSGIContainer(app))
    http_server.listen(5003)
    IOLoop.instance().start()
    #app.run(threaded=True,port=5003)




    