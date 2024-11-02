# app/controllers/parent_controller.py

from flask import Blueprint, request, jsonify
from app.services.parent_service import ParentService
from app.models.parent import Parent
from app.utils.db import db
from app.utils.jwt_utils import generate_parent_jwt_token, parent_required
from app.services.child_service import ChildService
from app.services.personalization_service import PersonalizationService
from app.services.psychologist_service import PsychologistService
from app.services.consultation_service import ConsultationService
from app.repositories.exercise_repository import ExerciseRepository
from datetime import date
from app.services.assessment_service import AssessmentService
from app.utils.gemini_api import GeminiAPI
from app.repositories.child_repository import ChildRepository
from app.services.chatbot_service import ChatbotService

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


@parent_bp.route("/child/<int:child_id>/available_exercises", methods=["GET"])
@parent_required
def get_available_exercises_for_child(child_id):
    parent_id = request.parent_id  # Retrieved from JWT

    # Check if the child belongs to the requesting parent
    if not ChildService.is_child_owned_by_parent(child_id, parent_id):
        return jsonify({"error": "Access denied: Child does not belong to this parent"}), 403

    # Retrieve available exercises
    exercises, error = ChildService.get_available_exercises_for_child(child_id)
    if error:
        return jsonify({"error": error}), 404

    return jsonify(exercises), 200

@parent_bp.route("/child/<int:child_id>/assessment/<int:assessment_id>/complete", methods=["POST"])
@parent_required
def complete_assessment(child_id, assessment_id):
    parent_id = request.parent_id  # Retrieved from JWT

    # Ensure the child belongs to the parent
    if not ChildService.is_child_owned_by_parent(child_id, parent_id):
        return jsonify({"error": "Access denied: Child does not belong to this parent"}), 403

    # Complete the assessment and generate questions for the parent
    assessment, questions, error = ChildService.complete_assessment_and_generate_questions(child_id, assessment_id)
    if error:
        return jsonify({"error": error}), 404

    return jsonify({
        "message": "Assessment marked as completed",
        "assessment": {
            "child_id": assessment.child_id,
            "psychologist_id": assessment.psychologist_id,
            "task_description": assessment.task_description,
            "is_completed": assessment.is_completed
        },
        "evaluation_questions": questions
    }), 200
    
@parent_bp.route("/child/<int:child_id>/submit_responses", methods=["POST"])
@parent_required
def submit_responses(child_id):
    parent_id = request.parent_id  # Retrieved from JWT

    # Check if the child belongs to the requesting parent
    if not ChildService.is_child_owned_by_parent(child_id, parent_id):
        return jsonify({"error": "Access denied: Child does not belong to this parent"}), 403

    data = request.json.get("responses", [])  # Expected: [{"question_id": int, "response_score": int}]
    if not data:
        return jsonify({"error": "Responses are required"}), 400

    # Apply impacts for each response
    for response in data:
        question_id = response["question_id"]
        response_score = response["response_score"]
        ChildService.apply_response_impact(child_id, question_id, response_score)

    return jsonify({"message": "Responses submitted and mental health scores updated"}), 200

@parent_bp.route("/child/<int:child_id>/psychologist/<int:psychologist_id>", methods=["GET"])
@parent_required
def get_psychologist_detail(child_id, psychologist_id):
    parent_id = request.parent_id  # Retrieved from JWT

    # Check if the child belongs to the requesting parent
    if not ChildService.is_child_owned_by_parent(child_id, parent_id):
        return jsonify({"error": "Access denied: Child does not belong to this parent"}), 403

    # Fetch the psychologist details, including the schedule
    psychologist_data, error = PsychologistService.get_psychologist_details(psychologist_id)
    if error:
        return jsonify({"error": error}), 404

    return jsonify(psychologist_data), 200

@parent_bp.route("/child/<int:child_id>/psychologist/<int:psychologist_id>/book_consultation", methods=["POST"])
@parent_required
def book_consultation(child_id, psychologist_id):
    parent_id = request.parent_id  # Retrieved from JWT

    # Check if the child belongs to the requesting parent
    if not ChildService.is_child_owned_by_parent(child_id, parent_id):
        return jsonify({"error": "Access denied: Child does not belong to this parent"}), 403

    data = request.json
    consultation_date = data.get("consultation_date")
    start_time = data.get("start_time")
    end_time = data.get("end_time")

    # Validate required fields
    if not all([consultation_date, start_time, end_time]):
        return jsonify({"error": "Consultation date, start time, and end time are required"}), 400

    # Book consultation through the service
    consultation, error = ConsultationService.book_consultation(
        child_id=child_id,
        psychologist_id=psychologist_id,
        consultation_date=consultation_date,
        start_time=start_time,
        end_time=end_time
    )

    if error:
        return jsonify({"error": error}), 400

    return jsonify({
        "message": "Consultation booked successfully",
        "consultation_id": consultation.id,
        "consultation_date": str(consultation.consultation_date),
        "start_time": str(consultation.start_time),
        "end_time": str(consultation.end_time)
    }), 201
    
@parent_bp.route("/child/<int:child_id>/assign_exercises", methods=["POST"])
@parent_required
def assign_exercises_to_child(child_id):
    parent_id = request.parent_id  # Retrieved from JWT

    # Verify the child belongs to the requesting parent
    if not ChildService.is_child_owned_by_parent(child_id, parent_id):
        return jsonify({"error": "Access denied: Child does not belong to this parent"}), 403

    # Assign exercises using Gemini API
    exercises, error = ChildService.assign_exercises_based_on_issues(child_id)
    if error:
        return jsonify({"error": error}), 400

    return jsonify({
        "message": "Exercises assigned successfully",
        "exercises": [
            {"title": exercise["title"], "description": exercise["description"]}
            for exercise in exercises
        ]
    }), 200



