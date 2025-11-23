from flask import jsonify, request, Blueprint, current_app
from app.extensions import db
from flask_login import current_user
from app.models import Machines, Notes

delete_bp = Blueprint("delete", __name__)

@delete_bp.route("/delete/<int:id>", methods=["DELETE"])
def delete_machine(id):
    machine = Machines.query.get(id)
    if not machine:
        return jsonify(success=False, message=f"Machine with ID {id} not found"), 404
    db.session.delete(machine)
    return jsonify(success=True, message="Machine has been deleted."), 200

@delete_bp.route("/delete_note/<int:id>", methods=["DELETE"])
def delete_note(id):
    note = Notes.query.get(id)
    if not note:
        return jsonify(success=False, message="There was an error when deleting note."), 404
    return jsonify(success=True, message="Note has been removed."), 200