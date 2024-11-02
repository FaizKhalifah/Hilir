# app/controllers/psychologist_controller.py

from flask import Blueprint, request, jsonify
from app.services.psychologist_service import PsychologistService
from app.utils.jwt_utils import generate_psychologist_jwt_token, parent_required, psychologist_required

psychologist_bp = Blueprint("psychologist_bp", __name__)
parent_bp = Blueprint("parent_bp", __name__)

# Register psychologist
@psychologist_bp.route("/register", methods=["POST"])
def register_psychologist():
    data = request.json
    required_fields = ["full_name", "email", "password", "specialization"]
    if not all(field in data for field in required_fields):
        return jsonify({"error": "All fields are required"}), 400

    psychologist = PsychologistService.register_psychologist(data)
    return jsonify({
        "id": psychologist.id,
        "full_name": psychologist.full_name,
        "email": psychologist.email,
        "specialization": psychologist.specialization,
        "message": "Registration successful!"
    }), 201

# Login psychologist
@psychologist_bp.route("/login", methods=["POST"])
def login_psychologist():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    psychologist = PsychologistService.authenticate_psychologist(email, password)
    if not psychologist:
        return jsonify({"error": "Invalid credentials"}), 401

    # Generate JWT for psychologist
    token = generate_psychologist_jwt_token(psychologist)
    return jsonify({"message": "Login successful", "token": token}), 200

# Psychologist-specific route (for psychologists only)
@psychologist_bp.route("/psychologist-only-data", methods=["GET"])
@psychologist_required
def get_psychologist_data():
    return jsonify({"message": "This data is only for psychologists"})

# Get all children for a psychologist with paid consultations
# Get all children associated with a psychologist’s paid consultations
@psychologist_bp.route("/all_children", methods=["GET"])
@psychologist_required
def get_all_children_for_psychologist():
    psychologist_id = request.psychologist_id  # Retrieved from JWT

    # Fetch all children associated with the psychologist
    children = PsychologistService.get_all_children_for_psychologist(psychologist_id)
    return jsonify(children), 200

# Get details for a specific child for a psychologist with paid consultations
@psychologist_bp.route("/child/<int:child_id>/report", methods=["GET"])
@psychologist_required
def get_child_report_for_psychologist(child_id):
    psychologist_id = request.psychologist_id  # Retrieved from JWT

    # Fetch child report
    report, error = PsychologistService.get_child_mental_health_report_for_psychologist(psychologist_id, child_id)
    if error:
        return jsonify({"error": error}), 403

    return jsonify(report), 200