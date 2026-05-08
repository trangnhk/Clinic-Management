from flask import Blueprint, request, jsonify
from app.modules.doctor.dao import *
from datetime import datetime
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

doctor_bp = Blueprint("doctor_api", __name__)

def doctor_only():
    claims = get_jwt()

    if claims["role"] != "DOCTOR":
        return False
    
    return True

# DOCTOR PROFILE
@doctor_bp.route("/profile", methods=["GET"])
@jwt_required()
def get_profile():
    """
    Get doctor profile (Thông tin hồ sơ bác sĩ)
    ---
    tags:
      - Doctor
    responses:
      200:
        description: Thông tin hồ sơ bác sĩ
        schema:
          type: object
          properties:
            doctor_id:
              type: string
              description: Mã bác sĩ định dạng DR000000001
              example: "DR000000001"
            fullname:
              type: string
              example: "BS. Nguyễn Minh Khoa"
            phone_number:
              type: string
              nullable: true
              example: "0901234567"
            date_of_birth:
              type: string
              nullable: true
              example: "1985-06-15"
            address:
              type: string
              nullable: true
              example: "123 Lê Lợi, Q.1, TP.HCM"
            specialization:
              type: string
              nullable: true
              example: "Cardiology"
            specialization_id:
              type: integer
              nullable: true
              example: 1
            experience_years:
              type: integer
              nullable: true
              example: 10
            description:
              type: string
              nullable: true
              example: "Bác sĩ có nhiều năm kinh nghiệm"
            rating:
              type: number
              example: 4.5
            avatar:
              type: string
              nullable: true
              example: "https://example.com/avatar.png"
      403:
        description: Không có quyền truy cập
        schema:
          type: object
          properties:
            error:
              type: string
              example: Forbidden
      500:
        description: Lỗi máy chủ nội bộ
        schema:
          type: object
          properties:
            error:
              type: string
    """
    
    try:
        current_user = get_jwt_identity()

        if not doctor_only():
            return jsonify({"error": "Forbidden"}), 403
        
        profile = get_doctor_profile(user_id=current_user)
        return jsonify(profile), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@doctor_bp.route("/profile", methods=["PATCH"])
@jwt_required()
def patch_profile():
    """
    Update doctor profile (Cập nhật hồ sơ bác sĩ)
    ---
    tags:
      - Doctor
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            fullname:
              type: string
              example: "BS. Nguyễn Minh Khoa"
            phone_number:
              type: string
              description: Phải đúng 10 chữ số
              example: "0901234567"
            experience_years:
              type: integer
              minimum: 0
              example: 10
            description:
              type: string
              example: "Bác sĩ chuyên khoa tim mạch"
    responses:
      200:
        description: Cập nhật thành công, trả về profile mới nhất
        schema:
          type: object
          properties:
            doctor_id:
              type: string
              example: "DR000000001"
            fullname:
              type: string
              example: "BS. Nguyễn Minh Khoa"
            phone_number:
              type: string
              example: "0901234567"
            experience_years:
              type: integer
              example: 10
            description:
              type: string
              example: "Bác sĩ chuyên khoa tim mạch"
            specialization:
              type: string
              example: "Cardiology"
            rating:
              type: number
              example: 4.5
            avatar:
              type: string
              example: "https://example.com/avatar.png"
      400:
        description: |
          - phone_number không đúng 10 chữ số
          - experience_years < 0
      403:
        description: Không có quyền truy cập
      500:
        description: Lỗi máy chủ nội bộ
    """
    
    try:
        current_user = get_jwt_identity()

        if not doctor_only():
            return jsonify({"error": "Forbidden"}), 403
        
        data = request.get_json() or {}

        updated = update_doctor_profile(
            user_id=current_user,
            experience_years=data.get("experience_years"),
            description=data.get("description"),
            fullname=data.get("fullname"),
            phone_number=data.get("phone_number")
        )

        return jsonify(updated), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@doctor_bp.route("/profile/calendar", methods=["GET"])
