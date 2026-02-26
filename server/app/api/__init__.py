from flask import Blueprint
from .auth import auth_bp
from .create import create_bp
from .delete import delete_bp
from .read import read_bp
from .update import update_bp
from .export import export_bp
from .print import print_bp


api_bp = Blueprint("api", __name__, url_prefix="/api")


api_bp.register_blueprint(auth_bp, url_prefix="/auth")
api_bp.register_blueprint(create_bp, url_prefix="/create")
api_bp.register_blueprint(delete_bp, url_prefix="/delete")
api_bp.register_blueprint(read_bp, url_prefix="/read")
api_bp.register_blueprint(update_bp, url_prefix="/update")
api_bp.register_blueprint(export_bp, url_prefix="/export")
api_bp.register_blueprint(print_bp, url_prefix="/print")
