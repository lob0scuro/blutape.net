from flask import Blueprint, jsonify, request, current_app
from app.extensions import db
from flask_login import current_user
from app.models import Machines, Notes
from datetime import datetime, timezone

create_bp = Blueprint("create", __name__)

@create_bp.route("/add_machine", methods=["POST"])
def add_machine():
    try:
        data = request.get_json()
        if not data:
            return jsonify(success=False, message="No data in payload"), 400
        brand = data.get("brand")
        model = data.get("model")
        serial = data.get("serial")
        style = data.get("style")
        color = data.get("color")
        condition = data.get("condition")
        vendor = data.get("vendor")
        type_of = data.get("type_of")
        now = datetime.today().date()
        
        
        exists = Machines.query.filter_by(serial=serial.upper()).first()
        if exists:
            return jsonify(success=False, message="Duplicate entry detected: a machine with this serial number already exists."), 409
        
        new_machine = Machines(brand=brand, model=model.upper(), serial=serial.upper(), style=style, color=color, condition=condition, vendor=vendor, type_of=type_of, technician_id=current_user.id, started_on=now)
        db.session.add(new_machine)
        
        db.session.flush()
        
        new_note = Notes(content=f"Machine added on {now} \n {{THIS NOTE HAS BEEN AUTO GENERATED FROM THE SERVER}}", date=now, author=current_user, machine=new_machine)
        db.session.add(new_note)
        
        
        db.session.commit()
        
        current_app.logger.info(f"{current_user.first_name} {current_user.last_name[0]}. logged a new {style} {type_of} into the database/// model:{model.upper()} serial:{serial.upper()}")
        return jsonify(success=True, message=f"Machine has been logged.", machine_id=new_machine.id), 200
    except Exception as e:
        current_app.logger.error(f"An error occured when inputing a new machine: {e}")
        db.session.rollback()
        return jsonify(success=False, message=f"Error when logging new machine: {e}"), 500
    
    
@create_bp.route("/add_note", methods=["POST"])
def add_note():
    try:
        data = request.get_json()
        machine_id = data.get("machine_id")
        note = data.get("note")
        
        new_note = Notes(
            content=note, date=datetime.today().date(), machine_id=machine_id, user_id=current_user.id
        )
        db.session.add(new_note)
        db.session.commit()
        current_app.logger.info(f"{current_user.first_name} {current_user.last_name} has added a new note to machine {machine_id}")
        return jsonify(success=True, message="Note added!", note=new_note.serialize()), 201
    except Exception as e:
        current_app.logger.error(f"[NOTE ERROR]: {e}")
        db.session.rollback()
        return jsonify(success=False, message="There was an error when submitting new note."), 500
    