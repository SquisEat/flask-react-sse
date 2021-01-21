import datetime

from flask_sse import sse

from api import app


def server_side_event(type='newOrder', supplierID=None, data=None):
    """ Function to publish server side event """
    with app.app_context():
        channel = f"supplierID_{supplierID}"
        app.logger.info(f"Publishing to channel={channel}, data={data}")
        sse.publish(data, type='newOrder', channel=channel)
        # logger.info("Sending server-side-event of {type=} to {supplierID=} on channel={channel=} "
        #            "with {data=} ")