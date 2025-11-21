from flask import jsonify, request, Blueprint, current_app
from app.extensions import db
from flask_login import current_user
from app.models import Machines, Users
from datetime import datetime, timezone

update_bp = Blueprint("update", __name__)