@jwt_required()
def get_calendar():
    """
    Get doctor appointment calendar (Lịch hẹn theo tháng)
    ---
    tags:
      - Doctor
    parameters:
      - name: month
        in: query
        type: integer
        required: true
        description: Tháng cần xem (1-12)
        example: 4
      - name: year
        in: query
        type: integer
        required: true
        description: Năm cần xem (2026-2100)
        example: 2026
    responses:
      200:
        description: Dữ liệu lịch hẹn theo từng ngày trong tháng
        schema:
          type: object
          properties:
            month:
              type: integer
              example: 4
            year:
              type: integer
              example: 2026
            days_with_appointments:
              type: array
              description: Danh sách các ngày có lịch hẹn (đã sắp xếp)
              items:
                type: integer
              example: [1, 5, 10, 15]
            calendar:
              type: object
              description: Key là số ngày, value là danh sách lịch hẹn trong ngày đó
              additionalProperties:
                type: array
                items:
                  type: object
                  properties:
                    appointment_id:
                      type: integer
                      example: 10
                    status:
                      type: string
                      example: "WAITING_EXAMINATION"
                    start_time:
                      type: string
                      example: "08:00"
      400:
        description: |
          - Thiếu month hoặc year
          - month không hợp lệ (ngoài 1-12)
          - year không hợp lệ (ngoài 2026-2100)
      403:
        description: Không có quyền truy cập
      500:
        description: Lỗi máy chủ nội bộ
    """
    
    try:
        current_user = get_jwt_identity()

        if not doctor_only():
            return jsonify({"error": "Forbidden"}), 403
        
        month = request.args.get("month", type=int)
        year = request.args.get("year", type=int)

        if not month or not year:
            return jsonify({"error": "month and year are required"}), 400

        data = get_doctor_calendar(
            user_id=current_user,
            month=month,
            year=year
        )

        return jsonify(data), 200
    
    
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# APPOINTMENT SCHEDULE
@doctor_bp.route("/appointments", methods=["GET"])
@jwt_required()
def get_appointment_in_day():
    """
    Get doctor's appointments in a day (Xem lịch khám trong ngày)
    ---
    tags:
      - Doctor
    parameters:
      - name: date
        in: query
        type: string
        required: true
        description: Ngày cần xem lịch (định dạng YYYY-MM-DD)
        example: "2026-04-15"
      - name: status
        in: query
        type: string
        required: false
        description: Lọc theo trạng thái
        enum:
          - WAITING_EXAMINATION
          - PENDING_RESULT
          - COMPLETED
    responses:
      200:
        description: Danh sách lịch khám trong ngày, sắp xếp theo giờ tăng dần
        schema:
          type: array
          items:
            type: object
            properties:
              appointment_id:
                type: integer
                example: 10
              date:
                type: string
                example: "2026-04-15"
              status:
                type: string
                example: "WAITING_EXAMINATION"
              start_time:
                type: string
                example: "08:00"
              end_time:
                type: string
                example: "08:30"
              can_examine:
                type: boolean
                example: true
              can_complete:
                type: boolean
                example: false
              patient:
                type: object
                properties:
                  id:
                    type: integer
                    example: 1
                  name:
                    type: string
                    example: "Nguyễn Văn An"
                  email:
                    type: string
                    example: "patient@mail.com"
                  date_of_birth:
                    type: string
                    nullable: true
                    example: "1990-01-01"
                  address:
                    type: string
                    nullable: true
                    example: "TP.HCM"
      400:
        description: |
          - Thiếu date
          - Sai định dạng date
      403:
        description: Không có quyền truy cập / status filter không hợp lệ
      404:
        description: Không tìm thấy bác sĩ
    """
    
    try:
        current_user = get_jwt_identity()

        if not doctor_only():
            return jsonify({"error": "Forbidden"}), 403

        # get doctor profile
        doctor = get_doctor_by_user_id(user_id=current_user)
        
        if not doctor:
            return jsonify({"error": "Doctor not found"}), 404

        # get date
        date_str = request.args.get("date")

        if not date_str:
            return jsonify({"error": "Missing date"}), 400
        
        try:
            query_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            return jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400
        
        status_filter = request.args.get("status")

        appointments = get_doctor_appointments_by_date(doctor.id, query_date)

        allowed_status = [
            AppointmentStatusEnum.IN_PROGRESS,
            AppointmentStatusEnum.COMPLETED,
            AppointmentStatusEnum.WAITING_EXAMINATION,
            AppointmentStatusEnum.PENDING_RESULT
        ]

        appointments = [
            a for a in appointments
            if a.status in allowed_status
        ]

        if status_filter:
            if status_filter in [AppointmentStatusEnum.IN_PROGRESS, AppointmentStatusEnum.COMPLETED, AppointmentStatusEnum.WAITING_EXAMINATION, AppointmentStatusEnum.PENDING_RESULT]:
                appointments = [a for a in appointments
                                if (a.status.value if hasattr(a.status,'value') else a.status) == status_filter]

            else:
                return jsonify({"error": "Forbidden"}), 403

        return jsonify([format_appointment(a) for a in appointments]), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
