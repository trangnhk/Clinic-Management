from flask import Blueprint, request, jsonify
from .dao import register_user, login_user
from app.db.db import db
from flask_jwt_extended import create_access_token

auth_bp = Blueprint("auth_api", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    """
    Register new user (Đăng ký tài khoản)
    ---
    tags:
      - Auth
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - username
            - email
            - password
          properties:
            username:
              type: string
              example: "user01"
            email:
              type: string
              example: "user01@gmail.com"
            password:
              type: string
              example: "123456"
    responses:
      200:
        description: Đăng ký thành công
        schema:
          type: object
          properties:
            id:
              type: integer
              example: 1
    """
    data = request.json
    try:
        user = register_user(
            data.get("username"),
            data.get("email"),
            data.get("password")
        )
        db.session.refresh(user)
        return jsonify(user.to_dict())
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@auth_bp.route("/login", methods=["POST"])
def login():
    """
    Login user (Đăng nhập)
    ---
    tags:
      - Auth
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - username
            - password
          properties:
            username:
              type: string
              example: "user01"
            password:
              type: string
              example: "123456"
    responses:
      200:
        description: Đăng nhập thành công
        schema:
          type: object
          properties:
            id:
              type: integer
              example: 1
            role:
              type: string
              example: "patient"
      401:
        description: Sai thông tin đăng nhập
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Invalid"
    """
    data = request.json
    try:
        user = login_user(data["username"], data["password"])
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
    if not user:
        return jsonify({"error": "Invalid"}), 401
    access_token = create_access_token(
        identity=str(user.id),
        additional_claims={
            "role": user.role
        }
    )
    return jsonify({
        "access_token": access_token,
        "user": {
            "id": user.id,
            "username": user.username,
            "role": user.role
        }
    })