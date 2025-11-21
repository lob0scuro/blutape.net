from flask import Blueprint, jsonify, request, current_app
from app.extensions import db
from flask_login import current_user
from app.models import Machines, Notes
from datetime import datetime, timezone

create_bp = Blueprint("create", __name__)