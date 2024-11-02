from flask import request, jsonify
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

def register():
    data = request.json
    required_fields = ["username", "email", "password"]
    if not all(field in data for field in required_fields):
        return jsonify({"error": "All fields are required"}), 400

    parent = ParentService.register_parent(data)
    return jsonify({
        "id": parent.id,
        "username": parent.username,
        "email": parent.email,
        "message": "Registration successful! Your account is verified."
    }), 201

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

def get_all_parents():
    parents = Parent.query.all()
    return jsonify([{"id": p.id, "email": p.email, "username": p.username} for p in parents]), 200

def resend_otp():
    data = request.json
    email = data.get("email")

    if not email:
        return jsonify({"error": "Email is required"}), 400

    parent, message = ParentService.resend_otp(email)
    if not parent:
        return jsonify({"error": message}), 404

    return jsonify({"message": message}), 200

def create_child():
    data = request.json
    child_data = {
        "name": data.get("name"),
        "date_of_birth": data.get("date_of_birth"),
        "gender": data.get("gender")
    }
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

def get_child_detail(child_id):
    parent_id = request.parent_id
    if not ChildService.is_child_owned_by_parent(child_id, parent_id):
        return jsonify({"error": "Access denied: Child does not belong to this parent"}), 403

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

def get_all_children():
    parent_id = request.parent_id
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

def answer_questions(child_id):
    parent_id = request.parent_id
    if not ChildService.is_child_owned_by_parent(child_id, parent_id):
        return jsonify({"error": "Access denied: Child does not belong to this parent"}), 403

    data = request.json
    answers = data.get("answers")
    
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

def get_child_report(child_id):
    parent_id = request.parent_id
    if not ChildService.is_child_owned_by_parent(child_id, parent_id):
        return jsonify({"error": "Access denied: Child does not belong to this parent"}), 403

    report, error = ChildService.get_child_mental_health_report(child_id)
    
    if error:
        return jsonify({"error": error}), 404
    
    return jsonify(report), 200

def get_all_psychologists_for_parent(child_id):
    parent_id = request.parent_id
    if not ChildService.is_child_owned_by_parent(child_id, parent_id):
        return jsonify({"error": "Access denied: Child does not belong to this parent"}), 403

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

def get_available_exercises_for_child(child_id):
    parent_id = request.parent_id
    if not ChildService.is_child_owned_by_parent(child_id, parent_id):
        return jsonify({"error": "Access denied: Child does not belong to this parent"}), 403

    exercises, error = ChildService.get_available_exercises_for_child(child_id)
    if error:
        return jsonify({"error": error}), 404

    return jsonify(exercises), 200

def complete_assessment(child_id, assessment_id):
    parent_id = request.parent_id
    if not ChildService.is_child_owned_by_parent(child_id, parent_id):
        return jsonify({"error": "Access denied: Child does not belong to this parent"}), 403

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

def submit_responses(child_id):
    parent_id = request.parent_id
    if not ChildService.is_child_owned_by_parent(child_id, parent_id):
        return jsonify({"error": "Access denied: Child does not belong to this parent"}), 403

    data = request.json.get("responses", [])
    if not data:
        return jsonify({"error": "Responses are required"}), 400

    for response in data:
        question_id = response["question_id"]
        response_score = response["response_score"]
        ChildService.apply_response_impact(child_id, question_id, response_score)

    return jsonify({"message": "Responses submitted and mental health scores updated"}), 200

def get_psychologist_detail(child_id, psychologist_id):
    parent_id = request.parent_id
    if not ChildService.is_child_owned_by_parent(child_id, parent_id):
        return jsonify({"error": "Access denied: Child does not belong to this parent"}), 403

    psychologist_data, error = PsychologistService.get_psychologist_details(psychologist_id)
    if error:
        return jsonify({"error": error}), 404

    return jsonify(psychologist_data), 200

