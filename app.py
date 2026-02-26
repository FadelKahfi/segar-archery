import json

from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
import os
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

# Load .env
load_dotenv()

# .env Variable
SESSION_KEY = os.getenv("SECRET_KEY")

app = Flask(__name__)
app.secret_key = SESSION_KEY
app.permanent_session_lifetime = timedelta(days=30)

@app.before_request
def cek_masa_sesi():
  kedaluwarsa = session.get("kedaluwarsa")
  
  if kedaluwarsa:
    waktu_sekarang = datetime.now(timezone.utc)
    waktu_kedaluwarsa = datetime.fromisoformat(kedaluwarsa)

    if waktu_sekarang > waktu_kedaluwarsa:
        session.clear()
        redirect(url_for("pages_route.coach"))

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
