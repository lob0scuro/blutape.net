from flask import jsonify, current_app, Blueprint, request, Response, render_template
from app.extensions import db
from app.models import Machines, Users
from flask_login import login_required, current_user
import pandas as pd
from io import BytesIO, StringIO
from flask_mailman import EmailMessage
from datetime import datetime
import csv
import pdfkit
import os



export_bp = Blueprint("export", __name__)

def generate_user_report_csv(report):
    output = StringIO()
    writer = csv.writer(output)
    
    writer.writerow([
        "Brand",
        "Machine Type",
        "Machine Style",
        "Status",
        "Date"
    ])
    
    for r in report["rows"]:
        writer.writerow([
            r["brand"],
            r["machine_type"],
            r["machine_style"],
            r["status"],
            r["date"]
        ])
        
    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={
            "Content-Disposition": "attachment; filename=user_report.csv"
        }
    )
    
def generate_user_report_pdf(report, start_date, end_date):
    html = render_template(
        "user_report.html",
        report=report,
        start=start_date,
        end=end_date
    )
    WKTHMLTOPDF_PATH = (
        r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
        if os.name == "nt"
        else "/usr/bin/wkhtmltopdf"
    )

    config = pdfkit.configuration(
        wkhtmltopdf=WKTHMLTOPDF_PATH
    )
    
    pdf = pdfkit.from_string(
        html,
        False,
        options={
            "quiet": "",
            "encoding": "UTF-8"
        },
        configuration=config
    )
    
    return Response(
        pdf,
        mimetype="application/pdf",
        headers={
            "Content-Disposition": "inline; filename=user_report.pdf"
        }
    )
    

@export_bp.route("/user_report/<int:id>", methods=["GET"])
@login_required
def export_user_report(id):
    user = Users.query.get(id)
    if not user:
        return jsonify(success=False, message="User not found"), 404
    
    start_str = request.args.get("start")
    end_str = request.args.get("end")
    fmt = request.args.get("format", "pdf")
    
    try:
        start_date = datetime.strptime(start_str, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_str, "%Y-%m-%d").date()
    except (ValueError, TypeError):
        return jsonify(success=False, message="Invalid date format, use YYYY-MM-DD"), 400
    
    report = Machines.metrics_report(id, start_date, end_date)
    
    if not report["rows"]:
        return jsonify(success=False, message="No records in date range"), 404
    
    if fmt == "csv":
        return generate_user_report_csv(report)
    elif fmt == "pdf":
        return generate_user_report_pdf(report, start_date, end_date)
    else:
        return jsonify(success=False, message="Invalid format request."), 400
        
    