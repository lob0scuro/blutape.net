from flask import Blueprint, jsonify, request, current_app
from app.extensions import db
from flask_login import current_user
from app.models import Machine, MachineNote, WorkOrder, WorkOrderEvent
from app.models.enums import CategoryEnum, ConditionEnum, VendorEnum, StatusEnum, EventEnum, EventReasonEnum

create_bp = Blueprint("create", __name__)


@create_bp.post("/machine")
def add_new_machine():
    data = request.get_json()
    if not data:
        return jsonify(success=False, message="No data in payload"), 400
    
    serial = (data.get("serial") or "").strip().upper()
    if not serial:
        return jsonify(success=False, message="Serial number is required"), 400
    
    required = ["brand", "model", "form_factor", "color", "category", "condition", "vendor"]
    missing = [k for k in required if not (data.get(k) or "").strip()]
    if missing:
        return jsonify(success=False, message=f"Missing required fields: {",".join(missing)}"), 400
    
    existing = db.session.query(Machine).filter_by(serial=serial).first()
    if existing:
        return jsonify(success=False, message="Machine already exists in database."), 409
    
    try:
        category = CategoryEnum((data.get("category") or "").strip().lower())
        condition = ConditionEnum((data.get("condition") or "").strip().lower())
        vendor = VendorEnum((data.get("vendor") or "").strip().lower())
    except (KeyError, ValueError):
        return jsonify(success=False, message="Bad data in one or more [category, condition, vendor]"), 400
    
    new_machine = Machine(
        brand=(data.get("brand") or "").strip().lower(),
        model=(data.get("model") or "").strip().upper(),
        serial=serial,
        category=category,
        form_factor=(data.get("form_factor") or "").strip().lower(),
        color=(data.get("color") or "").strip().lower(),
        condition=condition,
        vendor=vendor
    )
    db.session.add(new_machine)
    db.session.flush()
    
    new_work_order = WorkOrder(
        machine_id=new_machine.id,
        initiated_by=current_user.id,
        current_status=StatusEnum.IN_PROGRESS
    )
    db.session.add(new_work_order)
    db.session.flush()
    
    new_event = WorkOrderEvent(
        work_order_id=new_work_order.id,
        machine_id=new_machine.id,
        event_type=EventEnum.INITIATED,
        from_status=None,
        to_status=StatusEnum.IN_PROGRESS,
        technician_id=current_user.id,
        reason=EventReasonEnum.DEFAULT
    )
    db.session.add(new_event)
    
    new_note = MachineNote(
        content=(data.get("note_content") or ""),
        technician_id=current_user.id,
        machine_id=new_machine.id
    )
    db.session.add(new_note)
    
    try:
        db.session.commit()
        current_app.logger.info(f"[NEW MACHINE ADDED]: {current_user.first_name} {current_user.last_name} has added a new {new_machine.category}")
        return jsonify(
            success=True, 
            message="New machine added!",
            machine_id=new_machine.id
        ), 201
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"[NEW MACHINE ERROR]: {e}")
        return jsonify(success=False, message="There was an error when adding new machine"), 500
    
    
@create_bp.post("/note/<int:machine_id>")
def add_note_to_machine(machine_id):
    machine = db.session.get(Machine, machine_id)
    if not machine:
        return jsonify(success=False, message="Machine not found"), 404
    
    data = request.get_json()
    if not data:
        return jsonify(success=False, message="No data in payload"), 400
    
    note = MachineNote(
        content=(data.get("content") or ""),
        technician_id=current_user.id,
        machine_id=machine.id
    )
    
    db.session.add(note)
    
    try:
        db.session.commit()
        current_app.logger.info(f"[NEW NOTE ADDED]: {current_user.first_name} {current_user.last_name} notated machine [{machine.id}]")
        return jsonify(success=True, message="Note has been added", note=note.serialize()), 201
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"[NEW NOTE ERROR]: {e}")
        return jsonify(success=False, message="There was an error when adding note"), 500

