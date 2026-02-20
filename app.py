import json
import os
from datetime import datetime, timedelta, timezone

import bcrypt
import requests
from dotenv import load_dotenv
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
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from requests.sessions import Request

# Load .env
load_dotenv()

# .env Variable
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")


def get_client():
    # URI ke Atlas
    atlas_uri = f"mongodb+srv://{DB_USER}:{DB_PASSWORD}{DB_HOST}"

    # Coba Atlas dulu
    try:
        client = MongoClient(atlas_uri, server_api=ServerApi("1"))
        client.admin.command("ping")  # test koneksi
        return client
    except Exception as e:
        print(f"Gagal connect Atlas: {e}")


# Client aktif
client = get_client()


# Database
def use_db():
    return client["SegarArcheryDB"]


# Collection
collection = use_db()
userData = collection["coaches"]

app = Flask(__name__)


# Respon API
def respon_api(status, code, message, data, pagination):
    respon = {
        "status": status,
        "code": code,
        "message": message,
        "data": data if data else [],
        "pagination": pagination if pagination else {},
    }
    return jsonify(respon)


# Coach Login
@app.route("/api/coach/login", methods=["POST", "GET"])
def coachLogin():
    try:
        if request.method == "POST":
            data = request.json
            username = str(data.get("username"))
            password = data.get("password")

            # Check Account
            account = userData.find_one({"username": username})

            if account:
                dbpw = account["password"]
                dbpw = dbpw.encode("utf-8")
                encodepw = password.encode("utf-8")

                valid = bcrypt.checkpw(encodepw, dbpw)
                if valid:
                    return respon_api("success", 200, "Sukses", [], {})
                else:
                    return respon_api("failed", 404, "Tetot", [], {}), 404

            else:
                return respon_api("failed", 404, "Account not found", [], {}), 404
        else:
            return respon_api("error", 400, "Req Method not POST", [], {}), 400

    except Exception as error:
        return respon_api("error", 500, str(error), [], {}), 500


# Home pages
@app.route("/coach")
def coach():
    return render_template("coach/index.html")


@app.route("/")
def home():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
