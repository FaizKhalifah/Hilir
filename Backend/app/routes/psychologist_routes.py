from flask import Blueprint
from app.controllers.psychologist_controller import (
    register_psychologist,
    login_psychologist,
    get_all_children_for_psychologist,
    get_child_report_for_psychologist,
    add_and_assign_exercise_to_child,
    get_exercises_for_specialization,
    add_assessment,
    add_assessment_with_questions,
    get_all_assessments,
    get_psychologist_schedule,
)
from app.utils.jwt_utils import psychologist_required

psychologist_bp = Blueprint("psychologist_bp", __name__)

# Routes without @psychologist_required
psychologist_bp.route("/register", methods=["POST"])(register_psychologist)
psychologist_bp.route("/login", methods=["POST"])(login_psychologist)

# Routes with @psychologist_required
psychologist_bp.route("/all_children", methods=["GET"])(psychologist_required(get_all_children_for_psychologist))
psychologist_bp.route("/child/<int:child_id>/report", methods=["GET"])(psychologist_required(get_child_report_for_psychologist))
psychologist_bp.route("/child/<int:child_id>/assign_exercise", methods=["POST"])(psychologist_required(add_and_assign_exercise_to_child))
psychologist_bp.route("/exercises", methods=["GET"])(psychologist_required(get_exercises_for_specialization))
psychologist_bp.route("/child/<int:child_id>/add_assessment", methods=["POST"])(psychologist_required(add_assessment))
psychologist_bp.route("/child/<int:child_id>/add_assessment_with_questions", methods=["POST"])(psychologist_required(add_assessment_with_questions))
psychologist_bp.route("/all_assessments", methods=["GET"])(psychologist_required(get_all_assessments))
psychologist_bp.route("/schedule", methods=["GET"])(psychologist_required(get_psychologist_schedule))
from flask import Blueprint
from app.controllers.psychologist_controller import (
    register_psychologist,
    login_psychologist,
    get_all_children_for_psychologist,
    get_child_report_for_psychologist,
    add_and_assign_exercise_to_child,
    get_exercises_for_specialization,
    add_assessment,
    add_assessment_with_questions,
    get_all_assessments,
    get_psychologist_schedule,
)
from app.utils.jwt_utils import psychologist_required

psychologist_bp = Blueprint("psychologist_bp", __name__)

# Routes without @psychologist_required
psychologist_bp.route("/register", methods=["POST"])(register_psychologist)
psychologist_bp.route("/login", methods=["POST"])(login_psychologist)

# Routes with @psychologist_required
psychologist_bp.route("/all_children", methods=["GET"])(psychologist_required(get_all_children_for_psychologist))
psychologist_bp.route("/child/<int:child_id>/report", methods=["GET"])(psychologist_required(get_child_report_for_psychologist))
psychologist_bp.route("/child/<int:child_id>/assign_exercise", methods=["POST"])(psychologist_required(add_and_assign_exercise_to_child))
psychologist_bp.route("/exercises", methods=["GET"])(psychologist_required(get_exercises_for_specialization))
psychologist_bp.route("/child/<int:child_id>/add_assessment", methods=["POST"])(psychologist_required(add_assessment))
psychologist_bp.route("/child/<int:child_id>/add_assessment_with_questions", methods=["POST"])(psychologist_required(add_assessment_with_questions))
psychologist_bp.route("/all_assessments", methods=["GET"])(psychologist_required(get_all_assessments))
psychologist_bp.route("/schedule", methods=["GET"])(psychologist_required(get_psychologist_schedule))
