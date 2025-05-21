from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from models.user import User
from models.database import db
from utils.security import hash_password, verify_password
import datetime

auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if not name or not email or not password:
        return jsonify({"error": "Missing fields"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already exists"}), 409

    new_user = User(
        name=name,
        email=email,
        password=hash_password(password)
    )
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered"}), 201

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()
    if not user or not verify_password(password, user.password):
        return jsonify({"error": "Invalid credentials"}), 401

    expires = datetime.timedelta(days=1)
    token = create_access_token(identity=user.id, expires_delta=expires)
    
    
    return jsonify({"access_token": token}), 200