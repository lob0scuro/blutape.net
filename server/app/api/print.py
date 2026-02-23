from flask import jsonify, request, Blueprint, current_app
from app.extensions import db
from flask_login import current_user
from app.models import Machine, MachineNote, User
from datetime import datetime, timezone
from flask_login import login_required, current_user
import pandas as pd
from io import BytesIO
from flask_mailman import EmailMessage
import socket
import requests


print_bp = Blueprint("print", __name__)



    

@print_bp.route("/export", methods=["GET"])
@login_required
def export_machines():
    machines = Machine.query.filter_by(status="completed").all()
    
    if not machines:
        return jsonify(success=True, message="No machines found."), 404
    
    data = [{
            "Brand": m.brand,
            "Model": m.model,
            "Serial": m.serial,
            "Style": m.form_factor,
            "Category": m.category,
            "Color": m.color,
            "Condition": m.condition,
            "Status": m.status,
            "User": m.technician.first_name,
        } for m in machines]
    
    output = BytesIO()
    df = pd.DataFrame(data)
    
    #Write Excel file
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name=f"Machine Export - {datetime.today().date()}")
    output.seek(0)
    
    #Update machines before sending email
    try:
        for m in machines:
            m.status = "exported"
            m.exported_on = datetime.today().date()
        
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"[MACHINE EXPORT ERROR]: {e}")
        return jsonify(success=False, message="Failed to update machine status."), 500
    
    #Send email with attachement
    try:
        msg = EmailMessage(
            subject=f"{datetime.today().date()} - Machine Export",
            body="Machine export list has been attached to this email.",
            to=[current_user.email],
        )
        
        msg.attach(
            filename=f"machine-export-{datetime.today().date()}.xlsx",
            content=output.getvalue(),
            mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        
        msg.send()
        
        current_app.logger.info(f"[EXPORT]: {current_user.first_name} {current_user.last_name} exported XLSX to {current_user.email}")
        return jsonify(success=True, message="Export successful, email has been sent"), 200
    
    except Exception as e:
        current_app.logger.error(f"[EMAIL SENDING ERROR]: {e}")
        
        for m in machines:
            m.status = "completed"
            m.exported_on = None
            
        db.session.commit()
        return jsonify(success=False, message="Email failed, export aborted"), 500
    
    
    
    
#--------------------------
#   SOCKET TO PI
#--------------------------
PiIP = "100.71.48.104"
PiPORT = 5555
def send_to_pi(zpl:str) -> None:
    payload = zpl.encode("utf-8")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(5)
        s.connect((PiIP, PiPORT))
        s.sendall(payload)
        s.shutdown(socket.SHUT_WR)
        
        try:
            resp = s.recv(1024).decode("utf-8", "replace").strip()
            current_app.logger.info(f"[PRINT GATEWAY]: {resp}")
        except Exception:
            pass
    
#--------------------------
#   PRINT LABELS
#   NEED TO HOOK UP ONCE DEPLOYED
#--------------------------
PRINTER_IP = "100.71.48.104"
ZEBRA_IP = "192.168.1.153"
PRINTER_PORT = 5000
URL = "http://100.71.48.104:5000/print"


def generate_ZPL_label(data):
    zpl = f"""
    ^XA
    ^FO10,25^GB775,365,6^FS
    ^FO50, 60^A0,35^FDbluTape/ Matt's Appliances^FS
    ^FO530, 60^A0,35^FDID: {data["id"]}^FS
    ^FO50,105^BQN,2,9^FDLA,{data["serial"]}^FS
    ^FO300,130^A0,35^FDBrand: {data["brand"]}^FS
    ^FO300,175^A0,35^FDModel: {data["model"]}^FS
    ^FO300,220^A0,35^FDSerial: {data["serial"]}^FS
    ^FO300,265^A0,35^FDStyle: {data["form_factor"]}^FS
    ^FO300,310^A0,35^FDColor: {data["color"]}^FS
    ^XZ
    """
    return zpl

@print_bp.route("/label", methods=['POST'])
def print_label():
    """
    Accepts JSON like:
    {
        "id": "machine id",
        "model": "Machine Model Number",
        "serial": "Serial number", 
        "brand": "Machine brand",
        "form_factor": "Machine form factor",
        "color": "Machine color"
    }
    Generates ZPL and sends it to the Zebra printer via Raspberry Pi (Tailscale).
    """
    try:
        data = request.get_json()
        required_fields = ["id", "model", "serial", "brand", "form_factor", "color"]
        
        if not data or any(field not in data for field in required_fields):
            return jsonify(success=False, message="Missing required fields"), 400
        
        zpl = generate_ZPL_label(data)
        send_to_pi(zpl)
        
        current_app.logger.info(
            f"[LABEL]: {current_user.first_name} {current_user.last_name} "
            f"printed MachinID: {data.get('id')}"
        )
        return jsonify(success=True, message="Label sent to printer"), 200
    except socket.timeout:
        current_app.logger.error(f"[LABEL ERROR]: Print gateway timemout")
        return jsonify(success=False, message="Printer gateway timeout"), 504
    
    except Exception as e:
        current_app.logger.error(f"[LABEL ERROR]: {e}")
        return jsonify(success=False, message=f"Error sending label: {e}"), 500
        
    