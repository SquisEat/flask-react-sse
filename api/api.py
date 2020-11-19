from flask import Flask, jsonify, request, abort, g, Response, redirect
import simplejson as json
from flask_sse import sse
import logging
from flask_cors import CORS
import datetime
from flask_login import current_user, LoginManager, UserMixin, login_required, logout_user, login_user

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

# config
app.config.update(
    DEBUG=True,
    SECRET_KEY='secret_xxx'
)

# flask-login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


# silly user model
class User(UserMixin):

    def __init__(self, id):
        self.id = id
        self.name = "user" + str(id)
        self.password = "password"

    def __repr__(self):
        return "%d/%s/%s" % (self.id, self.name, self.password)


# create some users with ids 1 to 20
users = [User(id) for id in range(1, 21)]


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

@sse.before_request
def check_access():
    if not current_user.is_authenticated:
        abort(403)
    if request.args.get('channel').replace('supplierID_') != current_user.id:
        abort(403)


@app.route('/')
def index():
    return jsonify(next(get_data()))


@app.route('/send-data', methods=['POST'])
@login_required
def send_data():
    if not current_user.is_authenticated:
        abort(401)
    supplierID = current_user.id
    server_side_event(scheduled=False, supplierID=supplierID)
    return f"Sent event to {supplierID=}", 200


# somewhere to login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if password == "password":
            id = str(username).replace("user", "")
            user = User(id)
            login_user(user)
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
@app.errorhandler(401)
def page_not_found(e):
    return Response('<p>Login failed</p>')


# callback to reload the user object
@login_manager.user_loader
def load_user(userid):
    return User(userid)


if __name__ == '__main__':
   app.run(debug=True, port=5001)