from flask import request, jsonify
from app.services.psychologist_service import PsychologistService
from app.utils.jwt_utils import generate_psychologist_jwt_token
from datetime import datetime
from app.utils.gemini_api import GeminiAPI
from app.services.chatbot_service import ChatbotService
from app.repositories.child_repository import ChildRepository

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

def login_psychologist():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    psychologist = PsychologistService.authenticate_psychologist(email, password)
    if not psychologist:
        return jsonify({"error": "Invalid credentials"}), 401

    token = generate_psychologist_jwt_token(psychologist)
    return jsonify({"message": "Login successful", "token": token}), 200

def get_all_children_for_psychologist():
    psychologist_id = request.psychologist_id
    children = PsychologistService.get_all_children_for_psychologist(psychologist_id)
    return jsonify(children), 200

def get_child_report_for_psychologist(child_id):
    psychologist_id = request.psychologist_id
    report, error = PsychologistService.get_child_mental_health_report_for_psychologist(psychologist_id, child_id)
    if error:
        return jsonify({"error": error}), 403

    return jsonify(report), 200

def add_and_assign_exercise_to_child(child_id):
    psychologist_id = request.psychologist_id
    data = request.json

    required_fields = ["title", "mental_health_issue_id", "assigned_date"]
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Title, mental_health_issue_id, and assigned_date are required"}), 400

    child_exercise, error = PsychologistService.add_and_assign_exercise_to_child(psychologist_id, child_id, data)
    if error:
        return jsonify({"error": error}), 403

    return jsonify({
        "message": "Exercise assigned successfully",
        "child_exercise": {
            "child_id": child_exercise.child_id,
            "exercise_id": child_exercise.exercise_id,
            "assigned_date": str(child_exercise.assigned_date),
            "is_completed": child_exercise.is_completed
        }
    }), 201

def get_exercises_for_specialization():
    psychologist_id = request.psychologist_id
    exercises, error = PsychologistService.get_exercises_for_psychologist(psychologist_id)
    if error:
        return jsonify({"error": error}), 400

    return jsonify(exercises), 200

def add_assessment(child_id):
    psychologist_id = request.psychologist_id
    data = request.json
    required_fields = ["task_description", "due_date", "frequency"]
    if not all(field in data for field in required_fields):
        return jsonify({"error": "task_description, due_date, and frequency are required"}), 400

    assessment, error = PsychologistService.add_assessment(psychologist_id, child_id, data)
    if error:
        return jsonify({"error": error}), 403

    return jsonify({
        "message": "Assessment added successfully",
        "assessment": {
            "child_id": assessment.child_id,
            "psychologist_id": assessment.psychologist_id,
            "task_description": assessment.task_description,
            "due_date": str(assessment.due_date),
            "frequency": assessment.frequency,
            "is_completed": assessment.is_completed
        }
    }), 201

def add_assessment_with_questions(child_id):
    psychologist_id = request.psychologist_id
    data = request.json
    required_fields = ["task_description", "due_date", "frequency", "questions"]
    if not all(field in data for field in required_fields):
        return jsonify({"error": "task_description, due_date, frequency, and questions are required"}), 400

    assessment_data = {
        "task_description": data["task_description"],
        "due_date": data["due_date"],
        "frequency": data["frequency"]
    }

    questions = data["questions"]
    assessment, error = PsychologistService.add_assessment_with_questions(
        psychologist_id, child_id, assessment_data, questions
    )

    if error:
        return jsonify({"error": error}), 403

    return jsonify({
        "message": "Assessment and questions added successfully",
        "assessment": {
            "child_id": assessment.child_id,
            "psychologist_id": assessment.psychologist_id,
            "task_description": assessment.task_description,
            "due_date": str(assessment.due_date),
            "frequency": assessment.frequency,
            "is_completed": assessment.is_completed
        }
    }), 201

def get_all_assessments():
    psychologist_id = request.psychologist_id
    assessments, error = PsychologistService.get_all_assessments(psychologist_id)
    if error:
        return jsonify({"error": error}), 400

    return jsonify(assessments), 200

def get_psychologist_schedule():
    psychologist_id = request.psychologist_id
    date_str = request.args.get('date')
    if date_str:
        try:
            requested_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            return jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}), 400
    else:
        requested_date = datetime.now().date()

    schedule, error = PsychologistService.get_schedule_for_psychologist(psychologist_id, requested_date)
    if error:
        return jsonify({"error": error}), 404

    return jsonify(schedule), 200
def chat_with_child():
    child_message = request.json.get("message")
    if not child_message:
        return jsonify({"error": "Message is required"}), 400

    # Generate prompt with general mental health issues
    prompt = ChatbotService.generate_chatbot_prompt_for_general_issues(child_message)
    response_json, error = GeminiAPI.get_exercises_for_prompt(prompt)
    if error:
        return jsonify({"error": f"Failed to fetch response from Gemini API: {error}"}), 500

    bot_response = response_json.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "").strip()
    if not bot_response:
        return jsonify({"error": "No valid response could be parsed from the chatbot."}), 500

    return jsonify({"bot_response": bot_response}), 200