@doctor_bp.route("/appointments/<int:id>", methods=["GET"])
@jwt_required()
def get_appointment_detail_route(id):
    """
    Get appointment detail (Xem chi tiết lịch khám)
    ---
    tags:
      - Doctor
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID lịch khám
    responses:
      200:
        description: Chi tiết lịch khám bao gồm thông tin bệnh nhân và bệnh án (nếu có)
        schema:
          type: object
          properties:
            appointment_id:
              type: integer
              example: 10
            date:
              type: string
              example: "2026-04-15"
            status:
              type: string
              example: "IN_PROGRESS"
            symptoms:
              type: string
              nullable: true
              example: "Đau đầu, sốt nhẹ"
            patient:
              type: object
              properties:
                id:
                  type: integer
                  example: 1
                patient_code:
                  type: string
                  example: "BN000000001"
                fullname:
                  type: string
                  example: "Nguyễn Văn An"
                phone_number:
                  type: string
                  example: "0901234567"
                email:
                  type: string
                  example: "patient@mail.com"
                date_of_birth:
                  type: string
                  example: "1990-01-01"
                address:
                  type: string
                  example: "TP.HCM"
            examination:
              type: object
              nullable: true
              properties:
                id:
                  type: integer
                  example: 5
                created_date:
                  type: string
                  example: "2026-04-15"
                diagnosis:
                  type: string
                  example: "Viêm họng"
                prescription:
                  type: object
                  nullable: true
                  properties:
                    id:
                      type: integer
                      example: 3
                    details:
                      type: array
                      items:
                        type: object
                        properties:
                          id:
                            type: integer
                          medicine_id:
                            type: integer
                          medicine_name:
                            type: string
                          quantity:
                            type: integer
                          unit_price:
                            type: number
                          subtotal:
                            type: number
                          dosage:
                            type: string
                          instruction:
                            type: string
                    total_medicine_cost:
                      type: number
                      example: 150000
                    consultation_fee:
                      type: number
                      example: 500000
                    total:
                      type: number
                      example: 650000
                lab_tests:
                  type: array
                  items:
                    type: object
                    properties:
                      id:
                        type: integer
                      test_id:
                        type: integer
                      test_name:
                        type: string
                      test_price:
                        type: number
                      status:
                        type: string
                        enum: [PENDING, IN_PROGRESS, DONE]
      400:
        description: Không tìm thấy lịch khám hoặc không thuộc bác sĩ này
      403:
        description: Không có quyền truy cập
    """
    
    try:
        current_user = get_jwt_identity()
        if not doctor_only():
            return jsonify({"error": "Forbidden"}), 403
        
        detail = get_appointment_detail(appointment_id=id, user_id=current_user)
        return jsonify(detail), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# EXAMINATION
