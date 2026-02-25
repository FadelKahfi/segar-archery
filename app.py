import json

from datetime import datetime, timedelta, timezone

import bcrypt
import requests
from flask import (
    Flask,
    jsonify,
    redirect,
    render_template,
    request,
    send_from_directory,
    session,
    url_for,
)

app = Flask(__name__)

from routes.api_route import api_route
from routes.pages_route import pages_route

# Blueprint
app.register_blueprint(api_route, url_prefix="/api/")
app.register_blueprint(pages_route, url_prefix="/pages/")

# Home pages
@app.route("/")
def home():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
