from flask import jsonify, request, Blueprint, current_app
from app.extensions import db
from flask_login import current_user
from app.models import Machines, Notes, Users
from datetime import datetime, timezone

read_bp = Blueprint("read", __name__)