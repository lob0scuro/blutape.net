from flask import jsonify, current_app, Blueprint, request
from app.extensions import db
from app.models import Machines
from flask_login import login_required, current_user
import pandas as pd
from io import BytesIO
from flask_mailman import EmailMessage


export_bp = Blueprint("export", __name__)