@parent_bp.route('/child/<int:childid>/exercise', methods=['POST'])
@parent_required
def child_chat(childid):
    parent_id = request.parent_id
    
    # Verify if the child belongs to the requesting parent
    if not ChildService.is_child_owned_by_parent(childid, parent_id):
        return jsonify({"error": "Access denied: Child does not belong to this parent"}), 403

    # Generate exercises for the child based on mental health issues above threshold
    exercises, error = ChildService.assign_exercises_based_on_issues(childid)
    
    if error:
        return jsonify({"error": error}), 500

    # Store exercises in database
    stored_exercises = []
    db_errors = []
    
    for exercise in exercises:
        stored_exercise, db_error = ExerciseRepository.create_exercise_with_child(
            title=exercise["title"],
            description=exercise["description"],
            mental_health_issue_id=exercise["mental_health_issue_id"],
            child_id=childid
        )
        
        if db_error:
            db_errors.append(db_error)
        elif stored_exercise:
            stored_exercises.append({
                "id": stored_exercise.id,
                "title": stored_exercise.title,
                "description": stored_exercise.description,
                "mental_health_issue_id": stored_exercise.mental_health_issue_id,
                "assigned_date": date.today().isoformat()
            })

    # If there were any database errors, include them in the response
    response_data = {
        "childid": childid,
        "exercises": stored_exercises,
    }
    
    if db_errors:
        response_data["warnings"] = db_errors

    # Return success even if some exercises failed to store
    status_code = 207 if db_errors else 200  # 207 Multi-Status if partial success
    return jsonify(response_data), status_code

@parent_bp.route('/child/<int:child_id>/assessment', methods=['POST'])
@parent_required
def generate_and_assign_assessments(child_id):
    """
    Generates and assigns multiple assessments for a child based on mental health needs.
    """
    # Retrieve mental health issues that exceed the threshold (limit to 3)
    child_personalizations = ChildRepository.get_child_personalizations(child_id)
    exceeded_issues = [
        {"id": personalization.mental_health_issue_id, "name": personalization.mental_health_issue.name}
        for personalization in child_personalizations
        if personalization.personalization_score >= personalization.mental_health_issue.threshold_score
    ][:3]

    if not exceeded_issues:
        return jsonify({"error": "No mental health issues exceed the threshold for an assessment."}), 400

    # Generate prompts for each mental health issue
    prompts = AssessmentService.generate_assessment_prompts(exceeded_issues)
    assessments = []
    db_errors = []

    # Generate an assessment for each prompt
    for prompt, issue in zip(prompts, exceeded_issues):
        # Get task description from Gemini API
        response_json, error = GeminiAPI.get_exercises_for_prompt(prompt)
        if error:
            db_errors.append(f"Failed to fetch assessment for {issue['name']} from Gemini API: {error}")
            continue

        # Parse response for task description
        task_description = response_json.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "").strip()
        if not task_description:
            db_errors.append(f"No valid task description for {issue['name']}.")
            continue

        # Create and save the assessment
        assessment, db_error = AssessmentService.create_assessment_for_child(
            child_id=child_id,
            task_description=task_description,
            days_to_complete=7
        )
        
        if db_error:
            db_errors.append(f"Database error for {issue['name']}: {db_error}")
        elif assessment:
            assessments.append({
                "assessment_id": assessment.id,
                "task_description": assessment.task_description,
                "due_date": assessment.due_date.isoformat(),
                "mental_health_issue_id": issue["id"],
                "mental_health_issue_name": issue["name"]
            })

    # If there were errors, include them in the response
    response_data = {
        "child_id": child_id,
        "assessments": assessments,
    }
    if db_errors:
        response_data["warnings"] = db_errors

    status_code = 207 if db_errors else 200  # 207 Multi-Status if partial success
    return jsonify(response_data), status_code

@parent_bp.route('/child/<int:child_id>/chat', methods=['POST'])
@parent_required
def chat_with_bot(child_id):
    """
    Chatbot route to assist parents by answering questions based on the child’s mental health data.
    """
    # Retrieve the message from the parent
    parent_message = request.json.get("message")
    if not parent_message:
        return jsonify({"error": "Message is required"}), 400

    # Use parent_id from JWT token
    parent_id = request.parent_id

    # Fetch child’s mental health issues that exceed the threshold
    child_personalizations = ChildRepository.get_child_personalizations(child_id)
    mental_health_issues = [
        {"id": personalization.mental_health_issue_id, "name": personalization.mental_health_issue.name}
        for personalization in child_personalizations
        if personalization.personalization_score >= personalization.mental_health_issue.threshold_score
    ]
    
    if not mental_health_issues:
        return jsonify({"error": "No mental health issues exceed the threshold for this child."}), 400

    # Generate chatbot prompt with child’s mental health context
    prompt = ChatbotService.generate_chatbot_prompt(parent_message, mental_health_issues)

    # Get chatbot response using Gemini API
    response_json, error = GeminiAPI.get_exercises_for_prompt(prompt)
    if error:
        return jsonify({"error": f"Failed to fetch response from Gemini API: {error}"}), 500

    # Extract response text
    bot_response = response_json.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "").strip()
    if not bot_response:
        return jsonify({"error": "No valid response could be parsed from the chatbot."}), 500

    return jsonify({"bot_response": bot_response}), 200