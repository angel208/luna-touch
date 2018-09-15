from luna_touch import touch_detect, calibration
from flask import Flask

app = Flask(__name__)

surface_model = calibration.run_calibration_process()

#this should go in a thread
touch_detect.start_detection_service( surface_model )

#API DEFINITIONS:   

#@app.route('/touch', methods=['GET', 'POST'])
@app.route('/touch')
def hello_world():
    return 'Hello, World!'

@app.route('/touch/<idx>')
def hello_world2(idx):
    # show the user profile for that user
    return 'User %s' % idx






#RUN WEB SERVER
if __name__ == '__main__':
    app.run(threaded=True,port=5001)