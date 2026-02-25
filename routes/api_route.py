from flask import Blueprint, jsonify, request, render_template, session, flash, redirect, url_for, current_app, abort
from itsdangerous import TimestampSigner, BadSignature, SignatureExpired
from datetime import datetime, timedelta, timezone
from pymongo import ReturnDocument
from functools import wraps
from markupsafe import escape
from database import mongodb
from bson.objectid import ObjectId
import bcrypt, math, pytz

# API
# Convert _id
def convert_objectid_to_str(doc):
    if isinstance(doc, ObjectId):
        return str(doc)
    elif isinstance(doc, dict):
        return {k: convert_objectid_to_str(v) for k, v in doc.items()}
    elif isinstance(doc, list):
        return [convert_objectid_to_str(i) for i in doc]
    elif isinstance(doc, str):  
        # sanitasi string dengan escape
        return escape(doc)
    else:
        return doc

# Respon API
def respon_api(status, code, message, data, pagination):
    respon = {
        "status": status,
        "code": code,
        "message": message,
        "data": data if data else [],
        "pagination": pagination if pagination else {}
    }
    return jsonify(respon)

# Atur route
api_route = Blueprint("api", __name__)

# Collection
collection = mongodb.use_db()
userData = collection["coaches"]

# Coach Login
@api_route.route("/coach/login", methods=["POST", "GET"])
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