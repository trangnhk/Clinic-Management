from flask import Blueprint, request, jsonify
from app.modules.patient.dao import *
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from datetime import date
from app.models import AppointmentStatusEnum
from app.config.config import BusinessConfig
from app.modules.doctor.dao import get_doctor_by_user_id, get_avg_rating_by_doctor_id

patient_bp = Blueprint("patient_api", __name__)

def patient_only():
    try:
        claims = get_jwt()
        return claims.get("role") == "PATIENT"
    except:
        return False

# FLOW BOOK APPOINTMENT
@patient_bp.route("/specializations", methods=["GET"])
def get_specializations():
    """
    Get all specializations (Danh sách chuyên khoa)
    ---
    tags:
      - Patient
    responses:
      200:
        description: Danh sách chuyên khoa
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
                example: 1
              name:
                type: string
                example: "Cardiology"
    """
    specs = get_all_specialization()

    return jsonify([
        {
            "id": s.id,
            "name": s.name
        } for s in specs
    ])

@patient_bp.route("/doctors", methods=["GET"])
def get_doctors():
    """
    Get doctors (Lấy danh sách bác sĩ)
    ---
    tags:
      - Patient
    parameters:
      - name: specialization_id
        in: query
        type: integer
        required: false
        description: Lọc theo ID chuyên khoa (bỏ trống để lấy tất cả)
    responses:
      200:
        description: Danh sách bác sĩ
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
                example: 2
              name:
                type: string
                example: "BS. Nguyễn Minh Khoa"
              specialization:
                type: string
                nullable: true
                example: "Cardiology"
              avatar:
                type: string
                nullable: true
                example: "https://example.com/avatar.png"
              rating:
                type: integer
                example: 5
      400:
        description: specialization_id không phải số nguyên
    """
    specialization_id = request.args.get("specialization_id")
    if specialization_id:
      try:
          specialization_id = int(specialization_id)
      except:
          return jsonify({"error": "Invalid specialization_id"}), 400
      
    doctors = get_doctor_by_specialization(specialization_id)

    return jsonify([
        {
            "id": d.id,
            "name": d.user.fullname if d.user else None,
            "specialization": d.specialization.name if d.specialization else None,
            "avatar": d.user.avatar if hasattr(d.user, "avatar") else None,
            "rating": d.rating if hasattr(d, "rating") else 5
        }
        for d in doctors
    ])

@patient_bp.route("/doctors/<int:id>", methods=["GET"])
def get_doctor_detail(id):
    """
    Get doctor detail (Xem chi tiết bác sĩ)
    ---
    tags:
      - Patient
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID bác sĩ
    responses:
      200:
        description: Thông tin chi tiết bác sĩ
        schema:
          type: object
          properties:
            id:
              type: integer
              example: 2
            name:
              type: string
              nullable: true
              example: "BS. Nguyễn Minh Khoa"
            specialization:
              type: string
              nullable: true
              example: "Cardiology"
            avatar:
              type: string
              nullable: true
              example: "https://example.com/avatar.png"
            rating:
              type: number
              nullable: true
              example: 4.5
            introduce:
              type: string
              nullable: true
              example: "Bác sĩ có 10 năm kinh nghiệm"
            total_reviews:
              type: integer
              example: 12
      404:
        description: Không tìm thấy bác sĩ
    """
    doctor = Doctor.query.get(id)

    if not doctor:
        return jsonify({"error": "Doctor not found"}), 404
    
    rating = get_avg_rating_by_doctor_id(id)
    
    return jsonify({
        "id": doctor.id,
        "name": doctor.user.fullname if doctor.user is not None else None,
        "specialization": doctor.specialization.name if doctor.specialization is not None else None,
        "avatar": doctor.user.avatar if doctor.user is not None else None,
        "rating": rating,
        "introduce": doctor.description,
        "total_reviews": len(doctor.reviews)
    })

