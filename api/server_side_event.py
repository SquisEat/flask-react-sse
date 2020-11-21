import datetime

from flask_sse import sse

from api import app
from helper import get_data


def server_side_event(scheduled=True, supplierID=None):
    """ Function to publish server side event """
    with app.app_context():
        channel = f"supplierID_{supplierID}"
        print(channel)
        sse.publish(next(get_data()), type='newOrder', channel=channel)
        if scheduled:
            print("Event Scheduled at ", datetime.datetime.now())
        else:
            print(f"Event triggered for channel=supplierID_{supplierID} at ", datetime.datetime.now())