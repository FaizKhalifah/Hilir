# app/controllers/parent_controller.py

from flask import Blueprint, request, jsonify
from app.services.parent_service import ParentService
from app.models.parent import Parent
from app.utils.db import db
from app.utils.email_utils import send_otp_email
from app.utils.jwt_utils import generate_parent_jwt_token, parent_required
from werkzeug.security import generate_password_hash, check_password_hash
from app.services.child_service import ChildService
from app.services.personalization_service import PersonalizationService
from app.services.psychologist_service import PsychologistService
from app.repositories.parent_repository import ParentRepository

parent_bp = Blueprint("parent_bp", __name__)

@parent_bp.route("/register", methods=["POST"])
def register():
    data = request.json
    required_fields = ["username", "email", "password"]
    if not all(field in data for field in required_fields):
        return jsonify({"error": "All fields are required"}), 400

    # Create the parent account and handle OTP generation within the service
    parent = ParentService.register_parent(data)

    return jsonify({
        "id": parent.id,
        "username": parent.username,
        "email": parent.email,
        "message": "Registration successful! Check your email for OTP."
    }), 201


# Confirm OTP
@parent_bp.route("/confirm_otp", methods=["POST"])
def confirm_otp():
    data = request.json
    email = data.get("email")
    otp_code = data.get("otp_code")
    
    if not email or not otp_code:
        return jsonify({"error": "Email and OTP code are required"}), 400

    parent = Parent.query.filter_by(email=email).first()
    if not parent:
        return jsonify({"error": "Invalid email"}), 400

    if not ParentService.confirm_otp(parent.id, otp_code):
        return jsonify({"error": "Invalid or expired OTP"}), 400

    parent.is_verified = True
    db.session.commit()
    return jsonify({"message": "OTP confirmed. Account verified."}), 200

@parent_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")
    
    parent = Parent.query.filter_by(email=email).first()
    if not parent or not parent.check_password(password):
        return jsonify({"error": "Invalid credentials"}), 401
    if not parent.is_verified:
        return jsonify({"error": "Account not verified"}), 401

    token = generate_parent_jwt_token(parent)
    return jsonify({"message": "Login successful", "token": token}), 200


# Get all parents
@parent_bp.route("/all_parents", methods=["GET"])
def get_all_parents():
    parents = Parent.query.all()
    return jsonify([{"id": p.id, "email": p.email, "username": p.username} for p in parents]), 200

# Resend OTP
@parent_bp.route("/resend_otp", methods=["POST"])
def resend_otp():
    data = request.json
    email = data.get("email")

    if not email:
        return jsonify({"error": "Email is required"}), 400

    parent, message = ParentService.resend_otp(email)

    if not parent:
        return jsonify({"error": message}), 404

    return jsonify({"message": message}), 200

# Child-related routes
@parent_bp.route("/create_child", methods=["POST"])
@parent_required
def create_child():
    data = request.json
    
    child_data = {
        "name": data.get("name"),
        "date_of_birth": data.get("date_of_birth"),
        "gender": data.get("gender")
    }

    # Retrieve the parent_id from the JWT token
    parent_id = request.parent_id

    if not all(child_data.values()):
        return jsonify({"error": "Name, date_of_birth, and gender are required"}), 400

    child = ChildService.create_child(parent_id, child_data)
    return jsonify({
        "message": "Child created successfully",
        "child_id": child.id,
        "name": child.name,
        "gender": child.gender,
        "date_of_birth": str(child.date_of_birth),
        "age": child.age
    }), 201


@parent_bp.route("/get_child_detail/<int:child_id>", methods=["GET"])
@parent_required
def get_child_detail(child_id):
    parent_id = request.parent_id  # Retrieved from JWT

    # Check if the child belongs to the requesting parent
    if not ChildService.is_child_owned_by_parent(child_id, parent_id):
        return jsonify({"error": "Access denied: Child does not belong to this parent"}), 403

    # Fetch the child details
    child = ChildService.get_child_detail(parent_id, child_id)
    if not child:
        return jsonify({"error": "Child not found"}), 404

    child_data = {
        "id": child.id,
        "name": child.name,
        "date_of_birth": str(child.date_of_birth),
        "age": child.age,
        "gender": child.gender
    }
    return jsonify(child_data), 200


@parent_bp.route("/get_all_children", methods=["GET"])
@parent_required
def get_all_children():
    parent_id = request.parent_id  # Retrieved from JWT
    children = ChildService.get_all_children(parent_id)

    children_data = [
        {
            "id": child.id,
            "name": child.name,
            "date_of_birth": str(child.date_of_birth),
            "age": child.age,
            "gender": child.gender
        } for child in children if child.parent_id == parent_id
    ]
    return jsonify(children_data), 200


@parent_bp.route("/answer_questions/<int:child_id>", methods=["POST"])
@parent_required
def answer_questions(child_id):
    parent_id = request.parent_id  # Retrieved from JWT

    # Check if the child belongs to the requesting parent
    if not ChildService.is_child_owned_by_parent(child_id, parent_id):
        return jsonify({"error": "Access denied: Child does not belong to this parent"}), 403

    data = request.json
    answers = data.get("answers")  # Expected to be a list of {"question_id": int, "response_score": int}
    
    if not answers:
        return jsonify({"error": "Answers are required"}), 400
    
    for answer in answers:
        question_id = answer["question_id"]
        response_score = answer["response_score"]
        PersonalizationService.save_response(child_id, question_id, response_score)
    
    issues_above_threshold = PersonalizationService.calculate_score(child_id)
    
    return jsonify({
        "message": "Answers recorded and scores calculated",
        "issues_above_threshold": issues_above_threshold
    }), 200

@parent_bp.route("/get_child_report/<int:child_id>", methods=["GET"])
@parent_required
def get_child_report(child_id):
    parent_id = request.parent_id  # Retrieved from JWT

    # Check if the child belongs to the requesting parent
    if not ChildService.is_child_owned_by_parent(child_id, parent_id):
        return jsonify({"error": "Access denied: Child does not belong to this parent"}), 403

    # Fetch the report from the service
    report, error = ChildService.get_child_mental_health_report(child_id)
    
    if error:
        return jsonify({"error": error}), 404
    
    return jsonify(report), 200

@parent_bp.route("/<int:child_id>/all_psychologists", methods=["GET"])
@parent_required
def get_all_psychologists_for_parent(child_id):
    # Ensure that the parent has access to the child
    parent_id = request.parent_id  # Retrieved from JWT token
    if not ChildService.is_child_owned_by_parent(child_id, parent_id):
        return jsonify({"error": "Access denied: Child does not belong to this parent"}), 403

    # Fetch all psychologists that can be viewed by a parent
    psychologists = PsychologistService.get_all_psychologists()
    psychologists_data = [
        {
            "id": psychologist.id,
            "full_name": psychologist.full_name,
            "email": psychologist.email,
            "specialization": psychologist.specialization,
            "bio": psychologist.bio
        } for psychologist in psychologists
    ]
    return jsonify(psychologists_data), 200