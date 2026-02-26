from flask import Blueprint, jsonify, request, render_template, session, flash, redirect, url_for, current_app, abort
from itsdangerous import TimestampSigner, BadSignature, SignatureExpired
from datetime import datetime, timedelta, timezone
from pymongo import ReturnDocument
from functools import wraps
from markupsafe import escape
from database import mongodb
from bson.objectid import ObjectId
import bcrypt, math, pytz

# Atur route
pages_route = Blueprint("pages", __name__)

# Route
@pages_route.route("/coach")
def coach():
    if "user_id" in session:
        return redirect (url_for("pages.dashboard"))
    else:
        return render_template("coach/index.html")

@pages_route.route("/coach/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect (url_for("pages.coach"))
    else:
        return render_template("coach/dashboard.html", nama_coach = session["name"], username_coach = session["username"])