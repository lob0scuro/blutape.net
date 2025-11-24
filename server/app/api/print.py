from flask import jsonify, request, Blueprint, current_app
from app.extensions import db
from flask_login import current_user
from app.models import Machines, Notes, Users
from datetime import datetime, timezone

print_bp = Blueprint("print", __name__)

@print_bp.route("/metrics/<int:id>", methods=["GET"])
def print_metrics():
    user = Users.query.get(id)
    if not user:
        return jsonify(success=False, message="User not found."), 404
    
    statuses = request.args.getlist("stats") #?status=in_progress&status=completed ...
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")
    date_column = request.args.get("date_column", "started_on")
    
    metrics = user.stats(
        statuses=statuses or None,
        start_date=start_date,
        end_date=end_date,
        date_column=date_column
    )
    
    HTML = """
    <body>
        <div>
        </div>
    </body>
    """
    
    
    