from flask import jsonify, request, Blueprint, current_app
from app.extensions import db
from flask_login import current_user, login_required
from app.models import Machines, Notes, Users
from datetime import datetime, timezone

read_bp = Blueprint("read", __name__)


#--------------------
#    USER QUERY
#--------------------
@read_bp.route("user/<int:id>", methods=["GET"])
def get_user(id):
    try:
        user = Users.query.get(id)
        if not user:
            return jsonify(success=False, message=f"User with id {id} not found"), 404
        return jsonify(success=True, user=user.serialize()), 200
    except Exception as e:
        current_app.logger.error(f"[USER QUERY ERROR]: {e}")
        return jsonify(success=False, message=f"There was an erro when querying for user {id}"), 500

@read_bp.route("users", methods=["GET"])
def get_users():
    try:
        users = Users.query.all()
        return jsonify(success=True, users=[u.serialize() for u in users]), 200
    except Exception as e:
        current_app.logger.error(f"[USER QUERY ERROR]: {e}")
        return jsonify(success=False, message="Something went wrong when querying for users"), 500


#--------------------
#    MACHINE QUERY
#--------------------
@read_bp.route("/machine/<int:id>", methods=["GET"])
def get_machine(id):
    try:
        machine = Machines.query.get(id)
        if not machine:
            return jsonify(success=False, message=f"Machine with id {id} not found"), 404
        return jsonify(success=True, machine=machine.serialize()), 200
    except Exception as e:
        current_app.logger.error(f"[MACHINE QUERY ERROR]: {e}")
        return jsonify(success=False, message=f"Something went wrong when querying for machine with id {id}"), 500

@read_bp.route("/machines", methods=["GET"])
def get_machines():
    try:
        user_id = request.args.get("user_id", type=int)
        status = request.args.get("status")
        page = request.args.get("page", 1, type=int)
        per_page = 8
        
        query = Machines.query
        
        if user_id:
            query = query.filter_by(technician_id=user_id)
        if status:
            query = query.filter_by(status=status)
            
        query = query.order_by(Machines.started_on.desc())
        
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        machines = pagination.items
        
        return jsonify(
            success=True, 
            machines=[m.serialize() for m in machines], 
            page=page, 
            total_pages=pagination.pages, 
            total_items=pagination.total
            ), 200
        
    except Exception as e:
        current_app.logger.error(f"[MACHINE QUERY ERROR]: {e}")
        return jsonify(success=False, message="There was an error when querying for machines"), 500
    
@read_bp.route("/serial/<serial>", methods=["GET"])
def serial_search(serial):
    try:
        machine = Machines.query.filter_by(serial=serial.strip().upper()).first()
        if not machine:
            return jsonify(success=False, message="Machine not found."), 404
        return jsonify(success=True, machine=machine.serialize()), 200
    except Exception as e:
        current_app.logger.error(f"[SERIAL SEARCH ERROR]: {e}")
        return jsonify(success=False, message="There was an error when searching for machine by serial number"), 500
    
    
    
    
#--------------------
#    USER METRICS
#--------------------

@read_bp.route("/metrics/<int:id>", methods=["GET"])
def user_metrics(id):
    user = Users.query.get(id)
    if not user:
        return jsonify(success=False, message="User not found."), 404
    
    statuses = request.args.getlist("stats") #?status=in_progress&status=completed ...
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")
    date_column = request.args.get("date_column", "started_on")
    
    stats = user.stats(
        statuses=statuses or None,
        start_date=start_date,
        end_date=end_date,
        date_column=date_column,  
    )
    
    return jsonify(success=True, metrics=stats, user=f"{user.first_name} {user.last_name}" if user else None), 200


#--------------------
#    EXPORT MACHINES
#--------------------
@read_bp.route("/export", methods=["GET"])
@login_required
def export_list():
    try:
        machines = Machines.query.filter_by(status="completed").all()
        if not machines:
            return jsonify(success=True, message="No machines to export"), 200
        return jsonify(success=True, machines=[m.serialize() for m in machines]), 200
    except Exception as e:
        current_app.logger.error(f"[MACHINE EXPORT ERROR]: {e}")
        return jsonify(success=False, message="There was an error when getting Export list"), 500