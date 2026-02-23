from flask import jsonify, request, Blueprint, current_app
from app.extensions import db
from flask_login import current_user
from app.models import (
    Machine, 
    User, 
    MachineNote, 
    WorkOrder, 
    WorkOrderEvent, 
    CategoryEnum, 
    ConditionEnum, 
    EventReasonEnum, 
    EventEnum, 
    RoleEnum, 
    StatusEnum, 
    VendorEnum
)
from datetime import datetime, timezone, date

update_bp = Blueprint("update", __name__)


def _status_to_event_type(old_status: StatusEnum, new_status: StatusEnum) -> EventEnum:
    if new_status == StatusEnum.COMPLETED:
        return EventEnum.COMPLETED
    if new_status == StatusEnum.TRASHED:
        return EventEnum.TRASHED
    if new_status == StatusEnum.ARCHIVED:
        return EventEnum.ARCHIVED
    if new_status == StatusEnum.IN_PROGRESS and old_status in {StatusEnum.COMPLETED, StatusEnum.TRASHED}:
        return EventEnum.REOPENED
    return EventEnum.INITIATED


@update_bp.patch("/work_order/<int:work_order_id>/status")
def update_work_order_status(work_order_id):
    work_order = db.session.get(WorkOrder, work_order_id)
    if not work_order:
        return jsonify(success=False, message="Work order not found"), 404

    data = request.get_json() or {}
    raw_status = (data.get("new_status") or "").strip().lower()
    raw_reason = (data.get("reason") or "").strip().lower()

    if not raw_status:
        return jsonify(success=False, message="new_status is required"), 400

    try:
        new_status = StatusEnum(raw_status)
    except ValueError:
        return jsonify(success=False, message="Invalid status"), 400

    reason = EventReasonEnum.DEFAULT
    if raw_reason:
        try:
            reason = EventReasonEnum(raw_reason)
        except ValueError:
            return jsonify(success=False, message="Invalid event reason"), 400

    old_status = work_order.current_status
    if old_status == new_status:
        return jsonify(success=True, message="No status change", work_order=work_order.serialize()), 200

    work_order.current_status = new_status

    if new_status in {StatusEnum.COMPLETED, StatusEnum.TRASHED}:
        work_order.closed_on = date.today()
    elif new_status == StatusEnum.IN_PROGRESS:
        work_order.closed_on = None

    event = WorkOrderEvent(
        work_order_id=work_order.id,
        machine_id=work_order.machine_id,
        event_type=_status_to_event_type(old_status, new_status),
        from_status=old_status,
        to_status=new_status,
        technician_id=current_user.id,
        reason=reason,
    )
    db.session.add(event)

    try:
        db.session.commit()
        return jsonify(
            success=True,
            message="Work order status updated",
            work_order=work_order.serialize(),
            event=event.serialize(),
        ), 200
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"[WORK ORDER STATUS UPDATE ERROR]: {e}")
        return jsonify(success=False, message="Failed to update work order status"), 500


@update_bp.patch("/machine/<int:machine_id>")
def update_machine_fields(machine_id):
    machine = db.session.get(Machine, machine_id)
    if not machine:
        return jsonify(success=False, message="Machine not found"), 404

    data = request.get_json() or {}
    if not data:
        return jsonify(success=False, message="No payload in request"), 400

    if "brand" in data and data["brand"] is not None:
        machine.brand = str(data["brand"]).strip().lower()
    if "model" in data and data["model"] is not None:
        machine.model = str(data["model"]).strip().upper()
    if "form_factor" in data and data["form_factor"] is not None:
        machine.form_factor = str(data["form_factor"]).strip().lower()
    if "color" in data and data["color"] is not None:
        machine.color = str(data["color"]).strip().lower()

    if "serial" in data and data["serial"] is not None:
        serial = str(data["serial"]).strip().upper()
        if not serial:
            return jsonify(success=False, message="serial cannot be empty"), 400

        duplicate = (
            db.session.query(Machine)
            .filter(Machine.serial == serial, Machine.id != machine.id)
            .first()
        )
        if duplicate:
            return jsonify(success=False, message="Machine serial already exists"), 409
        machine.serial = serial

    try:
        if "category" in data and data["category"] is not None:
            machine.category = CategoryEnum(str(data["category"]).strip().lower())
        if "condition" in data and data["condition"] is not None:
            machine.condition = ConditionEnum(str(data["condition"]).strip().lower())
        if "vendor" in data and data["vendor"] is not None:
            machine.vendor = VendorEnum(str(data["vendor"]).strip().lower())
    except ValueError:
        return jsonify(success=False, message="Invalid category, condition, or vendor"), 400

    try:
        db.session.commit()
        return jsonify(success=True, message="Machine updated", machine=machine.serialize()), 200
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"[MACHINE UPDATE ERROR]: {e}")
        return jsonify(success=False, message="Failed to update machine"), 500