@doctor_bp.route("/examinations", methods=["POST"])
@jwt_required()
def create_exam_route():
    """
    Create examination (Tạo phiếu khám bệnh)
    ---
    tags:
      - Doctor
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - appointment_id
          properties:
            appointment_id:
              type: integer
              example: 10
            diagnosis:
              type: string
              example: "Viêm họng cấp"
            symptoms:
              type: string
              description: Ghi đè vào notes của appointment
              example: "Đau họng, sốt 38 độ"
    responses:
      201:
        description: Tạo phiếu khám thành công, appointment chuyển sang IN_PROGRESS
        schema:
          type: object
          properties:
            id:
              type: integer
              example: 5
            appointment_id:
              type: integer
              example: 10
            created_date:
              type: string
              example: "2026-04-15"
            diagnosis:
              type: string
              example: "Viêm họng cấp"
            symptoms:
              type: string
              nullable: true
              example: "Đau họng, sốt 38 độ"
      400:
        description: |
          - Thiếu appointment_id
          - Appointment không ở trạng thái WAITING_EXAMINATION
          - Đã tồn tại examination cho appointment này
          - appointment_id không thuộc bác sĩ này
      403:
        description: Không có quyền truy cập
    """
    
    try:
        current_user = get_jwt_identity()

        if not doctor_only():
          return jsonify({"error": "Forbidden"}), 403

        data = request.get_json()
        if not data:
            return jsonify({"error": "Request body is required"}), 400
        
        appointment_id = data.get("appointment_id")
        diagnosis = data.get("diagnosis", "")

        if not appointment_id:
            return jsonify({"error": "appointment_id is required"}), 400
        
        exam = create_examination(
            appointment_id=appointment_id,
            diagnosis=diagnosis,
            user_id=current_user,
            symptoms=data.get("symptoms")
        )

        return jsonify({
            "id": exam.id,
            "appointment_id": exam.appointment_id,
            "created_date": str(exam.created_date),
            "diagnosis": exam.diagnosis,
            "symptoms": exam.appointment.notes
        }), 201
    
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@doctor_bp.route("/examinations/<int:id>", methods=["PATCH"])
@jwt_required()
def update_exam_route(id):
    """
    Update examination (Cập nhật phiếu khám)
    ---
    tags:
      - Doctor
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID phiếu khám
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            diagnosis:
              type: string
              example: "Viêm họng mãn tính"
            symptoms:
              type: string
              example: "Đau họng kéo dài"
    responses:
      200:
        description: Cập nhật thành công
        schema:
          type: object
          properties:
            id:
              type: integer
              example: 5
            diagnosis:
              type: string
              example: "Viêm họng mãn tính"
            symptoms:
              type: string
              nullable: true
              example: "Đau họng kéo dài"
      400:
        description: |
          - Appointment không ở trạng thái IN_PROGRESS hoặc PENDING_RESULT
          - Không phải bác sĩ phụ trách
      403:
        description: Không có quyền truy cập
      500:
        description: Lỗi máy chủ nội bộ
    """
    
    try:
        current_user = get_jwt_identity()

        if not doctor_only():
            return jsonify({"error": "Forbidden"}), 403
        
        data = request.get_json() or {}

        exam = update_examination(
            exam_id=id,
            user_id=current_user,
            diagnosis=data.get("diagnosis"),
            symptoms=data.get("symptoms")
        )

        return jsonify({
            "id": exam.id,
            "diagnosis": exam.diagnosis,
            "symptoms": exam.appointment.notes
        }), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 400
        
@doctor_bp.route("/examinations/<int:id>/prescriptions", methods=["POST"])
@jwt_required()
def add_prescription_route(id):
    """
    Add prescription detail (Thêm thuốc vào đơn thuốc)
    ---
    tags:
      - Doctor
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID phiếu khám (examination_id)
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - medicine_id
            - quantity
          properties:
            medicine_id:
              type: integer
              example: 3
            quantity:
              type: integer
              minimum: 1
              example: 10
            dosage:
              type: string
              example: "2 lần/ngày"
            instruction:
              type: string
              example: "Uống sau ăn"
    responses:
      201:
        description: Thêm thuốc thành công (tự tạo Prescription nếu chưa có)
        schema:
          type: object
          properties:
            prescription_id:
              type: integer
              example: 3
            detail_id:
              type: integer
              example: 8
            medicine_id:
              type: integer
              example: 3
            quantity:
              type: integer
              example: 10
            dosage:
              type: string
              example: "2 lần/ngày"
            instruction:
              type: string
              example: "Uống sau ăn"
      400:
        description: |
          - Thiếu medicine_id hoặc quantity
          - medicine_id / quantity không phải số nguyên
          - Không tìm thấy medicine hoặc examination
          - Appointment không ở trạng thái hợp lệ
      403:
        description: Không có quyền truy cập
      500:
        description: Lỗi máy chủ nội bộ
    """
    
    try:
        current_user = get_jwt_identity()
        if not doctor_only():
            return jsonify({"error": "Forbidden"}), 403
        
        data = request.get_json()
        if not data:
            return jsonify({"error": "Request body is required"}), 400
        
        medicine_id = data.get("medicine_id")
        quantity = data.get("quantity")
        
        if not medicine_id or not quantity:
            return jsonify({"error": "medicine_id and quantity are required"}), 400
        
        if not isinstance(quantity, int) or not isinstance(medicine_id, int):
            return jsonify({"error": "medicine_id and quantity must be interger"}), 400
        
        # Tạo hoặc lấy prescription
        pres = create_or_get_prescription(exam_id=id, user_id=current_user)
        
        detail = add_prescription_detail(
            pres_id=pres.id,
            medicine_id=medicine_id,
            quantity=quantity,
            dosage=data.get("dosage", ""),
            instruction=data.get("instruction", ""),
            user_id=current_user
        )
        return jsonify({
            "prescription_id": pres.id,
            "detail_id": detail.id,
            "medicine_id": detail.medicine_id,
            "quantity": detail.quantity,
            "dosage": detail.dosage,
            "instruction": detail.instruction
        }), 201
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 400

