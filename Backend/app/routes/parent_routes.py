from flask import Blueprint, jsonify
from app.controllers.parent_controller import (
    register,
    confirm_otp,
    login,
    get_all_parents,
    resend_otp,
    create_child,
    get_child_detail,
    get_all_children,
    answer_questions,
    get_child_report,
    get_all_psychologists_for_parent,
    get_available_exercises_for_child,
    complete_assessment,
    submit_responses,
    get_psychologist_detail,
    book_consultation,
    assign_exercises_to_child,
    child_chat,
    generate_and_assign_assessments,
    chat_with_bot,
    show_all_parents,
    show_personalized_questions
)
from app.utils.jwt_utils import parent_required

parent_bp = Blueprint("parent_bp", __name__)

# Routes without @parent_required
parent_bp.route("/register", methods=["POST"])(register)
parent_bp.route("/confirm_otp", methods=["POST"])(confirm_otp)
parent_bp.route("/login", methods=["POST"])(login)
parent_bp.route("/resend_otp", methods=["POST"])(resend_otp)

# Routes with @parent_required
parent_bp.route("/create_child", methods=["POST"])(parent_required(create_child))
parent_bp.route("/get_child_detail/<int:child_id>", methods=["GET"])(parent_required(get_child_detail))
parent_bp.route("/get_all_children", methods=["GET"])(parent_required(get_all_children))
parent_bp.route("/answer_questions/<int:child_id>", methods=["POST"])(parent_required(answer_questions))
parent_bp.route("/get_child_report/<int:child_id>", methods=["GET"])(parent_required(get_child_report))
parent_bp.route("/<int:child_id>/all_psychologists", methods=["GET"])(parent_required(get_all_psychologists_for_parent))
parent_bp.route("/child/<int:child_id>/available_exercises", methods=["GET"])(parent_required(get_available_exercises_for_child))
parent_bp.route("/child/<int:child_id>/assessment/<int:assessment_id>/complete", methods=["POST"])(parent_required(complete_assessment))
parent_bp.route("/child/<int:child_id>/submit_responses", methods=["POST"])(parent_required(submit_responses))
parent_bp.route("/child/<int:child_id>/psychologist/<int:psychologist_id>", methods=["GET"])(parent_required(get_psychologist_detail))
parent_bp.route("/child/<int:child_id>/psychologist/<int:psychologist_id>/book_consultation", methods=["POST"])(parent_required(book_consultation))
parent_bp.route("/child/<int:child_id>/assign_exercises", methods=["POST"])(parent_required(assign_exercises_to_child))
parent_bp.route('/child/<int:childid>/exercise', methods=['POST'])(parent_required(child_chat))
parent_bp.route('/child/<int:child_id>/assessment', methods=['POST'])(parent_required(generate_and_assign_assessments))
parent_bp.route('/child/<int:child_id>/chat', methods=['POST'])(parent_required(chat_with_bot))
parent_bp.route("/personalized_questions", methods=["GET"])(show_personalized_questions)
parent_bp.route("/all_parents", methods=["GET"])(show_all_parents)