def book_consultation(child_id, psychologist_id):
    parent_id = request.parent_id
    if not ChildService.is_child_owned_by_parent(child_id, parent_id):
        return jsonify({"error": "Access denied: Child does not belong to this parent"}), 403

    data = request.json
    consultation_date = data.get("consultation_date")
    start_time = data.get("start_time")
    end_time = data.get("end_time")

    if not all([consultation_date, start_time, end_time]):
        return jsonify({"error": "Consultation date, start time, and end time are required"}), 400

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

def assign_exercises_to_child(child_id):
    parent_id = request.parent_id
    if not ChildService.is_child_owned_by_parent(child_id, parent_id):
        return jsonify({"error": "Access denied: Child does not belong to this parent"}), 403

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

def child_chat(childid):
    parent_id = request.parent_id
    if not ChildService.is_child_owned_by_parent(childid, parent_id):
        return jsonify({"error": "Access denied: Child does not belong to this parent"}), 403

    exercises, error = ChildService.assign_exercises_based_on_issues(childid)
    if error:
        return jsonify({"error": error}), 500

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

    response_data = {
        "childid": childid,
        "exercises": stored_exercises,
    }
    
    if db_errors:
        response_data["warnings"] = db_errors

    status_code = 207 if db_errors else 200
    return jsonify(response_data), status_code

def generate_and_assign_assessments(child_id):
    child_personalizations = ChildRepository.get_child_personalizations(child_id)
    exceeded_issues = [
        {"id": personalization.mental_health_issue_id, "name": personalization.mental_health_issue.name}
        for personalization in child_personalizations
        if personalization.personalization_score >= personalization.mental_health_issue.threshold_score
    ][:3]

    if not exceeded_issues:
        return jsonify({"error": "No mental health issues exceed the threshold for an assessment."}), 400

    prompts = AssessmentService.generate_assessment_prompts(exceeded_issues)
    assessments = []
    db_errors = []

    for prompt, issue in zip(prompts, exceeded_issues):
        response_json, error = GeminiAPI.get_exercises_for_prompt(prompt)
        if error:
            db_errors.append(f"Failed to fetch assessment for {issue['name']} from Gemini API: {error}")
            continue

        task_description = response_json.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "").strip()
        if not task_description:
            db_errors.append(f"No valid task description for {issue['name']}.")
            continue

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

    response_data = {
        "child_id": child_id,
        "assessments": assessments,
    }
    if db_errors:
        response_data["warnings"] = db_errors

    status_code = 207 if db_errors else 200
    return jsonify(response_data), status_code

def chat_with_bot(child_id):
    parent_message = request.json.get("message")
    if not parent_message:
        return jsonify({"error": "Message is required"}), 400

    parent_id = request.parent_id
    child_personalizations = ChildRepository.get_child_personalizations(child_id)
    mental_health_issues = [
        {"id": personalization.mental_health_issue_id, "name": personalization.mental_health_issue.name}
        for personalization in child_personalizations
        if personalization.personalization_score >= personalization.mental_health_issue.threshold_score
    ]
    
    if not mental_health_issues:
        return jsonify({"error": "No mental health issues exceed the threshold for this child."}), 400

    prompt = ChatbotService.generate_chatbot_prompt(parent_message, mental_health_issues)
    response_json, error = GeminiAPI.get_exercises_for_prompt(prompt)
    if error:
        return jsonify({"error": f"Failed to fetch response from Gemini API: {error}"}), 500

    bot_response = response_json.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "").strip()
    if not bot_response:
        return jsonify({"error": "No valid response could be parsed from the chatbot."}), 500

    return jsonify({"bot_response": bot_response}), 200

def show_personalized_questions():
    questions = ParentService.get_personalized_questions()
    return jsonify([
        {"id": q.id, "question": q.question} for q in questions
    ]), 200

def show_all_parents():
    parents = ParentService.get_all_parents()
    return jsonify([
        {"id": p.id, "username": p.username, "email": p.email} for p in parents
    ]), 200