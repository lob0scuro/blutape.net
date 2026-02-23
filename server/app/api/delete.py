from datetime import date

from flask import Blueprint, jsonify
from flask_login import current_user, login_required

from app.extensions import db
from app.models import Machine, MachineNote, WorkOrder, WorkOrderEvent
from app.models.enums import EventEnum, EventReasonEnum, StatusEnum

delete_bp = Blueprint("delete", __name__)

@delete_bp.delete("/note/<int:note_id>")
@login_required
def delete_note(note_id):
    note = db.session.get(MachineNote, note_id)
    if not note:
        return jsonify(success=False, message="Note not found"), 404

    db.session.delete(note)
    try:
        db.session.commit()
        return jsonify(success=True, message="Note deleted"), 200
    except Exception as e:
        db.session.rollback()
        return jsonify(success=False, message=f"Failed to delete note: {e}"), 500


@delete_bp.patch("/machine/<int:machine_id>/archive")
@login_required
def archive_machine(machine_id):
    machine = db.session.get(Machine, machine_id)
    if not machine:
        return jsonify(success=False, message="Machine not found"), 404

    work_order = (
        db.session.query(WorkOrder)
        .filter_by(machine_id=machine.id)
        .order_by(WorkOrder.id.desc())
        .first()
    )
    if not work_order:
        return jsonify(success=False, message="Work order not found"), 404

    if work_order.current_status == StatusEnum.ARCHIVED:
        return jsonify(success=True, message="Machine is already archived"), 200

    previous_status = work_order.current_status
    work_order.current_status = StatusEnum.ARCHIVED
    work_order.archived_on = date.today()

    event = WorkOrderEvent(
        work_order_id=work_order.id,
        machine_id=machine.id,
        event_type=EventEnum.ARCHIVED,
        from_status=previous_status,
        to_status=StatusEnum.ARCHIVED,
        technician_id=current_user.id,
        reason=EventReasonEnum.DEFAULT,
    )
    db.session.add(event)

    try:
        db.session.commit()
        return jsonify(success=True, message="Machine archived"), 200
    except Exception as e:
        db.session.rollback()
        return jsonify(success=False, message=f"Failed to archive machine: {e}"), 500


@delete_bp.patch("/machine/<int:machine_id>/unarchive")
@login_required
def unarchive_machine(machine_id):
    machine = db.session.get(Machine, machine_id)
    if not machine:
        return jsonify(success=False, message="Machine not found"), 404

    work_order = (
        db.session.query(WorkOrder)
        .filter_by(machine_id=machine.id)
        .order_by(WorkOrder.id.desc())
        .first()
    )
    if not work_order:
        return jsonify(success=False, message="Work order not found"), 404

    if work_order.current_status != StatusEnum.ARCHIVED:
        return jsonify(success=False, message="Machine is not archived"), 400

    work_order.current_status = StatusEnum.IN_PROGRESS
    work_order.archived_on = None

    event = WorkOrderEvent(
        work_order_id=work_order.id,
        machine_id=machine.id,
        event_type=EventEnum.UNARCHIVED,
        from_status=StatusEnum.ARCHIVED,
        to_status=StatusEnum.IN_PROGRESS,
        technician_id=current_user.id,
        reason=EventReasonEnum.DEFAULT,
    )
    db.session.add(event)

    try:
        db.session.commit()
        return jsonify(success=True, message="Machine unarchived"), 200
    except Exception as e:
        db.session.rollback()
        return jsonify(success=False, message=f"Failed to unarchive machine: {e}"), 500


@delete_bp.delete("/work_order/<int:work_order_id>")
@login_required
def delete_work_order(work_order_id):
    work_order = db.session.get(WorkOrder, work_order_id)
    if not work_order:
        return jsonify(success=False, message="Work order not found"), 404

    db.session.delete(work_order)
    try:
        db.session.commit()
        return jsonify(success=True, message="Work order deleted"), 200
    except Exception as e:
        db.session.rollback()
        return jsonify(success=False, message=f"Failed to delete work order: {e}"), 500


@delete_bp.delete("/machine/<int:machine_id>")
@login_required
def delete_machine(machine_id):
    machine = db.session.get(Machine, machine_id)
    if not machine:
        return jsonify(success=False, message="Machine not found"), 404

    db.session.delete(machine)
    try:
        db.session.commit()
        return jsonify(success=True, message="Machine deleted"), 200
    except Exception as e:
        db.session.rollback()
        return jsonify(success=False, message=f"Failed to delete machine: {e}"), 500
