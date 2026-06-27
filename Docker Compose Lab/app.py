import os
import socket
from flask import Flask
from redis import Redis, RedisError

app = Flask(__name__)

# "redis" is the SERVICE NAME from compose.yaml.
# Docker's embedded DNS on the user-defined network resolves it
# to the redis container's IP — no hard-coded host needed.
redis = Redis(host="redis", port=6379, socket_connect_timeout=2)


@app.route("/")
def hello():
    try:
        visits = redis.incr("counter")
    except RedisError:
        # Back-end is down? Still serve the page so the demo keeps working.
        visits = "<i>could not connect to Redis, counter disabled</i>"

    html = (
        "<h3>Hello {name}!</h3>"
        "<b>Hostname:</b> {hostname}<br/>"
        "<b>Visits:</b> {visits}"
    )
    return html.format(
        name=os.getenv("NAME", "world"),
        hostname=socket.gethostname(),
        visits=visits,
    )


if __name__ == "__main__":
    # Bind to 0.0.0.0 so the container's port 80 is reachable from the host.
    app.run(host="0.0.0.0", port=80)