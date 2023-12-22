from flask import (
    Blueprint,
    Flask,
    render_template,
    send_from_directory,
)
import os

import redis
from flask_socketio import SocketIO, join_room, leave_room, emit

from flask_session import Session

app = Flask(__name__)

# Redis for managing sessions - To Test if necessary.
app.config["SECRET_KEY"] = "vnkdjnfjknfl1232#"
app.config["SESSION_TYPE"] = "redis"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_USE_SIGNER"] = True
app.config["SESSION_REDIS"] = redis.from_url(
    "redis://10.216.93.243:6379"
)  # IP is not public

angular = Blueprint("angular", __name__, template_folder="angular/dist/angular")
app.register_blueprint(angular)

Session(app)
socketio = SocketIO(
    app,
    manage_session=False,
    cors_allowed_origins="*",
    message_queue="redis://10.216.93.243:6379",
)


@app.route("/assets/<path:filename>")
def custom_static_for_assets(filename):
    return send_from_directory("angular/dist/angular/assets", filename)


@app.route("/<path:filename>")
def custom_static(filename):
    return send_from_directory("angular/dist/angular/", filename)


@app.route("/")
def index():
    return render_template("index.html")


@socketio.on("join", namespace="/chat")
def join(message):
    join_room(message["room"])
    emit("status", {"msg": "you have entered the room."}, room=message["room"])


@socketio.on("text", namespace="/chat")
def text(message):
    emit("message", {"msg": message["msg"]}, room=message["room"])


@socketio.on("left", namespace="/chat")
def left(message):
    leave_room(message["room"])
    emit("status", {"msg": "You have left the room."}, room=message["room"])


if __name__ == "__main__":
    from flask_cors import CORS

    CORS(app)
    # socketio.run(app, host="127.0.0.1", port=8080, debug=True) #LOCAL
    socketio.run(
        app, host="0.0.0.0", port=int(os.environ.get("PORT", 8080))
    )  # Cloud run
