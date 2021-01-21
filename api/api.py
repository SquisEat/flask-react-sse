import os
import random
import sys

from flask import Flask, jsonify, request, abort, g, Response, redirect
import simplejson as json
from flask_sse import sse
import logging
from flask_cors import CORS
import datetime
from flask_login import current_user, LoginManager, UserMixin, login_required, logout_user, login_user

sys.path.append(os.path.join(os.path.dirname(__file__), '../'))


app = Flask(__name__)
CORS(app, support_credentials=True)
app.config["REDIS_URL"] = "redis://localhost"

log = app.logger
log.setLevel(logging.DEBUG)
fmt = logging.Formatter('%(levelname)s:%(name)s:%(message)s')
h = logging.StreamHandler()
h.setFormatter(fmt)
log.addHandler(h)

# config
app.config.update(
    DEBUG=True,
    SECRET_KEY='secret_xxx',
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_SAMESITE='None',
    CORS_ORIGINS=['http://127.0.0.1:3000', 'http://localhost:3000']
)

# flask-login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


app.register_blueprint(sse, url_prefix="/events")


# silly user model
class User(UserMixin):

    def __init__(self, id):
        self.id = id
        self.name = "user" + str(id)
        self.password = "password"

    def __repr__(self):
        return "%d/%s/%s" % (self.id, self.name, self.password)


# create some users with ids 1 to 20
users = [User(id) for id in range(1, 20)]


@app.route('/')
def index():
    if current_user.is_authenticated:
        return jsonify(f"user authenticated = {current_user.name}")
    return jsonify("User non authenticated")


@app.route('/send-data', methods=['POST'])
def send_data():
    supplierID = random.choice(users).id
    # supplierID = 1
    from server_side_event import server_side_event
    from helper import get_data
    server_side_event(supplierID=supplierID, data=next(get_data()))
    return f"Sent event to supplierID={supplierID}", 200


# somewhere to login
@app.route("/login", methods=["GET", "POST"])
def login():
    global users
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if password == "password":
            id = str(username).replace("user", "")
            user = User(id)
            assert user in users
            login_user(user, remember=True)
            return redirect(request.args.get("next"))
        else:
            return abort(401)
    else:
        return Response('''
        <form action="" method="post">
            <p><input type=text name=username>
            <p><input type=password name=password>
            <p><input type=submit value=Login>
        </form>
        ''')


# somewhere to logout
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return Response('<p>Logged out</p>')


# handle login failed
@login_manager.unauthorized_handler
def page_not_found():
    return Response('<p>Login failed</p>', status=401)


# callback to reload the user object
@login_manager.user_loader
def load_user(userid):
    if userid is not None:
        user = User(userid)
        if user in users:
            return user
    return None


if __name__ == '__main__':
    app.run(debug=True, port=5000)