@patient_bp.route("/timeslots", methods=["GET"])
def get_timeslots():
    """
    Get available timeslots (Lấy lịch trống)
    ---
    tags:
      - Patient
    parameters:
      - name: doctor_id
        in: query
        type: integer
        required: true
        example: 2
      - name: date
        in: query
        type: string
        required: true
        example: "2026-04-15"
    responses:
      200:
        description: Danh sách timeslot
        schema:
          type: array
          items:
            type: object
            properties:
              schedule_id:
                type: integer
                example: 5
              start_time:
                type: string
                example: "08:00"
              end_time:
                type: string
                example: "09:00"
              available:
                type: boolean
                example: true
      400:
        description: Thiếu tham số
    """
    try:
      try:
          doctor_id = int(request.args.get("doctor_id"))
      except:
          return jsonify({"error": "doctor_id must be integer"}), 400
      date = request.args.get("date")

      if not doctor_id or not date:
          return jsonify({"error": "Missing parameters"}), 400
      try:
          date_obj = datetime.strptime(date, "%Y-%m-%d").date()
      except:
          return jsonify({"error": "Invalid date format"}), 400

      timeslots = get_availables_timeslots(doctor_id, date)

      return jsonify(timeslots)
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

@patient_bp.route("/appointments", methods=["POST"])
@jwt_required()
def book_appointment():
    """
    Book appointment (Đặt lịch khám)
    ---
    tags:
      - Patient
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - patient_id
            - doctor_id
            - schedule_id
            - date
          properties:
            patient_id:
              type: integer
              example: 1
            doctor_id:
              type: integer
              example: 2
            schedule_id:
              type: integer
              example: 5
            date:
              type: string
              example: "2026-04-15"
            notes:
              type: string
              example: "Đau đầu"
    responses:
      200:
        description: Đặt lịch thành công
        schema:
          type: object
          properties:
            id:
              type: integer
              example: 10
            patient_name:
              type: string
              example: "Nguyen Van A"
            doctor_name:
              type: string
              example: "Dr. Strange"
            date:
              type: string
              example: "2026-04-15"
            status:
              type: string
              example: "PENDING_PAYMENT"
            payment:
              type: string
              example: "PENDING"
      400:
        description: Thiếu hoặc sai dữ liệu
      403:
        description: Không có quyền
      404:
        description: Không tìm thấy bệnh nhân
    """
    data = request.json

    try:
        current_user = get_jwt_identity()

        if not patient_only():
            return jsonify({"error": "Forbidden"}), 403
        
        patient = Patient.query.filter_by(user_id=current_user).first()

        if not data.get("doctor_id") or not data.get("schedule_id") or not data.get("date"):
            return jsonify({"error": "Missing required fields"}), 400
        
        appt = create_appointment(
            patient.id,   
            data["doctor_id"],
            data["schedule_id"],
            data["date"],
            data.get("notes")
        )

        return jsonify({
            "id": appt.id,
            "patient_name": appt.patient.user.username,
            "doctor_name": appt.doctor.user.username,
            "date": str(appt.date),
            "status": appt.status,
            "payment": appt.payment_status
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

@patient_bp.route("/payments", methods=["POST"])
@jwt_required()
def payment():
  """
  Make payment for appointment (Thanh toán lịch khám)
  ---
  tags:
    - Patient
  parameters:
    - in: body
      name: body
      required: true
      schema:
        type: object
        required:
          - appointment_id
          - amount
        properties:
          appointment_id:
            type: integer
            example: 10
          amount:
            type: number
            example: 150.0
  responses:
    200:
      description: Thanh toán thành công
      schema:
        type: object
        properties:
          payment_id:
            type: integer
            example: 5
          status:
            type: string
            enum: [PENDING, PAID, FAILED]
            example: "PAID"
          amount:
            type: number
            example: 150.0
          payment_type:
            type: string
            enum: [DEPOSIT, FINAL, MEDICINE, LAB_TEST]
            example: "DEPOSIT"
    400:
      description: |
        - Thiếu appointment_id hoặc amount
        - Lỗi xử lý thanh toán
    403:
      description: Không có quyền truy cập
  """
  if not patient_only():
      return jsonify({"error": "Forbidden"}), 403

  data = request.get_json() or {}

  if "appointment_id" not in data or "amount" not in data:
      return jsonify({"error": "Missing required fields"}), 400

  try:
      current_user = get_jwt_identity()

      payment = make_payment(
          appointment_id=data["appointment_id"],
          amount=data["amount"],
          user_id=current_user
      )

      return jsonify({
          "payment_id": payment.id,
          "status": payment.status.value,
          "amount": payment.amount,
          "payment_type": payment.payment_type.value
      }), 200

  except Exception as e:
      db.session.rollback()
      return jsonify({"error": str(e)}), 400
    
# FLOW CHECK APPOINTMENT STATUS
@patient_bp.route("/appointments", methods=["GET"])
@jwt_required()
def get_appts():
    """
    Get patient appointments (Xem lịch đã đặt)
    ---
    tags:
      - Patient
    parameters:
      - name: status
        in: query
        type: string
        required: false
        description: |
          Filter theo trạng thái lịch khám
        enum:
          - WAITING_EXAMINATION
          - PENDING_PAYMENT
          - PENDING_RESULT
          - COMPLETED
          - CANCELED
    responses:
      200:
        description: Danh sách lịch khám
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
                example: 2
              date:
                type: string
                example: "2026-04-15"
              status:
                type: string
                example: "COMPLETED"
    """
    current_user = get_jwt_identity()

    if not patient_only():
        return jsonify({"error": "Forbidden"}), 403

    patient = Patient.query.filter_by(user_id=current_user).first()
    
    status = request.args.get("status")

    if status:
        status = status.upper()
        valid_status = [s.value for s in AppointmentStatusEnum]

        if status not in valid_status:
            return jsonify({"error": f"Invalid status. Must be one of {valid_status}"}), 400

    appts = get_patient_appointments(patient.id, status)

    return jsonify([{
        "id": a.id,
        "date": str(a.date),
        "status": a.status
    } for a in appts])

@patient_bp.route("/appointments/<int:id>", methods=["GET"])
@jwt_required()
def get_appointment_detail(id):
    """
    Get appointment detail (Xem chi tiết lịch khám)
    ---
    tags:
      - Patient
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID của lịch khám
    responses:
      200:
        description: Chi tiết lịch khám
        schema:
          type: object
          properties:
            id:
              type: integer
              example: 10
            patient_name:
              type: string
              example: "Nguyen Van A"
            doctor_name:
              type: string
              example: "Dr. B"
            date:
              type: string
              example: "2026-04-15"
            status:
              type: string
              example: "BOOKED"
            notes:
              type: string
              example: "Đau đầu"
      403:
        description: Không có quyền truy cập
      404:
        description: Không tìm thấy lịch khám
    """

    current_user = get_jwt_identity()

    if not patient_only():
        return jsonify({"error": "Forbidden"}), 403

    patient = Patient.query.filter_by(user_id=current_user).first()

    appt = Appointment.query.get(id)
    if not appt:
      return jsonify({"error": "Appointment not found"}), 404

    if appt.patient_id != patient.id:
        return jsonify({"error": "Not your appointment"}), 403
    
    return jsonify(get_appointment_detail_dao(appt, current_user))

@patient_bp.route("/appointments/<int:id>/cancel", methods=["PATCH"])
@jwt_required()
def cancel_appt(id):
    """
    Cancel appointment (Huỷ lịch khám)
    ---
    tags:
      - Patient
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID lịch khám cần huỷ
    responses:
      200:
        description: Huỷ lịch thành công
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Canceled successfully"
      400:
        description: |
          - Không thể huỷ lịch đã COMPLETED / CANCELED
          - Lịch khám không tồn tại
      403:
        description: Không có quyền truy cập
    """
    if not patient_only():
        return jsonify({"error": "Forbidden"}), 403

    try:
        current_user = get_jwt_identity()

        cancel_appointment(id, current_user)

        return jsonify({
            "message": "Canceled successfully"
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

# FLOW PROFILE
@patient_bp.route("/profile", methods=["GET"])
@jwt_required()
def get_profile():
  """
  Get patient profile (Xem thông tin cá nhân + lịch sử khám)
  ---
  tags:
    - Patient
  parameters:
    - name: page
      in: query
      type: integer
      required: false
      default: 1
      description: Trang hiện tại
    - name: per_page
      in: query
      type: integer
      required: false
      default: 10
      description: Số bản ghi mỗi trang (tối đa theo MAX_PER_PAGE)
  responses:
    200:
      description: Thông tin bệnh nhân và lịch sử khám
      schema:
        type: object
        properties:
          profile:
            type: object
            properties:
              id:
                type: integer
                example: 1
              fullname:
                type: string
                example: "Nguyen Van A"
              gender:
                type: string
                example: "MALE"
              phone:
                type: string
                example: "0901234567"
          medical_history:
            type: object
            properties:
              items:
                type: array
                items:
                  type: object
                  properties:
                    date:
                      type: string
                      example: "2026-04-15"
                    doctor:
                      type: string
                      example: "BS. Nguyễn Minh Khoa"
                    status:
                      type: string
                      example: "COMPLETED"
                    payment:
                      type: string
                      example: "PAID"
                    start_time:
                      type: string
                      example: "08:00"
                    end_time:
                      type: string
                      example: "09:00"
              pagination:
                type: object
                properties:
                  page:
                    type: integer
                    example: 1
                  per_page:
                    type: integer
                    example: 10
                  total:
                    type: integer
                    example: 25
    400:
      description: |
        - page < 1
        - per_page không hợp lệ
    403:
      description: Không có quyền truy cập
  """
  try:
      current_user = get_jwt_identity()

      if not patient_only():
          return jsonify({"error": "Forbidden"}), 403
      
      page = request.args.get("page", BusinessConfig.DEFAULT_PAGE, type=int)
      per_page = request.args.get("per_page", BusinessConfig.DEFAULT_PER_PAGE, type=int)

      if page < 1:
          return jsonify({"error": "Invalid page"}), 400

      if per_page < 1 or per_page > BusinessConfig.MAX_PER_PAGE:
          return jsonify({"error": "Invalid per_page"}), 400
      per_page = min(per_page, BusinessConfig.MAX_PER_PAGE)
      
      data = get_patient_profile(
          user_id=current_user, 
          page=page,
          per_page=per_page
          )

      return jsonify({
          "profile": data["profile"],
          "medical_history": {
              "items": [
                  {
                      "id": a.id,
                      "date": str(a.date),
                      "doctor": a.doctor.user.fullname,
                      "status": a.status,
                      "payment": a.payment_status,
                      "start_time": str(a.timeslot.start_time),
                      "end_time": str(a.timeslot.end_time)
                  }
                  for a in data["appointments"]
              ],
              "pagination": data["pagination"]
          },
          "laboratory_results": data["laboratory_results"]
      })

  except ValueError as e:
      db.session.rollback()
      return jsonify({"error": str(e)}), 400
    
@patient_bp.route("/profile", methods=["PATCH"])
@jwt_required()
def update_profile():
    """
    Update patient profile (Cập nhật hồ sơ bệnh nhân)
    ---
    tags:
      - Patient
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            fullname:
              type: string
              example: "Nguyen Van A"
            date_of_birth:
              type: string
              example: "2002-05-10"
            address:
              type: string
              example: "Ho Chi Minh City"
            phone_number:
              type: string
              example: "0901234567"
    responses:
      200:
        description: Cập nhật thành công
        schema:
          type: object
          properties:
            patient_id:
              type: integer
              example: 1
            fullname:
              type: string
              example: "Nguyen Van A"
            address:
              type: string
              example: "Ho Chi Minh City"
            date_of_birth:
              type: string
              example: "2002-05-10"
            phone_number:
              type: string
              example: "0901234567"
            email:
              type: string
              example: "patient@gmail.com"
      400:
        description: |
          - Field không hợp lệ
          - Sai dữ liệu đầu vào
      403:
        description: Không có quyền truy cập
    """
    
    # data = request.json
    data = request.get_json() or {}

    try:
        current_user = get_jwt_identity()

        if not patient_only():
            return jsonify({"error": "Forbidden"}), 403
        
        allowed_fields = ["fullname", "date_of_birth", "address", "phone_number"]
        for key in data.keys():
            if key not in allowed_fields:
                return jsonify({"error": f"You can not update {key}"}), 400
            
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        profile = update_patient_profile(
            user_id=current_user,
            fullname=data.get("fullname"),
            date_of_birth=data.get("date_of_birth"),
            address=data.get("address"),
            phone_number=data.get("phone_number")
        )

        return jsonify({
            "fullname": profile.user.fullname,
            "address": profile.address,
            "date_of_birth": str(profile.date_of_birth) if profile.date_of_birth else None,
            "patient_id": profile.id,
            "phone_number": profile.user.phone_number,
            "email": profile.user.email        
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
    
# FLOW MEDICAL HISTORY
@patient_bp.route("/appointments/<int:id>/medical-history", methods=["GET"])
@jwt_required()
def get_medical_history(id):
    """
    Get medical history (Xem bệnh án sau khám)
    ---
    tags:
      - Patient
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID của lịch khám
    responses:
      200:
        description: Thông tin bệnh án
        schema:
          type: object
          properties:
            appointment_id:
              type: integer
              example: 10
            diagnosis:
              type: string
              example: "Viêm họng"
            prescription:
              type: array
              items:
                type: object
                properties:
                  medicine_name:
                    type: string
                    example: "Paracetamol"
                  dosage:
                    type: string
                    example: "2 lần/ngày"
            test_results:
              type: array
              items:
                type: object
                properties:
                  test_name:
                    type: string
                    example: "Blood Test"
                  result:
                    type: string
                    example: "Normal"
      400:
        description: |
          - Appointment chưa hoàn thành
      403:
        description: Không có quyền truy cập
      404:
        description: Không tìm thấy lịch khám
    """
    try:
        current_user = get_jwt_identity()

        if not patient_only():
          return jsonify({"error": "Forbidden"}), 403
        
        patient = Patient.query.filter_by(user_id=current_user).first()

        appt = Appointment.query.get(id)

        if not appt:
          return jsonify({"error": "Appointment not found"}), 404

        if appt.patient_id != patient.id:
          return jsonify({"error": "Forbidden"}), 403
        
        if appt.status != "COMPLETED":
          return jsonify({
              "error": "Medical history not available. Appointment not completed"
          }), 400
        
        data = get_medical_history_detail(appt)

        return jsonify(data)
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

@patient_bp.route("/appointments/<int:id>/review", methods=["POST"])
@jwt_required()
def review(id):
    """
    Create review (Đánh giá bác sĩ sau khám)
    ---
    tags:
      - Patient
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID lịch khám
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - rating
          properties:
            rating:
              type: integer
              minimum: 1
              maximum: 5
              example: 5
            comment:
              type: string
              example: "Bác sĩ rất tận tình"
    responses:
      200:
        description: Đánh giá thành công
        schema:
          type: object
          properties:
            review_id:
              type: integer
              example: 3
            message:
              type: string
              example: "Review success"
      400:
        description: |
          - Appointment không tồn tại
          - Chỉ lịch COMPLETED mới được review
          - Đã review trước đó
      403:
        description: Không có quyền truy cập
    """
    if not patient_only():
        return jsonify({"error": "Forbidden"}), 403

    try:
        current_user = get_jwt_identity()
        data = request.get_json() or {}

        appt = Appointment.query.get(id)
        patient = get_patient_by_user(current_user)

        if not appt:
          return jsonify({"error": "Appointment no found"}), 404

        if appt.patient_id != patient.id:
            return jsonify({"error": "Forbidden"}), 403

        if appt.status != "COMPLETED":
            return jsonify({"error": "Only completed appointment can review"}), 400
        
        if "rating" not in data:
            return jsonify({"error": "Rating is required"}), 400
        
        rv = create_review(
            appt_id=id,
            rating=data["rating"],
            comment=data.get("comment"),
            user_id=current_user
        )

        return jsonify({
            "review_id": rv.id,
            "message": "Review success"
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400

@patient_bp.route("/doctors/<int:id>/reviews", methods=["GET"])
def doctor_reviews(id):
    """
    Get doctor reviews (Xem đánh giá bác sĩ)
    ---
    tags:
      - Patient
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID bác sĩ
    responses:
      200:
        description: Tổng hợp đánh giá và danh sách review của bác sĩ
        schema:
          type: object
          properties:
            doctor_id:
              type: integer
              example: 2
            average_rating:
              type: number
              example: 4.5
            total_reviews:
              type: integer
              example: 20
            rating_breakdown:
              type: object
              description: Số lượng đánh giá theo từng mức sao
              example:
                "1": 0
                "2": 1
                "3": 3
                "4": 7
                "5": 9
            reviews:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                    example: 1
                  rating:
                    type: integer
                    example: 5
                  comment:
                    type: string
                    nullable: true
                    example: "Bác sĩ rất tận tình"
                  created_date:
                    type: string
                    example: "2026-04-27"
      404:
        description: Không tìm thấy bác sĩ
    """
    doctor = Doctor.query.get(id)
    if not doctor:
        return jsonify({"error": "Doctor not found"}), 404
    
    data = get_doctor_reviews(id)

    return jsonify({
        "doctor_id": data["doctor_id"],
        "average_rating": data["average_rating"],
        "total_reviews": data["total_reviews"],
        "rating_breakdown": data["rating_breakdown"],
        "reviews": [
            {
                "id": r.id,
                "rating": r.rating,
                "comment": r.comment,
                "created_date": str(r.created_date)
            }
            for r in data["reviews"]
        ]
    }), 200

    
    


