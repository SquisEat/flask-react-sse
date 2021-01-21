import os
import sys

from gevent.pywsgi import WSGIServer
sys.path.append(os.path.join(os.path.dirname(__file__), '../'))

from api import app

app.debug = True

http_server = WSGIServer(('localhost', 5000), app).serve_forever()