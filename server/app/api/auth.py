from flask import Blueprint, jsonify, request, session, current_app
from app.extensions import db, bcrypt, serializer
from ..models import Users
from flask_login import login_user, logout_user, current_user, login_required
from flask_mailman import EmailMessage
from itsdangerous import BadSignature, SignatureExpired
from datetime import datetime, timezone

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
def register():
    try:
        data = request.get_json()
        if not data:
            return jsonify(success=False, message="No payload in request"), 400
        
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        role = data.get("role")
        is_admin = data.get("is_admin")
        email = data.get("email")
        password1 = data.get("password1")
        password2 = data.get("password2")
        
        check_email = Users.query.filter_by(email=email).first()
        if check_email:
            return jsonify(success=False, message="User already exists with this email. If you forgot your password please request a reset link."), 400
        
        if password1 != password2:
            return jsonify(success=False, message="Passwords do not match, please chack inputs and try again."), 403
        
        new_user = Users(first_name=first_name.capitalize(), last_name=last_name.capitalize(), role=role, is_admin=is_admin, email=email, password_hash=bcrypt.generate_password_hash(password1).decode("utf-8"))
        
        db.session.add(new_user)
        db.session.commit()
        current_app.logger.info(f"{new_user.first_name} has been added to the database")
        return jsonify(success=True, message=f"{new_user.first_name} has been registered!"), 200
    except Exception as e:
        current_app.logger.error(f"Error when adding user: {e}")
        db.session.rollback()
        return jsonify(success=False, message=f"Error when adding user: {e}"), 500
    
    
@auth_bp.route("/login/<int:id>", methods=["POST"])
def login(id):
    id = int(id)
    try:
        user = Users.query.get(id)
        if not user:
            return jsonify(success=False, message="User not found. please check inputs and try again"), 400
        data = request.get_json()
        password = data.get("password")
        if not password:
            return jsonify(success=False, message="Password field is required"), 400
        if not bcrypt.check_password_hash(user.password_hash, password):
            return jsonify(success=False, message="Invalid credentials, please check your inputs and try again."), 401
        login_user(user)
        session["user"] = f"{user.first_name} {user.last_name[0]}"
        session["device"] = request.headers.get("User-Agent")
        current_app.logger.info(f"{user.first_name} {user.last_name} has logged in at {datetime.now(timezone.utc)}")
        return jsonify(success=True, message=f"Logged in as {user.first_name} {user.last_name[0]}.", user=user.serialize()), 200
    except Exception as e:
        current_app.logger.error(f"There was an error when {user.first_name} {user.last_name} was logging in: {e}")
        return jsonify(success=False, message=f"There was an error when {user.first_name} {user.last_name} was logging in: {e}"), 500
    
    
@auth_bp.route("/logout", methods=["GET"])
def logout():
    try:
        current_app.logger.info(f"{current_user.first_name} {current_user.last_name[0]}. has logged out.")
        logout_user()
        return jsonify(success=True, message="User logged out."), 200
    except Exception as e:
        current_app.logger.error(f"There was an error when {current_user.first_name} {current_user.last_name} was logging out: {e}")
        return jsonify(success=False, message=f"There was an error when {current_user.first_name} {current_user.last_name} was logging out: {e}"), 500
    
    
@auth_bp.route("/hydrate", methods=['GET'])
@login_required
def hydrate():
    return jsonify(success=True, user=current_user.serialize()), 200