@doctor_bp.route("/prescriptions/<int:detail_id>", methods=["DELETE"])
@jwt_required()
def delete_prescription_detail_route(detail_id):
    try:
        current_user = get_jwt_identity()
        if not doctor_only():
            return jsonify({"error": "Forbidden"}), 403
        
        delete_prescription_detail(detail_id=detail_id, user_id=current_user)
        return jsonify({"message": "Deleted successfully"}), 200
    
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 400

@doctor_bp.route("/examinations/<int:id>/lab-tests", methods=["POST"])
@jwt_required()
def add_lab_test(id):
    try:
        current_user = get_jwt_identity()
        if not doctor_only():
            return jsonify({"error": "Forbidden"}), 403
        
        data = request.get_json()
        if not data or not data.get("test_id"):
            return jsonify({"error": "test_id is required"}), 400
        
        tr = create_lab_test_request(
            exam_id=id,
            test_id=data["test_id"],
            user_id=current_user
        )
        return jsonify({
            "id": tr.id,
            "test_id": tr.test_id,
            "appointment_id": tr.appointment_id,
            "status": tr.status.value if hasattr(tr.status,'value') else tr.status
        }), 201
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 400


@doctor_bp.route("/examinations/<int:id>/lab-tests", methods=["GET"])
@jwt_required()
def get_lab_tests(id):
    try:
        current_user = get_jwt_identity()

        if not doctor_only():
            return jsonify({"error": "Forbidden"}), 403
        
        data = get_lab_tests_by_exam(exam_id=id, user_id=current_user)

        return jsonify(data), 200
    
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 400


@doctor_bp.route("/lab-tests/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_lab_test(id):
    try:
        current_user = get_jwt_identity()

        if not doctor_only():
            return jsonify({"error": "Forbidden"}), 403
        
        delete_lab_test_request(test_request_id=id, user_id=current_user)

        return jsonify({"message": "Deleted"}), 200
    
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 400

@doctor_bp.route("/examinations/<int:id>/save", methods=["POST"])
@jwt_required()
def save_exam_route(id):
    """
    Save examination — upsert Payment MEDICINE + LAB_TEST (status=PENDING)
    ---
    tags:
      - Doctor
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID phiếu khám (examination_id)
    responses:
      200:
        description: Đã lưu, trả về medicine cost và lab test cost mới nhất
        schema:
          type: object
          properties:
            medicine:
              type: number
              example: 150000
            lab_test:
              type: number
              example: 100000
      400:
        description: Examination not found / Appointment status không hợp lệ
      403:
        description: Forbidden
    """
    try:
        current_user = get_jwt_identity()
        if not doctor_only():
            return jsonify({"error": "Forbidden"}), 403

        result = save_examination(exam_id=id, user_id=current_user)
        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400

@doctor_bp.route("/appointments/<int:id>/complete", methods=["POST"])
@jwt_required()
def complete_appointment_route(id):
    try:
        current_user = get_jwt_identity()

        if not doctor_only():
            return jsonify({"error": "Forbidden"}), 403
        
        appointment = complete_appointment(
            appointment_id=id, 
            user_id=current_user
            )

        return jsonify({
            "appointment_id": appointment.id,
            "status": appointment.status.value if hasattr(appointment.status,'value') else appointment.status,
            "message": "Appointment completed successfully"
        }), 200
    
    
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@doctor_bp.route("/medicines", methods=["GET"])
@jwt_required()
def get_medicines_route():
    try:
        if not doctor_only():
            return jsonify({"error": "Forbidden"}), 403
        
        medicines = get_all_medicines()
        return jsonify(medicines), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
@doctor_bp.route("/tests", methods=["GET"])
@jwt_required()
def get_tests_route():
    try:
        if not doctor_only():
            return jsonify({"error": "Forbidden"}), 403
        
        tests = get_all_tests()
        return jsonify(tests), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 400

