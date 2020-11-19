from flask import Flask, jsonify, request
import simplejson as json
from flask_sse import sse
import logging
from apscheduler.schedulers.background import BackgroundScheduler
from flask_cors import CORS
import datetime

from helper import get_data, get_schd_time

app = Flask(__name__)
CORS(app)
app.config["REDIS_URL"] = "redis://localhost"
app.register_blueprint(sse, url_prefix='/events')
log = logging.getLogger('apscheduler.executors.default')
log.setLevel(logging.INFO)
fmt = logging.Formatter('%(levelname)s:%(name)s:%(message)s')
h = logging.StreamHandler()
h.setFormatter(fmt)
log.addHandler(h)


def server_side_event(scheduled=True, supplierID=None):
    """ Function to publish server side event """
    with app.app_context():
        sse.publish(next(get_data()), type='newOrder', channel=f"supplierID_{supplierID}")
        if scheduled:
            print("Event Scheduled at ", datetime.datetime.now())
        else:
            print(f"Event triggered for channel=supplierID_{supplierID} at ", datetime.datetime.now())


# sched = BackgroundScheduler(daemon=True)
# sched.add_job(server_side_event,'interval',seconds=get_schd_time())
# sched.start()


@app.route('/')
def index():
    return jsonify(next(get_data()))


@app.route('/send-data', methods=['POST'])
def send_data():
    data = request.get_json()
    supplierID = data.get('supplierID')
    server_side_event(scheduled=False, supplierID=supplierID)
    return f"Sent event to {supplierID=}", 200


if __name__ == '__main__':
   app.run(debug=True, port=5001)