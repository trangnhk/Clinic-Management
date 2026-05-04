from flask import Blueprint, jsonify, request
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from app.modules.menu_bar.dao import get_menu_by_role
from app.models import User

menu_bp = Blueprint("menu", __name__, url_prefix="/api/menu")


@menu_bp.route("/", methods=["GET"])
def get_menu():
    """
    Get navigation menu by role (Menu điều hướng theo vai trò)
    ---
    tags:
      - Menu
    parameters:
      - name: Authorization
        in: header
        type: string
        required: false
        description: "Bearer token (tuỳ chọn). Nếu có, trả về menu theo role của user."
        example: "Bearer <access_token>"
    responses:
      200:
        description: Danh sách menu theo role (guest nếu chưa đăng nhập)
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: true
            role:
              type: string
              enum: [guest, patient, doctor, admin]
              description: Role hiện tại của người dùng
              example: patient
            menus:
              type: array
              items:
                type: object
                properties:
                  label:
                    type: string
                    description: Tên hiển thị của mục menu
                    example: "Lịch khám"
                  path:
                    type: string
                    description: Đường dẫn URL
                    example: "/appointments"
                  icon:
                    type: string
                    description: Tên icon (tuỳ chọn)
                    example: "calendar"
    """
    role = "guest"

    try:
        verify_jwt_in_request(optional=True)

        user_id = get_jwt_identity()

        if user_id:
            user = User.query.get(user_id)

            if user:
                role = str(user.role.value).lower()
                print(f"User ID: {user_id}, Role: {role}")

                user_info = None

                if user:
                    user_info = {
                        "id": user.id,
                        "username": user.username,
                        "fullname": user.fullname,
                        "avatar": user.avatar
                    }

    except:
        role = "guest"

    menu = get_menu_by_role(role)

    return jsonify({
        "success": True,
        "role": user.role if role != "guest" else "guest",
        "menus": menu,
        "user": user_info if role != "guest" else None
    }), 200