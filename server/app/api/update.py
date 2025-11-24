from flask import jsonify, request, Blueprint, current_app
from app.extensions import db
from flask_login import current_user
from app.models import Machines, Users, MachineStatusHistory
from datetime import datetime, timezone

update_bp = Blueprint("update", __name__)

UPDATABLE_FIELDS = [
    "brand",
    "type_of",
    "model",
    "serial",
    "style",
    "color",
    "condition",
    "vendor",
    "status",
]

STATUS_FIELD_MAP = {
        "completed": "completed_on",
        "trashed": "trashed_on",
        "exported": "exported_on",
        "in_progress": "started_on"
    }
        
def update_machine_status(machine: Machines, new_status: str):
    if machine.status == new_status:
        return
    
    old_status = machine.status
    machine.status = new_status
    
    today = datetime.today().date()
    
    
    field_name = STATUS_FIELD_MAP.get(new_status)
    if field_name:
        setattr(machine, field_name, today)
        
    history = MachineStatusHistory(
        machine=machine,
        status=new_status,
        prev_status=old_status,
        changed_on=today,
        changed_by=getattr(current_user, "id", None)
    )
    db.session.add(history)


@update_bp.route("/update/<int:id>", methods=["PATCH"])
def update_machine(id):
    data = request.get_json() or {}
    machine = Machines.query.get(id)

    if not machine:
        return jsonify(success=False, message="Machine not found"), 404

    try:
        for field in UPDATABLE_FIELDS:
            if field == "status": 
                continue
            if field in data and data[field] is not None:
                value = data[field]

                # Strip strings only
                if isinstance(value, str):
                    value = value.strip()

                setattr(machine, field, value)
                
        if 'status' in data and data["status"]:
            update_machine_status(machine, data["status"])

        db.session.commit()
        current_app.logger.info(f"[MACHINE UPDATED] User {current_user.id} updated machine {id}")
        return jsonify(success=True, machine=machine.serialize(), message="machine status updated!"), 200

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"[MACHINE UPDATE ERROR]: {e}")
        return jsonify(success=False, message="Failed to update machine"), 500