from flask import jsonify, request, Blueprint, current_app
from app.extensions import db
from flask_login import current_user
from app.models import Machines, Users
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


@update_bp.route("/update/<int:id>", methods=["PATCH"])
def update_machine(id):
    data = request.get_json() or {}
    machine = Machines.query.get(id)

    if not machine:
        return jsonify(success=False, message="Machine not found"), 404

    try:
        for field in UPDATABLE_FIELDS:
            if field in data and data[field] is not None:
                value = data[field]

                # Strip strings only
                if isinstance(value, str):
                    value = value.strip()

                setattr(machine, field, value)

        db.session.commit()
        current_app.logger.info(f"[MACHINE UPDATED] User {current_user.id} updated machine {id}")
        return jsonify(success=True, machine=machine.serialize(), message="machine status updated!"), 200

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"[MACHINE UPDATE ERROR]: {e}")
        return jsonify(success=False, message="Failed to update machine"), 500