from flask import request, jsonify, current_app, Blueprint
import socket
import requests
from flask_login import current_user

labels_bp = Blueprint("labels", __name__)